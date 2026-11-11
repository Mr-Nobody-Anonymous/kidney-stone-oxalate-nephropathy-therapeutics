"""Cycle 3: requirements exploration informed by a published receptor.
NOT a molecular prediction. Not fitted to digestive/clinical data.
Uses cycle2 sequential batch model unchanged. Python + NumPy.
"""
from pathlib import Path
import sys, json, csv
import numpy as np
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE.parent/'next_steps'))
from simulate_v2 import scenarios,run,summarize
# TPPC aqueous ITC apparent Ka_ox ~2e6/M -> Kd .0005 mM.
# These are extrapolative surrogates, NOT jointly fitted intrinsic constants.
SOURCE_KD=.0005
CONDITIONS={
 'nominal':dict(sites=1,kd=1,comp=1,tau=1),
 'competition_3x':dict(sites=1,kd=1,comp=3,tau=1),
 'competition_10x':dict(sites=1,kd=1,comp=10,tau=1),
 'half_sites':dict(sites=.5,kd=1,comp=1,tau=1),
 'access_10x_slower':dict(sites=1,kd=1,comp=1,tau=10),
 'affinity_100x_weaker':dict(sites=1,kd=100,comp=1,tau=1),
 'combined':dict(sites=.6,kd=10,comp=3,tau=3),
 'severe_combined':dict(sites=.3,kd=100,comp=10,tau=10),
}
def make(n,seed):
 d=scenarios(n,seed); r=np.random.default_rng(seed+100)
 lu=lambda a,b:np.exp(r.uniform(np.log(a),np.log(b),n))
 # Added competition surrogate. All concentrations/unknown affinities assumed.
 # Chloride uses NMR Ka=589/M; sulfate uses ITC Ka=2e4/M.
 chloride=r.uniform(50,150,n); sulfate=lu(.1,5)
 phosphate=lu(1,20); citrate=lu(.1,5)
 kd_p=lu(.01,10); kd_c=lu(.01,10)
 d['comp']=chloride*589/1000+sulfate*20000/1000+phosphate/kd_p+citrate/kd_c
 return d,dict(kd_phosphate_mM=kd_p,kd_citrate_mM=kd_c,competition=d['comp'])
def evaluate(d,design,condition):
 c=CONDITIONS[condition]
 z=dict(d); z['comp']=d['comp']*c['comp']
 des=dict(design); des['sites']*=c['sites']; des['kd']*=c['kd']; des['tau']*=c['tau']
 return run(z,des)
def metric(z):return float(np.mean(z['capture']>=.7))
if __name__=='__main__':
 dev,_=make(2000,20261113); test,extra=make(10000,20261114)
 grid=[]
 for loss in [10,100,1000]:
  for sites in [.5,2,4]:
   for tau in [.1,.5]:
    grid.append(dict(label=f'loss{loss}_sites{sites}_tau{tau}',sites=sites,kd=SOURCE_KD*loss,competitor_factor=1,tau=tau,source_affinity_loss=loss))
 ranking=[]
 for design in grid:
  scores=[metric(evaluate(dev,design,c)) for c in ['nominal','combined']]
  ranking.append(dict(design=design,nominal=scores[0],combined=scores[1],objective=min(scores)))
 ranking.sort(key=lambda a:(a['objective'],a['nominal']),reverse=True)
 best=ranking[0]['design']; results={}
 for name in CONDITIONS: results[name]=summarize(evaluate(test,best,name))
 # Molecular-edit outcomes are unknown: report same property grid under independent holdout.
 grid_test=[]
 for design in grid:
  zz=evaluate(test,design,'combined')
  grid_test.append(dict(label=design['label'],combined_capture_ge70_fraction=metric(zz),combined_median_capture_percent=float(np.median(zz['capture'])*100)))
 base=evaluate(test,best,'nominal')
 # Unknown phosphate affinity sensitivity, holding all other sampled inputs fixed:
 # reconstruct proxy using same generator but adjust just C_p/Kd_p via deterministic repeats.
 sensitivities={}
 # Correlations are scenario associations, not causal effects.
 from scipy.stats import spearmanr
 for name,x in extra.items(): sensitivities[name]=float(spearmanr(x,base['capture']).statistic)
 out=dict(disclaimer='Hypothetical extrapolation of apparent soluble-receptor data; not a predicted or validated material.',
  source_Kd_oxalate_mM=SOURCE_KD,source='Xu et al., Chemical Science 2024, DOI 10.1039/D4SC05236F',
  development_n=2000,holdout_n=10000,selection='maximize minimum fraction capture>=70% over nominal and combined development conditions',
  selected=best,conditions=CONDITIONS,development_ranking=ranking,holdout=results,grid_combined_holdout=grid_test,
  spearman_nominal_capture=sensitivities,
  population_fraction_enteric_ge70=float(np.mean(test['f']>=.7)))
 (HERE/'cycle3_results.json').write_text(json.dumps(out,indent=2))
 with (HERE/'grid_results.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(grid_test[0]));w.writeheader();w.writerows(grid_test)
 arr=[]; headers=[]
 for cond in CONDITIONS:
  z=evaluate(test,best,cond)
  for key in ['capture','enteric_avoided','urine']:
   arr.append(z[key]*100);headers.append(cond+'_'+key+'_percent')
 np.savetxt(HERE/'selected_holdout.csv',np.column_stack(arr),delimiter=',',header=','.join(headers),comments='')
 print('Selected:',best)
 for name,z in results.items():print(name,'capture',z['capture'],'urine',z['urine'])
 print('Correlations',sensitivities)
