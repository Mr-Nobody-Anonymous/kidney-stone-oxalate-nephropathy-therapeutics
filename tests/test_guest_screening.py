"""
test_guest_screening.py
Tests verifying guest screening SDF poses, competitive anions, and reference data.
"""

from pathlib import Path
import pytest
from rdkit import Chem

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_guest_screen_poses_exist():
    guest_dir = REPO_ROOT / "BGOX1_guest_screen"
    expected = [
        "oxalate_example_pose.sdf",
        "citrate_example_pose.sdf",
        "hydrogen_phosphate_example_pose.sdf",
        "sulfate_example_pose.sdf",
        "chloride_example_pose.sdf"
    ]
    for filename in expected:
        p = guest_dir / filename
        assert p.exists(), f"Missing guest pose: {filename}"
        suppl = Chem.SDMolSupplier(str(p), removeHs=False)
        mols = [m for m in suppl if m is not None]
        assert len(mols) > 0, f"Failed to load molecules from {filename}"

def test_reference_data_integrity():
    ref_dir = REPO_ROOT / "reference_data"
    assert ref_dir.exists(), "reference_data directory must exist"
    
    metadata_file = ref_dir / "reference_ions_metadata.json"
    assert metadata_file.exists(), "reference_ions_metadata.json must exist"
    
    ox_ref = ref_dir / "oxalate_dianion_reference.sdf"
    assert ox_ref.exists(), "oxalate_dianion_reference.sdf must exist"
    suppl = Chem.SDMolSupplier(str(ox_ref), removeHs=False)
    mol = next(suppl)
    assert mol is not None
    assert Chem.GetFormalCharge(mol) == -2, "Oxalate dianion reference must have formal charge -2"
