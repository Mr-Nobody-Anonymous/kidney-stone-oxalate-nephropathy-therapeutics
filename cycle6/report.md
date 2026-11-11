# Simulation-only inverse design: more than 80% in every tested condition

**10 November 2026 | A mathematically passing property specification—not a validated molecule**

## Result
A hypothetical parameter specification achieved **at least 85.04% equilibrium oxalate capture in all 6,144 enumerated corner tests**, spanning the six previously stated condition envelopes. It also passed **60,000 evaluations at independently sampled interior points** (10,000 points × six envelopes), with minimum capture 91.77% there.

**Critical qualification:** passing required extreme, unsupported property changes, especially a **100-million-fold reduction in affinity for every modeled competitor**. This is not an improvement demonstrated for any chemical structure. The result answers “what assumptions make this model pass?”, not “have we designed a feasible medicine?”

## Fixed goals and constraints
- Capture target for selection: ≥85%, giving margin above 80%.
- Phosphate and citrate removal: each ≤10% in every test.
- The 10% constraints are illustrative engineering limits, not demonstrated safety thresholds.
- Same oxalate loads, volumes, accessibility ranges, competitor concentration ranges and six environmental challenge definitions as cycle 5.
- Changeable properties: oxalate affinity multiplier, competitor affinity multiplier, and nominal pocket amount.

We did not preserve the original material-property uncertainty bounds unchanged: those original Kd bounds are multiplied by the newly selected property-improvement factors. Such changes are explicitly hypothetical and not inferred from molecular edits.

## How the search works
In the shared-pocket equilibrium model, for a target 85% oxalate occupancy, required free-pocket concentration is:

`s_min = (0.85 / 0.15) * Kd_oxalate`

For ≤10% phosphate/citrate occupancy:

`s_max = min(Kd_phosphate, Kd_citrate) / 9`

At either value, the corresponding total pocket amount is obtained by adding free pockets and all bound ligands, multiplying by volume and accounting for accessibility/site retention. Across all corner tests, the program computes a lower pocket-amount limit for capture and an upper limit for the off-target constraints.

A property bundle passes the inverse screen when a single fixed nominal pocket amount satisfies both bounds across all listed corner tests. The selected amount is 0.1% above the calculated lower bound. The forward equilibrium solver then independently calculates binding for all corners and newly sampled interior points.

An initial 6×6 multiplier grid, through one million-fold changes, found no joint solution. The grid was expanded to include competitor Kd multipliers of 100 million and 10 billion **to quantify the extreme mathematical requirements**, not because literature supports those changes. The final script evaluates 48 multiplier combinations. This extension is disclosed rather than presenting the result as a preregistered discovery.

The ranking score is an arbitrary transparent sum of log multipliers and a capacity penalty. It is not synthesis cost, chemical feasibility or a global optimum. The code reports all tested bundles.

## Selected property specification
| Property | Assumed change |
|---|---:|
| Oxalate Kd | Divide original scenario value by **100** (stronger binding) |
| Every competing-ligand Kd | Multiply by **100,000,000** (weaker binding) |
| Nominal pocket amount | **10.404 mmol**, before accessibility and challenge losses |

The original nominal pocket amount was 4 mmol. Pocket amounts are not gram doses: accessible capacity per gram and a physiological exposure model are unknown.

### Why the enormous selectivity change matters
The model effectively suppresses almost all competitor binding. Some resulting Kd values are far outside physically accessible aqueous concentrations; this is a mathematical near-nonbinding limit, not a measured property or a credible synthesized material specification.

We have no molecular calculation, experimental evidence, or demonstrated structural edit capable of producing the chosen changes. These factors must not be assigned to the previously drawn tether fragments. No new chemical structure was designed or validated by this parameter search.

## Forward test results
The following are minima over the 1,024 corners per condition—not average capture.

| Condition envelope | Minimum capture | Maximum phosphate removal | Maximum citrate removal |
|---|---:|---:|---:|
| Nominal | 99.986% | 0.0515% | 0.0515% |
| Oxalate affinity 10× weaker | 99.865% | 0.0515% | 0.0515% |
| Competitors bind 10× stronger | 99.986% | 0.5125% | 0.5126% |
| Half sites | 99.955% | 0.0255% | 0.0255% |
| Combined | 99.693% | 0.0920% | 0.0921% |
| Severe combined | **85.042%** | 0.1508% | 0.1508% |

All 6,144 corner evaluations passed the capture/off-target criteria. Independently sampled interior points also passed all 60,000 evaluations; their worst capture was 91.771% in the severe envelope. Corner counts and random-point fractions are not population probabilities or clinical success rates.

There is no proof here of performance throughout the entire continuous domain, outside it, or under unmodeled conditions. “Every tested condition” does not mean “every possible condition.”

## Comparison without changing affinity/selectivity
If original affinity/selectivity assumptions are retained and only capacity is increased, the calculated nominal pockets needed for at least 85% capture across the listed corners reach approximately **1,391 mmol**. This capture-only calculation does not satisfy the off-target goals in general and is not a proposed material burden or dose. It illustrates why loading alone is an unsuitable route to the joint target in this envelope.

## What was tested computationally
- Analytic inverse bounds followed by forward equilibrium solutions.
- Conservation of free plus bound sites checked numerically in every forward call.
- A fixed final property specification tested at all enumerated corners and independent interior points.
- Full input and output files retained for reproduction.

The equilibrium equation, unknown binding constants and biological simplifications remain unvalidated. Passing these numerical checks does not validate the chemistry.

## What is NOT covered
No time-dependent digestion, downstream release, absorption, urinary reduction, stone prevention, toxicity, swelling, degradation, leaching, drug interactions or clinical efficacy was established. The 85% result applies only to equilibrium capture in this mathematical model.

## Scientific conclusion
**The requested simulation target can be made to pass, but only by adopting extreme hypothetical properties in this search.** That is useful as a requirements/feasibility analysis, not a breakthrough or a feasible molecular design. The next chemical research task is to determine what much smaller affinity/selectivity improvements a fully specified derivative can actually achieve, then repeat the tests with defensible parameter bounds.

## Files and reproduction
Requires Python and NumPy. Run `python optimize.py`.
- `results.json`: complete grid, selected properties, and all condition summaries.
- `test_outputs.csv`: all 66,144 forward evaluations.
- `corner_inputs.csv`: 1,024 parameter corners, reused across six envelopes.
- `interior_inputs.csv`: 10,000 independently sampled interior points; seed 20261116.

No internet source is cited as support for the chosen improvement factors: there is none established in this work. The underlying receptor literature and its limitations are documented in earlier cycle reports.
