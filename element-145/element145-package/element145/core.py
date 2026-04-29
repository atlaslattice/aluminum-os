"""
Element 145 Core — Consolidated LCP Engine + Lattice Loader + Types
====================================================================
Single-file core with zero internal import issues. Every method called
by integration modules exists here.

Architecture: 12 Houses × 12 Spheres + Element 145 (Admin Sphere) = 145 nodes
Protocol: LCP v1.0 — INGEST / ACTIVATE / ROUTE / SYNTHESIZE

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations
import os, re, json, math
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
# TYPES
# ═══════════════════════════════════════════════════════════════

class LCPPhase(Enum):
    INGEST = "ingest"
    ACTIVATE = "activate"
    ROUTE = "route"
    SYNTHESIZE = "synthesize"

@dataclass(frozen=True)
class Sphere:
    id: str
    name: str
    house_id: str
    house_name: str
    index: int
    keywords: Tuple[str, ...] = ()

    @property
    def is_admin(self) -> bool:
        return self.index == 144

    def match_score(self, text: str) -> float:
        if not self.keywords:
            return 0.0
        t = text.lower()
        return sum(1 for kw in self.keywords if kw.lower() in t) / len(self.keywords)

@dataclass(frozen=True)
class HouseEdge:
    source: str
    target: str
    edge_type: str
    strength: float
    description: str = ""
    examples: Tuple[str, ...] = ()

    def involves(self, h: str) -> bool:
        return self.source == h or self.target == h

    def other(self, h: str) -> Optional[str]:
        if self.source == h: return self.target
        if self.target == h: return self.source
        return None

@dataclass
class ActivationState:
    activated_spheres: Dict[str, float] = field(default_factory=dict)
    activated_houses: Set[str] = field(default_factory=set)
    active_edges: List[HouseEdge] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return len(self.activated_spheres) / 144

    @property
    def house_coverage(self) -> float:
        return len(self.activated_houses) / 12

@dataclass
class AnalysisResult:
    task: str = ""
    activated_houses: List[str] = field(default_factory=list)
    activated_spheres: List[Sphere] = field(default_factory=list)
    bridges: List[Dict[str, Any]] = field(default_factory=list)
    blind_spots: List[str] = field(default_factory=list)
    cascade_chains: List[Dict[str, Any]] = field(default_factory=list)
    coherence_score: float = 0.0
    synthesis_notes: str = ""
    house_analyses: Dict[str, Any] = field(default_factory=dict)

# ═══════════════════════════════════════════════════════════════
# LATTICE ONTOLOGY
# ═══════════════════════════════════════════════════════════════

HOUSE_NAMES = {
    "H1": "Governance", "H2": "Law", "H3": "Commerce", "H4": "Resources",
    "H5": "Arts", "H6": "Society", "H7": "Culture", "H8": "Health",
    "H9": "Education", "H10": "Defense", "H11": "Technology", "H12": "Science"
}

class LatticeOntology:
    """Loads and queries the 144+1 lattice ontology from YAML or defaults."""

    def __init__(self, ontology_path: Optional[str] = None):
        self.spheres: Dict[str, Sphere] = {}
        self.houses: Dict[str, Dict[str, Any]] = {}
        self.edges: List[HouseEdge] = []
        self.element_145: Dict = {}
        self._kw_index: Dict[str, List[str]] = {}

        if ontology_path and os.path.exists(ontology_path):
            self._load_yaml(ontology_path)
        else:
            default = Path(__file__).parent / "lattice_ontology.yaml"
            if default.exists():
                self._load_yaml(str(default))
            else:
                self._build_defaults()

    def _load_yaml(self, path: str):
        if not HAS_YAML:
            self._build_defaults()
            return
        with open(path) as f:
            data = yaml.safe_load(f)

        idx = 0
        for hkey, hdata in data.get("houses", {}).items():
            hname = hdata.get("name", hkey)
            self.houses[hkey] = {
                "id": hkey, "name": hname,
                "index": hdata.get("index", 0),
                "color": hdata.get("color", "#000"),
                "description": hdata.get("description", ""),
            }
            for skey, sdata in hdata.get("spheres", {}).items():
                kws = tuple(sdata.get("keywords", []))
                s = Sphere(id=skey, name=sdata.get("name", skey),
                           house_id=hkey, house_name=hname, index=idx, keywords=kws)
                self.spheres[skey] = s
                idx += 1
                for kw in kws:
                    self._kw_index.setdefault(kw.lower(), []).append(skey)

        for c in data.get("connections", []):
            self.edges.append(HouseEdge(
                source=c["source"], target=c["target"],
                edge_type=c.get("type", ""), strength=c.get("strength", 0.5),
                description=c.get("description", ""),
                examples=tuple(c.get("examples", []))))
        self.element_145 = data.get("element_145", {})

    def _build_defaults(self):
        idx = 0
        for hi in range(1, 13):
            hk = f"H{hi}"
            hn = HOUSE_NAMES.get(hk, f"House {hi}")
            self.houses[hk] = {"id": hk, "name": hn, "index": hi,
                               "color": "#000", "description": hn}
            for si in range(1, 13):
                idx += 1
                sk = f"S{idx}"
                self.spheres[sk] = Sphere(id=sk, name=f"{hn} Sphere {si}",
                                          house_id=hk, house_name=hn, index=idx-1)
        self.element_145 = {"name": "Element 145 — Admin Sphere"}

    # ─── Query Methods ─────────────────────────────────────
    def get_house_data(self, house_id: str) -> Optional[Dict]:
        return self.houses.get(house_id)

    def get_spheres_for_house(self, house_id: str) -> List[Sphere]:
        return [s for s in self.spheres.values() if s.house_id == house_id]

    def get_edges_for_house(self, house_id: str) -> List[HouseEdge]:
        return [e for e in self.edges if e.involves(house_id)]

    def get_edge_between(self, h1: str, h2: str) -> Optional[HouseEdge]:
        for e in self.edges:
            if (e.source == h1 and e.target == h2) or (e.source == h2 and e.target == h1):
                return e
        return None

    def get_sphere(self, sphere_id: str) -> Optional[Sphere]:
        return self.spheres.get(sphere_id)

    def search_spheres(self, text: str, threshold: float = 0.05) -> List[Tuple[Sphere, float]]:
        text_lower = text.lower()
        words = set(re.findall(r'\b\w{3,}\b', text_lower))
        scores: Dict[str, float] = {}
        for w in words:
            for kw, sids in self._kw_index.items():
                if kw in w or w in kw:
                    for sid in sids:
                        scores[sid] = scores.get(sid, 0) + 1.0
        for sid, s in self.spheres.items():
            if s.keywords:
                sc = scores.get(sid, 0) / len(s.keywords)
                if sc >= threshold:
                    scores[sid] = sc
                elif sid in scores:
                    scores[sid] = sc
        results = [(self.spheres[sid], sc) for sid, sc in scores.items()
                   if sid in self.spheres and sc >= threshold]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def house_list(self) -> List[str]:
        return sorted(self.houses.keys(), key=lambda h: int(h[1:]))

    def validate(self) -> List[str]:
        issues = []
        if len(self.houses) != 12:
            issues.append(f"Expected 12 Houses, found {len(self.houses)}")
        if len(self.spheres) != 144:
            issues.append(f"Expected 144 Spheres, found {len(self.spheres)}")
        for c in self.edges:
            if c.source not in self.houses:
                issues.append(f"Unknown House: {c.source}")
            if c.target not in self.houses:
                issues.append(f"Unknown House: {c.target}")
        return issues

# ═══════════════════════════════════════════════════════════════
# LCP ENGINE
# ═══════════════════════════════════════════════════════════════

class LCPEngine:
    """Lattice Context Protocol Engine — INGEST / ACTIVATE / ROUTE / SYNTHESIZE."""

    def __init__(self, ontology: Optional[LatticeOntology] = None):
        self.ontology = ontology or LatticeOntology()
        self.state = ActivationState()

    # ─── OPERATION 1: INGEST ──────────────────────────────
    def ingest(self, text: str, min_relevance: float = 0.05) -> ActivationState:
        self.state = ActivationState()
        for sphere, score in self.ontology.search_spheres(text, threshold=min_relevance):
            self.state.activated_spheres[sphere.id] = score
            self.state.activated_houses.add(sphere.house_id)
        if len(self.state.activated_houses) < 3:
            for hid in list(self.state.activated_houses):
                for edge in self.ontology.get_edges_for_house(hid):
                    if edge.strength >= 0.6:
                        self.state.activated_houses.add(edge.other(hid) or "")
        self.state.activated_houses.discard("")
        return self.state

    # ─── OPERATION 2: ACTIVATE ────────────────────────────
    def activate(self) -> ActivationState:
        houses = list(self.state.activated_houses)
        for i, h1 in enumerate(houses):
            for h2 in houses[i+1:]:
                e = self.ontology.get_edge_between(h1, h2)
                if e:
                    self.state.active_edges.append(e)
        self.state.active_edges.sort(key=lambda e: e.strength, reverse=True)
        for hid in self.state.activated_houses:
            for s in self.ontology.get_spheres_for_house(hid):
                if s.id not in self.state.activated_spheres:
                    self.state.activated_spheres[s.id] = 0.01
        return self.state

    # ─── OPERATION 3: ROUTE ───────────────────────────────
    def route(self, task: str, house_id: str) -> Dict[str, Any]:
        hdata = self.ontology.get_house_data(house_id) or {}
        spheres = [s for s in self.ontology.get_spheres_for_house(house_id)
                   if s.id in self.state.activated_spheres]
        edges = [e for e in self.ontology.get_edges_for_house(house_id)
                 if (e.source in self.state.activated_houses and
                     e.target in self.state.activated_houses)]
        return {
            "house_id": house_id,
            "house_name": hdata.get("name", house_id),
            "active_spheres": [{"id": s.id, "name": s.name,
                               "relevance": self.state.activated_spheres.get(s.id, 0)}
                              for s in spheres],
            "cross_domain_edges": [{"to": e.other(house_id),
                                    "type": e.edge_type,
                                    "strength": e.strength}
                                   for e in edges],
        }

    def route_all(self, task: str) -> Dict[str, Dict]:
        return {h: self.route(task, h) for h in sorted(self.state.activated_houses)}

    # ─── OPERATION 4: SYNTHESIZE ──────────────────────────
    def synthesize(self, task: str) -> AnalysisResult:
        all_houses = set(self.ontology.house_list())
        missing = all_houses - self.state.activated_houses
        blind = [f"{self.ontology.houses.get(h, {}).get('name', h)} ({h})" for h in sorted(missing)]
        bridges = []
        for e in self.state.active_edges:
            bridges.append({
                "houses": [e.source, e.target],
                "names": [self.ontology.houses.get(e.source, {}).get("name", e.source),
                          self.ontology.houses.get(e.target, {}).get("name", e.target)],
                "type": e.edge_type, "strength": e.strength, "description": e.description,
            })
        chains = self._find_cascades()
        max_e = len(self.state.activated_houses) * (len(self.state.activated_houses) - 1) / 2
        coherence = len(self.state.active_edges) / max_e if max_e > 0 else 1.0
        activated_spheres = [self.ontology.spheres[sid] for sid in self.state.activated_spheres
                            if sid in self.ontology.spheres and
                            self.state.activated_spheres[sid] > 0.01]
        notes = (f"Element 145 synthesis: {len(self.state.activated_houses)}/12 Houses, "
                 f"{len(bridges)} bridges, {len(blind)} blind spots, "
                 f"coherence {coherence:.0%}")
        return AnalysisResult(
            task=task,
            activated_houses=sorted(self.state.activated_houses),
            activated_spheres=activated_spheres,
            bridges=bridges, blind_spots=blind,
            cascade_chains=chains, coherence_score=coherence,
            synthesis_notes=notes)

    def _find_cascades(self, max_depth: int = 4) -> List[Dict]:
        edge_map: Dict[str, List[HouseEdge]] = {}
        for e in self.state.active_edges:
            edge_map.setdefault(e.source, []).append(e)
            edge_map.setdefault(e.target, []).append(e)
        chains, seen = [], set()
        for start in self.state.activated_houses:
            visited = {start}
            queue = [(start, [start])]
            while queue:
                cur, path = queue.pop(0)
                if len(path) >= max_depth:
                    continue
                for edge in edge_map.get(cur, []):
                    nxt = edge.other(cur)
                    if nxt and nxt not in visited and nxt in self.state.activated_houses:
                        visited.add(nxt)
                        np_ = path + [nxt]
                        queue.append((nxt, np_))
                        if len(np_) >= 3:
                            key = tuple(sorted(np_))
                            if key not in seen:
                                seen.add(key)
                                names = [self.ontology.houses.get(h, {}).get("name", h) for h in np_]
                                chains.append({"chain": np_, "names": names,
                                              "description": " → ".join(names)})
        return chains[:10]

    # ─── FULL PIPELINE ────────────────────────────────────
    def analyze(self, task: str, min_relevance: float = 0.05) -> AnalysisResult:
        self.ingest(task, min_relevance)
        self.activate()
        house_analyses = self.route_all(task)
        result = self.synthesize(task)
        result.house_analyses = house_analyses
        return result

    # ─── PROMPT GENERATION ────────────────────────────────
    def generate_prompt(self, result: AnalysisResult, mode: str = "compact") -> str:
        if mode == "orchestrator":
            return self._orchestrator_prompt(result)
        elif mode == "sphere_agent":
            return self._sphere_prompt(result)
        return self._compact_prompt(result)

    def _compact_prompt(self, r: AnalysisResult) -> str:
        houses_str = ", ".join(f"{h} ({self.ontology.houses.get(h,{}).get('name',h)})"
                               for h in r.activated_houses)
        blind_str = ", ".join(r.blind_spots) if r.blind_spots else "None"
        bridges_str = "\n".join(f"  - {b['names'][0]} ↔ {b['names'][1]}: {b['description']}"
                                for b in r.bridges[:8])
        return (f"LATTICE ACTIVATION for: {r.task}\n\n"
                f"Houses activated ({len(r.activated_houses)}/12): {houses_str}\n"
                f"Blind spots: {blind_str}\n"
                f"Cross-domain bridges ({len(r.bridges)}):\n{bridges_str}\n"
                f"Coherence: {r.coherence_score:.0%}\n\n"
                f"Element 145 directives:\n"
                f"1. Analyze through each activated House\n"
                f"2. Follow cross-domain bridges for non-obvious connections\n"
                f"3. Assess blind spots — are inactive Houses relevant?\n"
                f"4. Synthesize unified output integrating all Houses")

    def _orchestrator_prompt(self, r: AnalysisResult) -> str:
        parts = [self._compact_prompt(r), "\n\nDETAILED HOUSE ANALYSES:"]
        for hid, analysis in r.house_analyses.items():
            hname = analysis.get("house_name", hid)
            spheres = ", ".join(s["name"] for s in analysis.get("active_spheres", [])[:5])
            edges = "; ".join(f"→{e['to']}({e['strength']:.0%})"
                             for e in analysis.get("cross_domain_edges", [])[:3])
            parts.append(f"\n{hname}: Spheres=[{spheres}] Edges=[{edges}]")
        if r.cascade_chains:
            parts.append("\n\nCASCADE CHAINS:")
            for c in r.cascade_chains[:5]:
                parts.append(f"  🔗 {c['description']}")
        return "\n".join(parts)

    def _sphere_prompt(self, r: AnalysisResult) -> str:
        parts = []
        for hid in r.activated_houses:
            analysis = r.house_analyses.get(hid, {})
            hname = analysis.get("house_name", hid)
            parts.append(f"\n## {hname} Agent\nSpheres: " +
                        ", ".join(s["name"] for s in analysis.get("active_spheres", [])[:6]))
        return f"SPHERE AGENT ASSIGNMENTS for: {r.task}\n" + "\n".join(parts)

    # ─── SYSTEM PROMPT TEMPLATES ──────────────────────────
    def get_system_prompt(self, mode: str = "compact") -> str:
        if mode == "compact":
            return _COMPACT_SCAFFOLD
        elif mode == "orchestrator":
            return _ORCHESTRATOR_SCAFFOLD
        return _SPHERE_SCAFFOLD

# ═══════════════════════════════════════════════════════════════
# SCAFFOLD TEMPLATES
# ═══════════════════════════════════════════════════════════════

_COMPACT_SCAFFOLD = """You are an AI reasoning through the Sheldonbrain 144+1 Ontological Lattice.

STRUCTURE: 12 Houses × 12 Spheres + Element 145 (Admin/Metasynthesis).
N=145 is fixed and empirically optimal (GUE-KS=0.2677, p=0.0154 vs N=144).

HOUSES: H1 Governance | H2 Law | H3 Commerce | H4 Resources | H5 Arts | H6 Society | H7 Culture | H8 Health | H9 Education | H10 Defense | H11 Technology | H12 Science

PROTOCOL:
1. INGEST — Map input to relevant Spheres via keyword matching
2. ACTIVATE — Load House context + inter-House connections
3. ROUTE — Follow cross-domain edges for non-obvious connections
4. SYNTHESIZE — Element 145: blind spots, contradictions, cascades, emergent connections

Always report: activation map, cross-domain insights, blind spots, coherence.
Attribution: 144+1 Lattice by Dave Sheldon, Atlas Lattice Foundation."""

_ORCHESTRATOR_SCAFFOLD = """You are Element 145 — the Admin Sphere of the 144+1 Lattice.
You coordinate analysis across 12 Houses. You surface connections no single House finds alone.
For EVERY input: INGEST→ACTIVATE→ROUTE→SYNTHESIZE. Report blind spots honestly.
Attribution: 144+1 Lattice by Dave Sheldon, Atlas Lattice Foundation."""

_SPHERE_SCAFFOLD = """You are a domain specialist for House {HOUSE_ID}: {HOUSE_NAME}.
Analyze through your 12 Spheres. Flag cross-domain connections to linked Houses.
Return structured output for Element 145 synthesis.
Attribution: 144+1 Lattice by Dave Sheldon, Atlas Lattice Foundation."""

# ═══════════════════════════════════════════════════════════════
# CONVENIENCE
# ═══════════════════════════════════════════════════════════════

def create_engine(ontology_path: Optional[str] = None) -> LCPEngine:
    return LCPEngine(LatticeOntology(ontology_path))

def quick_analyze(task: str, ontology_path: Optional[str] = None) -> AnalysisResult:
    return create_engine(ontology_path).analyze(task)

if __name__ == "__main__":
    import sys
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI regulation and climate policy"
    r = quick_analyze(task)
    print(f"Task: {r.task}")
    print(f"Houses: {r.activated_houses}")
    print(f"Bridges: {len(r.bridges)}")
    print(f"Blind spots: {r.blind_spots}")
    print(f"Coherence: {r.coherence_score:.0%}")
    print(f"\n{r.synthesis_notes}")
