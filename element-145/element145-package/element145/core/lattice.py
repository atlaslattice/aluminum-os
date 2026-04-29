"""
Lattice Loader — Lightweight standalone loader for the 144+1 ontology.
=======================================================================
Loads lattice_ontology.yaml and provides simple query methods without
the full LCP engine overhead. Use this when you need the ontology data
but not the INGEST/ACTIVATE/ROUTE/SYNTHESIZE pipeline.

For full LCP operations, use core.lcp.LCPEngine instead.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import os
import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from pathlib import Path

from element145.core.types import House, Sphere, Connection, Element145


# Default ontology path (relative to package root)
_DEFAULT_ONTOLOGY = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "lattice_ontology.yaml"
)


@dataclass
class Lattice:
    """
    Lightweight loader for the 144+1 Sheldonbrain lattice ontology.

    Provides:
      - House / Sphere / Connection lookup
      - Keyword search across Spheres
      - Neighbor queries (which Houses connect to a given House)
      - Element 145 metadata

    Does NOT provide LCP operations — use LCPEngine for that.
    """

    houses: Dict[str, House] = field(default_factory=dict)
    spheres: Dict[str, Sphere] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)
    element_145: Optional[Element145] = None
    metadata: Dict = field(default_factory=dict)

    # Internal indexes
    _keyword_index: Dict[str, List[str]] = field(default_factory=dict, repr=False)
    _house_spheres: Dict[str, List[str]] = field(default_factory=dict, repr=False)
    _house_connections: Dict[str, List[Connection]] = field(default_factory=dict, repr=False)

    @classmethod
    def load(cls, path: Optional[str] = None) -> "Lattice":
        """
        Load the lattice from a YAML ontology file.

        Parameters
        ----------
        path : str, optional
            Path to lattice_ontology.yaml. Defaults to the bundled file.

        Returns
        -------
        Lattice
            Loaded and indexed lattice.
        """
        if path is None:
            path = _DEFAULT_ONTOLOGY

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        lattice = cls()
        lattice.metadata = data.get("metadata", {})

        # Load Houses
        for h_data in data.get("houses", []):
            house = House(
                id=h_data["id"],
                name=h_data["name"],
                color=h_data.get("color", ""),
                harmonic=h_data.get("harmonic", 0),
                description=h_data.get("description", ""),
            )
            lattice.houses[house.id] = house
            lattice._house_spheres[house.id] = []
            lattice._house_connections[house.id] = []

        # Load Spheres
        sphere_index = 0
        for h_data in data.get("houses", []):
            house_id = h_data["id"]
            for s_data in h_data.get("spheres", []):
                keywords = s_data.get("keywords", [])
                if isinstance(keywords, str):
                    keywords = [keywords]

                sphere = Sphere(
                    id=s_data["id"],
                    name=s_data["name"],
                    house_id=house_id,
                    index=sphere_index,
                    keywords=tuple(kw.lower() for kw in keywords),
                )
                lattice.spheres[sphere.id] = sphere
                lattice._house_spheres[house_id].append(sphere.id)

                # Build keyword index
                for kw in sphere.keywords:
                    if kw not in lattice._keyword_index:
                        lattice._keyword_index[kw] = []
                    lattice._keyword_index[kw].append(sphere.id)

                sphere_index += 1

        # Load Connections
        for c_data in data.get("connections", []):
            conn = Connection(
                source_house=c_data["source"],
                target_house=c_data["target"],
                connection_type=c_data.get("type", ""),
                strength=c_data.get("strength", 0.5),
                description=c_data.get("description", ""),
            )
            lattice.connections.append(conn)

            if conn.source_house in lattice._house_connections:
                lattice._house_connections[conn.source_house].append(conn)
            if conn.target_house in lattice._house_connections:
                lattice._house_connections[conn.target_house].append(conn)

        # Load Element 145
        e145_data = data.get("element_145", {})
        if e145_data:
            lattice.element_145 = Element145(
                id=e145_data.get("id", "S145"),
                name=e145_data.get("name", "Element 145 — Admin Sphere"),
                operations=tuple(e145_data.get("operations", [])),
            )

        return lattice

    # ─── Queries ─────────────────────────────────────────────

    @property
    def N(self) -> int:
        """Canonical lattice size (always 145 for production)."""
        return len(self.spheres) + (1 if self.element_145 else 0)

    @property
    def num_houses(self) -> int:
        return len(self.houses)

    @property
    def num_spheres(self) -> int:
        return len(self.spheres)

    def get_house(self, house_id: str) -> Optional[House]:
        """Get a House by ID."""
        return self.houses.get(house_id)

    def get_sphere(self, sphere_id: str) -> Optional[Sphere]:
        """Get a Sphere by ID."""
        return self.spheres.get(sphere_id)

    def get_house_spheres(self, house_id: str) -> List[Sphere]:
        """Get all Spheres belonging to a House."""
        sphere_ids = self._house_spheres.get(house_id, [])
        return [self.spheres[sid] for sid in sphere_ids if sid in self.spheres]

    def get_house_connections(self, house_id: str) -> List[Connection]:
        """Get all connections involving a House."""
        return self._house_connections.get(house_id, [])

    def get_house_neighbors(self, house_id: str) -> List[str]:
        """Get IDs of all Houses connected to the given House."""
        neighbors = set()
        for conn in self.get_house_connections(house_id):
            other = conn.other_house(house_id)
            if other:
                neighbors.add(other)
        return sorted(neighbors)

    def search_spheres(self, text: str, max_results: int = 10) -> List[Tuple[Sphere, float]]:
        """
        Search Spheres by keyword matching against input text.

        Parameters
        ----------
        text : str
            Input text to match against Sphere keywords.
        max_results : int
            Maximum number of results.

        Returns
        -------
        list of (Sphere, float)
            Matched Spheres with relevance scores, sorted descending.
        """
        text_lower = text.lower()
        tokens = set(text_lower.split())

        scores: Dict[str, float] = {}
        for token in tokens:
            # Exact keyword match
            for kw, sphere_ids in self._keyword_index.items():
                if kw in token or token in kw:
                    for sid in sphere_ids:
                        scores[sid] = scores.get(sid, 0) + 1.0

        # Sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for sid, score in ranked[:max_results]:
            if sid in self.spheres:
                results.append((self.spheres[sid], score))

        return results

    def get_connection(self, house_a: str, house_b: str) -> Optional[Connection]:
        """Get the connection between two specific Houses, if any."""
        for conn in self.connections:
            if (conn.source_house == house_a and conn.target_house == house_b) or \
               (conn.source_house == house_b and conn.target_house == house_a):
                return conn
        return None

    def house_list(self) -> List[str]:
        """Return all House IDs in order."""
        return sorted(self.houses.keys(), key=lambda h: int(h[1:]))

    def sphere_list(self) -> List[str]:
        """Return all Sphere IDs in order."""
        return sorted(self.spheres.keys(), key=lambda s: int(s[1:]))

    # ─── Diagnostics ─────────────────────────────────────────

    def summary(self) -> Dict:
        """Generate a summary of the lattice structure."""
        return {
            "N": self.N,
            "num_houses": self.num_houses,
            "num_spheres": self.num_spheres,
            "num_connections": len(self.connections),
            "has_element_145": self.element_145 is not None,
            "total_keywords": sum(len(s.keywords) for s in self.spheres.values()),
            "houses": [
                {
                    "id": h.id,
                    "name": h.name,
                    "spheres": len(self._house_spheres.get(h.id, [])),
                    "connections": len(self._house_connections.get(h.id, [])),
                }
                for h in sorted(self.houses.values(), key=lambda x: int(x.id[1:]))
            ],
        }

    def validate(self) -> List[str]:
        """
        Validate lattice integrity. Returns list of issues (empty = valid).

        Checks:
          - 12 Houses exist
          - 144 Spheres exist (12 per House)
          - Element 145 exists
          - All connections reference valid Houses
          - No orphan Spheres
        """
        issues = []

        if self.num_houses != 12:
            issues.append(f"Expected 12 Houses, found {self.num_houses}")

        if self.num_spheres != 144:
            issues.append(f"Expected 144 Spheres, found {self.num_spheres}")

        for h_id, sphere_ids in self._house_spheres.items():
            if len(sphere_ids) != 12:
                issues.append(f"House {h_id} has {len(sphere_ids)} Spheres (expected 12)")

        if self.element_145 is None:
            issues.append("Element 145 (Admin Sphere) is missing")

        for conn in self.connections:
            if conn.source_house not in self.houses:
                issues.append(f"Connection references unknown House: {conn.source_house}")
            if conn.target_house not in self.houses:
                issues.append(f"Connection references unknown House: {conn.target_house}")
            if not 0.0 <= conn.strength <= 1.0:
                issues.append(f"Connection {conn.source_house}→{conn.target_house} has invalid strength: {conn.strength}")

        return issues

    def __repr__(self) -> str:
        return (
            f"Lattice(N={self.N}, houses={self.num_houses}, "
            f"spheres={self.num_spheres}, connections={len(self.connections)})"
        )


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    lattice = Lattice.load()
    print(f"Loaded: {lattice}")
    print()

    # Validate
    issues = lattice.validate()
    if issues:
        print("⚠ Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Lattice valid (12 Houses × 12 Spheres + Element 145)")

    print()
    print(json.dumps(lattice.summary(), indent=2))

    # Example search
    print("\nSearch: 'climate change policy'")
    for sphere, score in lattice.search_spheres("climate change policy"):
        print(f"  {sphere.id} ({sphere.house_id}): {sphere.name} [score={score}]")
