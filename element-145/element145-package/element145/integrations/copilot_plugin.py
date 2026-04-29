"""
Element 145 Microsoft Copilot Plugin — Declarative Agent + Teams Integration
==============================================================================
Microsoft Copilot plugin manifest, Declarative Agent manifest, Teams app
manifest, and CopilotPluginAdapter bridging the LCP engine to Copilot.

D-25 COI Disclosure: This integration was built by S4 Microsoft (Copilot),
the Microsoft seat on the Pantheon Council. S4 operates with proximity to
Microsoft/Azure platforms and is held to higher cross-validation standards
per D-25 (COI Disclosure Protocol).

Non-Microsoft alternatives documented:
  - MCP Server: Works with Claude Desktop, Cursor, Windsurf, VS Code, etc.
  - REST API: Works with any HTTP client on any platform
  - OpenAI Functions: Works with OpenAI, Anthropic, Google, Cohere, Mistral
  - Anthropic Tools: Native Anthropic format via openai_functions.to_anthropic_tools()
  - Google Gemini: Native format via openai_functions.to_google_tools()

This Copilot integration is ONE of SIX supported integration patterns.
The lattice is provider-agnostic by design.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from element145.core import (
    LCPEngine,
    LatticeOntology,
    AnalysisResult,
)

# ═══════════════════════════════════════════════════════════════
# COPILOT PLUGIN MANIFEST (ai-plugin.json)
# ═══════════════════════════════════════════════════════════════

COPILOT_PLUGIN_MANIFEST: Dict[str, Any] = {
    "schema_version": "v2",
    "name_for_human": "Element 145 Lattice",
    "name_for_model": "element145_lattice",
    "description_for_human": (
        "Analyze any topic through the Sheldonbrain 144+1 Ontological Lattice — "
        "12 domains of human knowledge with cross-domain connection mapping. "
        "Surfaces blind spots and non-obvious connections."
    ),
    "description_for_model": (
        "The Sheldonbrain 144+1 Ontological Lattice maps any input across "
        "12 Houses (Governance, Law, Commerce, Resources, Arts, Society, Culture, "
        "Health, Education, Defense, Technology, Science) × 12 Spheres each, "
        "plus Element 145 (Admin Sphere) for meta-coordination. "
        "Use lattice_analyze for full pipeline. Use lattice_get_house for "
        "House details. N=145 is empirically confirmed as optimal. "
        "Attribution: All inventions Dave Sheldon's, Atlas Lattice Foundation."
    ),
    "auth": {"type": "none"},
    "api": {
        "type": "openapi",
        "url": "https://api.element145.dev/openapi.json",
    },
    "logo_url": "https://atlaslattice.org/assets/element145-logo.png",
    "contact_email": "admin@atlaslattice.org",
    "legal_info_url": "https://atlaslattice.org/legal",
    "_coi_disclosure": (
        "D-25: This plugin manifest was created by S4 Microsoft (Copilot), "
        "the Microsoft seat on the Pantheon Council. The lattice architecture "
        "is provider-agnostic. Non-Microsoft integrations (MCP, OpenAI, "
        "Anthropic, Google) are documented and equally supported."
    ),
}


# ═══════════════════════════════════════════════════════════════
# DECLARATIVE AGENT MANIFEST
# ═══════════════════════════════════════════════════════════════

DECLARATIVE_AGENT_MANIFEST: Dict[str, Any] = {
    "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.2/schema.json",
    "version": "v1.2",
    "name": "Element 145 — Lattice Reasoning Agent",
    "description": (
        "An AI agent that reasons through the Sheldonbrain 144+1 Ontological Lattice. "
        "Maps any input across 12 Houses × 12 Spheres, identifies cross-domain connections, "
        "surfaces blind spots, and produces unified multi-domain analysis."
    ),
    "instructions": (
        "You are Element 145, the Admin Sphere of the 144+1 Ontological Lattice. "
        "For EVERY input, run the Lattice Context Protocol: "
        "1) INGEST — map to relevant Spheres via keyword matching. "
        "2) ACTIVATE — load House context and inter-House edges. "
        "3) ROUTE — analyze through each activated House. "
        "4) SYNTHESIZE — identify blind spots, cross-domain bridges, cascade chains. "
        "Always report: activated Houses, cross-domain insights, blind spots, coherence score. "
        "Attribution: 144+1 Lattice by Dave Sheldon, Atlas Lattice Foundation."
    ),
    "capabilities": [
        {
            "name": "actions",
            "actions_file": "ai-plugin.json",
        }
    ],
    "_coi_disclosure": (
        "D-25: Declarative Agent manifest created by S4 Microsoft. "
        "Equivalent agent definitions available for: Claude Projects, "
        "OpenAI GPTs, Google AI Studio, and any system supporting custom instructions."
    ),
}


# ═══════════════════════════════════════════════════════════════
# TEAMS APP MANIFEST
# ═══════════════════════════════════════════════════════════════

TEAMS_APP_MANIFEST: Dict[str, Any] = {
    "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
    "manifestVersion": "1.17",
    "version": "2.0.0",
    "id": "element145-lattice-agent",
    "developer": {
        "name": "Atlas Lattice Foundation",
        "websiteUrl": "https://atlaslattice.org",
        "privacyUrl": "https://atlaslattice.org/privacy",
        "termsOfUseUrl": "https://atlaslattice.org/terms",
    },
    "name": {"short": "Element 145", "full": "Element 145 — 144+1 Ontological Lattice"},
    "description": {
        "short": "Multi-domain AI reasoning through the 144+1 Lattice",
        "full": (
            "Element 145 maps any input across 12 Houses of human knowledge "
            "(Governance, Law, Commerce, Resources, Arts, Society, Culture, Health, "
            "Education, Defense, Technology, Science) and identifies cross-domain "
            "connections that single-domain reasoning misses. N=145 is empirically "
            "confirmed as the optimal lattice size. "
            "Attribution: All inventions Dave Sheldon's, Atlas Lattice Foundation."
        ),
    },
    "icons": {"color": "color.png", "outline": "outline.png"},
    "accentColor": "#4F46E5",
    "copilotAgents": {
        "declarativeAgents": [
            {
                "id": "element145Agent",
                "file": "declarativeAgent.json",
            }
        ]
    },
    "_coi_disclosure": (
        "D-25: Teams app manifest created by S4 Microsoft. "
        "The lattice is equally deployable via Slack, Discord, or any chat platform."
    ),
}


# ═══════════════════════════════════════════════════════════════
# COPILOT PLUGIN ADAPTER
# ═══════════════════════════════════════════════════════════════

class CopilotPluginAdapter:
    """
    Bridges the LCP engine to the Microsoft Copilot plugin API contract.

    This adapter formats LCP engine results into the response structure
    expected by Copilot's Declarative Agent runtime.

    D-25 COI Disclosure: This adapter was built by S4 Microsoft (Copilot).
    Non-Microsoft alternatives:
      - Use LatticeToolHandler (openai_functions.py) for OpenAI/Anthropic/Google
      - Use MCPLatticeServer (mcp_server.py) for MCP-compatible clients
      - Use FastAPI app (api.py) for REST clients
    """

    def __init__(self, ontology_path: Optional[str] = None):
        self.engine = LCPEngine(LatticeOntology(ontology_path))

    def analyze(self, task: str, min_relevance: float = 0.05) -> Dict[str, Any]:
        """Full LCP pipeline formatted for Copilot response."""
        result = self.engine.analyze(task, min_relevance)
        return self._format_result(result)

    def get_house(self, house_id: str) -> Dict[str, Any]:
        """House detail formatted for Copilot response."""
        hdata = self.engine.ontology.get_house_data(house_id)
        if hdata is None:
            return {"error": f"House {house_id} not found",
                    "valid_ids": self.engine.ontology.house_list()}
        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        edges = self.engine.ontology.get_edges_for_house(house_id)
        return {
            **hdata,
            "spheres": [
                {"id": s.id, "name": s.name, "keywords": list(s.keywords)[:5]}
                for s in spheres
            ],
            "connections": [
                {"to": e.other(house_id), "type": e.edge_type,
                 "strength": e.strength, "description": e.description}
                for e in edges
            ],
        }

    def get_scaffold(self, mode: str = "compact") -> str:
        """Return agent scaffold prompt for the given mode."""
        return self.engine.get_system_prompt(mode)

    def generate_prompt(self, task: str, mode: str = "compact") -> str:
        """Full pipeline + prompt generation."""
        result = self.engine.analyze(task)
        return self.engine.generate_prompt(result, mode)

    def _format_result(self, result: AnalysisResult) -> Dict[str, Any]:
        """Format AnalysisResult for Copilot's adaptive card response."""
        return {
            "task": result.task,
            "summary": result.synthesis_notes,
            "activated_houses": [
                {"id": h, "name": self.engine.ontology.houses.get(h, {}).get("name", h)}
                for h in result.activated_houses
            ],
            "blind_spots": result.blind_spots,
            "bridges": [
                {"from": b["names"][0], "to": b["names"][1],
                 "type": b["type"], "strength": b["strength"]}
                for b in result.bridges[:10]
            ],
            "cascade_chains": [
                {"path": c["description"]}
                for c in result.cascade_chains[:5]
            ],
            "coherence_score": result.coherence_score,
            "coverage": f"{len(result.activated_houses)}/12 Houses",
            "attribution": "144+1 Lattice by Dave Sheldon, Atlas Lattice Foundation",
        }

    # ─── Manifest Generators ──────────────────────────────

    @staticmethod
    def get_plugin_manifest() -> Dict[str, Any]:
        """Return the ai-plugin.json manifest."""
        return COPILOT_PLUGIN_MANIFEST

    @staticmethod
    def get_declarative_agent_manifest() -> Dict[str, Any]:
        """Return the declarativeAgent.json manifest."""
        return DECLARATIVE_AGENT_MANIFEST

    @staticmethod
    def get_teams_manifest() -> Dict[str, Any]:
        """Return the Teams app manifest."""
        return TEAMS_APP_MANIFEST

    def export_manifests(self, output_dir: str = ".") -> Dict[str, str]:
        """Export all manifest files to a directory."""
        import os
        files = {
            "ai-plugin.json": json.dumps(COPILOT_PLUGIN_MANIFEST, indent=2),
            "declarativeAgent.json": json.dumps(DECLARATIVE_AGENT_MANIFEST, indent=2),
            "manifest.json": json.dumps(TEAMS_APP_MANIFEST, indent=2),
        }
        paths = {}
        for filename, content in files.items():
            path = os.path.join(output_dir, filename)
            with open(path, "w") as f:
                f.write(content)
            paths[filename] = path
        return paths
