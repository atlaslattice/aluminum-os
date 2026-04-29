"""
Core Type Definitions — Frozen Dataclasses for the 144+1 Lattice
=================================================================
Canonical data structures used across all Element 145 modules.
All types are frozen (immutable) for safety in multi-agent routing.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, FrozenSet
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════

class LCPPhase(Enum):
    """The four phases of the Lattice Context Protocol."""
    INGEST = "ingest"
    ACTIVATE = "activate"
    ROUTE = "route"
    SYNTHESIZE = "synthesize"


class ConnectionType(Enum):
    """Types of inter-House connections in the lattice topology."""
    REGULATORY = "regulatory"
    FINANCIAL = "financial"
    CULTURAL = "cultural"
    TECHNOLOGICAL = "technological"
    GOVERNANCE = "governance"
    ECOLOGICAL = "ecological"
    EPISTEMIC = "epistemic"
    INFRASTRUCTURAL = "infrastructural"
    SOCIAL = "social"
    STRATEGIC = "strategic"


class ScaffoldScale(Enum):
    """Agent scaffold complexity tiers."""
    COMPACT = "compact"           # ~800 tokens
    ORCHESTRATOR = "orchestrator" # ~2000 tokens
    SPHERE_AGENT = "sphere_agent" # ~400 tokens


# ═══════════════════════════════════════════════════════════════
# LATTICE STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Sphere:
    """A single sphere (domain node) within a House."""
    id: str                    # e.g., "S1", "S145"
    name: str                  # e.g., "Constitutional Law"
    house_id: str              # e.g., "H1"
    index: int                 # 0-based position in lattice
    keywords: Tuple[str, ...]  # Semantic matching keywords

    @property
    def is_admin(self) -> bool:
        """Whether this is Element 145 (Admin Sphere)."""
        return self.id == "S145" or self.index == 144


@dataclass(frozen=True)
class House:
    """One of the 12 Houses in the Sheldonbrain ontology."""
    id: str                    # e.g., "H1"
    name: str                  # e.g., "Governance"
    color: str                 # Chromatic frequency assignment
    harmonic: int              # Harmonic register (1-12)
    description: str           # Full description
    sphere_ids: Tuple[str, ...] = ()  # IDs of contained Spheres


@dataclass(frozen=True)
class Connection:
    """A typed, weighted edge between two Houses."""
    source_house: str          # e.g., "H1"
    target_house: str          # e.g., "H3"
    connection_type: str       # e.g., "regulatory"
    strength: float            # 0.0 to 1.0
    description: str = ""      # What this connection represents

    def involves(self, house_id: str) -> bool:
        """Check if this connection involves a specific House."""
        return self.source_house == house_id or self.target_house == house_id

    def other_house(self, house_id: str) -> Optional[str]:
        """Get the other House in this connection."""
        if self.source_house == house_id:
            return self.target_house
        elif self.target_house == house_id:
            return self.source_house
        return None


@dataclass(frozen=True)
class Element145:
    """
    The Admin Sphere — Element 145.

    Not a domain specialist. The metasynthesis coordinator that sits
    above the 12×12 grid and provides cross-domain integration.
    Architecturally necessary: N=145 > N=144 with p=0.0154.
    """
    id: str = "S145"
    name: str = "Element 145 — Admin Sphere"
    operations: Tuple[str, ...] = (
        "cross_house_cascade_detection",
        "blind_spot_identification",
        "contradiction_surfacing",
        "emergent_connection_mapping",
        "coherence_scoring",
    )


# ═══════════════════════════════════════════════════════════════
# LCP OPERATION TYPES
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ActivationResult:
    """Result of the INGEST + ACTIVATE phases."""
    activated_spheres: Tuple[str, ...]        # Sphere IDs
    activated_houses: Tuple[str, ...]         # House IDs (unique)
    activation_scores: Dict[str, float]       # sphere_id → confidence
    active_connections: Tuple[Connection, ...]  # Relevant inter-House edges
    blind_spots: Tuple[str, ...]              # Houses with no activation


@dataclass(frozen=True)
class RoutingPath:
    """A single reasoning path through the lattice."""
    houses: Tuple[str, ...]          # Ordered House traversal
    connections_used: Tuple[str, ...]  # Connection descriptions
    total_strength: float             # Product of edge strengths
    length: int                       # Number of hops


@dataclass(frozen=True)
class SynthesisResult:
    """Result of the SYNTHESIZE phase (Element 145 output)."""
    activation: ActivationResult
    routing_paths: Tuple[RoutingPath, ...]
    cross_domain_insights: Tuple[str, ...]
    blind_spots: Tuple[str, ...]
    contradictions: Tuple[str, ...]
    coherence_score: float             # 0.0 to 1.0
    house_coverage: float              # Fraction of Houses activated
    element_145_notes: str             # Metasynthesis commentary


# ═══════════════════════════════════════════════════════════════
# LATTICE NODE (GENERIC)
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class LatticeNode:
    """
    Generic lattice node — used for graph algorithms.

    Can represent a Sphere, House, or Element 145 depending
    on the level of abstraction.
    """
    id: str
    label: str
    node_type: str  # "sphere", "house", "admin"
    metadata: Dict[str, str] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
# HSUF TYPES
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class HSUFResult:
    """Result from a single HSUF operator construction + measurement."""
    N: int
    gue_ks: float
    eigenvalue_count: int
    spectral_range: Tuple[float, float]
    params_used: Dict[str, float]
    seed: Optional[int] = None


@dataclass(frozen=True)
class EnsembleStats:
    """Statistical summary from a K-trial ensemble."""
    N: int
    K: int
    mean_ks: float
    std_ks: float
    median_ks: float
    min_ks: float
    max_ks: float
    p_value_vs_reference: Optional[float] = None
    reference_N: Optional[int] = None
