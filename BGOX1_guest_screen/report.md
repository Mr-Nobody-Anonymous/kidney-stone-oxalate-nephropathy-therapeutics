# BGOX-1: oxalate and competitor geometric pose screen

**10 November 2026 | New host–guest geometry test, not a binding-affinity simulation**

## What this test can answer
Can an ion be placed near both guanidinium arms of BGOX-1 without major heavy-atom overlap under the stated geometric rules?

This tests one part of the unknowns: **physical pose accessibility**. It does not answer whether binding is thermodynamically favorable, how strong it is, what percentage is captured in solution, or whether the molecule is safe.

## Work executed
- The exact BGOX-1 dication from the previous design was used.
- Generated 24 receptor conformers and optimized their geometry using MMFF with constant dielectric 78.4. This is a simplified electrostatic treatment, not explicit water.
- Prepared one guest geometry each for oxalate, hydrogen phosphate, sulfate, citrate and chloride, with fixed charge states.
- For each receptor shape and guest, sampled 4,000 random orientations/positions in a cube ±4 Å around the midpoint of the two guanidinium central carbons.
- **96,000 poses per guest; 480,000 poses total.**

### Prespecified geometric rules
1. Reject a pose if any guest–host heavy-atom distance is below 0.75 times the sum of the atoms' van der Waals radii.
2. A two-arm proximity pose has at least one oxygen/Cl atom 2.5–3.5 Å from a nitrogen on each guanidinium arm.
3. Also count a stricter variant requiring different guest oxygen atoms near the two arms.

These thresholds are arbitrary, transparent screening rules. They are not validated cutoffs for binding. Nitrogen–oxygen proximity does not establish a hydrogen bond: donor direction, hydrogen positions, oxygen chemistry, hydration and energetics are not included. All guest oxygen atoms were considered geometrically, including hydroxyl oxygens; they are not all equivalent hydrogen-bond acceptors.

## Results
| Guest | Sampled poses passing clash + two-arm proximity rules | Of those, different oxygen atoms can contact the two arms | Receptor conformers with at least one two-arm pose |
|---|---:|---:|---:|
| Oxalate | 1,152 | 1,080 | 24 / 24 |
| Hydrogen phosphate | 1,112 | 1,067 | 23 / 24 |
| Sulfate | 1,076 | 1,036 | 24 / 24 |
| Citrate | 1,178 | 1,144 | 24 / 24 |
| Chloride | 379 | Not applicable: one atom | 12 / 24 |

### Interpretation
**Oxalate is not geometrically excluded** from the sampled two-arm region. That supports continuing to investigate accessibility, not a conclusion that oxalate binds strongly.

**The competing polyatomic ions are not geometrically excluded either.** This screen supplies no evidence for a strongly oxalate-exclusive pocket. That is a design concern because the previous passing equilibrium specification required extreme competitor rejection.

The raw counts must NOT be ranked as binding affinity or efficacy. Different guests have different size, flexibility, oxygen count and charge. Citrate has more oxygen atoms and only one sampled internal conformation here; its count is not evidence that it binds better. Chloride's single-atom nature also makes the distinct-oxygen metric inapplicable.

## Which unknowns are now partially addressed?
| Question | Updated status |
|---|---|
| Can oxalate physically approach both arms in sampled geometries? | Yes, under this limited geometric screen |
| Is there obvious geometric exclusion of phosphate/sulfate/citrate? | No, not in the sampled shapes and rules |
| Does BGOX-1 bind oxalate favorably in water? | Still unknown |
| Does it bind oxalate more strongly than competitors? | Still unknown |
| Does it capture 80% in a mixture? | Still unknown; not calculated from these poses |
| Is it stable, nonabsorbed or safe? | Not tested |

## Why this is not a binding result
No host–guest interaction energy or binding free energy was calculated. The screen omits explicit water and ions, counterion release, desolvation, entropy, solution speciation, induced fit, guest conformational ensembles, concentrations and coupled competition. A fixed uniform dielectric is not a substitute for these effects.

Each guest was screened separately, not in a competitive molecular mixture. The ion representations were oxalate −2, hydrogen phosphate −2, sulfate −2, citrate −3 and chloride −1, with receptor +2. Real pH-dependent mixtures were not modeled.

The receptor shapes and random positions are not thermal samples. Pose fractions are not binding probabilities or success rates. Lack of a sampled pose would not prove impossibility; finding one does not prove stable binding.

## Practical conclusion
The screen provides a limited positive result for **accessibility**, but no positive evidence of **selectivity**. BGOX-1 should remain an exploratory comparator rather than a validated lead. The next useful computational level would require a calibrated aqueous host–guest free-energy workflow and appropriate guest/host ensembles. Repeating this geometric screen cannot replace that step.

## Files
- `pose_screen.py`: executable screen; requires Python, NumPy, SciPy and RDKit.
- `pose_results.json`, `pose_counts.csv`: counts and conditions.
- Five `*_example_pose.sdf` files: selected geometric examples, NOT stable complexes or predicted binding structures.
- `run_log.txt`: final successful run output.

An export conformer-ID mismatch was corrected and the simulation rerun. Final SDF files were checked for finite coordinates and two disconnected components. That validates file structure, not binding chemistry.
