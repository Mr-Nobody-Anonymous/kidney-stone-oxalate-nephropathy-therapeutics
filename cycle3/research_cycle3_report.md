# Research cycle 3: literature-led structural redesign and expanded challenge testing

**10 November 2026 | Completed bounded computational cycle | No breakthrough established**

## Executive decision
**Do not claim a new medicine or a robust 70% result.** A literature search identified a more concrete starting receptor than our original generic polymer: the published TPPC³⁺ bicyclic amide cage. We proposed a tethering modification and tested conditional performance losses and possible improvements in a sequential digestion model.

The important improvement is methodological: the new study includes much stronger chloride competition, sulfate, broad unknown phosphate/citrate competition, and loss of affinity on attachment. Performance becomes less impressive and more uncertain than the previous optimistic specification. That is useful negative evidence about our assumptions—not proof that any actual material fails.

**Recommended direction:** investigate preservation of the cage's binding geometry during immobilization, with early measurement of phosphate/citrate competition. Pause broad claims and avoid adding more exposed cationic polymer sites merely to raise theoretical capacity.

## 1. What the internet search changed
### A. The original guanidinated polymer has an obvious off-target concern
US5880208A describes poly(allylguanidinium) and related polymers specifically as phosphate binders. Thus guanidination is not an evidence-backed route to oxalate selectivity on its own. This source is a patent, not independent validation of every claim; it nevertheless supplies both prior art and a direct design warning. [S1]

### B. A published water-binding receptor supplies a more specific starting scaffold
Xu et al. describe TPPC³⁺·3Cl⁻, a preorganized bicyclic amide cage with six convergent NH donors and pyridinium charge carriers. Their ITC measurements in water give apparent association constants of approximately:

| Guest | Published apparent association constant | Illustrative inverse |
|---|---:|---:|
| Oxalate | (2.0 ± 0.9) × 10⁶ M⁻¹ | ~0.5 µM |
| Sulfate | (2.0 ± 0.6) × 10⁴ M⁻¹ | ~50 µM |

The authors also report chloride association by NMR in D₂O at 589 ± 25 M⁻¹. Their Table 1 does not supply phosphate or citrate constants. Crucially, they explain that the apparent affinities reflect displacement of chloride counterions; they are not a jointly fitted set of intrinsic competition constants. [S2]

These measurements are for a soluble receptor under the paper's conditions, not a tethered polymer in digestive fluid. A ratio near 100 between the central oxalate and sulfate association constants does not mean sulfate can be ignored: abundance matters too.

### C. Core–shell oxalate-binding designs also have prior art
US20050220890A1 discusses core–shell materials for gastrointestinal binding including oxalate. Therefore “put a protective shell around an oxalate binder” is not established as our invention either. [S3]

## 2. Structural redesign proposed—not made
See `structural_edit_brief.md`.

The proposed family replaces a single N-methyl substituent on the published cage with a tether-bearing N-alkyl group, attached to a neutral PEG-rich crosslinked support. The intended objective is to retain the cage and its inward-facing amide donors while keeping it accessible and immobilized.

Connectivity sketch of the changed substituent:

`cage–N⁺–CH3` → `cage–N⁺–CH2CH2CH2–O–(CH2CH2O)6–CH2–[network attachment]`

This is a **proposed chemical-module edit**, not an experimentally validated molecule or full chemical specification. Linker length six is a screening choice. No synthesis, atomic-coordinate modeling, force-field validation, quantum calculation, docking, molecular dynamics, or free-energy calculation has been conducted on it. It may be infeasible or lose the desired binding behavior. The full support composition and attachment chemistry are unresolved.

### Specific parts needing attention
1. **Attachment point and linker:** preserve cavity geometry and avoid steric blockage; attachment effects are unknown.
2. **Amide donors:** preserve the NH donors initially; removing donors could undermine the intended recognition motif.
3. **Bulk surface charge:** replace broad cationic backbone exposure with discrete sites as a hypothesis, not a demonstrated safety improvement.
4. **Surface shielding:** balance access and fouling; PEG is not assumed to distinguish oxalate from small competing ions.
5. **Support integrity and burden:** quantify accessible pockets per gram, swelling, degradation and leaching.

## 3. Computation actually executed
The cycle reuses the version-2 sequential batch digestion model: reversible equilibrium-directed binding, finite access time, first-order absorption of free oxalate, gastric/intestine/colon-like stages, dilution, and loss of available sites.

### New competition surrogate
We changed the hypothetical competitor term to include:

`competition = chloride*589/1000 + sulfate*20000/1000 + phosphate/Kd_P + citrate/Kd_C`

Concentrations and Kd values in this expression use mM. Chloride and sulfate coefficients draw on published central values but are used **only as illustrative surrogates**, not as a validated intrinsic binding model. Mixing D₂O NMR chloride data with H₂O ITC data, and treating apparent affinities as independent constants, is a substantial limitation. Possible counterion double counting is not resolved. The simulation does not reconstruct the paper's experiments.

New/updated assumptions:
- Chloride: 50–150 mM, uniform.
- Sulfate: 0.1–5 mM, log-uniform.
- Phosphate: 1–20 mM, log-uniform; unknown Kd 0.01–10 mM, log-uniform.
- Citrate: 0.1–5 mM, log-uniform; unknown Kd 0.01–10 mM, log-uniform.
- Other oxalate, volume, transit, uptake, site-loss and enteric-fraction distributions are inherited from cycle 2, including the assumed uniform 20–80% enteric contribution.

All digestive ranges and unknown Kd distributions are assumptions, not established measurements for this scaffold or a population. Bile, food proteins/lipids, protonation, precipitation and biological safety are not explicitly resolved.

### Fixed parameter grid
Eighteen hypothetical design bundles:
- Apparent oxalate affinity weakened 10×, 100×, or 1,000× from the parent's illustrative inverse affinity.
- Pocket amounts 0.5, 2, or 4 mmol before sampled accessibility penalties.
- Access time constants 0.1 or 0.5 hour before sampled penalties.

No tested value is calculated from a chemical edit. The grid asks what happens **if** those properties result after immobilization. Pocket amount is not a human dose.

### Selection and evaluation
- Development: 2,000 scenarios, seed 20261113.
- Holdout: 10,000 scenarios, seed 20261114.
- Rule: maximize the smaller of the development fractions achieving ≥70% capture under nominal and combined-challenge conditions.
- Selected bundle: 4 mmol nominal pockets, 0.005 mM oxalate Kd (10× loss from parent illustrative inverse), 0.1-hour access, no assumed extra competitor discrimination.
- Reported all 18 designs in `grid_results.csv`.

Eight finite challenge envelopes were examined—not “all conditions”:
1. Nominal.
2. Threefold competition.
3. Tenfold competition.
4. Half accessible sites.
5. Tenfold slower access.
6. Hundredfold weaker oxalate affinity.
7. Combined: 0.6× sites, 10× weaker affinity, 3× competition, 3× slower access.
8. Severe combined: 0.3× sites, 100× weaker affinity, 10× competition, 10× slower access.

The held-out draws come from the same assumed distributions and are not external experimental validation. The robustness score is restricted to the stated scenarios; it is not a worst-case guarantee.

## 4. Main holdout results: failure to reach robust 70%
All values below are simulated. “Urinary reduction” means proportional absorption reduction multiplied by the assumed enteric fraction; it is not a prediction of patient response.

| Condition | Median final capture | Scenarios with ≥70% capture | Median urinary reduction |
|---|---:|---:|---:|
| Nominal | 46.34% | 18.88% | 26.02% |
| Competition 3× | 22.44% | 3.23% | 15.45% |
| Competition 10× | 7.74% | 0.10% | 6.60% |
| Half accessible sites | 28.52% | 5.19% | 18.06% |
| Access 10× slower | 45.72% | 16.17% | 23.06% |
| Affinity 100× weaker | 0.78% | 0% | 0.79% |
| Combined | 1.59% | 0% | 1.52% |
| Severe combined | 0.03% | 0% | 0.02% |

These lower numbers do not contradict an experiment: there is no experiment on our candidate. They show that previous optimistic numbers are not stable to changes in assumed chemistry and competition. Different cycle results must not be interpreted as measured improvements or deterioration of the same material.

## 5. Counterfactual edit tests: which properties matter?
A separate script evaluates improvements as requirements. It **does not predict** that the proposed tether/support edits achieve them. Same 10,000 holdout scenarios; these comparisons are exploratory analyses, not another independent validation set.

| Hypothetical achieved properties | Nominal median capture | Nominal scenarios ≥70% capture | Combined median capture | Severe median capture |
|---|---:|---:|---:|---:|
| Selected penalized reference | 46.34% | 18.88% | 1.59% | 0.03% |
| Preserve parent's illustrative affinity after attachment | 88.96% | 85.01% | 14.38% | 0.25% |
| 10× lower competition, but half capacity and 5× slower access | 73.39% | 56.02% | 7.74% | 0.14% |
| Both improvements, with those penalties | 94.69% | 93.47% | 37.48% | 1.35% |

The combined-improvement variant's nominal modeled urinary reduction is 45.66%, and its combined-challenge value 18.37%. It still does not establish the requested 70% urinary result or robust capture across challenges.

**Interpretation:** preserving affinity and reducing competition could matter more than simply speeding access in this scenario set. However, they may not be independently adjustable, and the assumed affinity loss/competition reduction need measurement. Surface shielding alone does not establish tenfold small-anion selectivity.

## 6. Unknown phosphate binding is an early decision point
In nominal holdout scenarios, Spearman association between assumed phosphate Kd and final capture was +0.384; between citrate Kd and capture +0.107; between total competition burden and capture −0.556. Higher Kd means weaker competing binding. These are associations within sampled inputs, not causal effects or experimental sensitivity estimates.

**Practical priority:** measure phosphate and citrate competition and chloride dependence early, rather than pursuing more receptor loading without knowing what occupies it. An attractive oxalate affinity in water can coexist with inadequate capture in a mixed fluid.

## 7. What the tests establish—and do not
The simulation calls inherit mass-conservation and nonnegativity assertions from version 2. Development/holdout separation, finite challenge envelopes, a full parameter grid and counterfactual edit comparisons were executed. Version-2 numerical-control results remain in its original report; they are not newly repeated molecular validation.

No cell, animal, human, swelling, nutrient-binding, medicine-binding or leaching test was conducted. No optimized binding geometry was computed. No new receptor constant was predicted from atoms. No clinically meaningful dose or success rate is established.

## 8. Why stop this computational cycle here?
The unmet bottleneck is identifiable: we lack a verified modified structure and binding/selectivity data under relevant conditions. More parameter sweeps can always be made to look successful by assuming enough affinity or capacity; that would not be a discovery.

Next warranted steps are: verify the scaffold/attachment structure, measure parent and derivative competitive binding in matched conditions, measure retention and access kinetics, establish accessible capacity per gram and material integrity, and run the safety/interactions panel. Molecular free-energy work would require a validated, explicit-solvent host–guest setup and a fully specified derivative, not generic protein docking.

**Final verdict:** a more specific literature-led design hypothesis and a clearer failure mechanism—not a breakthrough, not a new medicine, and not proof that 70% efficacy is achievable safely.

## Files and reproduction
Requires Python, NumPy and SciPy.

From the cycle3 directory:
```
python simulate_cycle3.py
python test_edit_requirements.py
```
Keep the sibling `next_steps/simulate_v2.py`, which supplies the simulation engine. The downloadable package includes it. Results:
- `cycle3_results.json`: grid selection, challenge summaries, and scenario associations.
- `grid_results.csv`: all 18 grid bundles under combined holdout conditions.
- `selected_holdout.csv`: selected-design outputs for all 10,000 scenarios in eight conditions.
- `edit_requirement_results.json`: four counterfactual edit outcomes.
- `structural_edit_brief.md`: exact proposed substitution module and unresolved chemistry.

## Sources
[S1] US5880208A, Polymer compounds: https://patents.google.com/patent/US5880208

[S2] Xu et al., Charge-assisted hydrogen bonding in a bicyclic amide cage: an effective approach to anion recognition and catalysis in water, Chemical Science 15 (2024), 16040–16049. DOI 10.1039/D4SC05236F. Primary article and Table 1 read: https://pubs.rsc.org/sc/article/15/39/16040/869866/Charge-assisted-hydrogen-bonding-in-a-bicyclic

[S3] US20050220890A1, Ion binding compositions: https://patents.google.com/patent/US20050220890

Searches were targeted, not a systematic review or exhaustive patent analysis. No current clinical approval claim is made for any receptor or proposed material.
