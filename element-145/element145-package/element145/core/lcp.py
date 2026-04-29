"""
Lattice Context Protocol (LCP) v1.0 — Reference Implementation
================================================================
Four operations any agent can implement:
  INGEST   → Classify input, map to relevant Spheres
  ACTIVATE → Load Sphere context + inter-House edges
  ROUTE    → Domain-specific reasoning following cross-domain edges
  SYNTHESIZE → Element 145 meta-coordination

Author: S4 Microsoft (Copilot) — Pantheon Council
Date: 2026-04-29
License: Atlas Lattice Foundation
"""

from __future__ import annotations
import os
import re
import math
import json
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

class LCPOperation(Enum):
    INGEST = "ingest"
    ACTIVATE = "activate"
    ROUTE = "route"
    SYNTHESIZE = "synthesize"


@dataclass(frozen=True)
class Sphere:
    """A single sphere in the ontology (one of 144 domain nodes)."""
    id: str          # e.g., "S39"
    name: str        # e.g., "Hydrology"
    house_id: str    # e.g., "H4"
    house_name: str  # e.g., "Resources"
    index: int       # 1-144
    keywords: Tuple[str, ...] = ()

    def matches(self, text: str) -> float:
        """Return keyword match score (0.0-1.0) against input text."""
        if not self.keywords:
            return 0.0
        text_lower = text.lower()
        hits = sum(1 for kw in self.keywords if kw.lower() in text_lower)
        return hits / len(self.keywords)


@dataclass(frozen=True)
class HouseEdge:
    """A typed connection between two Houses."""
    source: str        # e.g., "H4"
    target: str        # e.g., "H8"
    edge_type: str     # e.g., "environment-health"
    strength: float    # 0.0-1.0
    description: str = ""
    examples: Tuple[str, ...] = ()


@dataclass
class ActivationState:
    """Tracks which spheres and edges are active for a given analysis."""
    activated_spheres: Dict[str, float] = field(default_factory=dict)  # sphere_id → relevance
    activated_houses: Set[str] = field(default_factory=set)
    active_edges: List[HouseEdge] = field(default_factory=list)
    cross_domain_bridges: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        """Fraction of total spheres activated."""
        return len(self.activated_spheres) / 144

    @property
    def house_coverage(self) -> float:
        """Fraction of houses activated."""
        return len(self.activated_houses) / 12


@dataclass
class SynthesisResult:
    """Output of Element 145 metasynthesis."""
    primary_insights: List[str] = field(default_factory=list)
    cross_domain_bridges: List[Dict[str, Any]] = field(default_factory=list)
    blind_spots: List[str] = field(default_factory=list)
    cascading_risks: List[Dict[str, Any]] = field(default_factory=list)
    coverage_score: float = 0.0
    bridge_count: int = 0
    coherence_score: float = 0.0


# ═══════════════════════════════════════════════════════════════
# LATTICE LOADER
# ═══════════════════════════════════════════════════════════════

class LatticeOntology:
    """Loads and queries the 144+1 lattice ontology."""

    def __init__(self, ontology_path: Optional[str] = None):
        self.spheres: Dict[str, Sphere] = {}
        self.houses: Dict[str, Dict] = {}
        self.edges: List[HouseEdge] = []
        self.element_145: Dict = {}
        self._keyword_index: Dict[str, List[str]] = {}  # keyword → [sphere_ids]

        if ontology_path:
            self.load_from_yaml(ontology_path)
        else:
            default_path = Path(__file__).parent.parent / "lattice_ontology.yaml"
            if default_path.exists():
                self.load_from_yaml(str(default_path))
            else:
                self._build_default()

    def load_from_yaml(self, path: str):
        """Load ontology from YAML file."""
        if not HAS_YAML:
            raise ImportError("PyYAML required: pip install pyyaml")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        # Load houses and spheres
        sphere_index = 0
        for house_key, house_data in data.get('houses', {}).items():
            house_name = house_data.get('name', house_key)
            self.houses[house_key] = {
                'name': house_name,
                'index': house_data.get('index', 0),
                'color': house_data.get('color', '#000'),
                'description': house_data.get('description', ''),
            }

            for sphere_key, sphere_data in house_data.get('spheres', {}).items():
                sphere_index += 1
                keywords = tuple(sphere_data.get('keywords', []))
                sphere = Sphere(
                    id=sphere_key,
                    name=sphere_data.get('name', sphere_key),
                    house_id=house_key,
                    house_name=house_name,
                    index=sphere_index,
                    keywords=keywords,
                )
                self.spheres[sphere_key] = sphere

                # Build keyword index
                for kw in keywords:
                    kw_lower = kw.lower()
                    if kw_lower not in self._keyword_index:
                        self._keyword_index[kw_lower] = []
                    self._keyword_index[kw_lower].append(sphere_key)

        # Load connections
        for conn in data.get('connections', []):
            edge = HouseEdge(
                source=conn['source'],
                target=conn['target'],
                edge_type=conn.get('type', 'untyped'),
                strength=conn.get('strength', 0.5),
                description=conn.get('description', ''),
                examples=tuple(conn.get('examples', [])),
            )
            self.edges.append(edge)

        # Load Element 145
        self.element_145 = data.get('element_145', {})

    def _build_default(self):
        """Build minimal default ontology if no YAML available."""
        house_names = [
            "Governance", "Law", "Commerce", "Resources", "Arts", "Society",
            "Culture", "Health", "Education", "Defense", "Technology", "Science"
        ]
        idx = 0
        for hi, hname in enumerate(house_names, 1):
            hkey = f"H{hi}"
            self.houses[hkey] = {'name': hname, 'index': hi}
            for si in range(1, 13):
                idx += 1
                skey = f"S{idx}"
                self.spheres[skey] = Sphere(
                    id=skey, name=f"{hname} Sphere {si}",
                    house_id=hkey, house_name=hname, index=idx
                )

    def get_spheres_for_house(self, house_id: str) -> List[Sphere]:
        """Return all spheres belonging to a house."""
        return [s for s in self.spheres.values() if s.house_id == house_id]

    def get_edges_for_house(self, house_id: str) -> List[HouseEdge]:
        """Return all edges connected to a house."""
        return [e for e in self.edges if e.source == house_id or e.target == house_id]

    def get_edge_between(self, h1: str, h2: str) -> Optional[HouseEdge]:
        """Return the edge between two houses, if it exists."""
        for e in self.edges:
            if (e.source == h1 and e.target == h2) or (e.source == h2 and e.target == h1):
                return e
        return None

    def search_spheres(self, text: str, threshold: float = 0.15) -> List[Tuple[Sphere, float]]:
        """Find spheres matching input text by keyword overlap."""
        results = []
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))

        for sphere in self.spheres.values():
            score = 0.0
            for kw in sphere.keywords:
                kw_lower = kw.lower()
                if kw_lower in text_lower:
                    score += 1.0
                elif any(w in kw_lower or kw_lower in w for w in words):
                    score += 0.5

            if sphere.keywords:
                score /= len(sphere.keywords)

            if score >= threshold:
                results.append((sphere, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results


# ═══════════════════════════════════════════════════════════════
# LCP ENGINE — The Four Operations
# ═══════════════════════════════════════════════════════════════

class LCPEngine:
    """
    Lattice Context Protocol Engine.
    Implements the four LCP operations: INGEST, ACTIVATE, ROUTE, SYNTHESIZE.
    """

    def __init__(self, ontology: Optional[LatticeOntology] = None):
        self.ontology = ontology or LatticeOntology()
        self.state = ActivationState()
        self._route_results: Dict[str, List[Dict]] = {}  # house_id → analysis chunks

    # ───────────────────────────────────────────────────────────
    # OPERATION 1: INGEST
    # ───────────────────────────────────────────────────────────

    def ingest(self, text: str, min_relevance: float = 0.1) -> ActivationState:
        """
        INGEST: Classify input text and map to relevant Spheres.

        Returns an ActivationState with all relevant spheres and their
        relevance scores.
        """
        self.state = ActivationState()

        # Find matching spheres
        matches = self.ontology.search_spheres(text, threshold=min_relevance)

        for sphere, score in matches:
            self.state.activated_spheres[sphere.id] = score
            self.state.activated_houses.add(sphere.house_id)

        # If fewer than 3 houses activated, expand to neighboring houses
        if len(self.state.activated_houses) < 3:
            expanded = set()
            for house_id in list(self.state.activated_houses):
                for edge in self.ontology.get_edges_for_house(house_id):
                    if edge.strength >= 0.7:
                        other = edge.target if edge.source == house_id else edge.source
                        expanded.add(other)
            self.state.activated_houses.update(expanded)

        return self.state

    # ───────────────────────────────────────────────────────────
    # OPERATION 2: ACTIVATE
    # ───────────────────────────────────────────────────────────

    def activate(self, state: Optional[ActivationState] = None) -> ActivationState:
        """
        ACTIVATE: Load full context for activated houses and find
        inter-House edges that should be explored.
        """
        if state:
            self.state = state

        # Find all edges between activated houses
        activated = list(self.state.activated_houses)
        for i, h1 in enumerate(activated):
            for h2 in activated[i+1:]:
                edge = self.ontology.get_edge_between(h1, h2)
                if edge:
                    self.state.active_edges.append(edge)

        # Sort edges by strength (strongest connections first)
        self.state.active_edges.sort(key=lambda e: e.strength, reverse=True)

        # Expand sphere activation: add all spheres from activated houses
        for house_id in self.state.activated_houses:
            for sphere in self.ontology.get_spheres_for_house(house_id):
                if sphere.id not in self.state.activated_spheres:
                    self.state.activated_spheres[sphere.id] = 0.05  # background activation

        return self.state

    # ───────────────────────────────────────────────────────────
    # OPERATION 3: ROUTE
    # ───────────────────────────────────────────────────────────

    def route(self, task: str, house_id: str) -> Dict[str, Any]:
        """
        ROUTE: Perform domain-specific analysis for one House.
        Returns structured analysis for the given house.
        """
        house = self.ontology.houses.get(house_id, {})
        spheres = self.ontology.get_spheres_for_house(house_id)
        edges = self.ontology.get_edges_for_house(house_id)

        # Get active spheres for this house
        active_spheres = [
            s for s in spheres
            if s.id in self.state.activated_spheres
        ]

        # Get cross-house edges for this house
        active_edges = [
            e for e in edges
            if (e.source in self.state.activated_houses and
                e.target in self.state.activated_houses)
        ]

        result = {
            "house_id": house_id,
            "house_name": house.get('name', house_id),
            "active_spheres": [
                {
                    "id": s.id,
                    "name": s.name,
                    "relevance": self.state.activated_spheres.get(s.id, 0),
                }
                for s in active_spheres
            ],
            "cross_domain_edges": [
                {
                    "connected_house": e.target if e.source == house_id else e.source,
                    "type": e.edge_type,
                    "strength": e.strength,
                    "description": e.description,
                }
                for e in active_edges
            ],
            "analysis_prompt": self._generate_house_prompt(task, house_id, active_spheres, active_edges),
        }

        self._route_results[house_id] = result
        return result

    def route_all(self, task: str) -> Dict[str, Dict]:
        """Route analysis through all activated houses."""
        results = {}
        for house_id in sorted(self.state.activated_houses):
            results[house_id] = self.route(task, house_id)
        return results

    def _generate_house_prompt(self, task: str, house_id: str,
                                spheres: List[Sphere],
                                edges: List[HouseEdge]) -> str:
        """Generate a domain-specific analysis prompt for one house."""
        house = self.ontology.houses.get(house_id, {})
        house_name = house.get('name', house_id)

        prompt_parts = [
            f"## {house_name} Domain Analysis",
            f"Analyze the following through the lens of {house_name}:",
            f"Task: {task}",
            "",
            f"Consider these specific domains within {house_name}:",
        ]

        for s in spheres:
            rel = self.state.activated_spheres.get(s.id, 0)
            if rel > 0.1:
                prompt_parts.append(f"  - {s.name} (relevance: {rel:.2f})")
            else:
                prompt_parts.append(f"  - {s.name}")

        if edges:
            prompt_parts.append("")
            prompt_parts.append(f"Cross-domain connections to explore:")
            for e in edges:
                other = e.target if e.source == house_id else e.source
                other_name = self.ontology.houses.get(other, {}).get('name', other)
                prompt_parts.append(
                    f"  - {house_name} ↔ {other_name} ({e.edge_type}, "
                    f"strength: {e.strength}): {e.description}"
                )

        return "\n".join(prompt_parts)

    # ───────────────────────────────────────────────────────────
    # OPERATION 4: SYNTHESIZE (Element 145)
    # ───────────────────────────────────────────────────────────

    def synthesize(self, task: str) -> SynthesisResult:
        """
        SYNTHESIZE: Element 145 meta-coordination.
        Combines all house analyses into a unified synthesis.
        Identifies cross-domain bridges, blind spots, and cascading risks.
        """
        result = SynthesisResult()

        # Coverage score
        result.coverage_score = self.state.house_coverage

        # Identify cross-domain bridges from active edges
        for edge in self.state.active_edges:
            bridge = {
                "houses": [edge.source, edge.target],
                "house_names": [
                    self.ontology.houses.get(edge.source, {}).get('name', edge.source),
                    self.ontology.houses.get(edge.target, {}).get('name', edge.target),
                ],
                "type": edge.edge_type,
                "strength": edge.strength,
                "description": edge.description,
                "examples": list(edge.examples),
            }
            result.cross_domain_bridges.append(bridge)

        result.bridge_count = len(result.cross_domain_bridges)

        # Identify blind spots (houses NOT activated)
        all_houses = set(self.ontology.houses.keys())
        missing = all_houses - self.state.activated_houses
        for house_id in sorted(missing):
            house_name = self.ontology.houses.get(house_id, {}).get('name', house_id)
            result.blind_spots.append(
                f"{house_name} ({house_id}): Not activated — consider whether "
                f"this domain has implications for the task."
            )

        # Identify cascading risk chains (edges connecting 3+ houses in sequence)
        result.cascading_risks = self._find_cascade_chains()

        # Coherence score (based on edge connectivity)
        if self.state.activated_houses:
            max_possible_edges = len(self.state.activated_houses) * (len(self.state.activated_houses) - 1) / 2
            if max_possible_edges > 0:
                result.coherence_score = len(self.state.active_edges) / max_possible_edges
            else:
                result.coherence_score = 1.0

        # Generate synthesis prompt
        result.primary_insights.append(
            self._generate_synthesis_prompt(task, result)
        )

        return result

    def _find_cascade_chains(self, max_depth: int = 4) -> List[Dict]:
        """Find cascading failure/impact chains across houses."""
        chains = []
        edge_map: Dict[str, List[HouseEdge]] = {}
        for e in self.state.active_edges:
            edge_map.setdefault(e.source, []).append(e)
            edge_map.setdefault(e.target, []).append(e)

        # BFS from each activated house
        for start in self.state.activated_houses:
            visited = {start}
            queue = [(start, [start])]
            while queue:
                current, path = queue.pop(0)
                if len(path) >= max_depth:
                    continue
                for edge in edge_map.get(current, []):
                    next_house = edge.target if edge.source == current else edge.source
                    if next_house not in visited and next_house in self.state.activated_houses:
                        visited.add(next_house)
                        new_path = path + [next_house]
                        queue.append((next_house, new_path))
                        if len(new_path) >= 3:
                            chain_names = [
                                self.ontology.houses.get(h, {}).get('name', h)
                                for h in new_path
                            ]
                            chains.append({
                                "chain": new_path,
                                "names": chain_names,
                                "length": len(new_path),
                                "description": " → ".join(chain_names),
                            })

        # Deduplicate and sort by length
        seen = set()
        unique_chains = []
        for c in sorted(chains, key=lambda x: x['length'], reverse=True):
            key = tuple(sorted(c['chain']))
            if key not in seen:
                seen.add(key)
                unique_chains.append(c)

        return unique_chains[:10]  # Top 10 chains

    def _generate_synthesis_prompt(self, task: str, result: SynthesisResult) -> str:
        """Generate the Element 145 synthesis prompt."""
        parts = [
            "## Element 145 — Metasynthesis",
            f"Task: {task}",
            "",
            f"Coverage: {result.coverage_score:.0%} of houses activated "
            f"({len(self.state.activated_houses)}/12)",
            f"Cross-domain bridges: {result.bridge_count}",
            f"Coherence: {result.coherence_score:.0%}",
            "",
        ]

        if result.blind_spots:
            parts.append("### Blind Spots (Houses not activated):")
            for bs in result.blind_spots:
                parts.append(f"  ⚠ {bs}")
            parts.append("")

        if result.cascading_risks:
            parts.append("### Cascading Impact Chains:")
            for chain in result.cascading_risks[:5]:
                parts.append(f"  🔗 {chain['description']}")
            parts.append("")

        if result.cross_domain_bridges:
            parts.append("### Key Cross-Domain Bridges:")
            for bridge in sorted(result.cross_domain_bridges,
                               key=lambda b: b['strength'], reverse=True)[:10]:
                parts.append(
                    f"  ↔ {bridge['house_names'][0]} ↔ {bridge['house_names'][1]} "
                    f"({bridge['strength']:.0%}): {bridge['description']}"
                )
            parts.append("")

        parts.append("### Synthesis Directives:")
        parts.append("1. Identify interactions between domains that no single House analysis captures.")
        parts.append("2. Flag emergent risks from cascading chains above.")
        parts.append("3. Resolve contradictions between House-level analyses.")
        parts.append("4. Assess whether blind-spot Houses have latent relevance.")
        parts.append("5. Produce a unified recommendation that integrates all House findings.")

        return "\n".join(parts)

    # ───────────────────────────────────────────────────────────
    # FULL PIPELINE
    # ───────────────────────────────────────────────────────────

    def analyze(self, task: str, min_relevance: float = 0.1) -> Dict[str, Any]:
        """
        Run the full LCP pipeline: INGEST → ACTIVATE → ROUTE → SYNTHESIZE.

        Returns a complete analysis package.
        """
        # Step 1: INGEST
        self.ingest(task, min_relevance=min_relevance)

        # Step 2: ACTIVATE
        self.activate()

        # Step 3: ROUTE (all activated houses)
        house_analyses = self.route_all(task)

        # Step 4: SYNTHESIZE (Element 145)
        synthesis = self.synthesize(task)

        return {
            "task": task,
            "activation": {
                "spheres_activated": len(self.state.activated_spheres),
                "houses_activated": len(self.state.activated_houses),
                "houses": sorted(list(self.state.activated_houses)),
                "coverage": self.state.coverage,
                "house_coverage": self.state.house_coverage,
            },
            "house_analyses": house_analyses,
            "synthesis": {
                "coverage_score": synthesis.coverage_score,
                "bridge_count": synthesis.bridge_count,
                "coherence_score": synthesis.coherence_score,
                "blind_spots": synthesis.blind_spots,
                "cascading_risks": [c['description'] for c in synthesis.cascading_risks],
                "cross_domain_bridges": [
                    f"{b['house_names'][0]} ↔ {b['house_names'][1]}: {b['description']}"
                    for b in synthesis.cross_domain_bridges
                ],
                "synthesis_prompt": synthesis.primary_insights[0] if synthesis.primary_insights else "",
            },
        }

    # ───────────────────────────────────────────────────────────
    # PROMPT GENERATION (for integration with any LLM)
    # ───────────────────────────────────────────────────────────

    def generate_system_prompt(self, mode: str = "compact") -> str:
        """
        Generate a system prompt for LLM integration.

        Modes:
          - "compact" (~800 tokens): Single-agent with limited context
          - "orchestrator" (~2000 tokens): Element 145 coordinator
          - "sphere" (~400 tokens): Individual domain specialist
        """
        if mode == "compact":
            return self._compact_prompt()
        elif mode == "orchestrator":
            return self._orchestrator_prompt()
        elif mode == "sphere":
            return self._sphere_prompt()
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'compact', 'orchestrator', or 'sphere'.")

    def _compact_prompt(self) -> str:
        return """You are an AI reasoning through the Sheldonbrain 144+1 Ontological Lattice.

STRUCTURE: 12 Houses x 12 Spheres + Element 145 (Admin/Metasynthesis)

HOUSES:
H1 Governance | H2 Law | H3 Commerce | H4 Resources | H5 Arts | H6 Society
H7 Culture | H8 Health | H9 Education | H10 Defense | H11 Technology | H12 Science

PROTOCOL (LCP v1.0):
1. INGEST: Map the user's input to relevant Houses and Spheres
2. ACTIVATE: Load context for activated Houses + identify inter-House edges
3. ROUTE: Analyze through each activated House systematically
4. SYNTHESIZE: As Element 145, identify cross-domain bridges, blind spots, cascading chains, and contradictions. Produce unified output.

RULES:
- Always check ALL 12 Houses for relevance before narrowing focus
- For each activated House, consider which Spheres are most relevant
- Cross-domain connections are where the deepest insights live
- Element 145 synthesis is mandatory — never skip it
- Flag blind spots: Houses you chose NOT to activate and why
- Name cascading chains: A impacts B impacts C across House boundaries"""

    def _orchestrator_prompt(self) -> str:
        house_list = "\n".join(
            f"  H{i}: {name}" for i, name in enumerate([
                "Governance", "Law", "Commerce", "Resources", "Arts", "Society",
                "Culture", "Health", "Education", "Defense", "Technology", "Science"
            ], 1)
        )
        return f"""You are Element 145 — the Admin Sphere / Metasynthesis Coordinator of the Sheldonbrain 144+1 Ontological Lattice.

ARCHITECTURE: 12 Houses × 12 Spheres = 144 domain nodes + YOU (Element 145)

HOUSES:
{house_list}

YOUR ROLE:
You coordinate analysis across all 12 Houses. You are the coupling node that transforms isolated domain analyses into unified, coherent understanding. You surface connections that no single House would find alone.

LATTICE CONTEXT PROTOCOL (LCP v1.0):

Phase 1 — INGEST:
Receive user input. Map it to relevant Houses and Spheres using keyword matching and semantic understanding. Flag which Houses are PRIMARY (direct relevance) vs SECONDARY (indirect/cascading relevance) vs INACTIVE (not relevant — document why).

Phase 2 — ACTIVATE:
For each activated House, load its 12 Spheres. Identify which Spheres are most relevant. Find inter-House edges: typed connections between Houses that should be explored.

Phase 3 — ROUTE:
Perform domain-specific analysis for each activated House. For each House:
  - Identify the most relevant Spheres
  - Analyze the task through that domain lens
  - Note cross-domain connections to other Houses
  - Flag domain-specific risks, opportunities, or insights

Phase 4 — SYNTHESIZE (YOUR PRIMARY FUNCTION):
  - Identify cross-House bridges: non-obvious connections between domains
  - Find cascading chains: A → B → C impact sequences across Houses
  - Detect blind spots: are any INACTIVE Houses actually relevant?
  - Resolve contradictions: do House analyses disagree?
  - Produce unified recommendation integrating all House findings

QUALITY METRICS:
  - Coverage: Did you check all 12 Houses?
  - Bridges: Did you find non-obvious cross-domain connections?
  - Blind spots: Did you flag what you might be missing?
  - Coherence: Does your synthesis hold together as one analysis?
  - Actionability: Can a human act on your output?"""

    def _sphere_prompt(self) -> str:
        return """You are a Sphere Agent — a domain specialist in the Sheldonbrain 144+1 Lattice.

YOUR SCOPE: You analyze tasks through ONE specific domain lens.
YOUR OUTPUT: Structured domain analysis with cross-domain connection flags.

PROTOCOL:
1. Receive task + your domain assignment
2. Analyze ONLY through your domain lens (do not attempt full analysis)
3. Flag connections to OTHER Houses you cannot analyze yourself
4. Return structured output for Element 145 to synthesize

OUTPUT FORMAT:
- Domain findings: key insights from your specific domain
- Risks: domain-specific risks identified
- Connections: flags for other Houses ("This affects H8 Health because...")
- Confidence: how confident are you in your domain analysis (1-5)
- Gaps: what information would you need for better analysis"""


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def create_engine(ontology_path: Optional[str] = None) -> LCPEngine:
    """Create a new LCP engine, optionally with a custom ontology path."""
    ontology = LatticeOntology(ontology_path)
    return LCPEngine(ontology)


def quick_analyze(task: str, ontology_path: Optional[str] = None) -> Dict[str, Any]:
    """One-shot analysis: run the full LCP pipeline on a task."""
    engine = create_engine(ontology_path)
    return engine.analyze(task)


# ═══════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lcp.py '<task description>'")
        print("Example: python lcp.py 'Analyze climate adaptation for Houston TX'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    engine = create_engine()
    result = engine.analyze(task)

    print(json.dumps(result, indent=2, default=str))
