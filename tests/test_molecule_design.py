"""
test_molecule_design.py
Tests verifying chemical structure, graph properties, conformer generation,
and distance geometry for the BGOX-1 molecular receptor.
"""

from pathlib import Path
import pytest
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_bgox1_smiles_parsing():
    smiles_file = REPO_ROOT / "molecule_design" / "BGOX-1.smiles"
    assert smiles_file.exists(), "BGOX-1.smiles must exist"
    smiles = smiles_file.read_text().strip()
    mol = Chem.MolFromSmiles(smiles)
    assert mol is not None, "Failed to parse BGOX-1 SMILES"
    
    # Check formal charge (+2 dication)
    formal_charge = Chem.GetFormalCharge(mol)
    assert formal_charge == 2, f"Expected formal charge +2, got {formal_charge}"
    
    # Check molecular formula
    formula = rdMolDescriptors.CalcMolFormula(mol)
    assert formula == "C16H30N6O4+2", f"Unexpected formula: {formula}"

def test_bgox1_sdf_files_exist():
    mol_dir = REPO_ROOT / "molecule_design"
    assert (mol_dir / "BGOX-1_2D.sdf").exists()
    assert (mol_dir / "BGOX-1_conformers.sdf").exists()
    assert (mol_dir / "BGOX-1_structure.png").exists()

def test_bgox1_conformer_ensemble_loading():
    sdf_file = REPO_ROOT / "molecule_design" / "BGOX-1_conformers.sdf"
    suppl = Chem.SDMolSupplier(str(sdf_file), removeHs=False)
    mols = [m for m in suppl if m is not None]
    assert len(mols) > 0, "Conformer SDF should contain valid conformers"
    
    # Verify each conformer has 3D coordinates
    for m in mols:
        conf = m.GetConformer()
        assert conf.Is3D(), "Conformer must have 3D coordinates"
