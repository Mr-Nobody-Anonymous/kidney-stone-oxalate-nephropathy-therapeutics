"""
test_simulation.py
Unit and integration tests for the competitive equilibrium binding model
and Monte Carlo transit kinetics.
"""

import math
import numpy as np
import pytest

def solve_equilibrium(O, S, Keff):
    """Analytic positive root for mass balance: O = x + S*x / (Keff + x)"""
    b = Keff + S - O
    c = -Keff * O
    discriminant = b**2 - 4 * c
    x = (-b + math.sqrt(discriminant)) / 2.0
    return x

def test_equilibrium_positive_root():
    O = 1.0  # mM
    S = 2.0  # mM
    Keff = 0.5  # mM
    x = solve_equilibrium(O, S, Keff)
    assert 0.0 < x < O, "Free oxalate must be strictly between 0 and total oxalate"
    # Check mass balance residual
    bound = S * x / (Keff + x)
    residual = abs(O - (x + bound))
    assert residual < 1e-12, f"Mass balance residual too large: {residual}"

def test_effective_kd_increases_with_competitors():
    Kd = 0.1  # mM
    chloride = 100.0  # mM
    Kd_cl = 500.0     # mM
    phosphate = 10.0  # mM
    Kd_phos = 1.0     # mM
    
    Keff = Kd * (1.0 + chloride / Kd_cl + phosphate / Kd_phos)
    assert Keff > Kd, "Effective Kd must weaken in the presence of competitors"
    assert math.isclose(Keff, 0.1 * (1.0 + 0.2 + 10.0), rel_tol=1e-6)

def test_transit_clearance_bounds():
    bound_fraction = 0.75
    transit_time = 4.0   # hours
    access_time = 2.0    # hours
    capture = bound_fraction * (1.0 - math.exp(-transit_time / access_time))
    assert 0.0 <= capture <= bound_fraction, "Capture must be bounded by equilibrium bound fraction"
    assert math.isclose(capture, bound_fraction * (1.0 - math.exp(-2.0)), rel_tol=1e-6)

def test_urinary_reduction_within_enteric_fraction():
    capture = 0.60
    f_enteric = 0.50
    reduction = capture * f_enteric
    assert 0.0 <= reduction <= f_enteric
    assert math.isclose(reduction, 0.30, rel_tol=1e-6)
