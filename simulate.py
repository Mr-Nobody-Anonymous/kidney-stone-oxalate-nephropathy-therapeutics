"""Hypothetical design-space exploration, NOT fitted pharmacology or clinical prediction.
Run: python simulate.py. Requires numpy. All input distributions are assumptions.
Concentrations are mol/L; Kd are mol/L; time is hours.
"""
from pathlib import Path
import json
import numpy as np
p=Path(__file__).parent
rng=np.random.default_rng(20261110)
n=20000
def logu(a,b): return np.exp(rng.uniform(np.log(a),np.log(b),n))
ox=logu(.0001,.002) # accessible soluble oxalate, not total dietary oxalate
sites=logu(.0002,.004) # accessible pocket concentration; NOT an administered dose
kd=logu(.00001,.001)
chloride=rng.uniform(.05,.15,n)
phosphate=logu(.001,.02)
citrate=logu(.0001,.005)
kcl=logu(.01,1)
kp=logu(.0001,.01)
kcit=logu(.0001,.01)
competition=chloride/kcl+phosphate/kp+citrate/kcit
transit=rng.uniform(1,6,n)
tau=logu(.1,5)
fenteric=rng.uniform(.2,.8,n)
def model(cap_factor=1,comp_factor=1,tau_factor=1):
    # Shared-site competitive Langmuir binding, competitors treated as reservoirs.
    # Solve x + S*x/(Kd*(1+sum(Ci/Kdi))+x) = Ox_total.
    S=sites*cap_factor
    keff=kd*(1+competition*comp_factor)
    b=keff+S-ox
    # Stable positive quadratic root for free oxalate.
    free=2*ox*keff/(np.sqrt(b*b+4*ox*keff)+b)
    eq=(ox-free)/ox
    captured=eq*(-np.expm1(-transit/(tau*tau_factor)))
    return captured, captured*fenteric
variants={
'baseline':(1,1,1),
'double_capacity':(2,1,1),
'selectivity_10x_with_penalties':(.8,.1,2),
'combined':(1.6,.1,2),
'fast_access_only':(1,1,.5),
}
summary={}
arrays={}
for name,pars in variants.items():
    c,u=model(*pars); arrays[name]=u
    summary[name]={
    'capture_percent_p10_p50_p90':(100*np.percentile(c,[10,50,90])).round(2).tolist(),
    'urinary_reduction_percent_p10_p50_p90':(100*np.percentile(u,[10,50,90])).round(2).tolist(),
    'fraction_scenarios_at_least_20pct_urinary_reduction':round(float(np.mean(u>=.2)),4)}
for name in arrays:
    summary[name]['fraction_better_than_paired_baseline']=round(float(np.mean(arrays[name]>arrays['baseline'])),4)
# Numerical checks: equilibrium mass conservation and physical bounds.
S=sites; keff=kd*(1+competition); b=keff+S-ox
x=2*ox*keff/(np.sqrt(b*b+4*ox*keff)+b)
res=np.max(np.abs(x+S*x/(keff+x)-ox))
assert res<1e-12
for a in arrays.values(): assert np.all((a>=0)&(a<=fenteric+1e-12))
summary['checks']={'maximum_mass_balance_error_M':float(res),'scenarios':n,'seed':20261110}
(p/'results.json').write_text(json.dumps(summary,indent=2))
np.savetxt(p/'scenario_results.csv',np.column_stack([arrays[k]*100 for k in arrays]),delimiter=',',header=','.join(k+'_urinary_reduction_percent' for k in arrays),comments='')
print(json.dumps(summary,indent=2))
