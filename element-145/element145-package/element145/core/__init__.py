"""Core lattice engine — types, ontology loader, and LCP protocol."""

from element145.core.lcp import (
    LCPEngine,
    LatticeOntology,
    LCPOperation,
    ActivationState,
    SynthesisResult,
    Sphere,
    HouseEdge,
    create_engine,
    quick_analyze,
)

__all__ = [
    "LCPEngine",
    "LatticeOntology",
    "LCPOperation",
    "ActivationState",
    "SynthesisResult",
    "Sphere",
    "HouseEdge",
    "create_engine",
    "quick_analyze",
]
