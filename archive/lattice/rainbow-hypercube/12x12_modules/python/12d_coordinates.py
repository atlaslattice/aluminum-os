"""
12D Coordinate Utilities for the Rainbow Hypercube Knowledge Graph
Version 0.1
"""

from typing import Tuple, Optional

Coordinate12D = Tuple[int, int, int, int, int, int, int, int, int, int, int, int]

DIMENSION_NAMES = [
    "D1 - Energy / Foundation",
    "D2 - Information / Compute",
    "D3 - Flow / Logistics",
    "D4 - Form / Embodiment",
    "D5 - Regeneration / Life",
    "D6 - Medium / Transmission",
    "D7 - Habitat / Structure",
    "D8 - Coherence / Integrity",
    "D9 - Evolution / Learning",
    "D10 - Governance / Law",
    "D11 - Boundary / Security",
    "D12 - Transcendence / Emergence",
]


def validate(coord: Coordinate12D) -> bool:
    """Check that all values are integers between 0 and 11."""
    if len(coord) != 12:
        return False
    return all(isinstance(d, int) and 0 <= d <= 11 for d in coord)


def normalize(coord: Coordinate12D) -> Tuple[float, ...]:
    """Convert discrete [0-11] to continuous [0.0-1.0]."""
    return tuple(d / 11.0 for d in coord)


def denormalize(norm_coord: Tuple[float, ...]) -> Coordinate12D:
    """Convert continuous [0.0-1.0] back to nearest discrete [0-11]."""
    return tuple(int(round(n * 11)) for n in norm_coord)


def distance(c1: Coordinate12D, c2: Coordinate12D) -> float:
    """Euclidean distance in normalized 12D space."""
    n1 = normalize(c1)
    n2 = normalize(c2)
    return sum((a - b) ** 2 for a, b in zip(n1, n2)) ** 0.5


def resonance(c1: Coordinate12D, c2: Coordinate12D) -> float:
    """Resonance score (1.0 = identical, 0.0 = maximally distant)."""
    return 1.0 - distance(c1, c2)


def dominant_dimensions(coord: Coordinate12D, top_n: int = 3) -> list:
    """Return the top N strongest dimensions for this coordinate."""
    indexed = list(enumerate(coord))
    sorted_dims = sorted(indexed, key=lambda x: x[1], reverse=True)
    return [DIMENSION_NAMES[i] for i, _ in sorted_dims[:top_n]]


if __name__ == "__main__":
    # Example usage
    flywheel = (9, 10, 8, 11, 7, 6, 5, 4, 8, 6, 3, 12)
    invariants = (2, 4, 3, 2, 1, 1, 6, 5, 8, 12, 11, 7)

    print("Distance between Flywheel and Invariants:", distance(flywheel, invariants))
    print("Resonance:", resonance(flywheel, invariants))
    print("Dominant dimensions of Flywheel:", dominant_dimensions(flywheel))
