#!/usr/bin/env python3
"""
download_and_generate_references.py
Downloads official PubChem 3D reference structures and generates physiologically
deprotonated anion references using RDKit for testing, docking, and simulation benchmarks.
"""

import os
import urllib.request
import urllib.parse
import json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

REF_DIR = Path(__file__).resolve().parent / "reference_data"
REF_DIR.mkdir(exist_ok=True)

# 1. PubChem 3D Reference Downloads
PUBCHEM_TARGETS = {
    "oxalic_acid_pubchem_3d.sdf": "oxalic acid",
    "citric_acid_pubchem_3d.sdf": "citric acid",
    "phosphoric_acid_pubchem_3d.sdf": "phosphoric acid",
    "calcium_oxalate_pubchem.sdf": "calcium oxalate",
    "sulfuric_acid_pubchem_3d.sdf": "sulfuric acid"
}

print("=== Downloading PubChem 3D Reference Files ===")
for filename, query in PUBCHEM_TARGETS.items():
    out_path = REF_DIR / filename
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(query)}/record/SDF?record_type=3d"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "KidneyStoneResearch/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            out_path.write_bytes(data)
            print(f"  [OK] Downloaded {filename} ({len(data)} bytes)")
    except Exception as e:
        # Fallback to 2D if 3D conformer record is absent
        url_2d = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(query)}/record/SDF"
        try:
            req = urllib.request.Request(url_2d, headers={"User-Agent": "KidneyStoneResearch/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                out_path.write_bytes(data)
                print(f"  [OK-2D] Downloaded {filename} ({len(data)} bytes)")
        except Exception as e2:
            print(f"  [FAIL] Could not download {filename}: {e2}")

# 2. Generate Physiologically Deprotonated Anions for Benchmarks
PHYSIOLOGICAL_ANIONS = {
    "oxalate_dianion_reference.sdf": {
        "name": "Oxalate Dianion",
        "smiles": "[O-]C(=O)C(=O)[O-]",
        "formal_charge": -2,
        "pKa1": 1.27,
        "pKa2": 4.27,
        "role": "Primary Nephrotoxic & Lithogenic Target",
        "target_concentration_mM": "0.1 - 2.0"
    },
    "citrate_trianion_reference.sdf": {
        "name": "Citrate Trianion",
        "smiles": "[O-]C(=O)CC(O)(CC(=O)[O-])C(=O)[O-]",
        "formal_charge": -3,
        "pKa": "3.13, 4.76, 6.40",
        "role": "Endogenous Stone Inhibitor / Strong Competitor",
        "target_concentration_mM": "0.1 - 5.0"
    },
    "hydrogen_phosphate_reference.sdf": {
        "name": "Hydrogen Phosphate Dianion",
        "smiles": "[O-]P(=O)([O-])O",
        "formal_charge": -2,
        "pKa2": 7.20,
        "role": "Abundant Intestinal Competitor",
        "target_concentration_mM": "1.0 - 20.0"
    },
    "sulfate_dianion_reference.sdf": {
        "name": "Sulfate Dianion",
        "smiles": "[O-]S(=O)(=O)[O-]",
        "formal_charge": -2,
        "pKa2": 1.99,
        "role": "Bivalent Anionic Competitor",
        "target_concentration_mM": "1.0 - 10.0"
    },
    "sevelamer_active_unit.sdf": {
        "name": "Sevelamer Active Unit (PAA Hydrochloride)",
        "smiles": "C(C[NH3+])CC[NH3+].[Cl-].[Cl-]",
        "formal_charge": 2,
        "role": "Clinical Phosphate/Oxalate Binder Comparator",
        "target_concentration_mM": "N/A"
    }
}

print("\n=== Generating 3D MMFF Energy-Minimized Reference Anions ===")
summary = {}

for filename, meta in PHYSIOLOGICAL_ANIONS.items():
    mol = Chem.MolFromSmiles(meta["smiles"])
    if not mol:
        print(f"  [ERROR] Could not parse SMILES for {meta['name']}")
        continue
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    try:
        AllChem.MMFFOptimizeMolecule(mol)
    except Exception:
        pass
    
    mol.SetProp("_Name", meta["name"])
    mol.SetProp("SMILES", meta["smiles"])
    mol.SetProp("FormalCharge", str(meta["formal_charge"]))
    mol.SetProp("Role", meta["role"])
    
    sdf_path = REF_DIR / filename
    w = Chem.SDWriter(str(sdf_path))
    w.write(mol)
    w.close()
    
    summary[meta["name"]] = {
        "file": filename,
        "smiles": meta["smiles"],
        "formal_charge": meta["formal_charge"],
        "role": meta["role"],
        "target_concentration_mM": meta["target_concentration_mM"]
    }
    print(f"  [OK] Generated {filename} ({meta['name']})")

summary_file = REF_DIR / "reference_ions_metadata.json"
summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"\nMetadata catalog written to: {summary_file}")
