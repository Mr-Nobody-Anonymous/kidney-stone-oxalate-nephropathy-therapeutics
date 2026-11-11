"""Limited computational triage of BGOX-1. Not binding/ADMET prediction.
Requires RDKit and NumPy. Two dielectric choices are sensitivity tests only.
"""
from pathlib import Path
import json,csv
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem,Descriptors,rdMolDescriptors,Lipinski
P=Path(__file__).parent
s='NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1'
m=Chem.MolFromSmiles(s);assert m is not None
assert Chem.GetFormalCharge(m)==2 and len(Chem.GetMolFrags(m))==1
assert Chem.MolToSmiles(Chem.MolFromSmiles(Chem.MolToSmiles(m)))==Chem.MolToSmiles(m)
centers=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()==6 and len(a.GetNeighbors())==3 and all(n.GetAtomicNum()==7 for n in a.GetNeighbors())]
assert len(centers)==2
arms=[[n.GetIdx() for n in m.GetAtomWithIdx(c).GetNeighbors()] for c in centers]
oxygens=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()==8]
desc=dict(formula=rdMolDescriptors.CalcMolFormula(m),mass_excluding_counterions_g_mol=Descriptors.MolWt(m),formal_charge=Chem.GetFormalCharge(m),
 polar_surface_area_A2=rdMolDescriptors.CalcTPSA(m),hydrogen_bond_donors=Lipinski.NumHDonors(m),hydrogen_bond_acceptors=Lipinski.NumHAcceptors(m),
 rotatable_bonds=rdMolDescriptors.CalcNumRotatableBonds(m),heavy_atoms=m.GetNumHeavyAtoms(),ring_count=rdMolDescriptors.CalcNumRings(m))
rows=[];summaries={}
for dielectric in [1.,78.4]:
 for seed in [20261118,20261119,20261120]:
  h=Chem.AddHs(m);params=AllChem.ETKDGv3();params.randomSeed=seed;params.pruneRmsThresh=.5
  ids=list(AllChem.EmbedMultipleConfs(h,numConfs=48,params=params))
  props=AllChem.MMFFGetMoleculeProperties(h,mmffVariant='MMFF94');props.SetMMFFDielectricConstant(dielectric)
  for cid in ids:
   ff=AllChem.MMFFGetMoleculeForceField(h,props,confId=cid)
   status=ff.Minimize(maxIts=2000)
   xyz=np.asarray(h.GetConformer(cid).GetPositions())
   distance=np.linalg.norm(xyz[centers[0]]-xyz[centers[1]])
   interN=min(np.linalg.norm(xyz[i]-xyz[j]) for i in arms[0] for j in arms[1])
   on=min(np.linalg.norm(xyz[i]-xyz[j]) for i in oxygens for j in arms[0]+arms[1])
   rows.append(dict(dielectric=dielectric,seed=seed,conformer=cid,status=int(status),MMFF_energy=ff.CalcEnergy(),
    guanidinium_carbon_distance_A=float(distance),minimum_interarm_N_distance_A=float(interN),minimum_chain_O_to_guanidinium_N_distance_A=float(on)))
 for_d=[r for r in rows if r['dielectric']==dielectric]
 summaries[str(dielectric)]={'generated':len(for_d),'converged':sum(r['status']==0 for r in for_d)}
 for key in ['guanidinium_carbon_distance_A','minimum_interarm_N_distance_A','minimum_chain_O_to_guanidinium_N_distance_A']:
  vals=[r[key] for r in for_d if r['status']==0]
  summaries[str(dielectric)][key+'_min_median_max']=np.round([np.min(vals),np.median(vals),np.max(vals)],3).tolist()
 with Chem.SDWriter(str(P/f'last_seed_dielectric_{dielectric}_conformers.sdf')) as w:
  for cid in ids:w.write(h,confId=cid)
out=dict(scope='Molecular descriptors, graph checks and isolated force-field geometry sensitivity only. No receptor-guest affinity, explicit solvent, physiological speciation or toxicity calculation.',descriptors=desc,conformational_screen=summaries,
 all_structural_checks_pass=True,clinical_or_binding_success='UNKNOWN',
 limitations=['Dielectric 78.4 is NOT explicit water or a validated solvent model.','Generated conformer fractions are not thermal populations.','MMFF energies cannot be compared as binding free energies.','No full support material, counterion or oxalate complex was modeled.'])
(P/'screen_results.json').write_text(json.dumps(out,indent=2))
with (P/'geometry_results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(out,indent=2))
