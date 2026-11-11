"""Exact small receptor-module proposal, not a drug or efficacy prediction.
Dependencies: rdkit, numpy. Fragment-free molecular graph; support not included.
"""
from pathlib import Path
import json
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem,Descriptors,rdMolDescriptors,Draw
P=Path(__file__).parent
SMILES='NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1'
m=Chem.MolFromSmiles(SMILES);assert m is not None
assert len(Chem.GetMolFrags(m))==1 and Chem.GetFormalCharge(m)==2
canonical=Chem.MolToSmiles(m)
m.SetProp('_Name','BGOX-1: hypothetical receptor module, NOT validated medicine')
AllChem.Compute2DCoords(m)
Draw.MolToFile(m,str(P/'BGOX-1_structure.png'),size=(1400,650),legend='BGOX-1 | proposed dicationic receptor module | no efficacy established')
writer=Chem.SDWriter(str(P/'BGOX-1_2D.sdf'));writer.write(m);writer.close()
h=Chem.AddHs(m)
p=AllChem.ETKDGv3();p.randomSeed=20261117;p.pruneRmsThresh=.5
ids=list(AllChem.EmbedMultipleConfs(h,numConfs=30,params=p));assert ids
assert AllChem.MMFFHasAllMoleculeParams(h)
res=AllChem.MMFFOptimizeMoleculeConfs(h,maxIters=1000)
centers=[a.GetIdx() for a in h.GetAtoms() if a.GetAtomicNum()==6 and len(a.GetNeighbors())==3 and all(n.GetAtomicNum()==7 for n in a.GetNeighbors())]
assert len(centers)==2
rows=[]
writer=Chem.SDWriter(str(P/'BGOX-1_conformers.sdf'))
for cid,(status,energy) in zip(ids,res):
 conf=h.GetConformer(cid);distance=float(np.linalg.norm(np.array(conf.GetAtomPosition(centers[0]))-np.array(conf.GetAtomPosition(centers[1]))))
 rows.append(dict(conformer_id=cid,optimization_status=int(status),MMFF_energy_kcal_mol=float(energy),guanidinium_carbon_distance_A=distance))
 h.SetProp('MMFF_energy_kcal_mol',str(energy));h.SetProp('scope','isolated force-field conformer; not aqueous binding or toxicity');writer.write(h,confId=cid)
writer.close()
out=dict(label='BGOX-1',status='proposed complete small receptor module; no synthesis, binding or safety validation',canonical_SMILES=canonical,
 formal_charge=2,formula=rdMolDescriptors.CalcMolFormula(m),molecular_mass_dication_excluding_counterions_g_mol=Descriptors.MolWt(m),
 chloride_salt_SMILES=canonical+'.[Cl-].[Cl-]',
 structural_identity='1,3-bis(guanidiniomethyl)-5-(triethylene-glycol-derived hydroxyethoxy)benzene connectivity as unambiguously defined by SMILES; label is not an IUPAC name',
 protonation='fixed dication representation; pH-dependent speciation not computed',
 conformers=rows,conformer_distance_range_A=[min(r['guanidinium_carbon_distance_A'] for r in rows),max(r['guanidinium_carbon_distance_A'] for r in rows)],
 limitation='MMFF calculations are isolated-molecule geometry exploration, not a binding simulation or predictive ranking. No claimed novelty or connection to the passing 80% simulation specification.')
(P/'BGOX-1_design.json').write_text(json.dumps(out,indent=2))
(P/'BGOX-1.smiles').write_text(canonical+' BGOX-1_hypothetical_module\n')
print(json.dumps({k:v for k,v in out.items() if k!='conformers'},indent=2))
