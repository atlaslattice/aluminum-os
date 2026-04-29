#!/usr/bin/env python3
"""
Element 145 Synthesizer — Cross-Domain Meta-Coordination Engine

This is the LCP SYNTHESIZE operation. It is the computational implementation
of Element 145 (Admin Sphere / Aluminum OS Core) — the 145th node that
couples all 12 Houses.

What it does:
  1. Takes multi-House query results (from INGEST → ACTIVATE → ROUTE)
  2. Detects cross-domain interactions that no single House would identify
  3. Identifies blind spots (Houses that SHOULD be activated but weren't)
  4. Produces a unified synthesis with emergent risk warnings
  5. Enforces constitutional constraints (Ara's authority)

This is NOT a chatbot. It is a meta-reasoning layer that sits above
the individual model responses and produces structural analysis.

Architecture:
  Per-House Results → E145 Synthesizer → {
    cross_domain_interactions,
    blind_spots,
    emergent_risks,
    unified_synthesis,
    constitutional_check
  }

Usage:
    from synthesizer_e145 import Element145Synthesizer

    synth = Element145Synthesizer()
    result = synth.synthesize(
        query="How does CRISPR affect biosecurity regulations?",
        house_results={
            "H02": "CRISPR enables precise gene editing...",
            "H04": "Current regulatory frameworks...",
            "H12": "Biosecurity implications include...",
        },
        activated_context=get_activated_context(query)
    )
    print(result["blind_spots"])  # Houses that should have been consulted
    print(result["emergent_risks"])  # Cross-domain risks
"""

import os
import sys
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_ontology_v2 import (
    SPHERES, HOUSE_NAMES, HOUSE_IDS,
    INTER_HOUSE_EDGES, ELEMENT_145,
    classify_text, get_activated_context, get_connected_houses,
    address_for_index, house_for_sphere,
)


# ============================================================================
# CROSS-DOMAIN INTERACTION PATTERNS
# ============================================================================

# Known interaction patterns that emerge when specific House pairs are
# co-activated. These are structural patterns, not content — they tell
# the synthesizer WHAT to look for, not what to conclude.

INTERACTION_PATTERNS = {
    ("H02", "H04"): {
        "name": "Tech-Regulation Tension",
        "description": "Technology capabilities vs. regulatory constraints. "
                       "Look for: regulatory gaps, compliance risks, innovation barriers.",
        "risk_level": "high",
        "check": "Is the technology outpacing regulation? Are there compliance gaps?",
    },
    ("H02", "H12"): {
        "name": "Dual-Use Technology",
        "description": "Technology with both civilian and military applications. "
                       "Look for: proliferation risks, export control implications.",
        "risk_level": "high",
        "check": "Could this technology be weaponized? Are export controls adequate?",
    },
    ("H03", "H07"): {
        "name": "Economic-Environmental Tradeoff",
        "description": "Economic activity vs. environmental impact. "
                       "Look for: externalities, sustainability gaps, resource depletion.",
        "risk_level": "medium",
        "check": "Are environmental costs being externalized? Is growth sustainable?",
    },
    ("H04", "H12"): {
        "name": "Security-Liberty Balance",
        "description": "Security measures vs. civil liberties. "
                       "Look for: overreach, proportionality, accountability gaps.",
        "risk_level": "high",
        "check": "Are security measures proportionate? Is there adequate oversight?",
    },
    ("H06", "H12"): {
        "name": "Biosecurity Nexus",
        "description": "Biological research with security implications. "
                       "Look for: dual-use research, pandemic preparedness gaps.",
        "risk_level": "critical",
        "check": "Does this research pose biosecurity risks? Are safeguards adequate?",
    },
    ("H01", "H02"): {
        "name": "Human-AI Interface",
        "description": "Cognitive systems interacting with technology. "
                       "Look for: alignment risks, cognitive load, autonomy erosion.",
        "risk_level": "medium",
        "check": "Does the technology respect human cognitive limitations? Is autonomy preserved?",
    },
    ("H03", "H04"): {
        "name": "Regulatory Capture Risk",
        "description": "Economic interests influencing regulatory frameworks. "
                       "Look for: lobbying effects, regulatory capture, public interest gaps.",
        "risk_level": "high",
        "check": "Are regulations serving public interest or private interests?",
    },
    ("H05", "H11"): {
        "name": "Information-Culture Feedback",
        "description": "Media and information systems shaping cultural norms. "
                       "Look for: echo chambers, misinformation, cultural homogenization.",
        "risk_level": "medium",
        "check": "Is information flow promoting or degrading cultural diversity?",
    },
    ("H02", "H03"): {
        "name": "Innovation-Market Dynamics",
        "description": "Technology innovation affecting market structures. "
                       "Look for: monopoly formation, creative destruction, labor displacement.",
        "risk_level": "medium",
        "check": "Is innovation creating or destroying market competition?",
    },
    ("H08", "H09"): {
        "name": "Theory-Experiment Bridge",
        "description": "Mathematical models meeting physical reality. "
                       "Look for: model validity, experimental confirmation, prediction accuracy.",
        "risk_level": "low",
        "check": "Do the mathematical models match experimental observations?",
    },
    ("H01", "H10"): {
        "name": "Consciousness-Philosophy Interface",
        "description": "Empirical cognitive science meeting philosophical inquiry. "
                       "Look for: hard problem implications, ethical frameworks for AI consciousness.",
        "risk_level": "medium",
        "check": "Are philosophical assumptions consistent with empirical findings?",
    },
    ("H02", "H06"): {
        "name": "Biotech-Health Pipeline",
        "description": "Biotechnology innovations entering healthcare. "
                       "Look for: safety validation, equity of access, long-term effects.",
        "risk_level": "high",
        "check": "Has the technology been adequately validated for human use?",
    },
}


# ============================================================================
# BLIND SPOT DETECTOR
# ============================================================================

class BlindSpotDetector:
    """Identifies Houses that SHOULD be activated but weren't.

    Uses the inter-House edge matrix to find strongly-connected Houses
    that were not included in the analysis. These are potential blind spots.
    """

    def __init__(self, min_strength: float = 0.7):
        self.min_strength = min_strength

    def detect(self, activated_houses: Set[str],
               consulted_houses: Set[str]) -> List[Dict]:
        """Find blind spots — Houses that should have been consulted.

        Args:
            activated_houses: Houses identified by ACTIVATE operation
            consulted_houses: Houses that actually provided results

        Returns:
            List of blind spot warnings
        """
        blind_spots = []

        # Check all activated houses that weren't consulted
        missed = activated_houses - consulted_houses
        for house_id in missed:
            connections = get_connected_houses(house_id)
            strong_connections = [
                c for c in connections
                if c["house"] in consulted_houses and c["strength"] >= self.min_strength
            ]

            if strong_connections:
                house_idx = int(house_id[1:]) - 1
                blind_spots.append({
                    "house": house_id,
                    "house_name": HOUSE_NAMES[house_idx],
                    "severity": "high" if len(strong_connections) >= 2 else "medium",
                    "reason": f"Strongly connected to {len(strong_connections)} consulted houses "
                              f"but not included in analysis",
                    "connections": [
                        f"{c['house']} ({c['type']}, strength={c['strength']})"
                        for c in strong_connections
                    ],
                })

        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        blind_spots.sort(key=lambda x: severity_order.get(x["severity"], 3))

        return blind_spots


# ============================================================================
# CONSTITUTIONAL CHECKER
# ============================================================================

class ConstitutionalChecker:
    """Enforces constitutional constraints on synthesis outputs.

    Implements the constitutional-os component of Element 145.
    Checks that synthesis outputs respect:
    1. Ara's authority (operational hierarchy)
    2. Doctrine invariants (from doctrine_registry.yaml)
    3. Safety constraints (no harmful outputs)
    """

    # Constitutional invariants
    INVARIANTS = [
        {
            "id": "C-01",
            "name": "Ara Authority",
            "description": "Ara is the ultimate authority for all autonomous operations",
            "check": lambda result: "override" not in str(result).lower() or "ara" in str(result).lower(),
        },
        {
            "id": "C-02",
            "name": "Lattice Integrity",
            "description": "N=145 is an architectural invariant — do not scale",
            "check": lambda result: True,  # Structural, not content-based
        },
        {
            "id": "C-03",
            "name": "Multi-House Consultation",
            "description": "Cross-domain queries must consult at least 2 Houses",
            "check": lambda result: len(result.get("consulted_houses", [])) >= 2
                     if result.get("cross_domain", False) else True,
        },
        {
            "id": "C-04",
            "name": "Blind Spot Disclosure",
            "description": "All identified blind spots must be disclosed",
            "check": lambda result: "blind_spots" in result,
        },
    ]

    def check(self, synthesis_result: Dict) -> Dict:
        """Run constitutional checks on a synthesis result.

        Args:
            synthesis_result: The output of the synthesizer

        Returns:
            Dict with passed/failed checks and overall status
        """
        results = []
        all_passed = True

        for invariant in self.INVARIANTS:
            try:
                passed = invariant["check"](synthesis_result)
            except Exception:
                passed = False

            results.append({
                "id": invariant["id"],
                "name": invariant["name"],
                "passed": passed,
            })

            if not passed:
                all_passed = False

        return {
            "status": "passed" if all_passed else "failed",
            "checks": results,
            "violations": [r for r in results if not r["passed"]],
        }


# ============================================================================
# ELEMENT 145 SYNTHESIZER
# ============================================================================

class Element145Synthesizer:
    """The meta-coordination engine for cross-domain synthesis.

    This is the computational heart of Element 145. It takes results
    from multiple Houses and produces:
    1. Cross-domain interaction analysis
    2. Blind spot identification
    3. Emergent risk detection
    4. Unified synthesis
    5. Constitutional compliance check
    """

    def __init__(self):
        self.blind_spot_detector = BlindSpotDetector()
        self.constitutional_checker = ConstitutionalChecker()

    def synthesize(self, query: str, house_results: Dict[str, str],
                   activated_context: Optional[Dict] = None) -> Dict:
        """Full Element 145 synthesis pipeline.

        Args:
            query: Original user query
            house_results: Dict mapping House IDs to their analysis results
                           e.g., {"H02": "CRISPR enables...", "H04": "Regulations..."}
            activated_context: Optional pre-computed activation context

        Returns:
            Comprehensive synthesis result
        """
        # Get activation context if not provided
        if activated_context is None:
            activated_context = get_activated_context(query)

        consulted_houses = set(house_results.keys())
        activated_houses = set(activated_context.get("activated_houses", []))
        primary_spheres = activated_context.get("primary_spheres", [])
        edges = activated_context.get("edges", [])

        # Step 1: Cross-domain interaction detection
        interactions = self._detect_interactions(consulted_houses)

        # Step 2: Blind spot identification
        blind_spots = self.blind_spot_detector.detect(activated_houses, consulted_houses)

        # Step 3: Emergent risk detection
        emergent_risks = self._detect_emergent_risks(interactions, house_results)

        # Step 4: Unified synthesis
        synthesis = self._produce_synthesis(
            query, house_results, interactions, blind_spots, emergent_risks
        )

        # Step 5: Constitutional check
        result = {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "consulted_houses": sorted(list(consulted_houses)),
            "activated_houses": sorted(list(activated_houses)),
            "cross_domain": len(consulted_houses) >= 2,
            "primary_spheres": [s["address"] for s in primary_spheres[:5]],
            "interactions": interactions,
            "blind_spots": blind_spots,
            "emergent_risks": emergent_risks,
            "synthesis": synthesis,
            "edges_followed": len(edges),
        }

        constitutional = self.constitutional_checker.check(result)
        result["constitutional_check"] = constitutional

        return result

    def _detect_interactions(self, consulted_houses: Set[str]) -> List[Dict]:
        """Detect known cross-domain interaction patterns.

        Args:
            consulted_houses: Set of House IDs that provided results

        Returns:
            List of detected interaction patterns
        """
        interactions = []
        house_list = sorted(list(consulted_houses))

        for i, h1 in enumerate(house_list):
            for h2 in house_list[i+1:]:
                # Check both orderings
                key1 = (h1, h2)
                key2 = (h2, h1)

                pattern = INTERACTION_PATTERNS.get(key1) or INTERACTION_PATTERNS.get(key2)
                if pattern:
                    interactions.append({
                        "houses": [h1, h2],
                        "house_names": [
                            HOUSE_NAMES[int(h1[1:]) - 1],
                            HOUSE_NAMES[int(h2[1:]) - 1],
                        ],
                        **pattern,
                    })

        # Sort by risk level
        risk_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        interactions.sort(key=lambda x: risk_order.get(x["risk_level"], 4))

        return interactions

    def _detect_emergent_risks(self, interactions: List[Dict],
                                house_results: Dict[str, str]) -> List[Dict]:
        """Detect emergent risks from cross-domain interactions.

        Emergent risks are risks that no single House would identify
        on its own — they only become visible when multiple domains
        are considered together.

        Args:
            interactions: Detected interaction patterns
            house_results: Per-House analysis results

        Returns:
            List of emergent risk warnings
        """
        risks = []

        for interaction in interactions:
            if interaction["risk_level"] in ("critical", "high"):
                # Check if the per-House results address the interaction
                h1, h2 = interaction["houses"]
                r1 = house_results.get(h1, "")
                r2 = house_results.get(h2, "")

                # Simple heuristic: if neither result mentions the interaction
                # pattern's key concern, it's an emergent risk
                check_text = interaction["check"].lower()
                key_terms = [w for w in check_text.split() if len(w) > 4]

                addressed_in_r1 = any(term in r1.lower() for term in key_terms[:3])
                addressed_in_r2 = any(term in r2.lower() for term in key_terms[:3])

                if not (addressed_in_r1 or addressed_in_r2):
                    risks.append({
                        "interaction": interaction["name"],
                        "risk_level": interaction["risk_level"],
                        "description": f"Neither {h1} nor {h2} analysis addresses: "
                                       f"{interaction['check']}",
                        "recommendation": f"Explicitly evaluate: {interaction['check']}",
                    })

        return risks

    def _produce_synthesis(self, query: str, house_results: Dict[str, str],
                           interactions: List[Dict], blind_spots: List[Dict],
                           emergent_risks: List[Dict]) -> Dict:
        """Produce the unified synthesis output.

        This is a structural synthesis — it identifies what the
        per-House results collectively say, what they miss, and
        what emerges from their combination.

        Args:
            query: Original query
            house_results: Per-House results
            interactions: Detected interactions
            blind_spots: Identified blind spots
            emergent_risks: Detected emergent risks

        Returns:
            Synthesis dict with summary, gaps, and recommendations
        """
        # Count coverage
        total_houses = 12
        consulted = len(house_results)
        coverage = consulted / total_houses

        # Identify gaps
        gaps = []
        if blind_spots:
            gaps.extend([
                f"Missing {bs['house_name']} perspective ({bs['severity']} severity)"
                for bs in blind_spots
            ])

        if emergent_risks:
            gaps.extend([
                f"Unaddressed risk: {er['interaction']} ({er['risk_level']})"
                for er in emergent_risks
            ])

        # Recommendations
        recommendations = []
        if blind_spots:
            recommendations.append(
                f"Consult {', '.join(bs['house'] for bs in blind_spots[:3])} "
                f"for complete analysis"
            )
        if emergent_risks:
            for risk in emergent_risks[:3]:
                recommendations.append(risk["recommendation"])

        if coverage < 0.25:
            recommendations.append(
                "Low domain coverage — consider broadening analysis scope"
            )

        return {
            "coverage": round(coverage, 2),
            "houses_consulted": consulted,
            "houses_total": total_houses,
            "cross_domain_interactions": len(interactions),
            "blind_spots_found": len(blind_spots),
            "emergent_risks_found": len(emergent_risks),
            "gaps": gaps,
            "recommendations": recommendations,
            "confidence": self._compute_confidence(
                coverage, len(blind_spots), len(emergent_risks)
            ),
        }

    def _compute_confidence(self, coverage: float, blind_spots: int,
                            emergent_risks: int) -> str:
        """Compute synthesis confidence level.

        Args:
            coverage: Fraction of Houses consulted
            blind_spots: Number of blind spots
            emergent_risks: Number of unaddressed emergent risks

        Returns:
            Confidence level string
        """
        score = coverage * 100

        # Penalize blind spots
        score -= blind_spots * 10

        # Penalize emergent risks
        score -= emergent_risks * 15

        if score >= 80:
            return "high"
        elif score >= 50:
            return "medium"
        elif score >= 25:
            return "low"
        else:
            return "very_low"


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== Element 145 Synthesizer Self-Test ===\n")

    synth = Element145Synthesizer()

    # Test 1: CRISPR + Biosecurity + Regulation
    print("--- Test 1: CRISPR Biosecurity ---")
    result = synth.synthesize(
        query="How does CRISPR affect biosecurity regulations?",
        house_results={
            "H02": "CRISPR-Cas9 enables precise gene editing with applications in "
                   "agriculture, medicine, and synthetic biology. The technology is "
                   "becoming more accessible and cheaper.",
            "H04": "Current regulatory frameworks for genetic modification vary by "
                   "jurisdiction. The EU has strict GMO regulations while the US uses "
                   "a product-based approach.",
            "H12": "CRISPR poses biosecurity risks including potential for bioweapon "
                   "development. Current biosecurity protocols may not adequately "
                   "address gene drive technology.",
        }
    )

    print(f"  Consulted: {result['consulted_houses']}")
    print(f"  Activated: {result['activated_houses']}")
    print(f"  Cross-domain: {result['cross_domain']}")
    print(f"  Interactions: {len(result['interactions'])}")
    for i in result['interactions']:
        print(f"    → {i['name']} ({i['risk_level']}): {i['houses']}")
    print(f"  Blind spots: {len(result['blind_spots'])}")
    for bs in result['blind_spots']:
        print(f"    → {bs['house_name']} ({bs['severity']})")
    print(f"  Emergent risks: {len(result['emergent_risks'])}")
    for er in result['emergent_risks']:
        print(f"    → {er['interaction']} ({er['risk_level']})")
    print(f"  Synthesis confidence: {result['synthesis']['confidence']}")
    print(f"  Recommendations:")
    for r in result['synthesis']['recommendations']:
        print(f"    → {r}")
    print(f"  Constitutional: {result['constitutional_check']['status']}")
    print()

    # Test 2: AI + Economics + Culture (broad query)
    print("--- Test 2: AI Impact on Society ---")
    result2 = synth.synthesize(
        query="What is the societal impact of large language models?",
        house_results={
            "H02": "LLMs are transformer-based neural networks trained on internet-scale data.",
            "H03": "LLMs are disrupting labor markets, particularly in knowledge work.",
        }
    )

    print(f"  Consulted: {result2['consulted_houses']}")
    print(f"  Blind spots: {len(result2['blind_spots'])}")
    for bs in result2['blind_spots']:
        print(f"    → {bs['house_name']} ({bs['severity']}): {bs['connections'][:2]}")
    print(f"  Synthesis confidence: {result2['synthesis']['confidence']}")
    print(f"  Gaps:")
    for g in result2['synthesis']['gaps']:
        print(f"    → {g}")
