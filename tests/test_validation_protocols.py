"""
test_validation_protocols.py
Tests verifying pre-registered laboratory validation templates and simulation summary results.
"""

from pathlib import Path
import json
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_laboratory_measurement_template_schema():
    template_file = REPO_ROOT / "next_steps" / "laboratory_measurements_BLANK.csv"
    assert template_file.exists(), "laboratory_measurements_BLANK.csv must exist"
    lines = template_file.read_text().strip().splitlines()
    assert len(lines) >= 1, "Template must contain header row"
    header = lines[0].split(",")
    required_cols = [
        "sample_id",
        "material_label",
        "batch_id",
        "condition_id",
        "free_oxalate_mmol",
        "bound_oxalate_mmol"
    ]
    for col in required_cols:
        assert col in header, f"Missing required column in lab measurement template: {col}"

def test_results_json_schema():
    results_file = REPO_ROOT / "results.json"
    assert results_file.exists(), "results.json must exist"
    data = json.loads(results_file.read_text())
    assert "designs" in data or "baseline" in data or "results" in data or len(data) > 0
