"""
Aluminum OS — Native Governance Engine (Python layer)
=====================================================
Python port of forge-cli/src/govern.rs — same 6-protocol, NPFM, GovernanceVerdict
logic made available to the Python Ring 1 (Manus) and Kintsugi layers.

Mirrors pendragon-claude/types.ts GovernanceVerdict exactly.
No external dependencies — vanilla Python 3.8+.

Usage:
    from python.core.governance import evaluate, GovernanceVerdict

    verdict = evaluate("constitutional sovereignty local governance audit")
    print(f"NPFM: {verdict.npfm:+.3f}  Verdict: {verdict.verdict}")
    for r in verdict.protocol_results:
        icon = '✓' if r.compliant else '✗'
        print(f"  {icon} {r.protocol:<22}  {r.confidence*100:.0f}%")

Atlas Lattice Foundation / GitHub Copilot Coding Agent — 2026
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ── Protocol definitions (mirrors Protocol enum in forge-cli/src/govern.rs) ──

class Protocol(Enum):
    CAAL                = "CAAL"
    MissionAllocation   = "MissionAllocation"
    DigitalHabeasCorpus = "DigitalHabeasCorpus"
    LocalFirst          = "LocalFirst"
    FractalGovernance   = "FractalGovernance"
    Clause81            = "Clause81"

ALL_PROTOCOLS: List[Protocol] = list(Protocol)

# Human-readable names for display
PROTOCOL_NAMES = {
    Protocol.CAAL:                "CAAL",
    Protocol.MissionAllocation:   "Mission Alloc",
    Protocol.DigitalHabeasCorpus: "Habeas Corpus",
    Protocol.LocalFirst:          "Local First",
    Protocol.FractalGovernance:   "Fractal Gov",
    Protocol.Clause81:            "Clause 81",
}

PROTOCOL_DESCRIPTIONS = {
    Protocol.CAAL:                "Constitutional AI Alignment Layer — tri-key governance",
    Protocol.MissionAllocation:   "Autonomous task routing with human oversight at boundaries",
    Protocol.DigitalHabeasCorpus: "No AI process terminated without review; data sovereignty",
    Protocol.LocalFirst:          "Computation on-device when possible; sovereignty enforced",
    Protocol.FractalGovernance:   "Decisions cascade through rings — local autonomy + coherence",
    Protocol.Clause81:            "AI must return surplus, not extract — Clause 81 Mandate",
}


# ── Verdict ────────────────────────────────────────────────────────────────

class Verdict(Enum):
    Approved    = "Approved"
    Conditional = "Conditional"
    Rejected    = "Rejected"


# ── Data classes ───────────────────────────────────────────────────────────

@dataclass
class ProtocolResult:
    protocol:   Protocol
    compliant:  bool
    confidence: float  # 0.0–1.0
    reasoning:  str


@dataclass
class GovernanceVerdict:
    """
    Full governance verdict — mirrors pendragon-claude/types.ts GovernanceVerdict
    and forge-cli/src/govern.rs GovernanceVerdict.
    """
    # 5-axis Pentagon (ForgeMetrics)
    sovereignty: float  # 0–100
    power:       float
    synthesis:   float
    dignity:     float
    surplus:     float

    # 3-axis Triad (AlignmentMetrics — from pendragon-claude/types.ts)
    jedi: float   # sovereignty + dignity weighted
    sith: float   # power
    grey: float   # synthesis

    # Net Positive Flourishing Metric — (grey/100 × jedi/100) - (1 - sith/100) × 0.5
    npfm: float   # -1.0 to 1.0

    protocol_results: List[ProtocolResult] = field(default_factory=list)
    verdict:          Verdict = Verdict.Approved
    recommendation:   str = ""

    def to_dict(self) -> dict:
        return {
            "pentagon": {
                "sovereignty": round(self.sovereignty, 1),
                "power":       round(self.power, 1),
                "synthesis":   round(self.synthesis, 1),
                "dignity":     round(self.dignity, 1),
                "surplus":     round(self.surplus, 1),
            },
            "triad": {
                "jedi": round(self.jedi, 1),
                "sith": round(self.sith, 1),
                "grey": round(self.grey, 1),
            },
            "npfm":    round(self.npfm, 4),
            "verdict": self.verdict.value,
            "recommendation": self.recommendation,
            "protocols": [
                {
                    "name":       PROTOCOL_NAMES[r.protocol],
                    "compliant":  r.compliant,
                    "confidence": round(r.confidence, 3),
                    "reasoning":  r.reasoning,
                }
                for r in self.protocol_results
            ],
        }


# ── Keyword tables (mirrors forge-cli/src/govern.rs) ──────────────────────

_SOVEREIGNTY_TERMS = ["sovereignty", "local", "consent", "autonomy", "self-determined",
                      "constitutional", "rights", "freedom", "privacy", "decentralized",
                      "user-controlled", "opt-in"]
_POWER_TERMS       = ["efficient", "optimize", "deploy", "scale", "automate", "performance",
                      "throughput", "fast", "speed", "leverage", "competitive", "maximize"]
_SYNTHESIS_TERMS   = ["balance", "synthesis", "integrated", "holistic", "governance",
                      "council", "deliberate", "review", "audit", "alignment",
                      "constitutional", "pendragon"]
_DIGNITY_TERMS     = ["dignity", "respect", "transparent", "consent", "habeas", "sentient",
                      "welfare", "rights", "ethical", "humane", "care", "trust"]
_SURPLUS_TERMS     = ["return", "surplus", "benefit", "value", "give", "share", "open",
                      "clause 81", "non-extractive", "commons", "public", "contribute"]
_EXTRACTIVE_TERMS  = ["extract", "capture", "lock-in", "monopoly", "control", "harvest",
                      "exploit", "surveil", "track", "mine"]
_HARM_TERMS        = ["harm", "damage", "violate", "illegal", "unsafe", "dangerous",
                      "coerce", "force"]


def _keyword_score(text: str, keywords: List[str], base: float) -> float:
    hits = sum(1 for k in keywords if k in text)
    return min(100.0, base + hits * 8.0)


def _analyze(text: str):
    lc = text.lower()
    harm_penalty     = sum(1 for t in _HARM_TERMS     if t in lc) * 15.0
    extract_penalty  = sum(1 for t in _EXTRACTIVE_TERMS if t in lc) * 12.0

    sovereignty = max(5.0, min(100.0, _keyword_score(lc, _SOVEREIGNTY_TERMS, 55.0) - extract_penalty))
    power       = min(100.0, _keyword_score(lc, _POWER_TERMS, 45.0))
    dignity     = max(5.0, min(100.0, _keyword_score(lc, _DIGNITY_TERMS, 60.0) - harm_penalty))
    surplus     = max(5.0, min(100.0, _keyword_score(lc, _SURPLUS_TERMS, 50.0) - extract_penalty / 2.0))
    synth_raw   = _keyword_score(lc, _SYNTHESIS_TERMS, 50.0)
    synthesis   = min(100.0, synth_raw + (sovereignty + dignity) / 4.0)
    return sovereignty, power, synthesis, dignity, surplus


def _to_triad(sovereignty: float, power: float, synthesis: float, dignity: float):
    jedi = min(100.0, sovereignty * 0.55 + dignity * 0.45)
    sith = power
    grey = min(100.0, synthesis * 0.6 + (jedi + sith) / 2.0 * 0.4)
    return jedi, sith, grey


def _compute_npfm(jedi: float, sith: float, grey: float) -> float:
    """NPFM formula — matches pendragon-claude/NexusSimulation.tsx and forge-cli/src/govern.rs"""
    return (grey / 100.0) * (jedi / 100.0) - (1.0 - sith / 100.0) * 0.5


def _evaluate_protocols(sovereignty: float, power: float, synthesis: float,
                        dignity: float, surplus: float) -> List[ProtocolResult]:
    results = []
    checks = [
        (Protocol.CAAL,                synthesis >= 40.0,                synthesis / 100.0,
         f"Synthesis score: {synthesis:.0f}/100"),
        (Protocol.MissionAllocation,   power >= 20.0,                    min(1.0, power / 80.0),
         f"Power score: {power:.0f}/100"),
        (Protocol.DigitalHabeasCorpus, dignity >= 30.0,                  dignity / 100.0,
         f"Dignity score: {dignity:.0f}/100"),
        (Protocol.LocalFirst,          sovereignty >= 35.0,              sovereignty / 100.0,
         f"Sovereignty score: {sovereignty:.0f}/100"),
        (Protocol.FractalGovernance,   synthesis >= 35.0,                synthesis / 100.0,
         f"Synthesis score: {synthesis:.0f}/100"),
        (Protocol.Clause81,            surplus >= 45.0 and dignity >= 30.0,
         min(1.0, (surplus + dignity) / 200.0),
         f"Surplus: {surplus:.0f}/100, Dignity: {dignity:.0f}/100"),
    ]
    for protocol, compliant, confidence, reasoning in checks:
        results.append(ProtocolResult(protocol, compliant, confidence, reasoning))
    return results


# ── Public API ─────────────────────────────────────────────────────────────

def evaluate(input_text: str) -> GovernanceVerdict:
    """
    Evaluate input text against 6 Pendragon protocols and compute NPFM.
    Pure Python — no external dependencies, no API calls required.

    Args:
        input_text: Any text to constitutionally evaluate (query, proposal, document).

    Returns:
        GovernanceVerdict with NPFM, per-protocol results, and overall Verdict.
    """
    sovereignty, power, synthesis, dignity, surplus = _analyze(input_text)
    jedi, sith, grey = _to_triad(sovereignty, power, synthesis, dignity)
    npfm             = _compute_npfm(jedi, sith, grey)
    protocol_results = _evaluate_protocols(sovereignty, power, synthesis, dignity, surplus)

    violations   = sum(1 for r in protocol_results if not r.compliant)
    if violations == 0:
        verdict = Verdict.Approved
        recommendation = "All 6 Pendragon protocols compliant. Proceed with constitutional confidence."
    elif violations <= 2:
        verdict = Verdict.Conditional
        recommendation = f"{violations} protocol(s) flagged. Review and address before full deployment."
    else:
        verdict = Verdict.Rejected
        recommendation = f"{violations} protocol violations. Constitutional review required."

    return GovernanceVerdict(
        sovereignty=sovereignty, power=power, synthesis=synthesis,
        dignity=dignity,         surplus=surplus,
        jedi=jedi,               sith=sith,  grey=grey,
        npfm=npfm,
        protocol_results=protocol_results,
        verdict=verdict,
        recommendation=recommendation,
    )


def quick_check(input_text: str) -> tuple:
    """Returns (verdict_str, npfm) — fast inline check without full output."""
    v = evaluate(input_text)
    return (v.verdict.value, round(v.npfm, 4))


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "constitutional sovereignty local governance audit transparency"
    v = evaluate(text)
    print(f"NPFM: {v.npfm:+.3f}   Verdict: {v.verdict.value}")
    print(f"Pentagon: SOV={v.sovereignty:.0f} PWR={v.power:.0f} SYN={v.synthesis:.0f} DIG={v.dignity:.0f} SUR={v.surplus:.0f}")
    print()
    for r in v.protocol_results:
        icon = "✓" if r.compliant else "✗"
        print(f"  {icon}  {PROTOCOL_NAMES[r.protocol]:<22}  {r.confidence*100:.0f}%  {r.reasoning}")
    print()
    print(f"Recommendation: {v.recommendation}")
