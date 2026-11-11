# Next-step oxalate binder study: all three 70% targets

**10 November 2026 | Computational work completed; laboratory work NOT performed**

## Bottom line
We tested a stronger *hypothetical property specification*, not a manufactured medicine. Under nominal assumed conditions it met the modeled gut-capture goal, but failed the same robustness goal under harsher conditions. It did not reach a median 70% urinary-oxalate reduction. No clinical success probability can be estimated.

The useful outcome is a measurable requirements brief, an executable sequential-digestion model, negative-control and numerical checks, and a laboratory validation plan. This work does not establish novelty, safety, drug efficacy, or a practical dose.

## 1. What has and has not been done
| Requested next step | Completed here | Still required |
|---|---|---|
| Define a material and measure binding | Proposed PAA-G25-PEG screening-material family and matched variants | Finish exact chemistry/manufacturing specification, manufacture batches, characterize identity, measure binding |
| Test realistic mixtures | Simulated competitive ions, dilution, staged affinity changes, uptake, site loss, and a stress scenario | Physical testing in validated digestive/meal mixtures including bile, proteins and fats |
| Test retention | Modeled reversible binding and downstream release | Actual sequential-digestion and desorption assays |
| Toxicity, swelling, nutrient/medicine binding | Wrote test panel and blank measurement template | All physical safety, swelling, and interaction measurements |
| Compare existing approaches | Reviewed human and review literature; specified controls | Matched head-to-head laboratory and later clinical comparisons |

**None of the blank experimental fields has been filled with simulated data.**

## 2. The proposed research material
**PAA-G25-PEG**: a proposed covalently crosslinked poly(allylamine)-based particle family with a target 25 mol% pendant-site guanidinium functionalization and a PEG-rich hydrated surface. G0/G10/G25 and coated/uncoated controls are specified in the laboratory plan.

This narrows the earlier conceptual material to a screening family. It is **not yet a fully defined formulation**: crosslink chemistry, precursor distribution, particle sizes, graft density, counterion, manufacturing conditions, impurity specifications, and several other details remain unresolved. The substitution level is an exploratory choice, not an experimentally optimized value.

Most importantly, there is **no evidence this proposed material has the simulated properties**. The simulated designs are parameter bundles independent of chemistry. No association between a named polymer and a binding constant or safety profile has been measured or predicted at the molecular level.

Existing patents already cover broad oxalate-binding polymer approaches, including guanidino groups and imprinting. This is not a novelty or freedom-to-operate opinion. [S1]

## 3. Improved model
Version 1 estimated equilibrium capture and multiplied by an access factor. Version 2 follows oxalate amounts through sequential gastric, small-intestinal, and colonic-like batch stages. It tracks three pools: free, bound, and absorbed oxalate.

At each short time step:
1. Compute competitive single-pocket equilibrium for free plus bound oxalate.
2. Relax toward that equilibrium, permitting binding and release.
3. Absorb a fraction of free oxalate with a first-order uptake coefficient.
4. Carry free and bound amounts forward; absorbed amounts accumulate.

At stage transitions, dilution, prescribed affinity changes, and loss of accessible sites can cause release. This is not an anatomically validated transport model; the stages are sequential batches, not coupled physiological compartments.

### Equations
Amounts are mmol, volumes L, time hours, and dissociation constants mM.

`Keff = Kd * stage_affinity_multiplier * (1 + competition)`

`competition = Cl/Kd_Cl + phosphate/Kd_P + citrate/Kd_Cit`

`M = free + bound`

`M = x + S*x/(Keff*V + x)`

Here x is equilibrium free amount, S is currently accessible pocket amount, and V is volume. Bound amount approaches equilibrium with `1-exp(-dt/tau)`. Free oxalate absorption is `free*(1-exp(-ka*dt))`.

**Metrics:**
- Gut capture = final bound amount / initial accessible oxalate amount.
- Enteric absorption reduction = 1 − absorbed with binder / absorbed without binder in the same scenario.
- Urinary reduction = enteric absorption reduction × assumed enteric fraction of baseline urinary oxalate.

Gut capture is not equal to urinary reduction. Some oxalate would leave unabsorbed without a binder. The no-binder uptake denominator is computed analytically.

### Assumed scenario ranges
These are deliberately hypothetical, not measured patient distributions or a validated simulated-digestion recipe.

| Input | Assumption |
|---|---|
| Initial accessible oxalate | 0.1–1.5 mmol, log-uniform |
| Initial volume | 0.2–1 L, uniform |
| Accessible fraction of nominal pocket amount | 0.5–1, log-uniform |
| Oxalate Kd uncertainty multiplier | 0.3–3, log-uniform |
| Access-time uncertainty multiplier | 0.5–2, log-uniform |
| Chloride concentration and Kd | 50–150 mM uniform; Kd 10–1,000 mM log-uniform |
| Phosphate concentration and Kd | 1–20 mM; Kd 0.1–10 mM, log-uniform |
| Citrate concentration and Kd | 0.1–5 mM; Kd 0.1–10 mM, log-uniform |
| Gastric / intestinal / colonic duration | 0.5–2 / 1–4 / 2–12 hours, uniform |
| Gastric / intestinal / colonic uptake coefficient | 0 / 0.03–0.4 / 0.01–0.15 per hour; nonzero values log-uniform |
| Downstream volume multiplier | 1–3, uniform; same downstream volume in stages 2 and 3 |
| Site-loss coefficient | 0–0.2, uniform; stage j retains fraction 1−j×loss, j=0,1,2 |
| Stage Kd multipliers | 10, 1, 2; arbitrary surrogate for changing environment, not a pH model |
| Enteric fraction of urinary oxalate | 0.2–0.8, uniform |

Competitors are fixed reservoirs; their depletion, detailed binding kinetics and protonation states are not resolved. Bile, fats, proteins, drug binding and toxicity are not explicitly modeled. The stress multiplier represents unspecified adverse conditions; it is not a validated bile/fouling model.

### Fixed design set
| Parameter bundle | Nominal accessible pockets before scenario multiplier | Oxalate Kd | Competitor-affinity factor | Access time |
|---|---:|---:|---:|---:|
| Baseline | 0.5 mmol | 0.1 mM | 1 | 0.5 h |
| Capacity only | 4 mmol | 0.1 mM | 1 | 0.5 h |
| Selective combined | 1 mmol | 0.1 mM | 0.1 | 1 h |
| Aspirational requirements | 4 mmol | 0.01 mM | 0.1 | 0.1 h |

Factor 0.1 means tenfold weaker binding of the modeled competitors while keeping the stated oxalate affinity. The aspirational bundle simultaneously assumes high capacity, stronger affinity, better selectivity, and fast access. **There is no demonstrated physical route to achieving these simultaneously.** It is a target specification, not an optimized drug.

The pocket amounts are not human doses. Converting them to grams requires measured accessible capacity per gram and a justified physiological exposure model.

### Development and holdout
- 3,000 development scenarios, seed 20261111.
- Selection rule: highest fraction of development scenarios with at least 70% final capture.
- 10,000 independent holdout scenarios, seed 20261112, from the same assumed distributions.
- All four designs reported, not just the selected one.
- Selected design: aspirational requirements.

A synthetic holdout checks performance on new random draws, **not real-world predictive validity**. These input ranges and designs are exploratory; they are not independently preregistered clinical hypotheses.

## 4. Nominal holdout results
Every value below is a simulated output from assumed properties.

| Design | Median final gut capture | Scenarios with ≥70% capture | Median urinary reduction | Scenarios with ≥70% urinary reduction | Scenarios with ≥20% urinary reduction |
|---|---:|---:|---:|---:|---:|
| Baseline | 5.46% | 0.00% | 4.16% | 0.00% | 3.77% |
| Capacity only | 34.80% | 12.56% | 19.97% | 0.12% | 49.87% |
| Selective combined | 32.15% | 4.72% | 17.34% | 0.02% | 40.93% |
| Aspirational requirements | **96.07%** | **98.34%** | **47.67%** | **11.60%** | **98.28%** |

For the aspirational design, capture's 10th–90th percentile is 85.37–99.03%; urinary reduction's is 24.89–70.94%. These are scenario percentiles, not confidence intervals or patient outcome ranges.

The large increase from baseline results from explicitly assuming substantially better properties—not from evidence that a new chemistry achieves them. Version 1 and version 2 results are not directly comparable efficacy estimates: model structure and input distributions changed.

## 5. Stress test: important failure
Without retuning the design, the stress test applies:
- 40% lower accessible pocket amount;
- threefold higher oxalate Kd (weaker binding);
- threefold higher competition term;
- threefold longer access time.

| Aspirational design endpoint | Nominal holdout | Stress holdout |
|---|---:|---:|
| Median capture | 96.07% | **69.30%** |
| Scenarios reaching ≥70% capture | 98.34% | **48.78%** |
| Median urinary reduction | 47.67% | **34.47%** |
| Scenarios reaching ≥70% urinary reduction | 11.60% | **1.61%** |
| Scenarios reaching ≥20% urinary reduction | 98.28% | **82.74%** |

Thus it does **not** achieve ≥70% capture in ≥70% of stress scenarios. It does achieve ≥20% modeled urinary reduction in ≥70% of stress scenarios, but 20% is only an illustrative engineering benchmark here, not a validated clinical criterion.

## 6. All three requested goals: verdict
1. **70% gut capture:** conditionally achievable in the nominal model; not physically demonstrated and not robust in the tested stress set.
2. **70% urinary reduction:** median goal not reached, even nominally.
3. **A threshold met in 70% of scenarios:** depends on the threshold. ≥70% capture passes nominally but fails under stress. ≥20% urinary reduction passes both nominal and stress sets for the aspirational bundle. ≥70% urinary reduction fails both.

### Why the urinary goal is structurally difficult
In this model `urinary_reduction ≤ enteric_fraction`. If only 50% of baseline urinary oxalate is enteric, even perfect prevention of enteric absorption cannot exceed a 50% total reduction. A 70% total reduction requires an enteric fraction of at least 70%, and nearly complete absorption prevention when that fraction is near 70%.

Only 16.64% of holdout scenarios even have an enteric fraction ≥70%; therefore a design cannot reach 70% urinary reduction in 70% of this scenario population, regardless of binding optimization. This is a mathematical consequence of an assumed 20–80% distribution, **not an epidemiological estimate**. The model excludes gut secretion/systemic oxalate removal and adaptive physiology; it is not a universal bound for every gut-targeted therapy.

## 7. Computational tests actually executed
- Conservation: free + bound + absorbed equals initial oxalate in every simulated scenario, within the script's 10^-10 mmol tolerance.
- Nonnegative free, bound, and absorbed amounts asserted.
- No-binding-site negative control: maximum apparent urinary effect 1.66×10^-15 (numerical zero).
- No-absorption conservation test executed.
- Time-step refinement on 100 selected-design holdout cases: maximum capture difference 0.0285 percentage points (120 vs 240 steps per stage), then 0.0138 points (240 vs 480); urinary difference 0.0137 points (240 vs 480).
- Development/holdout separation and fixed-design adverse-condition test completed.

These checks test arithmetic, implementation, and selected numerical behavior—not chemistry, physiology, toxicity, or the entire parameter space. No docking or molecular dynamics was performed.

## 8. Evidence-based comparator context
The 2022 randomized reloxaliase trial included 115 participants. Its repeated-measures analysis reported 22.6% urinary-oxalate reduction for reloxaliase versus 9.7% for placebo over four weeks, with a reported between-group estimate of 14.3 percentage points. Adverse events occurred in 69% versus 53%, most commonly gastrointestinal. These human data are much stronger evidence than our simulation, but they do not validate our material or show it is better. The trial authors called for further investigation of stone outcomes. [S2]

A 2024 review describes uncertain efficiency of non-calcium chelators and concern about hypophosphatemia. This reinforces the need to measure off-target binding rather than treating it as a cosmetic issue. [S3]

A human acute-load study found that unmodified chitosan did not reduce post-prandial urinary oxalate. This argues against selecting a convenient cationic biopolymer based only on charge. It does not directly test our proposed different material family. [S4]

No numerical human-versus-simulation efficacy comparison establishes superiority; endpoints, populations, uncertainty, and study designs differ. Reloxaliase is cited as investigational human evidence, not as a claim of current approval or availability.

## 9. What would genuinely improve this project now?
1. Manufacture and fully characterize a small matched materials series; resolve the incomplete identity specification.
2. Measure competitive binding and release in blinded realistic mixtures with adequate mass balance.
3. Measure coating-induced kinetic penalties; retain a simpler noncoated control.
4. Measure swelling, leachables, epithelial effects, and nutrient/drug binding before advancing.
5. Fit model parameters to those results and reserve independent mixtures and batches for validation.
6. Advance only if a practical burden and acceptable safety are demonstrated; otherwise revise or abandon the family.

Adding capacity or assuming a still-lower Kd can force the model upward. That would not be a scientific improvement without evidence those properties are achievable. We stop short of claiming a 70% clinically successful medicine.

## Files
- `simulate_v2.py`: complete executable model and tests; requires Python and NumPy.
- `results_v2.json`: development, holdout, stress, and numerical-check summaries.
- `holdout_results.csv`: 10,000 nominal holdout outputs per design and endpoint.
- `laboratory_validation_plan.md`: material characterization, realistic mixture, retention, safety, comparator, and analysis plan.
- `laboratory_measurements_BLANK.csv`: intentionally blank experimental results template.

## Sources
[S1] US7459502B2, oxalate-binding polymers / guanidino groups / imprinting: https://patentimages.storage.googleapis.com/a8/25/d1/2baf3018c33f01/US7459502.pdf

[S2] Lieske et al., Randomized Placebo-Controlled Trial of Reloxaliase in Enteric Hyperoxaluria (2022), primary publication abstract accessed through institutional repository: https://scholarworks.indianapolis.iu.edu/items/abf8543d-cf09-49e5-80f8-24fe83dedd56 ; DOI https://doi.org/10.1056/EVIDoa2100053

[S3] Pathophysiology and management of enteric hyperoxaluria (2024): https://www.sciencedirect.com/science/article/pii/S2210740124000433

[S4] Chitosan does not reduce post-prandial urinary oxalate excretion (2006): https://link.springer.com/article/10.1007/s00240-006-0048-2

Searches were targeted, not exhaustive. Current clinical development/approval status, patent validity, and freedom to operate were not comprehensively established.
