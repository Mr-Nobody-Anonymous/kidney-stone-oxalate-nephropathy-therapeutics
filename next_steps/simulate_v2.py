"""Uncalibrated sequential digestion model. NOT measured material or clinical data.
Run python simulate_v2.py (numpy). Amounts mmol; volume L; time hours.
"""
import numpy as np, json, csv
from pathlib import Path
P=Path(__file__).parent
DESIGNS={
 'baseline':dict(sites=.5,kd=.1,competitor_factor=1,tau=.5),
 'capacity_only':dict(sites=4,kd=.1,competitor_factor=1,tau=.5),
 'selective_combined':dict(sites=1,kd=.1,competitor_factor=.1,tau=1),
 'aspirational_requirements':dict(sites=4,kd=.01,competitor_factor=.1,tau=.1),
}
def scenarios(n,seed):
 r=np.random.default_rng(seed)
 def lu(a,b): return np.exp(r.uniform(np.log(a),np.log(b),n))
 return dict(ox=lu(.1,1.5),volume=r.uniform(.2,1,n),capacity=lu(.5,1),kd_mult=lu(.3,3),tau_mult=lu(.5,2),
  comp=r.uniform(50,150,n)/lu(10,1000)+lu(1,20)/lu(.1,10)+lu(.1,5)/lu(.1,10),
  f=r.uniform(.2,.8,n),t=np.array([r.uniform(.5,2,n),r.uniform(1,4,n),r.uniform(2,12,n)]),
  ka=np.array([np.zeros(n),lu(.03,.4),lu(.01,.15)]),dilution=r.uniform(1,3,n),loss=r.uniform(0,.2,n))
def run(d,design,steps=120,stress=False,no_abs=False):
 O=d['ox']; n=len(O); B=np.zeros(n); A=np.zeros(n); F=O.copy()
 S=design['sites']*d['capacity']; tau=design['tau']*d['tau_mult']
 comp=d['comp']*design['competitor_factor']; kd=design['kd']*d['kd_mult']
 if stress: S=S*.6; tau=tau*3; comp=comp*3; kd=kd*3
 # Sequential batch stages: gastric, small intestine, colon. Not anatomical transport.
 for j in range(3):
  V=d['volume']*(1 if j==0 else d['dilution'])
  Sj=S*(1-j*d['loss'])
  # Deactivated sites release bound oxalate into the same lumen.
  released=np.maximum(B-Sj,0); B-=released; F+=released
  K=kd*[10,1,2][j]*(1+comp)*V
  dt=d['t'][j]/steps
  relax=-np.expm1(-dt/tau)
  uptake=np.zeros(n) if no_abs else -np.expm1(-d['ka'][j]*dt)
  for _ in range(steps):
   M=F+B
   # Stable free-amount root; avoids subtractive cancellation in bound root.
   b=K+Sj-M
   free=2*M*K/(np.sqrt(b*b+4*M*K)+b)
   target=M-free
   newB=B+(target-B)*relax
   F+=B-newB; B=newB
   absorbed=F*uptake; F-=absorbed; A+=absorbed
 assert np.max(np.abs(F+B+A-O))<1e-10
 assert min(F.min(),B.min(),A.min())>-1e-10
 A0=O*(-np.expm1(-np.sum(d['ka']*d['t'],axis=0)))
 avoided=np.clip(1-A/A0,0,1)
 return dict(capture=B/O,enteric_avoided=avoided,urine=avoided*d['f'],mass_error=float(np.max(np.abs(F+B+A-O))))
def summarize(z):
 out={}
 for metric in ['capture','enteric_avoided','urine']:
  x=z[metric]
  out[metric]={'p10_p50_p90_percent':np.round(np.percentile(x,[10,50,90])*100,2).tolist(),
   'fraction_ge_70pct':float(np.mean(x>=.7)),'fraction_ge_20pct':float(np.mean(x>=.2))}
 out['mass_error_mmol']=z['mass_error']
 return out
if __name__=='__main__':
 # Selection rule fixed here: highest development fraction reaching capture >=70%.
 dev=scenarios(3000,20261111); test=scenarios(10000,20261112)
 result={'disclaimer':'All material properties and scenario distributions hypothetical; no clinical probability.', 'designs':DESIGNS,'development':{},'holdout':{},'stress':{}}
 for name,d in DESIGNS.items(): result['development'][name]=summarize(run(dev,d))
 winner=max(DESIGNS,key=lambda k:result['development'][k]['capture']['fraction_ge_70pct'])
 result['selected_on_development']=winner
 columns={}
 for name,d in DESIGNS.items():
  z=run(test,d); result['holdout'][name]=summarize(z)
  for k in ['capture','enteric_avoided','urine']: columns[name+'_'+k+'_percent']=z[k]*100
  result['stress'][name]=summarize(run(test,d,stress=True))
 # Numerical convergence, no-site negative control, no-absorption conservation.
 small={k:(v[:100] if v.ndim==1 else v[:,:100]) for k,v in test.items()}
 z1=run(small,DESIGNS[winner],steps=120); z2=run(small,DESIGNS[winner],steps=240); z3=run(small,DESIGNS[winner],steps=480)
 zero=run(small,dict(sites=0,kd=.1,competitor_factor=1,tau=.5))
 assert np.max(np.abs(zero['urine']))<1e-10
 na=run(small,DESIGNS[winner],no_abs=True)
 assert na['mass_error']<1e-10
 result['checks']={'zero_site_max_urine_effect':float(np.max(np.abs(zero['urine']))),
 'max_capture_difference_120_vs_240_percentage_points':float(np.max(np.abs(z1['capture']-z2['capture']))*100),
 'max_capture_difference_240_vs_480_percentage_points':float(np.max(np.abs(z2['capture']-z3['capture']))*100),
 'max_urine_difference_240_vs_480_percentage_points':float(np.max(np.abs(z2['urine']-z3['urine']))*100),
 'holdout_ceiling_fraction_f_ge_70pct':float(np.mean(test['f']>=.7))}
 (P/'results_v2.json').write_text(json.dumps(result,indent=2))
 np.savetxt(P/'holdout_results.csv',np.column_stack(list(columns.values())),delimiter=',',header=','.join(columns),comments='')
 print('Selected:',winner)
 for group in ['holdout','stress']:
  for name,z in result[group].items(): print(group,name,'capture',z['capture'],'urine',z['urine'])
 print(result['checks'])
