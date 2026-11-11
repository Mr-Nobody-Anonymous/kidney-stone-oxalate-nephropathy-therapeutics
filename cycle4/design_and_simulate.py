"""Cycle 4: valence-checked cage-panel fragments + finite-pool equilibrium.
Not a full cage design, atomic binding prediction, toxicity or clinical model.
Python: numpy, scipy, rdkit, matplotlib.
"""
from pathlib import Path
import json,csv
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw
P=Path(__file__).parent
names=['Oxalate','Chloride','Sulfate','Phosphate','Citrate']
# Local 3,5-dicarboxamide pyridinium panel. *1/*2 indicate continuation
# into cage; *3 indicates an unresolved network attachment.
fragments={
 'parent_panel':'[*:1]NC(=O)c1c[n+](C)cc(C(=O)N[*:2])c1',
 'tether_EG2':'[*:1]NC(=O)c1c[n+](CCCOCCOCCO[*:3])cc(C(=O)N[*:2])c1',
 'tether_EG4':'[*:1]NC(=O)c1c[n+](CCCOCCOCCOCCOCCO[*:3])cc(C(=O)N[*:2])c1',
 'tether_EG6':'[*:1]NC(=O)c1c[n+](CCCOCCOCCOCCOCCOCCOCCO[*:3])cc(C(=O)N[*:2])c1',
}
mols=[]; records=[]
for label,s in fragments.items():
 m=Chem.MolFromSmiles(s);assert m is not None
 assert Chem.GetFormalCharge(m)==1
 m.SetProp('_Name',label+'; FRAGMENT ONLY')
 mols.append(m); records.append(dict(label=label,canonical_fragment_smiles=Chem.MolToSmiles(m),formal_charge_of_fragment=1,scope='Local panel only; dummy atoms are unresolved attachments; not complete cage or medicine'))
(P/'fragment_designs.json').write_text(json.dumps(records,indent=2))
svg=Draw.MolsToGridImage(mols,molsPerRow=2,subImgSize=(650,320),legends=[k+' — FRAGMENT ONLY' for k in fragments],useSVG=True)
(P/'cage_panel_fragments.svg').write_text(svg)
w=Chem.SDWriter(str(P/'panel_fragments.sdf'))
for m in mols:w.write(m)
w.close()

def equilibrium(total,kd,sites):
 """Single shared independent pocket, finite ligand totals. mmol and mM.
 total: concentration mM, sites: concentration mM. Returns bound concentrations.
 All Kd values here are hypothetical intrinsic surrogates, NOT fitted constants.
 """
 lo=np.zeros_like(sites);hi=sites.copy()
 for _ in range(100):
  free=(lo+hi)/2
  bound=total*free[:,None]/(kd+free[:,None])
  residual=free+bound.sum(axis=1)-sites
  hi=np.where(residual>0,free,hi);lo=np.where(residual<=0,free,lo)
 free=(lo+hi)/2
 bound=total*free[:,None]/(kd+free[:,None])
 err=np.max(np.abs(free+bound.sum(axis=1)-sites))
 assert err<1e-9
 assert np.all(bound>=0) and np.all(bound<=total+1e-10)
 return bound,float(err)

r=np.random.default_rng(20261115);n=30000
lu=lambda a,b:np.exp(r.uniform(np.log(a),np.log(b),n))
V=r.uniform(.2,1,n)
T=np.column_stack([lu(.1,1.5)/V,r.uniform(50,150,n),lu(.1,5),lu(1,20),lu(.1,5)])
# Nominal source-inspired surrogate, broadened by factors; not actual gastric Kd.
K=np.column_stack([lu(.0005,.05),lu(.5,5),lu(.01,.5),lu(.001,10),lu(.001,10)])
access=lu(.5,1)
summary={};rows=[];maxerr=0
for capacity in [.5,2,4]:
 B,err=equilibrium(T,K,capacity*access/V);maxerr=max(maxerr,err)
 capture=B[:,0]/T[:,0]
 phosphate_depletion=B[:,3]/T[:,3]
 citrate_depletion=B[:,4]/T[:,4]
 x=dict(capture_p10_p50_p90_percent=np.round(np.percentile(capture,[10,50,90])*100,2).tolist(),
  fraction_capture_ge70=float(np.mean(capture>=.7)),
  phosphate_depletion_p10_p50_p90_percent=np.round(np.percentile(phosphate_depletion,[10,50,90])*100,2).tolist(),
  citrate_depletion_p10_p50_p90_percent=np.round(np.percentile(citrate_depletion,[10,50,90])*100,2).tolist(),
  fraction_capture_ge70_and_both_depletions_le10=float(np.mean((capture>=.7)&(phosphate_depletion<=.1)&(citrate_depletion<=.1))))
 summary[str(capacity)+'_mmol_nominal_pockets']=x
 rows.append(capture*100)
# Fixed-condition decision map: unknown phosphate and citrate affinities.
grid=np.logspace(-3,1,41)
a,b=np.meshgrid(grid,grid,indexing='ij');N=a.size
fixedT=np.tile([1,100,1,10,1],(N,1)) # .5 mmol oxalate / .5 L
fixedK=np.column_stack([np.full(N,.005),np.full(N,1000/589),np.full(N,.05),a.ravel(),b.ravel()])
B,_=equilibrium(fixedT,fixedK,np.full(N,4)) #2 mmol accessible sites/.5 L
cap=(B[:,0]/fixedT[:,0]).reshape(a.shape)*100
np.savetxt(P/'decision_map_capture_percent.csv',cap,delimiter=',')
(P/'decision_map_axes.json').write_text(json.dumps(dict(phosphate_kd_mM_rows=grid.tolist(),citrate_kd_mM_columns=grid.tolist(),scope='Fixed-condition equilibrium, not digestion or molecular prediction'),indent=2))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,6))
im=ax.pcolormesh(grid,grid,cap,shading='auto',vmin=0,vmax=100,cmap='viridis')
ax.set_xscale('log');ax.set_yscale('log')
ax.set_xlabel('Assumed citrate Kd (mM): higher = weaker competing binding')
ax.set_ylabel('Assumed phosphate Kd (mM)')
ax.set_title('Hypothetical equilibrium oxalate capture (%)\nFinite pools; not measured or clinical performance')
fig.colorbar(im,ax=ax,label='Equilibrium capture (%)')
fig.tight_layout();fig.savefig(P/'competition_decision_map.png',dpi=160);plt.close(fig)
# Limits: no sites, no ligand, isolated oxalate expected ~capacity bound if strong.
zero,_=equilibrium(T[:100],K[:100],np.zeros(100));assert np.max(zero)==0
empty,_=equilibrium(np.zeros((100,5)),K[:100],np.ones(100));assert np.max(empty)==0
single,_=equilibrium(np.array([[1.,0,0,0,0]]),np.full((1,5),1e-12),np.array([.5]))
assert abs(single[0,0]-.5)<1e-9
out=dict(disclaimer='Equilibrium model only. All distributions hypothetical. Does not predict properties of the designed fragments.',n=n,seed=20261115,summary=summary,max_site_balance_error_mM=maxerr,
 checks={'zero_sites':'pass','zero_ligands':'pass','strong_single_ligand_limit':'pass','bounds_and_site_balance':'pass'},
 caveat='No digestion, uptake, toxicity, pH, multivalent stoichiometry or ligand speciation. The 10% depletion constraint is an illustrative engineering threshold, not a safety criterion.')
(P/'cycle4_results.json').write_text(json.dumps(out,indent=2))
np.savetxt(P/'capture_scenarios.csv',np.column_stack(rows),delimiter=',',header='sites0.5_capture_percent,sites2_capture_percent,sites4_capture_percent',comments='')
print(json.dumps(out,indent=2))
