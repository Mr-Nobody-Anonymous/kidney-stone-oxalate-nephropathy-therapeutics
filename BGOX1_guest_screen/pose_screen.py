"""Rigid pose feasibility screen. NOT docking affinity, free energy, or efficacy.
Arbitrary transparent geometric thresholds; all sample counts are not probabilities.
Python + NumPy + SciPy + RDKit.
"""
from pathlib import Path
import json,csv
import numpy as np
from scipy.spatial.transform import Rotation
from rdkit import Chem
from rdkit.Chem import AllChem
P=Path(__file__).parent
hostsm='NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1'
h=Chem.AddHs(Chem.MolFromSmiles(hostsm));pr=AllChem.ETKDGv3();pr.randomSeed=20261121
ids=list(AllChem.EmbedMultipleConfs(h,numConfs=24,params=pr))
prop=AllChem.MMFFGetMoleculeProperties(h);prop.SetMMFFDielectricConstant(78.4)
for c in ids:AllChem.MMFFGetMoleculeForceField(h,prop,confId=c).Minimize(maxIts=2000)
h=Chem.RemoveHs(h)
centers=[a.GetIdx() for a in h.GetAtoms() if a.GetAtomicNum()==6 and len(a.GetNeighbors())==3 and all(n.GetAtomicNum()==7 for n in a.GetNeighbors())]
arms=[[n.GetIdx() for n in h.GetAtomWithIdx(c).GetNeighbors()] for c in centers]
pt=Chem.GetPeriodicTable();hr=np.array([pt.GetRvdw(a.GetAtomicNum()) for a in h.GetAtoms()])
guests={'oxalate':'O=C([O-])C(=O)[O-]','hydrogen_phosphate':'O=P([O-])([O-])O','sulfate':'O=S(=O)([O-])[O-]','citrate':'O=C([O-])CC(O)(CC(=O)[O-])C(=O)[O-]','chloride':'[Cl-]'}
rng=np.random.default_rng(20261122);npose=4000
out={};records=[]
for name,sm in guests.items():
 g0=Chem.MolFromSmiles(sm);g=Chem.AddHs(g0)
 if g.GetNumAtoms()==1:
  conf=Chem.Conformer(1);conf.SetAtomPosition(0,(0,0,0));g.AddConformer(conf)
 else:
  p=AllChem.ETKDGv3();p.randomSeed=20261123
  assert AllChem.EmbedMolecule(g,p)==0
  if AllChem.MMFFHasAllMoleculeParams(g):AllChem.MMFFOptimizeMolecule(g,maxIters=1000)
 g=Chem.RemoveHs(g)
 xyz=np.array(g.GetConformer().GetPositions());xyz-=xyz.mean(0)
 acc=[a.GetIdx() for a in g.GetAtoms() if a.GetAtomicNum() in [8,17]]
 gr=np.array([pt.GetRvdw(a.GetAtomicNum()) for a in g.GetAtoms()])
 pair_threshold=.75*(hr[:,None]+gr[None,:])
 counts={'poses':0,'clash_free':0,'both_arm_proximity':0,'distinct_acceptor_both_arm_proximity':0};hosthits=0;best=None
 for cid in ids:
  hx=np.array(h.GetConformer(cid).GetPositions())
  middle=(hx[centers[0]]+hx[centers[1]])/2
  rot=Rotation.random(npose,random_state=rng).as_matrix()
  # Identical sample volume per host and ligand: cube +/-4 A around arm midpoint.
  gx=np.einsum('pij,aj->pai',rot,xyz)+middle+rng.uniform(-4,4,(npose,1,3))
  d=np.linalg.norm(hx[None,:,None,:]-gx[:,None,:,:],axis=3)
  clear=np.all(d>=pair_threshold[None,:,:],axis=(1,2))
  da=d[:,arms[0],:][:,:,acc].min(axis=1)
  db=d[:,arms[1],:][:,:,acc].min(axis=1)
  ca=(da>=2.5)&(da<=3.5);cb=(db>=2.5)&(db<=3.5)
  both=clear&ca.any(1)&cb.any(1)
  distinct=np.zeros(npose,dtype=bool)
  for i in range(len(acc)):
   for j in range(len(acc)):
    if i!=j:distinct|=ca[:,i]&cb[:,j]
  distinct&=clear
  counts['poses']+=npose;counts['clash_free']+=int(clear.sum());counts['both_arm_proximity']+=int(both.sum());counts['distinct_acceptor_both_arm_proximity']+=int(distinct.sum())
  if both.any():hosthits+=1
  # Geometric pose objective only: proximity of each arm to an acceptor.
  objective=np.abs(da-3).min(1)+np.abs(db-3).min(1)
  objective[~both]=np.inf
  k=int(np.argmin(objective))
  if np.isfinite(objective[k]) and (best is None or objective[k]<best[0]):best=(float(objective[k]),cid,gx[k].copy())
 if best is not None:
  _,cid,gy=best
  hc=Chem.Mol(h);conf=Chem.Conformer(hc.GetConformer(cid));hc.RemoveAllConformers();hc.AddConformer(conf,assignId=True)
  gc=Chem.Mol(g);cf=Chem.Conformer(gc.GetNumAtoms())
  for i,pos in enumerate(gy):cf.SetAtomPosition(i,pos)
  gc.RemoveAllConformers();gc.AddConformer(cf)
  complexm=Chem.CombineMols(hc,gc);complexm.SetProp('_Name',name+' geometric example ONLY; not stable complex or affinity result')
  with Chem.SDWriter(str(P/(name+'_example_pose.sdf'))) as w:w.write(complexm)
 out[name]=dict(guest_smiles=sm,guest_formal_charge=Chem.GetFormalCharge(g),**counts,host_conformers_with_some_two_arm_pose=hosthits,host_conformers_screened=len(ids))
 records.append({'guest':name,**counts,'host_conformers_with_some_two_arm_pose':hosthits})
summary=dict(scope='Geometric accessibility/proximity only. No binding energy, explicit water, desolvation, entropy, ions, dynamics or toxicity. Pose counts are not binding probabilities.',
 thresholds=dict(contact_distance_A=[2.5,3.5],clash_cutoff_fraction_of_vdw_sum=.75,translations='cube +/-4 A about arm midpoint'),
 fixed_protonation='oxalate -2; hydrogen phosphate -2; sulfate -2; citrate -3; chloride -1; host +2; not a pH titration',results=out)
(P/'pose_results.json').write_text(json.dumps(summary,indent=2))
with (P/'pose_counts.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(summary,indent=2))
