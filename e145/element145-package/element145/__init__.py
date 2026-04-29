"""
Element 145 — Sheldonbrain 144+1 Ontological Lattice
=====================================================
A sovereign AI reasoning substrate: 12 Houses × 12 Spheres + Element 145 (Admin Sphere).
N=145 is fixed and empirically confirmed as the global optimum (GUE-KS p=0.0154 vs N=144).

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.

Quick start:
    from element145 import quick_analyze
    result = quick_analyze("AI regulation and climate policy")
    print(result.activated_houses)
    print(result.bridges)
"""

__version__ = "2.0.0"
__author__ = "Atlas Lattice Foundation"
__license__ = "Atlas Lattice Foundation License"

# Core types
from element145.core import (
    LCPPhase,
    Sphere,
    HouseEdge,
    ActivationState,
    AnalysisResult,
    HOUSE_NAMES,
)

# Lattice ontology
from element145.core import LatticeOntology

# LCP Engine
from element145.core import LCPEngine

# Convenience functions
from element145.core import create_engine, quick_analyze

# SHUGS (optional — requires numpy/scipy)
try:
    from element145.shugs import (
        HSUFParams,
        EnsembleStats,
        NComparison,
        SweepResult,
        von_mangoldt,
        build_hsuf_operator,
        gue_ks_distance,
        run_ensemble,
        compare_n_values,
        parameter_sweep,
        extract_house_couplings,
        admin_sphere_coupling,
        RIEMANN_ZEROS,
        CANONICAL_N,
    )
    HAS_SHUGS = True
except ImportError:
    HAS_SHUGS = False

__all__ = [
    # Version
    "__version__",
    # Core types
    "LCPPhase", "Sphere", "HouseEdge", "ActivationState", "AnalysisResult",
    "HOUSE_NAMES",
    # Ontology & Engine
    "LatticeOntology", "LCPEngine",
    # Convenience
    "create_engine", "quick_analyze",
    # SHUGS (conditional)
    "HAS_SHUGS",
    "HSUFParams", "EnsembleStats", "NComparison", "SweepResult",
    "von_mangoldt", "build_hsuf_operator", "gue_ks_distance",
    "run_ensemble", "compare_n_values", "parameter_sweep",
    "extract_house_couplings", "admin_sphere_coupling",
    "RIEMANN_ZEROS", "CANONICAL_N",
]
