"""
Element 145 MCP Server — Model Context Protocol Integration
=============================================================
6 MCP tools exposing the full LCP pipeline via stdio JSON-RPC transport.

Tools:
  lattice_ingest   — Map input text to relevant Spheres/Houses
  lattice_activate — Load cross-domain edges between activated Houses
  lattice_route    — Domain-specific analysis for one House
  lattice_synthesize — Element 145 meta-coordination
  lattice_get_house — Get House data with Spheres
  lattice_get_connections — Get inter-House connections

Transport: stdio (JSON-RPC 2.0)
Alternative MCP servers: Any provider can implement these 6 tools.

D-25 COI Disclosure: S4 Microsoft seat built this integration.
Non-Microsoft alternatives: This MCP server works with any MCP-compatible client
(Claude Desktop, Cursor, Windsurf, VS Code, etc.) — not Microsoft-specific.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from element145.core import (
    LCPEngine,
    LatticeOntology,
    AnalysisResult,
    ActivationState,
)

# ═══════════════════════════════════════════════════════════════
# MCP TOOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════

MCP_TOOLS = [
    {
        "name": "lattice_ingest",
        "description": (
            "Map input text to relevant Spheres and Houses in the 144+1 lattice. "
            "First step of the LCP pipeline (INGEST → ACTIVATE → ROUTE → SYNTHESIZE)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Input text to analyze"},
                "min_relevance": {
                    "type": "number", "default": 0.05,
                    "description": "Minimum relevance threshold for sphere activation",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "lattice_activate",
        "description": (
            "Load cross-domain edges between activated Houses. "
            "Must be called after lattice_ingest. Second step of LCP pipeline."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "lattice_route",
        "description": (
            "Get domain-specific analysis for one House, including active Spheres "
            "and cross-domain edges. Must be called after lattice_activate."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Analysis task description"},
                "house_id": {"type": "string", "description": "House ID (H1-H12)"},
            },
            "required": ["task", "house_id"],
        },
    },
    {
        "name": "lattice_synthesize",
        "description": (
            "Element 145 meta-coordination: identify blind spots, cross-domain bridges, "
            "cascade chains, and coherence score. Final step of LCP pipeline."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Analysis task description"},
            },
            "required": ["task"],
        },
    },
    {
        "name": "lattice_get_house",
        "description": "Get House metadata including all 12 Spheres and their keywords.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_id": {"type": "string", "description": "House ID (H1-H12)"},
            },
            "required": ["house_id"],
        },
    },
    {
        "name": "lattice_get_connections",
        "description": "Get all inter-House connections (edges) with types and strengths.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_id": {
                    "type": "string",
                    "description": "Optional: filter connections to this House",
                },
            },
        },
    },
]

# ═══════════════════════════════════════════════════════════════
# MCP SERVER
# ═══════════════════════════════════════════════════════════════

class MCPLatticeServer:
    """MCP server exposing the 144+1 lattice via JSON-RPC 2.0 over stdio."""

    def __init__(self, ontology_path: Optional[str] = None):
        self.engine = LCPEngine(LatticeOntology(ontology_path))

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route a JSON-RPC request to the appropriate handler."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        handlers = {
            "initialize": self._handle_initialize,
            "tools/list": self._handle_tools_list,
            "tools/call": self._handle_tools_call,
        }

        handler = handlers.get(method)
        if handler is None:
            return self._error(req_id, -32601, f"Method not found: {method}")

        try:
            result = handler(params)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        except Exception as e:
            return self._error(req_id, -32000, str(e))

    def _handle_initialize(self, params: Dict) -> Dict:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "element145-lattice",
                "version": "2.0.0",
                "description": (
                    "Sheldonbrain 144+1 Ontological Lattice — "
                    "AI reasoning substrate with Lattice Context Protocol. "
                    "Attribution: All inventions Dave Sheldon's, Atlas Lattice Foundation."
                ),
            },
        }

    def _handle_tools_list(self, params: Dict) -> Dict:
        return {"tools": MCP_TOOLS}

    def _handle_tools_call(self, params: Dict) -> Dict:
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        tool_handlers = {
            "lattice_ingest": self._tool_ingest,
            "lattice_activate": self._tool_activate,
            "lattice_route": self._tool_route,
            "lattice_synthesize": self._tool_synthesize,
            "lattice_get_house": self._tool_get_house,
            "lattice_get_connections": self._tool_get_connections,
        }

        handler = tool_handlers.get(name)
        if handler is None:
            return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                    "isError": True}

        try:
            result = handler(arguments)
            return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}

    # ─── Tool Implementations ─────────────────────────────

    def _tool_ingest(self, args: Dict) -> Dict:
        text = args.get("text", "")
        min_rel = args.get("min_relevance", 0.05)
        state = self.engine.ingest(text, min_rel)
        return {
            "phase": "INGEST",
            "activated_houses": sorted(state.activated_houses),
            "activated_spheres": {
                sid: {"name": self.engine.ontology.spheres[sid].name,
                      "house": self.engine.ontology.spheres[sid].house_id,
                      "relevance": score}
                for sid, score in sorted(state.activated_spheres.items(),
                                         key=lambda x: x[1], reverse=True)
                if sid in self.engine.ontology.spheres
            },
            "house_coverage": f"{state.house_coverage:.0%}",
            "sphere_coverage": f"{state.coverage:.0%}",
        }

    def _tool_activate(self, args: Dict) -> Dict:
        state = self.engine.activate()
        return {
            "phase": "ACTIVATE",
            "active_edges": [
                {"source": e.source, "target": e.target,
                 "type": e.edge_type, "strength": e.strength}
                for e in state.active_edges
            ],
            "total_edges": len(state.active_edges),
            "activated_houses": sorted(state.activated_houses),
        }

    def _tool_route(self, args: Dict) -> Dict:
        task = args.get("task", "")
        house_id = args.get("house_id", "")
        result = self.engine.route(task, house_id)
        result["phase"] = "ROUTE"
        return result

    def _tool_synthesize(self, args: Dict) -> Dict:
        task = args.get("task", "")
        result = self.engine.synthesize(task)
        return {
            "phase": "SYNTHESIZE",
            "task": result.task,
            "activated_houses": result.activated_houses,
            "bridges": result.bridges,
            "blind_spots": result.blind_spots,
            "cascade_chains": result.cascade_chains,
            "coherence_score": result.coherence_score,
            "synthesis_notes": result.synthesis_notes,
        }

    def _tool_get_house(self, args: Dict) -> Dict:
        house_id = args.get("house_id", "")
        hdata = self.engine.ontology.get_house_data(house_id)
        if hdata is None:
            return {"error": f"House {house_id} not found"}
        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        return {
            **hdata,
            "spheres": [
                {"id": s.id, "name": s.name, "index": s.index,
                 "keywords": list(s.keywords)}
                for s in spheres
            ],
            "sphere_count": len(spheres),
        }

    def _tool_get_connections(self, args: Dict) -> Dict:
        house_id = args.get("house_id")
        if house_id:
            edges = self.engine.ontology.get_edges_for_house(house_id)
        else:
            edges = self.engine.ontology.edges
        return {
            "connections": [
                {"source": e.source, "target": e.target,
                 "type": e.edge_type, "strength": e.strength,
                 "description": e.description,
                 "examples": list(e.examples)}
                for e in edges
            ],
            "total": len(edges),
        }

    # ─── Helpers ──────────────────────────────────────────

    @staticmethod
    def _error(req_id: Any, code: int, message: str) -> Dict:
        return {"jsonrpc": "2.0", "id": req_id,
                "error": {"code": code, "message": message}}

    def run_stdio(self):
        """Run the MCP server on stdio (JSON-RPC 2.0, one request per line)."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                response = self._error(None, -32700, "Parse error")
            else:
                response = self.handle_request(request)
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI entry point: element145-mcp"""
    import argparse
    parser = argparse.ArgumentParser(description="Element 145 MCP Server")
    parser.add_argument("--ontology", type=str, default=None,
                        help="Path to lattice_ontology.yaml")
    args = parser.parse_args()
    server = MCPLatticeServer(args.ontology)
    server.run_stdio()


if __name__ == "__main__":
    main()
