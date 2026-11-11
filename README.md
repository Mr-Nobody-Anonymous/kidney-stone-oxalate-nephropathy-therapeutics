# Enteric Hyperoxaluria Therapeutics: In Silico Design & Simulation of Gut-Restricted Oxalate-Trapping Polymers

[![Domain: Nephrology & Medicinal Chemistry](https://img.shields.io/badge/Domain-Nephrology%20%26%20Medicinal%20Chemistry-blue.svg)](#)
[![Target: Enteric Hyperoxaluria](https://img.shields.io/badge/Disease%20Target-Enteric%20Hyperoxaluria%20%2F%20Nephrolithiasis-teal.svg)](#)
[![Mechanism: Gastrointestinal Oxalate Sequestration](https://img.shields.io/badge/Mechanism-Intestinal%20Oxalate%20Sequestering%20Polymer-green.svg)](#)
[![Methodology: Molecular Modeling & Monte Carlo Sweep](https://img.shields.io/badge/Methods-RDKit%20%7C%20MMFF%20%7C%20Monte%20Carlo%20Kinetics-darkviolet.svg)](#)

---

## 1. Executive Summary & Clinical Background

### 1.1 Pathophysiology of Enteric Hyperoxaluria
**Enteric hyperoxaluria** is a secondary metabolic disorder predominantly arising from gastrointestinal fat malabsorption secondary to bariatric procedures (e.g., Roux-en-Y gastric bypass), inflammatory bowel diseases (e.g., Crohn's disease), chronic pancreatitis, celiac sprue, or short bowel syndrome.

```
Pathophysiological Cascade:
Fat Malabsorption ──> Luminal Free Fatty Acids chelate Ca²⁺ (Saponification)
                  ──> Unbound, soluble dietary Oxalate accumulates in lumen
                  ──> Colonic hyperpermeability (bile acid/fatty acid induced)
                  ──> Massive passive colonic oxalate hyperabsorption
                  ──> Systemic hyperoxalemia & marked hyperoxaluria (>0.5 mmol/24h)
                  ──> Calcium Oxalate Supersaturation (AP[CaOx] > critical threshold)
                  ──> Intratubular crystal nucleation, aggregation & obstruction
                  ──> Recurrent Nephrolithiasis, Nephrocalcinosis & Oxalate Nephropathy
                  ──> Progressive interstitial fibrosis & End-Stage Renal Disease (ESRD)
```

Unlike **primary hyperoxaluria** (types 1, 2, and 3), which are inborn errors of hepatic glyoxylate metabolism manageable via RNAi therapies (e.g., lumasiran, nedosiran), **enteric hyperoxaluria** is fundamentally driven by intestinal bioavailability. 

### 1.2 Therapeutic Strategy: Non-Systemic Gut-Restricted Sequestration
Current standard-of-care (dietary oxalate restriction, intensive oral hydration, and meal-time calcium carbonate/citrate supplementation) is frequently constrained by poor compliance, hypercalciuria risks, and modest binding efficacy in complex luminal environments.

This project investigates the rational design of a **non-absorbable, orally administered, gut-retained hydrogel / supramolecular polymeric sorbent** engineered to:
1. Selectively chelate free oxalate dianions in the intestinal fluid in the presence of massive stoichiometric excesses of physiological competing anions (chloride, phosphate, sulfate, citrate, bile acids).
2. Retain bound oxalate throughout gastrointestinal transit to facilitate fecal excretion.
3. Lower systemic oxalate bioavailability, reducing urinary oxalate excretion below stone-forming and crystal-nephropathy thresholds.

---

## 2. Molecular Candidate & Material Architecture

### 2.1 The BGOX-1 Bis-Guanidinium Receptor Module
As part of the design progression, a small-molecule screening receptor module—designated **BGOX-1**—was computationally formulated and characterized:

* **Chemical Graph:** 1,3,5-substituted benzene core functionalized with two flexible guanidiniomethyl recognition arms and a hydrated triethylene glycol (TEG) spacer terminating in a primary hydroxyl attachment handle.
* **Canonical SMILES:**  
  `NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1`
* **Salt Representation:**  
  `NC(=[NH2+])NCc1cc(CNC(N)=[NH2+])cc(OCCOCCOCCO)c1.[Cl-].[Cl-]`
* **Molecular Formula:** $\text{C}_{16}\text{H}_{30}\text{N}_6\text{O}_4^{2+}$ (dication)
* **Monoisotopic Mass:** 370.454 g/mol (free dication, excluding counterions)

```
       H₂N⁺=C(NH₂)NH-CH₂          CH₂-NH-C(=NH₂)NH₂⁺
                   \                  /
                    \                /
                     C == CH ─── CH = C
                    /                  \
                   CH ═════════════════ CH
                           |
                           O-CH₂-CH₂-O-CH₂-CH₂-O-CH₂-CH₂-OH
```

* **Conformational Analysis:** 3D conformational ensemble generation via RDKit ETKDGv3 with MMFF energy minimization identified inter-guanidinium central carbon separations ranging between **8.16 Å and 9.55 Å**, outlining the spatial geometry required for paired charge-assisted hydrogen bonding against the oxalate dianion ($^-\text{OOC}-\text{COO}^-$).

### 2.2 Polymeric Material Framework: PAA-G25-PEG
To translate molecular recognition into an oral therapeutic candidate:
* **Backbone Matrix:** Covalently crosslinked poly(allylamine) hydrogel matrix.
* **Functionalization:** Target conversion of 25 mol% of pendant amino groups into guanidinium-containing oxalate recognition pockets (`PAA-G25`).
* **Stealth Surface Barrier:** Covalently grafted polyethylene glycol (`PEG`) brush layer engineered to suppress macromolecular fouling (mucins, dietary proteins, bile salt aggregates) while allowing unhindered small anion diffusion.

---

## 3. Mathematical Modeling & Simulation Pipeline

### 3.1 Competitive Anion Equilibrium Model
The project models the steady-state fraction of soluble oxalate bound within the intestinal lumen. Let:
* $O$ = Total accessible soluble oxalate concentration
* $x$ = Free oxalate concentration
* $S$ = Accessible pocket / active site concentration
* $K_d$ = Oxalate dissociation constant
* $[A_i]$ = Competitor anion concentrations ($\text{Cl}^-$, $\text{HPO}_4^{2-}$, $\text{Citrate}^{3-}$)
* $K_{d,i}$ = Competitor dissociation constants

The effective dissociation constant $K_{\text{eff}}$ accounting for competitive occupation is expressed as:

$$K_{\text{eff}} = K_d \left( 1 + \sum_{i} \frac{[A_i]}{K_{d,i}} \right) = K_d \left( 1 + \frac{[\text{Cl}^-]}{K_{d,\text{Cl}}} + \frac{[\text{Phosphate}]}{K_{d,\text{phos}}} + \frac{[\text{Citrate}]}{K_{d,\text{cit}}} \right)$$

Mass-balance equilibrium is solved analytically:

$$O = x + \frac{S \cdot x}{K_{\text{eff}} + x} \implies x^2 + (K_{\text{eff}} + S - O)x - K_{\text{eff}} \cdot O = 0$$

### 3.2 Phenomenological Transit & Clearance Kinetics
Capture efficiency during GI transit is modeled as a function of transit time ($t_{\text{transit}}$) and characteristic diffusion/access time constant ($\tau_{\text{access}}$):

$$\text{Capture} = \left( \frac{O - x}{O} \right) \cdot \left[ 1 - \exp\left(-\frac{t_{\text{transit}}}{\tau_{\text{access}}}\right) \right]$$

### 3.3 Renal Urinary Oxalate Excretion Endpoint
$$\Delta \text{UOx}_{\text{reduction}} = \text{Capture} \times f_{\text{enteric}}$$

where $f_{\text{enteric}}$ represents the fractional contribution of intestinal absorption to total urinary oxalate excretion (evaluated across 20% to 80% based on clinical enteric hyperoxaluria patient phenotypes).

---

## 4. Key Findings across 20,000-Scenario Parameter Sweeps

Monte Carlo sweeps across physiologically broad, uncorrelated intestinal parameter spaces (`simulate.py`, $N = 20,000$, random seed `20261110`) demonstrated:

| Design Variant | Description | Median Modeled UOx Reduction | 10th–90th Percentile | Scenarios $\ge$ 20% Reduction |
|---|---|:---:|:---:|:---:|
| **Baseline** | Standard capacity & unoptimized selectivity | **12.70%** | 2.07% – 40.74% | 33.92% |
| **Double Capacity** | $2\times$ accessible site density | **19.14%** | 3.89% – 48.95% | 48.05% |
| **Selectivity Design** | $10\times$ weaker competitor affinity (with 20% capacity & $2\times$ diffusion penalty) | **17.05%** | 4.21% – 46.60% | 43.19% |
| **Combined** | $1.6\times$ capacity + enhanced selectivity | **23.06%** | 7.01% – 53.34% | **57.13%** |
| **Fast Access** | Accelerated diffusion ($0.5\times$ access $\tau$) | **14.16%** | 2.34% – 43.41% | 37.38% |

### Key Mechanistic Takeaways:
1. **The Capacity-Selectivity Trade-off:** High theoretical selectivity provides negligible clinical utility if achieved at the expense of high volumetric capacity or rapid mass transport.
2. **Diffusion Obstruction Risks:** Excessively dense polymer networks or overprotective brush coatings can impede small-molecule diffusion, diminishing capture before colonic transit is complete.
3. **Clinical Ceiling:** The theoretical maximum reduction in urinary oxalate is strictly bounded by the enteric fraction ($f_{\text{enteric}}$), reinforcing the distinction between enteric hyperoxaluria and endogenous hepatic hyperoxaluria.

---

## 5. Repository Structure

```
enteric-hyperoxaluria-therapeutics/
├── README.md                              # Main scientific overview & project documentation
├── research_report.md                     # Comprehensive preliminary research report & literature audit
├── simulate.py                            # Standalone 20,000-scenario Monte Carlo simulation engine
├── results.json                           # Quantitative simulation endpoints & percentile stats
├── scenario_results.csv                   # Full paired scenario dataset (20,000 rows x 5 designs)
│
├── molecule_design/                       # Concrete small-molecule receptor design (BGOX-1)
│   ├── BGOX-1.smiles                      # Authoritative canonical SMILES specification
│   ├── BGOX-1_2D.sdf                      # 2D chemical structure representation
│   ├── BGOX-1_conformers.sdf              # 3D ETKDGv3 MMFF-optimized conformer ensemble
│   ├── BGOX-1_design.json                 # Chemical descriptors, conformer coordinates & metrics
│   ├── BGOX-1_design_note.md              # Structural rationale, limitations & synthesis notes
│   ├── BGOX-1_structure.png               # 2D structure rendering
│   └── build_candidate.py                 # RDKit generation and conformer optimization script
│
├── BGOX1_guest_screen/                    # Docking & competitive guest screening poses
│   ├── pose_screen.py                     # Computational guest screening pipeline
│   ├── pose_results.json                  # Relative binding affinity metrics
│   ├── oxalate_example_pose.sdf           # Target guest: oxalate dianion pose
│   ├── citrate_example_pose.sdf           # Competitor: citrate pose
│   ├── hydrogen_phosphate_example_pose.sdf# Competitor: hydrogen phosphate pose
│   ├── sulfate_example_pose.sdf           # Competitor: sulfate pose
│   └── chloride_example_pose.sdf          # Competitor: chloride pose
│
├── BGOX1_screen/                          # Conformational geometry & dielectric sweeps
│   ├── screen.py                          # Dielectric screening (vacuum vs water)
│   ├── geometry_results.csv               # Inter-arm distance distributions
│   └── report.md                          # Geometric constraint findings
│
├── cycle3/                                # Iteration cycle 3: macrocyclic cages & fragment screening
├── cycle4/                                # Iteration cycle 4: decision boundary maps & capture surfaces
├── cycle5/                                # Iteration cycle 5: 80% feasibility frontier analysis
├── cycle6/                                # Iteration cycle 6: interior & corner space optimization sweeps
│
├── next_steps/                            # Experimental protocols & pre-registered validation plans
│   ├── laboratory_validation_plan.md      # Methodological protocol for in vitro digestion testing
│   ├── laboratory_measurements_BLANK.csv  # Standardized data capture template
│   ├── next_steps_report.md               # Summary of transition from in silico to wet lab
│   ├── simulate_v2.py                     # Second-generation simulation script
│   └── results_v2.json                    # Holdout set benchmark results
│
└── *.zip                                  # Standalone frozen archival bundles for cycles & screens
```

---

## 6. Reproducing the Simulations

### Prerequisites
* Python 3.9+
* NumPy (`pip install numpy`)
* RDKit (`pip install rdkit`)

### Running the Monte Carlo Transit & Binding Sweep
```powershell
python simulate.py
```
This generates and verifies 20,000 paired Monte Carlo scenarios with numerical mass-balance tolerance $< 10^{-17}\text{ M}$, validating equilibrium convergence.

### Generating & Optimizing the BGOX-1 Receptor Conformer Ensemble
```powershell
cd molecule_design
python build_candidate.py
```

---

## 7. Experimental Pre-Registration & Validation Framework

Before any experimental or translational claim can be established, the following prospective laboratory protocols (`next_steps/laboratory_validation_plan.md`) must be satisfied:
1. **Standardized Simulated Digestion:** Multi-compartment testing (simulated gastric fluid $\to$ simulated intestinal fluid $\to$ simulated colonic fluid) under standardized European INFOGEST 2.0 protocols.
2. **True Chromatographic Quantification:** Direct quantification of free vs. precipitated vs. bound oxalate via Ion Chromatography (IC) or isotope-dilution LC-MS/MS.
3. **Competitive Anion Challenge:** Isotherm binding measurements in physiological matrices containing bile acids, mucins, high chloride (100–140 mM), phosphate (5–20 mM), and competing dietary carboxylates.
4. **Toxicological & Barrier Safety:** In vitro human intestinal epithelial monolayer (Caco-2 / HT29-MTX co-cultures) TEER measurement, LDH release, and assessment of non-systemic retention (absence of systemic monomer/oligomer translocation).

---

## 8. Scientific & Medical Disclaimer

> **IMPORTANT NOTICE:**  
> This repository contains exploratory computational models, in silico chemical designs, and parameter simulations. **None of the compounds or materials presented herein have been manufactured, tested in animals or humans, or evaluated by regulatory bodies.**  
> 
> * Do not synthesize, ingest, or administer any material based on this repository.
> * This repository does not provide medical advice, diagnostic recommendations, clinical treatment protocols, or claims of patentability.
> * All efficacy metrics represent computational parameter explorations under hypothesized assumptions and do not constitute clinical efficacy predictions.

---

## 9. Key Medical & Biochemical Literature

1. **Pathophysiology and management of enteric hyperoxaluria.** *Curr Opin Nephrol Hypertens / Kidney Int.* (2024). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2210740124000433)
2. **Kidney Stone Pathophysiology, Evaluation and Management: Core Curriculum 2023.** *Am J Kidney Dis.* (2023). [AJKD Core Curriculum](https://www.ajkd.org/article/S0272-6386(23)00670-4/fulltext)
3. **Effective Therapy of Enteric Hyperoxaluria: In Vitro Binding of Oxalate by Anion-Exchange Resins and Aluminum Hydroxide.** *J Pharm Sci.* (1980). [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0022354915438717)
4. **Oxalate-binding polymers and methods of treatment.** *US Patent US7459502B2.* [USPTO / Google Patents](https://patentimages.storage.googleapis.com/a8/25/d1/2baf3018c33f01/US7459502.pdf)
5. **Aqueous Molecular Recognition of Oxoanions based on Guanidinium and Tetra-urea Receptors.** *Chem Sci.* (2024). [RSC Chemical Science](https://pubs.rsc.org/en/content/articlehtml/2024/sc/d4sc05236f)
