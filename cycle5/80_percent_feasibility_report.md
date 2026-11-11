# Can the design achieve 80% in every condition?

**10 November 2026 — requirements study, not a validated molecule**

## Answer
Not with evidence currently available. We can specify and test an 80% engineering target, but we cannot honestly design a proven 80%-effective-and-safe medicine from the present data. The current hypothetical property envelope fails the target, and some failures follow from basic capacity/selectivity limits rather than a lack of simulation effort.

This cycle evaluated **1,024 parameter corners in each of six condition envelopes: 6,144 equilibrium evaluations**. These are deliberately chosen extremes, not patients, population frequencies, all possible conditions, or physical experiments.

## What “80%” means here
Primary target: at least 80% equilibrium capture of accessible oxalate in each tested condition. Separately track phosphate and citrate removal, using no more than 10% removal of each as an illustrative design constraint. That constraint is NOT an established safety threshold. There is no universal “80% safe” score; toxicity and clinical benefit require different endpoints and evidence.

## A useful exact design requirement
For the simplified shared-pocket equilibrium model, the fraction of ligand i bound is:

`fraction_bound_i = s / (Kd_i + s)`

where s is the concentration of free binding pockets.

At least 80% oxalate binding requires:

`s ≥ 4 × Kd_oxalate`

No more than 10% binding of a competing ligand requires:

`s ≤ Kd_competitor / 9`

Therefore both can be satisfied only if:

**`Kd_competitor / Kd_oxalate ≥ 36`**

That means phosphate and citrate must each bind at least 36-fold more weakly than oxalate under the actual tested conditions. This is an exact necessary selectivity condition within this one-pocket model, not a newly discovered law or experimental finding. It does not by itself guarantee practical capacity, kinetics or safety.

If environmental changes make oxalate binding 100-fold weaker while competing binding becomes tenfold stronger, the *nominal* ratio must be at least **36,000** to retain that modeled selectivity requirement. Those challenge factors are hypothetical; they are not measured effects on the proposed receptor.

### Requirements by stated challenge
| Challenge | Minimum nominal competitor Kd / oxalate Kd ratio |
|---|---:|
| Nominal | 36 |
| Oxalate affinity 10× weaker | 360 |
| Competitor affinity 10× stronger | 360 |
| Half sites | 36 |
| Combined: oxalate affinity 10× weaker, competitor affinity 3× stronger | 1,080 |
| Severe: oxalate affinity 100× weaker, competitor affinity 10× stronger | 36,000 |

Capacity loss does not change this ratio but can independently make the capture target impossible.

## Capacity can prevent 80% even with ideal binding
Suppose accessible oxalate is 1.5 mmol, nominal pockets are 4 mmol, and only half the nominal pockets are accessible.

| Condition | Pockets available | Best possible capture based on capacity alone |
|---|---:|---:|
| No additional site loss | 2 mmol | Up to 100% |
| Half of those sites remain | 1 mmol | At most 66.7% |
| 60% of those sites remain | 1.2 mmol | At most 80% |
| 30% of those sites remain | 0.6 mmol | At most 40% |

These upper bounds ignore competitors and assume ideal retention. Real equilibrium capture is lower. Merely matching the bound leaves no room for competitor occupancy or free sites. Under the severe case, at least 8 mmol nominal pockets would be necessary for the 80% target before accounting for those penalties; it is not sufficient. This is not a human dose recommendation.

## Finite corner tests actually executed
Using the cycle-4 finite-pool shared-pocket equilibrium model, enumerate both endpoints of each assumed input range:
- oxalate amount: 0.1 or 1.5 mmol;
- fluid volume: 0.2 or 1 L;
- accessible fraction: 0.5 or 1;
- oxalate Kd: 0.0005 or 0.05 mM;
- phosphate/citrate Kd: 0.001 or 10 mM each;
- chloride: 50 or 150 mM;
- sulfate: 0.1 or 5 mM;
- phosphate: 1 or 20 mM;
- citrate: 0.1 or 5 mM.

Fixed surrogate chloride Kd is 1000/589 mM; sulfate Kd is 0.05 mM. As explained in cycle 4, source-inspired surrogate constants are not jointly fitted intrinsic constants for a tethered cage. All ranges are assumed exploratory bounds.

Six envelopes modify oxalate affinity, competitor affinity and available sites. Every point uses 4 mmol nominal pockets. The severe envelope has 100× weaker oxalate affinity, tenfold stronger competing affinities and 30% site retention before the sampled accessibility factor.

| Envelope | Corners meeting ≥80% capture | Corners meeting capture plus both off-target constraints |
|---|---:|---:|
| Nominal | 41.50% | 15.04% |
| Oxalate affinity 10× weaker | 24.71% | 10.16% |
| Competitors bind 10× stronger | 24.80% | 10.16% |
| Half sites | 24.02% | 9.96% |
| Combined | 9.67% | 4.30% |
| Severe combined | 0% | 0% |

**No envelope passed in every corner.** Equal-weight corner counts are not clinical success probabilities. Passing all corners would not establish all-condition robustness for a nonlinear model or unmodeled biology. Failing one included corner is sufficient to disprove the all-corners claim for this stated model/envelope.

The script also calculates nominal pockets needed for 80% capture alone. Some corner requirements are extremely large because the model fills competing pools. They are diagnostic signs of an unsuitable selectivity envelope, not practical prescriptions to administer more polymer. More capacity cannot repair every selectivity failure: if the ratio condition above fails, increasing sites eventually binds too much competitor.

## What should change in the molecular design?
### Keep the cage-based design as a research series, not a finished R80 molecule
The cycle-4 short/medium/long tether fragments are still unvalidated alternatives. We cannot assign the best selectivity to a particular tether without structural and binding evidence.

### Revised design priorities
1. **Cavity recognition before receptor loading.** Preserve the cage's convergent amide donors and investigate geometry changes only with validated aqueous structural/free-energy work. No exact atom substitution is proven to produce the required selectivity.
2. **Attachment must preserve function.** Compare the parent against fully specified, tethered derivatives under identical conditions. An apparently favorable linker can obstruct the cavity or change hydration.
3. **Accessible-site retention must be measured.** A stable total amount of polymer is not the same as a stable number of usable pockets.
4. **Avoid claiming PEG gives small-ion selectivity.** It may change access and surface interactions, but no demonstrated mechanism here selectively excludes phosphate/citrate while allowing oxalate.
5. **Reject property combinations that cannot satisfy joint constraints.** Do not raise the assumed affinity or capacity merely to obtain a passing result.

### Proposed “R80” specification—not a chemical identity
A candidate would need, under every *prespecified relevant* condition:
- measured ≥80% retained accessible oxalate capture over the relevant transit period;
- experimentally justified off-target binding limits;
- enough accessible pockets after losses, at a practical material burden;
- acceptable kinetics, stability, impurities, swelling, leaching, interactions and toxicity;
- independent validation on batches/mixtures not used for fitting.

The current work does not establish a material meeting this specification. Molecular novelty and manufacturability also remain unresolved.

## Tests that cannot be covered by this equilibrium calculation
No toxicity, human safety, swelling, degradation, nutrient/medicine interaction, timed digestion, absorption, urinary reduction or stone-prevention endpoint is validated here. An equilibrium 80% capture result cannot substitute for any of those. A gut binder also does not automatically produce an equal percentage reduction in urinary oxalate.

## Files and reproduction
Requires Python and NumPy. Run `python check_80_percent.py`.
- `results.json`: condition summaries, derived selectivity requirements and capacity bounds.
- `corner_inputs.csv`: all 1,024 parameter corner definitions.
- `corner_results.csv`: all 6,144 evaluations, including required pockets and selectivity feasibility.

## Conclusion
We did not achieve an 80%-in-all-conditions design. We obtained a clearer quantitative reason why the present design envelope fails and the requirements a future material would need to satisfy. The responsible next step is to resolve the exact chemical identity and obtain selectivity/site-retention evidence—not to declare success by assuming stronger properties.
