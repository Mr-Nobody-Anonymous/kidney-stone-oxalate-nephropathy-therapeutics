# BGOX-1 expanded computational screen

**10 November 2026 | Verdict: binding effectiveness and safety remain UNKNOWN.**

The molecule passed basic structural checks, but those are not tests of whether it treats disease. Its flexibility and environment-sensitive geometry make the earlier extreme selectivity assumptions particularly unjustified. No evidence supports assigning the passing 80%-capture parameter specification to BGOX-1.

## 1. Exact molecule tested
```
NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1
```

This is the previously proposed receptor dication, not a full gut-retained polymer. No guest, support, counterion or explicit water was included in this screen. Fixed charge +2 was used; aqueous protonation and ion-pair equilibria were not computed.

## 2. Tests actually run
### Structural identity and basic descriptors
- Parsed/sanitized graph: pass.
- Single connected receptor component: pass.
- Formal charge +2 and two guanidinium central-carbon groups: pass.
- Canonical SMILES read/write consistency: pass.

| Calculated descriptor | Value |
|---|---:|
| Formula | C16H30N6O4²⁺ |
| Mass excluding counterions | 370.454 g/mol |
| Topological polar surface area | 175.2 Å² |
| Hydrogen-bond donors, RDKit definition | 7 |
| Hydrogen-bond acceptors, RDKit definition | 4 |
| Rotatable bonds, RDKit definition | 13 |
| Heavy atoms | 26 |
| Rings | 1 |

These numbers describe the encoded structure. High polarity/charge does NOT demonstrate nonabsorption, safety, solubility, useful binding, or absence of drug interactions. Donor/acceptor counts depend on the representation and algorithm.

### Expanded conformational sensitivity screen
Three independent embedding seeds, 48 requested conformers per seed, under each of two constant-dielectric MMFF settings: **288 generated conformers total**, all reaching the optimizer's convergence criterion.

- Dielectric 1.0: an isolated/vacuum-like sensitivity setting.
- Dielectric 78.4: uniform electrostatic screening only. This is **not explicit water, a physiological environment, or a validated aqueous free-energy method**.

| Geometry metric | Dielectric 1.0: min / median / max | Dielectric 78.4: min / median / max |
|---|---:|---:|
| Guanidinium carbon–carbon separation | 8.10 / 9.19 / 9.60 Å | 5.83 / 8.06 / 8.97 Å |
| Closest nitrogen pair between the two arms | 6.34 / 6.90 / 7.35 Å | 4.15 / 6.02 / 6.91 Å |
| Closest chain O to guanidinium N | 2.57 / 2.75 / 5.17 Å | 3.43 / 5.31 / 5.43 Å |

These summaries are over generated optimized geometries, not Boltzmann-weighted thermal populations. The set is not exhaustive. Geometry alone cannot establish whether oxalate binds or whether both arms participate. Short O–N distances are possible close contacts; they are not automatically hydrogen bonds without angular and environmental analysis.

## 3. Findings that matter
### A. Flexibility is a real design concern
The encoded structure has 13 rotatable bonds, and its arm geometry varies across the generated conformers. It does not supply the preorganized cage geometry that motivated the earlier TPPC research direction. Binding could involve a conformational cost; that cost was not calculated.

### B. Geometry is sensitive to the electrostatic treatment
Changing dielectric treatment changes the observed range of arm separations. That means an isolated-molecule geometry cannot reliably stand in for the digestive environment. It is NOT evidence that the molecule binds better in real water.

### C. The side chain can approach a binding arm
Some geometries have close chain oxygen/guanidinium nitrogen contacts. This motivates checking whether the attachment chain masks or perturbs a binding group. The screen does not prove harmful self-binding or determine how frequently it occurs in solution.

### D. Nonabsorption and safety cannot be inferred
Even though the molecule is charged and polar, it is still a small receptor. There is no demonstrated gut-retained support, no permeability study and no toxicology. The positive groups could also bind unwanted anions; no selectivity measurement exists.

## 4. Works-or-not test matrix
| Question | Status after this work | Evidence needed |
|---|---|---|
| Is the encoded molecular graph chemically parsable? | PASS, basic computational check | Expert identity/synthetic feasibility review still needed |
| Can force-field conformers be generated? | PASS, limited numerical check | Does not establish synthesis or solution stability |
| Does it strongly bind oxalate in water? | UNKNOWN; not tested here | Calibrated host–guest computation and binding experiments |
| Does it reject phosphate, citrate, sulfate and chloride? | UNKNOWN | Matched competitive binding measurements |
| Does it capture ≥80% in digestive mixtures? | UNKNOWN | Measured properties, kinetics, sequential mixture tests |
| Does captured oxalate remain bound downstream? | UNKNOWN | Desorption/transit assays |
| Does it stay in the gut? | UNKNOWN | Uptake, fragment and leaching studies; define final material |
| Is it toxic to intestinal cells or other tissues? | UNKNOWN | Qualified toxicology program, starting with relevant in-vitro assays |
| Does it cause excessive swelling or degradation? | UNKNOWN for a future support material | Manufacture and characterize the actual formulation |
| Does it bind nutrients or medicines? | UNKNOWN | Pharmacist-informed interaction panel and assays |
| Does it reduce urinary oxalate or stones? | UNKNOWN | Appropriate preclinical/clinical evidence |

No unknown item should be called a pass because the molecule passed a graph check. No percentages of safety, clinical success or efficacy are calculated.

## 5. Recommendation
**Do not treat BGOX-1 as an established lead medicine or assign the 80% model result to it.** It is at most an exploratory comparator. The more defensible next molecular task is to compare fully specified, preorganized receptor designs using a validated aqueous host–guest method, with BGOX-1 as a flexible control. Preserving the published TPPC cavity is a separate, unresolved structure-design task.

Before further efficacy claims, prioritize:
1. Expert structure/feasibility and prior-art review.
2. Oxalate binding measured alongside phosphate/citrate/sulfate/chloride under identical conditions.
3. A validated explicit-solvent method calibrated against those measurements, if molecular predictions are used.
4. Safety, interaction, stability and retention tests on the actual proposed formulation.

This report supplies computational triage, not an experimental test plan approval. Do not synthesize, ingest or administer the proposed substance based on it.

## 6. Files and reproducibility
Run `python screen.py` with Python, RDKit and NumPy.
- `screen_results.json`: descriptors and geometry summaries.
- `geometry_results.csv`: all 288 conformer-level results and convergence statuses.
- `last_seed_dielectric_1.0_conformers.sdf`: 48 conformers from the final vacuum-like seed.
- `last_seed_dielectric_78.4_conformers.sdf`: 48 conformers from the final screened-electrostatics seed.

Only the final seed's conformer coordinates per dielectric are exported; all seeds' numeric results are retained. MMFF energies are not binding free energies and must not be compared as predicted affinity between settings.
