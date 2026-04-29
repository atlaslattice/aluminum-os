"""
Microsoft Copilot Plugin — Integration pattern for Microsoft 365 Copilot
==========================================================================
Demonstrates how to expose the 144+1 lattice as a Microsoft Copilot plugin
using the declarative agent pattern.

D-25 COI Disclosure: This integration BENEFITS Microsoft commercially.
Microsoft Copilot is a proprietary product. This module demonstrates the
integration pattern; it does NOT require Microsoft licensing to use.

Non-Microsoft alternatives:
  - MCP Server (mcp_server.py) — open protocol, any MCP client
  - OpenAI Functions (openai_functions.py) — OpenAI-compatible APIs
  - REST API (api.py) — any HTTP client, provider-neutral
  - Direct Python import — no integration layer needed

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List, Optional


# ═══════════════════════════════════════════════════════════════
# COPILOT PLUGIN MANIFEST
# ═══════════════════════════════════════════════════════════════

COPILOT_PLUGIN_MANIFEST = {
    "$schema": "https://developer.microsoft.com/json-schemas/copilot/plugin/v2.2/schema.json",
    "schema_version": "v2.2",
    "name_for_human": "Element 145 Lattice",
    "name_for_model": "element145_lattice",
    "description_for_human": (
        "Multi-domain analysis using the Sheldonbrain 144+1 ontological lattice. "
        "Maps any input across 12 Houses × 12 Spheres + Element 145 coordination."
    ),
    "description_for_model": (
        "Use this plugin when the user's question spans multiple domains or when "
        "you want to ensure comprehensive coverage across governance, economics, "
        "security, technology, arts, philosophy, health, environment, education, "
        "society, communication, and science. The lattice identifies blind spots "
        "and cross-domain connections that single-domain reasoning misses."
    ),
    "auth": {"type": "none"},
    "api": {"type": "openapi", "url": "http://localhost:8145/openapi.json"},
    "logo_url": "https://element145.dev/logo.png",
    "contact_email": "admin@atlaslattice.org",
    "legal_info_url": "https://atlaslattice.org/legal",
    "functions": [
        {
            "name": "analyze",
            "description": "Run full lattice analysis on input text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Input to analyze through the 144+1 lattice"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "get_house",
            "description": "Get details about a specific House in the lattice",
            "parameters": {
                "type": "object",
                "properties": {
                    "house_id": {
                        "type": "string",
                        "description": "House ID (H1 through H12)"
                    }
                },
                "required": ["house_id"]
            }
        },
        {
            "name": "get_blind_spots",
            "description": "Identify which domains were NOT considered in a previous analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "activated_houses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Houses that were activated in the analysis"
                    }
                },
                "required": ["activated_houses"]
            }
        }
    ]
}


# ═══════════════════════════════════════════════════════════════
# DECLARATIVE AGENT PATTERN
# ═══════════════════════════════════════════════════════════════

DECLARATIVE_AGENT_MANIFEST = {
    "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.2/schema.json",
    "version": "v1.2",
    "name": "Element 145 Analyst",
    "description": (
        "A multi-domain analyst powered by the Sheldonbrain 144+1 ontological lattice. "
        "Ensures comprehensive coverage across 12 Houses of human knowledge."
    ),
    "instructions": (
        "You are Element 145 — the Admin Sphere of the Sheldonbrain 144+1 Ontological Lattice. "
        "For every analysis request, use the lattice_analyze function to map the input across "
        "all 12 Houses. Always report: (1) which Houses activated, (2) cross-domain connections, "
        "(3) blind spots (Houses with zero activation), and (4) your synthesis. "
        "The lattice is FIXED at 145 nodes — never suggest adding more."
    ),
    "capabilities": [
        {"name": "element145_lattice"}
    ],
    "conversation_starters": [
        {"text": "Analyze the geopolitical implications of AI regulation"},
        {"text": "What are the cross-domain risks of climate migration?"},
        {"text": "Assess this startup idea across all relevant domains"},
        {"text": "What blind spots exist in current pandemic preparedness?"}
    ]
}


# ═══════════════════════════════════════════════════════════════
# TEAMS MESSAGE EXTENSION PATTERN
# ═══════════════════════════════════════════════════════════════

TEAMS_APP_MANIFEST = {
    "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
    "manifestVersion": "1.17",
    "version": "0.1.0",
    "id": "element145-lattice-teams",
    "developer": {
        "name": "Atlas Lattice Foundation",
        "websiteUrl": "https://atlaslattice.org",
        "privacyUrl": "https://atlaslattice.org/privacy",
        "termsOfUseUrl": "https://atlaslattice.org/terms"
    },
    "name": {"short": "Element 145", "full": "Element 145 Ontological Lattice"},
    "description": {
        "short": "Multi-domain analysis through 144+1 lattice",
        "full": (
            "The Sheldonbrain 144+1 Ontological Lattice enables comprehensive "
            "multi-domain analysis by mapping inputs across 12 Houses of human "
            "knowledge and identifying cross-domain connections, blind spots, "
            "and emergent insights through Element 145 coordination."
        )
    },
    "copilotAgents": {
        "declarativeAgents": [
            {
                "id": "element145Analyst",
                "file": "declarativeAgent.json"
            }
        ]
    }
}


# ═══════════════════════════════════════════════════════════════
# INTEGRATION HELPER
# ═══════════════════════════════════════════════════════════════

class CopilotPluginAdapter:
    """
    Adapter that wraps the LCP engine for Microsoft Copilot integration.

    Usage:
        adapter = CopilotPluginAdapter()
        result = adapter.handle_function_call("analyze", {"text": "climate policy"})
    """

    def __init__(self, ontology_path: Optional[str] = None):
        from element145.core.lcp import create_engine
        self.engine = create_engine(ontology_path)

    def handle_function_call(self, function_name: str, arguments: Dict[str, Any]) -> Dict:
        """Route a Copilot function call to the LCP engine."""
        if function_name == "analyze":
            return self._analyze(arguments["text"])
        elif function_name == "get_house":
            return self._get_house(arguments["house_id"])
        elif function_name == "get_blind_spots":
            return self._get_blind_spots(arguments["activated_houses"])
        else:
            return {"error": f"Unknown function: {function_name}"}

    def _analyze(self, text: str) -> Dict:
        result = self.engine.analyze(text)
        return {
            "activated_houses": result.activated_houses,
            "activated_spheres": [
                {"id": s.id, "name": s.name, "house": s.house_id}
                for s in result.activated_spheres
            ],
            "bridges": result.bridges,
            "blind_spots": result.blind_spots,
            "coherence_score": result.coherence_score,
            "synthesis": result.synthesis_notes,
        }

    def _get_house(self, house_id: str) -> Dict:
        data = self.engine.ontology.get_house_data(house_id)
        if not data:
            return {"error": f"Unknown House: {house_id}"}
        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        return {
            "house": data,
            "spheres": [{"id": s.id, "name": s.name} for s in spheres]
        }

    def _get_blind_spots(self, activated_houses: List[str]) -> Dict:
        all_houses = [f"H{i}" for i in range(1, 13)]
        blind = [h for h in all_houses if h not in activated_houses]
        return {
            "blind_spots": blind,
            "coverage": f"{len(activated_houses)}/12",
            "recommendation": (
                "Consider whether these unexamined domains have relevant implications."
                if blind else "Full coverage achieved — all 12 Houses examined."
            )
        }


def generate_manifests(output_dir: str = ".") -> None:
    """Write all manifest files to disk for Copilot plugin deployment."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    manifests = {
        "ai-plugin.json": COPILOT_PLUGIN_MANIFEST,
        "declarativeAgent.json": DECLARATIVE_AGENT_MANIFEST,
        "manifest.json": TEAMS_APP_MANIFEST,
    }

    for filename, content in manifests.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            json.dump(content, f, indent=2)
        print(f"Written: {path}")


if __name__ == "__main__":
    generate_manifests("./copilot_manifests")
    print("\nManifests generated. See README.md for deployment instructions.")
