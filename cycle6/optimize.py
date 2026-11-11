"""Inverse design of a hypothetical equilibrium PROPERTY SPECIFICATION.
Not molecular optimization. Python + NumPy; no chemical feasibility assumed.
Same biological/uncertainty ranges and six challenges as cycle5.
"""
import numpy as np,itertools,json,csv
from pathlib import Path
P=Path(__file__).parent
conditions={'nominal':(1,1,1),'weaker_oxalate_affinity_10x':(10,1,1),'competitors_bind_10x_stronger':(1,.1,1),'half_sites':(1,1,.5),'combined':(10,1/3,.6),'severe_combined':(100,.1,.3)}
a=np.array(list(itertools.product([.1,1.5],[.2,1],[.5,1],[.0005,.05],[.001,10],[.001,10],[50,150],[.1,5],[1,20],[.1,5])))
def unpack(a):
 O,V,acc,ko,kp,kc,cl,su,ph,ci=a.T
 T=np.column_stack([O/V,cl,su,ph,ci]);K=np.column_stack([ko,np.full(len(a),1000/589),np.full(len(a),.05),kp,kc])
 return V,acc,T,K
V,acc,T,K=unpack(a)
def required_amount(s,T,K,V,acc,ret):return (s+(T*s[:,None]/(K+s[:,None])).sum(1))*V/(acc*ret)
def bounds(aff,rejection):
 lower=0.;upper=np.inf
 for oxmult,cmult,ret in conditions.values():
  k=K.copy();k[:,0]*=oxmult/aff;k[:,1:]*=cmult*rejection
  s_capture=(.85/.15)*k[:,0]
  s_max=np.minimum(k[:,3],k[:,4])/9
  lower=max(lower,float(required_amount(s_capture,T,k,V,acc,ret).max()))
  upper=min(upper,float(required_amount(s_max,T,k,V,acc,ret).min()))
 return lower,upper
options=[]
# Initial 6x6 grid through 1e6 found no joint solution. Extend only to
# quantify how extreme a mathematically passing specification becomes.
for aff,reject in itertools.product([1,10,100,1000,10000,1000000],[1,10,100,1000,10000,1000000,100000000,10000000000]):
 low,high=bounds(aff,reject)
 Q=low*1.001
 feasible=Q<=high
 # Arbitrary transparent ranking, not physical synthetic cost.
 score=np.log10(aff)+np.log10(reject)+np.log2(max(Q/4,1))
 options.append(dict(affinity_improvement=aff,competitor_Kd_multiplier=reject,minimum_nominal_pockets_mmol=low,maximum_for_10pct_offtarget_mmol=high,chosen_pockets_mmol=Q,feasible=bool(feasible),ranking_score=float(score)))
feasible=[x for x in options if x['feasible']]
assert feasible
best=min(feasible,key=lambda x:x['ranking_score'])
def solve(T,k,S):
 lo=np.zeros_like(S);hi=S.copy()
 for _ in range(100):
  s=(lo+hi)/2;B=T*s[:,None]/(k+s[:,None]);res=s+B.sum(1)-S
  hi=np.where(res>0,s,hi);lo=np.where(res<=0,s,lo)
 s=(lo+hi)/2;B=T*s[:,None]/(k+s[:,None])
 assert np.max(np.abs(s+B.sum(1)-S))<1e-8
 return B
r=np.random.default_rng(20261116);n=10000
lu=lambda x,y:np.exp(r.uniform(np.log(x),np.log(y),n))
interior=np.column_stack([lu(.1,1.5),r.uniform(.2,1,n),r.uniform(.5,1,n),lu(.0005,.05),lu(.001,10),lu(.001,10),r.uniform(50,150,n),lu(.1,5),lu(1,20),lu(.1,5)])
results={};rows=[]
for group,inputs in [('corners',a),('independent_interior',interior)]:
 v,ac,t,k0=unpack(inputs);results[group]={}
 for name,(om,cm,ret) in conditions.items():
  k=k0.copy();k[:,0]*=om/best['affinity_improvement'];k[:,1:]*=cm*best['competitor_Kd_multiplier']
  B=solve(t,k,best['chosen_pockets_mmol']*ac*ret/v)
  c=B[:,0]/t[:,0];ph=B[:,3]/t[:,3];ci=B[:,4]/t[:,4]
  joint=(c>.8)&(ph<=.1)&(ci<=.1)
  assert joint.all()
  results[group][name]=dict(n=len(inputs),minimum_capture_percent=float(c.min()*100),median_capture_percent=float(np.median(c)*100),maximum_phosphate_depletion_percent=float(ph.max()*100),maximum_citrate_depletion_percent=float(ci.max()*100),joint_pass_fraction=float(joint.mean()))
  for i in range(len(inputs)):rows.append([group,name,i,c[i]*100,ph[i]*100,ci[i]*100])
caponly,_=bounds(1,1)
out=dict(disclaimer='Successful property-only inverse design under an unvalidated equilibrium model. No molecule has been shown to achieve these parameters.',target_capture=.85,offtarget_max=.1,selected=best,capture_only_without_affinity_or_selectivity_improvement_required_nominal_sites_mmol=caponly,results=results,grid=options)
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'test_outputs.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['group','condition','point_id','capture_percent','phosphate_depletion_percent','citrate_depletion_percent']);w.writerows(rows)
np.savetxt(P/'corner_inputs.csv',a,delimiter=',',comments='',header='oxalate_mmol,volume_L,accessibility,oxalate_Kd_mM,phosphate_Kd_mM,citrate_Kd_mM,chloride_mM,sulfate_mM,phosphate_mM,citrate_mM')
np.savetxt(P/'interior_inputs.csv',interior,delimiter=',',comments='',header='oxalate_mmol,volume_L,accessibility,oxalate_Kd_mM,phosphate_Kd_mM,citrate_Kd_mM,chloride_mM,sulfate_mM,phosphate_mM,citrate_mM')
print('Selected:',best,'\nCapture-only baseline sites for 85%:',caponly)
print(json.dumps(results,indent=2))
