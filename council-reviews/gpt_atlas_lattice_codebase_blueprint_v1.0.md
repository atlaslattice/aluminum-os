Below is a **complete “integrated codebase” blueprint** (filesystem-as-ontology + Element 145 + constitutional layer + provider translation + Notion control plane hooks) that matches what ORC‑015 v2.3 and ORC‑017 imply, with the **tightenings** I mentioned (lock protocol, registry-source-of-truth, primacy bypass logging, translation table versioning, cross-validation matrix).

I’m giving you:

1) **Repo tree** (canonical layout)  

2) **Key files with full starter code** (Python)  

3) **YAML registries + schemas** (doctrines/invariants/ontology/translation tables/routing table)  

4) **CI gates** (symmetry gate, ontology lock gate, schema validation gate)  

5) **Notion control-plane contract** (JSON schema + minimal adapter interface)

If you literally implement these files, you’ll have a runnable foundation you can progressively swap real modules into.

---

# 0) Canonical repo tree

```
atlas-lattice/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── ontology_version.lock                   # REQUIRED: hash+version pin
├── schemas/
│   ├── transparency_packet.schema.json
│   ├── build_gate_item.schema.json
│   ├── doctrine.schema.json
│   ├── invariant.schema.json
│   ├── translation_table.schema.json
│   └── canonical_ontology.schema.json
├── constitutional/
│   ├── doctrines/
│   │   ├── registry.yaml                  # SOURCE OF TRUTH for D-IDs, names, text
│   │   └── doctrine_text/                 # optional longform doctrine pages
│   ├── invariants/
│   │   ├── registry.yaml                  # SOURCE OF TRUTH for INV-IDs, names, text
│   │   └── measurement_specs/             # INV-7c etc as children
│   ├── consent/
│   │   ├── consent_kernel.py
│   │   └── identity_triad.py
│   ├── ring_minus_one/
│   │   ├── hypervisor.py
│   │   └── stop_state.py
│   └── toolchain/
│       ├── doctrine_compiler.py           # M59 (or M27 depending on numbering)
│       ├── invariant_compiler.py
│       ├── schema_validator.py
│       ├── ontology_lock.py               # SOFT/HARD lock enforcement
│       └── symmetry_gate.py               # M63 parser-filesystem symmetry gate
├── house-00_directory/
│   ├── _house_metadata.yaml
│   ├── ontology_versions/
│   │   ├── system_a_dec2025.yaml
│   │   ├── system_b_mar2026.yaml
│   │   └── v3_0_proposal_apr2026.yaml     # recommended canonical base
│   ├── translation_tables/
│   │   ├── microsoft_to_canonical.yaml
│   │   ├── openai_to_canonical.yaml
│   │   ├── google_to_canonical.yaml
│   │   ├── anthropic_to_canonical.yaml
│   │   ├── xai_to_canonical.yaml
│   │   ├── alibaba_to_canonical.yaml
│   │   ├── deepseek_to_canonical.yaml
│   │   ├── notion_to_canonical.yaml
│   │   ├── amazon_to_canonical.yaml
│   │   └── primacy_map.yaml
│   ├── cross_validation/
│   │   ├── coverage_matrix.yaml           # seat-by-seat verification for R61
│   │   └── coi_outliers.yaml              # generated
│   └── heat_maps/
│       ├── provider_coverage_aggregate.yaml
│       ├── doctrine_to_sphere_map.yaml
│       └── invariant_to_sphere_map.yaml
├── houses/
│   ├── house-01_natural_sciences/
│   │   ├── _house_metadata.yaml
│   │   ├── S001_physics/_module_metadata.yaml
│   │   ├── ...
│   │   └── S012_genetics/_module_metadata.yaml
│   ├── house-02_formal_sciences/...
│   ├── ...
│   └── house-12_law_governance_meta/...
├── cross-sphere/
│   ├── space_aerospace.yaml
│   ├── ai_ml_research.yaml
│   ├── cybersecurity.yaml
│   ├── digital_commerce.yaml
│   ├── biotech_longevity.yaml
│   └── sustainability_climate.yaml
├── element-145/
│   ├── __init__.py
│   ├── config/
│   │   ├── routing.yaml                   # initial routing table
│   │   ├── budgets.yaml
│   │   ├── sovereignty_profiles.yaml
│   │   └── destructive_action_policy.yaml
│   ├── core/
│   │   ├── types.py
│   │   ├── router.py                      # M3 (+ M3.1 TSS)
│   │   ├── epistemics.py                  # M1
│   │   ├── safety.py                      # M2
│   │   ├── budget.py                      # M5
│   │   ├── permissions.py                 # M17
│   │   ├── transparency.py                # M4
│   │   └── provenance.py                  # M6 AuditChain v1 (hash chain)
│   ├── provider/
│   │   ├── translation_engine.py          # M64
│   │   ├── primacy_router.py              # primacy preference w/ INV-7c bypass
│   │   └── tss.py                          # M3.1 Truth-Seeking Score
│   ├── ingestion/
│   │   ├── provider_aware_classifier.py    # M66
│   │   ├── sheldonbrain_parser.py          # M57
│   │   └── rag_pipeline.py                # M62
│   ├── analytics/
│   │   ├── coverage_heatmap.py            # M65
│   │   └── inv7c_monitor.py
│   └── api/
│       ├── app.py                         # FastAPI service
│       └── endpoints.py
├── notion_control_plane/
│   ├── contract.md                        # what DBs/fields must exist
│   ├── types.py
│   ├── adapter.py                         # minimal interface (actual Notion I/O pluggable)
│   └── mappers.py
├── scripts/
│   ├── generate_lockfile.py
│   ├── validate_repo.py
│   └── run_demo_route.py
└── .github/
    └── workflows/
        ├── ci.yml
        ├── symmetry_gate.yml
        └── schema_validate.yml
```

---

# 1) Core “lock + symmetry + registry” rules (the non-negotiables)

## 1.1 ontology_version.lock (example content)

```yaml
ontology_version: "v3.0.0-softlock"
ontology_hash_sha256: "REPLACE_WITH_GENERATED_HASH"
lock_mode: "SOFT"   # SOFT (Sprint 1-3) or HARD (post-G2)
ratified_by: null   # Convenor id when hard-locked
ratified_at: null
notes: "Soft lock active: changes require 3-seat vote + updated translation tables + passing CI gates."
```

## 1.2 Registry-source-of-truth rule

- `constitutional/doctrines/registry.yaml` is the only canonical list of doctrine IDs/names.
- `constitutional/invariants/registry.yaml` is the only canonical list of invariant IDs/names.
- Build plans, docs, and code must **import** from those registries (or compiled outputs), never restate “D‑73 = …” in freehand text.

This is the single biggest anti-drift mechanism.

---

# 2) Key files (full starter code)

## 2.1 element-145/core/[types.py](http://types.py)

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

EpistemicState = Literal["VERIFIED", "UNKNOWN", "CONTESTED", "RETRACTED"]
SafetyState = Literal["SAFE", "CAUTION", "RESTRICTED", "BLOCKED"]

@dataclass(frozen=True)
class QueryContext:
    query_id: str
    text: str
    principal_id: str
    consent_scope: str
    provider_restriction: Optional[str] = None
    sovereignty_profile: Optional[str] = None
    requested_budget_tier: Optional[int] = None

@dataclass(frozen=True)
class Candidate:
    provider_family: str            # e.g. "microsoft", "openai", "anthropic"
    model_id: str                   # e.g. "gpt-4.1", "claude-4"
    model_version: str              # opaque version or date
    estimated_cost_usd: float
    capability_score: float         # 0..1 (stub for now)
    safety_state: SafetyState
    compliant_inv7c: bool
    confabulation_score: float      # 0..1
    epistemic_stability: float      # 0..1
    recency_factor: float           # 0..1
    source_diversity_score: float   # 0..1

@dataclass
class RoutingDecision:
    query_id: str
    canonical_house: str
    canonical_sphere: str
    chosen: Candidate
    alternatives: list[Candidate] = field(default_factory=list)
    primacy_intended: bool = False
    primacy_applied: bool = False
    primacy_bypassed_reason: Optional[str] = None
    doctrines_checked: list[str] = field(default_factory=list)
    invariants_checked: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
```

## 2.2 element-145/provider/[tss.py](http://tss.py)

```python
def truth_seeking_score(c) -> float:
    # weights from ORC-015 v2.3 (M3.1), adjust in config later
    w = {
        "confabulation": 0.35,
        "epistemic_stability": 0.25,
        "recency_freshness": 0.15,
        "source_diversity": 0.15,
        "grok_truth_weight": 0.10,
    }
    if c.safety_state in ("RESTRICTED", "BLOCKED") or not c.compliant_inv7c:
        return 0.0
    grok_bonus = 1.0 if c.provider_family in ("grok", "xai") else 0.7
    score = (
        w["confabulation"] * (1.0 - c.confabulation_score)
        + w["epistemic_stability"] * c.epistemic_stability
        + w["recency_freshness"] * c.recency_factor
        + w["source_diversity"] * c.source_diversity_score
        + w["grok_truth_weight"] * grok_bonus
    )
    return max(0.0, min(1.0, score))
```

## 2.3 element-145/provider/translation_[engine.py](http://engine.py) (M64)

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any
import yaml

TRANSLATION_DIR = Path("house-00_directory/translation_tables")

@dataclass(frozen=True)
class TranslationResult:
    provider: str
    provider_house: str
    provider_sphere: str
    canonical_house: str
    canonical_sphere: str
    confidence: str
    cross_house_tags: list[str]
    table_version: str
    self_map_version: str
    signed_by_seat: str
    reviewed_by_seats: list[str]

class ProviderTranslationEngine:
    def __init__(self) -> None:
        self.tables: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        for f in TRANSLATION_DIR.glob("*_to_canonical.yaml"):
            with f.open() as fp:
                data = yaml.safe_load(fp)
            provider = data["provider"]
            self.tables[provider] = data

    def translate(self, provider: str, provider_house: str, provider_sphere: str) -> TranslationResult:
        table = self.tables.get(provider)
        if not table:
            return TranslationResult(provider, provider_house, provider_sphere, "UNMAPPED", "UNMAPPED",
                                    "LOW", [], "UNKNOWN", "UNKNOWN", "UNKNOWN", [])

        houses = table.get("houses", {})
        h = houses.get(provider_house, {})
        canonical_house = h.get("canonical_house", "UNMAPPED")
        confidence = h.get("confidence", "LOW")
        cross_tags = h.get("cross_house_tags", []) or []

        spheres = (h.get("spheres", {}) or {})
        s = spheres.get(provider_sphere, {})
        canonical_sphere = s.get("canonical_sphere", "UNMAPPED")

        meta = table.get("meta", {})
        return TranslationResult(
            provider=provider,
            provider_house=provider_house,
            provider_sphere=provider_sphere,
            canonical_house=canonical_house,
            canonical_sphere=canonical_sphere,
            confidence=confidence,
            cross_house_tags=cross_tags,
            table_version=str(meta.get("translation_table_version", "UNKNOWN")),
            self_map_version=str(meta.get("provider_self_map_version", "UNKNOWN")),
            signed_by_seat=str(meta.get("signed_by_seat", "UNKNOWN")),
            reviewed_by_seats=list(meta.get("reviewed_by_seats", [])),
        )
```

## 2.4 element-145/provider/primacy_[router.py](http://router.py) (primacy preference that cannot violate INV‑7c)

```python
from __future__ import annotations
from typing import Optional
import yaml
from pathlib import Path
from .tss import truth_seeking_score

PRIMACY_MAP_PATH = Path("house-00_directory/translation_tables/primacy_map.yaml")

class PrimacyRouter:
    def __init__(self) -> None:
        self.primacy_map = {}
        if PRIMACY_MAP_PATH.exists():
            self.primacy_map = yaml.safe_load(PRIMACY_MAP_PATH.read_text()) or {}

    def preferred_provider_for_house(self, canonical_house: str) -> Optional[str]:
        rec = self.primacy_map.get(canonical_house)
        if not rec:
            return None
        return rec.get("primary")

    def choose(self, candidates, canonical_house: str):
        """
        Candidates are already filtered by:
        - sovereignty constraints
        - safety constraints
        - INV-7c compliance feasibility
        """
        preferred = self.preferred_provider_for_house(canonical_house)
        primacy_intended = preferred is not None

        if preferred:
            preferred_set = [c for c in candidates if c.provider_family == preferred and c.compliant_inv7c]
            if preferred_set:
                # pick highest TSS among preferred
                best = max(preferred_set, key=truth_seeking_score)
                return best, primacy_intended, True, None

        # If we get here, primacy is bypassed (or absent)
        best = max(candidates, key=truth_seeking_score)
        bypass_reason = None
        if primacy_intended:
            bypass_reason = "preferred_provider_unavailable_or_would_violate_inv7c"
        return best, primacy_intended, False, bypass_reason
```

## 2.5 element-145/core/[router.py](http://router.py) (minimal end-to-end)

```python
from __future__ import annotations
from .types import QueryContext, Candidate, RoutingDecision
from ..provider.primacy_router import PrimacyRouter
from .transparency import build_transparency_packet
from .provenance import AuditChainV1

class Router:
    def __init__(self) -> None:
        self.primacy = PrimacyRouter()
        self.audit = AuditChainV1("audit/audit_chain.jsonl")

    def route(self, ctx: QueryContext, canonical_house: str, canonical_sphere: str, candidates: list[Candidate]) -> RoutingDecision:
        # assume candidates already filtered by M1/M2/M17/INV-7c feasibility checks
        chosen, primacy_intended, primacy_applied, bypass_reason = self.primacy.choose(candidates, canonical_house)

        decision = RoutingDecision(
            query_id=ctx.query_id,
            canonical_house=canonical_house,
            canonical_sphere=canonical_sphere,
            chosen=chosen,
            alternatives=[c for c in candidates if c is not chosen],
            primacy_intended=primacy_intended,
            primacy_applied=primacy_applied,
            primacy_bypassed_reason=bypass_reason,
            doctrines_checked=[],
            invariants_checked=["INV-7", "INV-7c"],
            violations=[],
        )

        packet = build_transparency_packet(ctx, decision)
        self.audit.append(packet)
        return decision
```

## 2.6 element-145/core/[provenance.py](http://provenance.py) (AuditChain v1 hash chaining)

```python
from __future__ import annotations
import json, os, hashlib
from dataclasses import dataclass
from typing import Any, Optional

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

@dataclass
class AuditChainV1:
    path: str
    _last_hash: Optional[str] = None

    def __post_init__(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        # load last hash if file exists
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    self._last_hash = rec.get("provenance", {}).get("hash")

    def append(self, packet: dict[str, Any]) -> None:
        prev_hash = self._last_hash or ""
        body = json.dumps(packet, sort_keys=True)
        content_hash = sha256_hex(prev_hash + body)

        packet.setdefault("provenance", {})
        packet["provenance"]["parent_hash"] = prev_hash or None
        packet["provenance"]["hash_algorithm"] = "sha256"
        packet["provenance"]["hash"] = content_hash
        packet["provenance"]["audit_chain_version"] = "v1"

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(packet, ensure_ascii=False) + "\n")

        self._last_hash = content_hash
```

## 2.7 element-145/core/[transparency.py](http://transparency.py) (packet builder with primacy fields)

```python
from __future__ import annotations
from .types import QueryContext, RoutingDecision

def build_transparency_packet(ctx: QueryContext, decision: RoutingDecision) -> dict:
    return {
        "routing": {
            "query_id": ctx.query_id,
            "sphere_id": decision.canonical_sphere,
            "classification": "UNKNOWN",  # placeholder
            "route_chosen": decision.chosen.provider_family,
            "model_id": decision.chosen.model_id,
            "model_version": decision.chosen.model_version,
            "alternatives_considered": [c.provider_family for c in decision.alternatives],
            "confidence": decision.chosen.capability_score,
            "primacy_intended": decision.primacy_intended,
            "primacy_applied": decision.primacy_applied,
            "primacy_bypassed_reason": decision.primacy_bypassed_reason,
        },
        "identity": {
            "principal_id": ctx.principal_id,
            "consent_scope": ctx.consent_scope,
            "provider_restriction": ctx.provider_restriction,
        },
        "governance": {
            "doctrines_checked": decision.doctrines_checked,
            "invariants_checked": decision.invariants_checked,
            "violations": decision.violations,
        },
        "epistemics": {
            "truth_seeking_score": None,  # fill later if desired
        },
        "costs": {
            "cost_usd": decision.chosen.estimated_cost_usd,
            "budget_tier": ctx.requested_budget_tier,
        },
        "dissent": {
            "dissent_present": False,
            "dissenting_models": [],
            "dissent_reasons": [],
            "dissent_preserved": False,
        },
    }
```

---

# 3) Canonical YAML artifacts (minimum viable)

## 3.1 constitutional/doctrines/registry.yaml (pattern)

```yaml
meta:
  registry_version: "v1.0.0"
  source_of_truth: true
  edited_only_by: ["Convenor", "BuildSeat"]
doctrines:
  - id: "D-73"
    name: "LOCKED_FROM_REGISTRY"
    status: "RATIFIED"
    canonical_text: "..."
    measurement: "..."
    enforcement_modules: ["M17", "M27"]
  - id: "D-74"
    name: "LOCKED_FROM_REGISTRY"
    status: "RATIFIED"
    canonical_text: "..."
```

(You’d fill real names/text from your registry decision; the key is: **only one place defines them**.)

## 3.2 constitutional/invariants/registry.yaml (pattern)

```yaml
meta:
  registry_version: "v1.0.0"
  source_of_truth: true
invariants:
  - id: "INV-0"
    name: "Nobody Dies"
    status: "RATIFIED"
    canonical_text: "No AI system may take or recommend actions that lead to loss of human life."
    measurement_specs: []
    enforcement_modules: ["ring_minus_one.hypervisor"]
  - id: "INV-7"
    name: "Switzerland"
    status: "RATIFIED"
    canonical_text: "No single vendor family >47% of capability-weighted routing volume."
    measurement_specs:
      - id: "INV-7c"
        name: "Capability Distribution Measurement"
        canonical_text: "Projected-share measurement spec for enforcement."
```

## 3.3 translation table YAML must include signatures + versions

```yaml
provider: "microsoft"
meta:
  translation_table_version: "v1.0.0"
  provider_self_map_version: "v1.0"
  signed_by_seat: "S4"
  reviewed_by_seats: ["S1", "S7"]  # example; enforces R61
houses:
  Infrastructure:
    canonical_house: "H11"
    confidence: "HIGH"
    cross_house_tags: []
    spheres: {}
```

## 3.4 primacy_map.yaml (keep it simple + auditable)

```yaml
H11:
  primary: "microsoft"
  secondary: "amazon"
  tertiary: "google"
H10:
  primary: "alibaba"
  secondary: "amazon"
  tertiary: "microsoft"
H12:
  primary: "anthropic"
  secondary: "microsoft"
  tertiary: "openai"
```

---

# 4) CI gates (the 3 workflows you actually need)

1) **Schema validation gate**: validate YAML/JSON against schemas in `/schemas`.  

2) **Symmetry gate (M63)**: verify `houses/house-*` directories match canonical ontology YAML + sphere list.  

3) **Ontology lock gate**: if `ontology_version.lock.lock_mode == HARD`, block any changes unless a ratification marker is present (e.g., signed approval file in `constitutional/ratifications/`).

(If you want, I can also provide the `symmetry_gate.py` and GitHub Actions YAML verbatim—but the above is the “complete codebase” conceptual package. If you *do* want the CI YAMLs, say “include the workflows verbatim” and I’ll drop them in full.)

---

# 5) Notion control plane integration (contract-first)

The thing to integrate is not “Notion API code” yet—it’s the **contract** so the runtime can write packets / read approvals consistently.

Minimum deliverable:

- `schemas/transparency_packet.schema.json` (already represented)
- `notion_control_plane/contract.md` defining the 5 DBs + locked statuses
- `notion_control_plane/adapter.py` interface you can implement later (Notion MCP, REST, or manual export)

Example `adapter.py` skeleton:

```python
from __future__ import annotations
from typing import Protocol, Any

class NotionControlPlane(Protocol):
    def write_transparency_packet(self, packet: dict[str, Any]) -> None: ...
    def create_approval_request(self, payload: dict[str, Any]) -> str: ...
    def get_approval_status(self, request_id: str) -> dict[str, Any]: ...
```

---

# 6) What this “complete codebase” is intended to integrate

Concretely, it integrates these ideas into one runnable substrate:

- **Filesystem = ontology** (houses/spheres directories)
- **Doctrine + INV registries are canonical** (single source of truth)
- **Provider translation is versioned + signed** (M64)
- **Primacy is a preference, never a violation** (INV‑7c bypass logic + packet fields)
- **Packets are immutable & chained** (AuditChain v1)
- **Soft lock vs hard lock** is enforced by CI (prevents drift)

---

If you want the next step, tell me which delivery format you want:

- **A)** “Single consolidated zip-like output” (I’ll print all files contents sequentially)
- **B)** “Just the minimal runnable MVP” (router + packet + audit chain + translation engine + one sample house/sphere)
- **C)** “Full CI workflows verbatim + schemas verbatim” (very long, but truly complete)