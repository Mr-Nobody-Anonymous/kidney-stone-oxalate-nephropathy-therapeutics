"""Exact equilibrium requirements and finite corner tests, not molecule prediction.
Python + NumPy. All condition envelopes and unknown constants are assumed.
"""
from pathlib import Path
import itertools,json,csv
import numpy as np
P=Path(__file__).parent
conditions={
 'nominal':dict(kox=1,competitor_kd=1,sites=1),
 'weaker_oxalate_affinity_10x':dict(kox=10,competitor_kd=1,sites=1),
 'competitors_bind_10x_stronger':dict(kox=1,competitor_kd=.1,sites=1),
 'half_sites':dict(kox=1,competitor_kd=1,sites=.5),
 'combined':dict(kox=10,competitor_kd=1/3,sites=.6),
 'severe_combined':dict(kox=100,competitor_kd=.1,sites=.3),
}
# Enumerated corners, not random patients. Finite shared-pocket model.
inputs=list(itertools.product([.1,1.5],[.2,1],[.5,1],[.0005,.05],[.001,10],[.001,10],[50,150],[.1,5],[1,20],[.1,5]))
a=np.array(inputs)
O,V,access,kox,kp,kc,cl,sulf,phos,cit=a.T
T=np.column_stack([O/V,cl,sulf,phos,cit])
baseK=np.column_stack([kox,np.full(len(a),1000/589),np.full(len(a),.05),kp,kc])
def eq(T,K,S):
 lo=np.zeros(len(S));hi=S.copy()
 for _ in range(100):
  x=(lo+hi)/2;B=T*x[:,None]/(K+x[:,None]);res=x+B.sum(1)-S
  hi=np.where(res>0,x,hi);lo=np.where(res<=0,x,lo)
 x=(lo+hi)/2;B=T*x[:,None]/(K+x[:,None])
 assert np.max(np.abs(x+B.sum(1)-S))<1e-9
 return B
rows=[];summaries={}
for cname,c in conditions.items():
 K=baseK.copy();K[:,0]*=c['kox'];K[:,1:]*=c['competitor_kd']
 B=eq(T,K,4*access*c['sites']/V)
 capture=B[:,0]/T[:,0];p=B[:,3]/T[:,3];ci=B[:,4]/T[:,4]
 # At minimal free-site concentration giving 80% ox capture:
 s=.8/(1-.8)*K[:,0]
 minB=T*s[:,None]/(K+s[:,None])
 req_sites=(s+minB.sum(1))*V/(access*c['sites'])
 selective=(minB[:,3]/T[:,3]<=.1)&(minB[:,4]/T[:,4]<=.1)
 summaries[cname]=dict(corners=len(a),minimum_capture_percent=float(capture.min()*100),maximum_capture_percent=float(capture.max()*100),
  fraction_corners_capture_ge80=float(np.mean(capture>=.8)),fraction_joint_ge80_capture_le10_depletions=float(np.mean((capture>=.8)&(p<=.1)&(ci<=.1))),
  all_corners_capture_ge80=bool(np.all(capture>=.8)),all_corners_selectivity_feasible_at_any_capacity=bool(np.all(selective)),
  max_required_nominal_sites_mmol_for_capture_alone=float(req_sites.max()))
 for i in range(len(a)):
  rows.append([cname,i,float(capture[i]*100),float(p[i]*100),float(ci[i]*100),float(req_sites[i]),bool(selective[i])])
# Necessary affinity ratios to satisfy capture >=80%, off-target occupancy <=10%.
# s>=4 Kox and s<=Kcomp/9 => Kcomp/Kox>=36.
ratios={c:36*v['kox']/v['competitor_kd'] for c,v in conditions.items()}
# Necessary capacity bound independent of affinity and competing ions.
maxload=1.5
ceilings={}
for c,v in conditions.items():
 available=4*.5*v['sites']
 ceilings[c]=dict(available_sites_at_half_accessibility_mmol=available,capacity_only_capture_ceiling_percent=min(1,available/maxload)*100,
 necessary_nominal_sites_for_80_capture_mmol=.8*maxload/(.5*v['sites']))
out=dict(scope='1024 equal-weight corners per condition; hypothetical equilibrium only. Not population probabilities or digestive tests.',
 target_capture=.8,illustrative_max_each_competitor_depletion=.1,nominal_site_amount_mmol=4,
 summaries=summaries,minimum_nominal_competitor_Kd_over_oxalate_Kd_ratios=ratios,capacity_bounds=ceilings,
 conclusion='No robust 80% capture-plus-selectivity result in this stated envelope. No molecular validation or safety prediction.')
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'corner_results.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['condition','corner_id','capture_percent','phosphate_depletion_percent','citrate_depletion_percent','required_nominal_sites_for_80capture_mmol','selectivity_feasible_at_80capture']);w.writerows(rows)
np.savetxt(P/'corner_inputs.csv',a,delimiter=',',header='oxalate_mmol,volume_L,accessibility,oxalate_Kd_mM,phosphate_Kd_mM,citrate_Kd_mM,chloride_mM,sulfate_mM,phosphate_mM,citrate_mM',comments='')
print(json.dumps(out,indent=2))
