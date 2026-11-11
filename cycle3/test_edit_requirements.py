"""Counterfactual edit outcomes, not molecular predictions. Run after simulate_cycle3.py."""
from pathlib import Path
import json
from simulate_cycle3 import make,evaluate,summarize
P=Path(__file__).parent
D,_=make(10000,20261114)
# Prespecified counterfactual changes relative to grid-selected specification.
variants={
 'selected_penalized_reference':dict(sites=4,kd=.005,competitor_factor=1,tau=.1),
 'preserve_parent_affinity':dict(sites=4,kd=.0005,competitor_factor=1,tau=.1),
 'selective_shield_with_capacity_and_access_penalties':dict(sites=2,kd=.005,competitor_factor=.1,tau=.5),
 'both_preservation_and_selective_shield_with_penalties':dict(sites=2,kd=.0005,competitor_factor=.1,tau=.5),
}
out={}
for name,design in variants.items():
 out[name]={'parameters':design}
 for cond in ['nominal','combined','severe_combined']:
  out[name][cond]=summarize(evaluate(D,design,cond))
(P/'edit_requirement_results.json').write_text(json.dumps(out,indent=2))
for name,z in out.items():
 print(name)
 for cond in ['nominal','combined','severe_combined']:
  print(cond,'median capture',z[cond]['capture']['p10_p50_p90_percent'][1],'>=70%',z[cond]['capture']['fraction_ge_70pct'],'median urine',z[cond]['urine']['p10_p50_p90_percent'][1])
