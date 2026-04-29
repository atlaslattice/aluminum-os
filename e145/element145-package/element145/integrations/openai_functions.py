"""
Element 145 OpenAI/Anthropic Tool Schemas — Provider-Agnostic Function Calling
================================================================================
6 tool schemas compatible with OpenAI function calling, Anthropic tool use,
Google Gemini, and any provider following the OpenAI tool schema convention.

Tools:
  lattice_analyze     — Full LCP pipeline
  lattice_ingest      — Map text to Spheres/Houses
  lattice_route       — Domain-specific House analysis
  lattice_synthesize  — Element 145 meta-coordination
  lattice_get_house   — House detail with Spheres
  lattice_search      — Search Spheres by keyword

Includes:
  - OpenAI-format tool schemas
  - Anthropic tool converter
  - LatticeToolHandler for routing calls from any provider

D-25 COI Disclosure: S4 Microsoft seat built this integration.
Non-Microsoft alternatives: These schemas work with OpenAI, Anthropic, Google,
Cohere, Mistral, and any provider supporting JSON Schema tool definitions.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from element145.core import (
    LCPEngine,
    LatticeOntology,
    AnalysisResult,
)

# ═══════════════════════════════════════════════════════════════
# OPENAI TOOL SCHEMAS
# ═══════════════════════════════════════════════════════════════

OPENAI_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "lattice_analyze",
            "description": (
                "Run the full Lattice Context Protocol pipeline on a task: "
                "INGEST → ACTIVATE → ROUTE → SYNTHESIZE. Returns activated Houses, "
                "cross-domain bridges, blind spots, cascade chains, and coherence score. "
                "Uses the Sheldonbrain 144+1 Ontological Lattice (12 Houses × 12 Spheres "
                "+ Element 145 Admin Sphere)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The analysis task, question, or scenario to evaluate",
                    },
                    "min_relevance": {
                        "type": "number",
                        "description": "Minimum relevance threshold for sphere activation (0.0-1.0)",
                        "default": 0.05,
                    },
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_ingest",
            "description": (
                "Map input text to relevant Spheres and Houses in the 144+1 lattice. "
                "Returns which of the 12 Houses and 144 Spheres are activated by the input."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Input text to classify against the lattice",
                    },
                    "min_relevance": {
                        "type": "number",
                        "description": "Minimum relevance threshold (0.0-1.0)",
                        "default": 0.05,
                    },
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_route",
            "description": (
                "Get domain-specific analysis for one House, including its active Spheres "
                "and cross-domain edges to other Houses. Call after lattice_ingest."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Analysis task description",
                    },
                    "house_id": {
                        "type": "string",
                        "description": "House ID (H1 through H12)",
                        "enum": [f"H{i}" for i in range(1, 13)],
                    },
                },
                "required": ["task", "house_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_synthesize",
            "description": (
                "Element 145 meta-coordination: identify blind spots (inactive Houses), "
                "cross-domain bridges, cascade chains, and overall coherence score."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Analysis task description",
                    },
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_get_house",
            "description": (
                "Get detailed information about a House including its 12 Spheres, "
                "keywords, and connections to other Houses."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "house_id": {
                        "type": "string",
                        "description": "House ID (H1 through H12)",
                        "enum": [f"H{i}" for i in range(1, 13)],
                    },
                },
                "required": ["house_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_search",
            "description": (
                "Search for Spheres matching keywords or a topic. Returns matching "
                "Spheres with relevance scores across all 12 Houses."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords or topic description)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        },
    },
]

# ═══════════════════════════════════════════════════════════════
# ANTHROPIC TOOL CONVERTER
# ═══════════════════════════════════════════════════════════════

def to_anthropic_tools(openai_tools: Optional[List[Dict]] = None) -> List[Dict]:
    """
    Convert OpenAI tool schemas to Anthropic tool format.

    Anthropic uses:
      {"name": ..., "description": ..., "input_schema": {...}}
    OpenAI uses:
      {"type": "function", "function": {"name": ..., "description": ..., "parameters": {...}}}
    """
    tools = openai_tools or OPENAI_TOOLS
    anthropic = []
    for tool in tools:
        func = tool.get("function", tool)
        anthropic.append({
            "name": func["name"],
            "description": func["description"],
            "input_schema": func.get("parameters", {"type": "object", "properties": {}}),
        })
    return anthropic


def to_google_tools(openai_tools: Optional[List[Dict]] = None) -> List[Dict]:
    """
    Convert OpenAI tool schemas to Google Gemini function declarations.

    Gemini uses:
      {"function_declarations": [{"name": ..., "description": ..., "parameters": {...}}]}
    """
    tools = openai_tools or OPENAI_TOOLS
    declarations = []
    for tool in tools:
        func = tool.get("function", tool)
        declarations.append({
            "name": func["name"],
            "description": func["description"],
            "parameters": func.get("parameters", {"type": "object", "properties": {}}),
        })
    return [{"function_declarations": declarations}]


# ═══════════════════════════════════════════════════════════════
# TOOL HANDLER
# ═══════════════════════════════════════════════════════════════

class LatticeToolHandler:
    """
    Routes tool calls from any provider to the LCP engine.

    Usage:
        handler = LatticeToolHandler()

        # OpenAI
        result = handler.handle("lattice_analyze", {"task": "climate policy"})

        # Anthropic
        result = handler.handle(tool_use.name, tool_use.input)

        # Generic
        result = handler.handle(function_name, arguments_dict)
    """

    def __init__(self, ontology_path: Optional[str] = None):
        self.engine = LCPEngine(LatticeOntology(ontology_path))

    def handle(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route a tool call to the appropriate handler."""
        handlers: Dict[str, Callable] = {
            "lattice_analyze": self._analyze,
            "lattice_ingest": self._ingest,
            "lattice_route": self._route,
            "lattice_synthesize": self._synthesize,
            "lattice_get_house": self._get_house,
            "lattice_search": self._search,
        }

        handler = handlers.get(tool_name)
        if handler is None:
            return {"error": f"Unknown tool: {tool_name}",
                    "available_tools": list(handlers.keys())}

        return handler(arguments)

    def _analyze(self, args: Dict) -> Dict:
        task = args.get("task", "")
        min_rel = args.get("min_relevance", 0.05)
        result = self.engine.analyze(task, min_rel)
        return {
            "task": result.task,
            "activated_houses": result.activated_houses,
            "activated_sphere_count": len(result.activated_spheres),
            "bridges": result.bridges,
            "blind_spots": result.blind_spots,
            "cascade_chains": result.cascade_chains,
            "coherence_score": result.coherence_score,
            "synthesis_notes": result.synthesis_notes,
            "house_analyses": result.house_analyses,
            "prompt_compact": self.engine.generate_prompt(result, "compact"),
        }

    def _ingest(self, args: Dict) -> Dict:
        text = args.get("text", "")
        min_rel = args.get("min_relevance", 0.05)
        state = self.engine.ingest(text, min_rel)
        return {
            "activated_houses": sorted(state.activated_houses),
            "activated_spheres": {
                sid: {"name": self.engine.ontology.spheres[sid].name,
                      "relevance": score}
                for sid, score in sorted(state.activated_spheres.items(),
                                         key=lambda x: x[1], reverse=True)
                if sid in self.engine.ontology.spheres and score > 0.01
            },
            "house_coverage": state.house_coverage,
        }

    def _route(self, args: Dict) -> Dict:
        return self.engine.route(args.get("task", ""), args.get("house_id", ""))

    def _synthesize(self, args: Dict) -> Dict:
        result = self.engine.synthesize(args.get("task", ""))
        return {
            "blind_spots": result.blind_spots,
            "bridges": result.bridges,
            "cascade_chains": result.cascade_chains,
            "coherence_score": result.coherence_score,
            "synthesis_notes": result.synthesis_notes,
        }

    def _get_house(self, args: Dict) -> Dict:
        house_id = args.get("house_id", "")
        hdata = self.engine.ontology.get_house_data(house_id)
        if hdata is None:
            return {"error": f"House {house_id} not found"}
        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        edges = self.engine.ontology.get_edges_for_house(house_id)
        return {
            **hdata,
            "spheres": [{"id": s.id, "name": s.name, "keywords": list(s.keywords)}
                        for s in spheres],
            "connections": [{"to": e.other(house_id), "type": e.edge_type,
                            "strength": e.strength}
                           for e in edges],
        }

    def _search(self, args: Dict) -> Dict:
        query = args.get("query", "")
        max_results = args.get("max_results", 10)
        results = self.engine.ontology.search_spheres(query)[:max_results]
        return {
            "query": query,
            "results": [
                {"id": s.id, "name": s.name, "house_id": s.house_id,
                 "house_name": s.house_name, "relevance": score,
                 "keywords": list(s.keywords)[:5]}
                for s, score in results
            ],
            "total": len(results),
        }

    @property
    def openai_tools(self) -> List[Dict]:
        return OPENAI_TOOLS

    @property
    def anthropic_tools(self) -> List[Dict]:
        return to_anthropic_tools()

    @property
    def google_tools(self) -> List[Dict]:
        return to_google_tools()
