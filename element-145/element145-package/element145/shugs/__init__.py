"""
SHUGS — Sheldonbrain Hypercube Unified-field Simulation
========================================================
Computational research framework for the Von Mangoldt-Sheldon HSUF operator.

Components:
  operator  — HSUF operator builder (N=145 fixed canonical)
  metrics   — GUE-KS measurement (Wigner surmise, unfolding, KS distance)
  ensemble  — K-trial ensemble runner with statistics

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from element145.shugs.operator import build_hsuf, von_mangoldt, extract_house_couplings
from element145.shugs.metrics import gue_ks_distance, wigner_surmise_cdf, unfold_eigenvalues
from element145.shugs.ensemble import run_ensemble, compare_n_values

__all__ = [
    "build_hsuf",
    "von_mangoldt",
    "extract_house_couplings",
    "gue_ks_distance",
    "wigner_surmise_cdf",
    "unfold_eigenvalues",
    "run_ensemble",
    "compare_n_values",
]
