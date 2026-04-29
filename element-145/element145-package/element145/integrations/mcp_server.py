"""
MCP Server — Model Context Protocol integration for the 144+1 Lattice
=======================================================================
Exposes the Lattice Context Protocol as MCP-compatible tools that any
MCP client (Claude Desktop, Cursor, VS Code, etc.) can call.

Six tools exposed:
  lattice_ingest       — Classify input text → activated Spheres/Houses
  lattice_activate     — Load context for activated Spheres + inter-House edges
  lattice_route        — Follow cross-domain edges, build reasoning paths
  lattice_synthesize   — Element 145 meta-coordination (full pipeline)
  lattice_get_house    — Get details for a specific House
  lattice_get_connections — Get all connections for a House

Usage:
  python -m element145.integrations.mcp_server [--port 8145] [--ontology path/to/yaml]

D-25 COI Disclosure: MCP is an open protocol originated by Anthropic. This
implementation is provider-neutral. Alternatives: OpenAI function calling
(see openai_functions.py), REST API (see api.py), direct Python import.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import json
import sys
import os
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# MCP TOOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════

MCP_TOOLS = [
    {
        "name": "lattice_ingest",
        "description": (
            "Classify input text into the Sheldonbrain 144+1 lattice. "
            "Maps keywords to relevant Spheres and Houses. Returns activation map. "
            "Use this as the first step when analyzing any multi-domain input."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Input text to classify across the 12 Houses × 12 Spheres lattice."
                },
                "max_spheres": {
                    "type": "integer",
                    "description": "Maximum number of Spheres to activate. Default 15.",
                    "default": 15
                },
                "min_houses": {
                    "type": "integer",
                    "description": "Minimum number of Houses to activate (auto-expands if below). Default 3.",
                    "default": 3
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "lattice_activate",
        "description": (
            "Load full context for activated Houses and their inter-House connections. "
            "Call after lattice_ingest to get the connection topology for routing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of House IDs to activate (e.g., ['H1', 'H4', 'H8'])."
                },
                "min_strength": {
                    "type": "number",
                    "description": "Minimum connection strength to include. Default 0.3.",
                    "default": 0.3
                }
            },
            "required": ["house_ids"]
        }
    },
    {
        "name": "lattice_route",
        "description": (
            "Follow cross-domain edges between activated Houses to discover "
            "non-obvious reasoning paths. Returns cascade chains and path strengths."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Activated House IDs to route between."
                },
                "max_hops": {
                    "type": "integer",
                    "description": "Maximum routing depth (hops between Houses). Default 3.",
                    "default": 3
                }
            },
            "required": ["house_ids"]
        }
    },
    {
        "name": "lattice_synthesize",
        "description": (
            "Run the full LCP pipeline: INGEST → ACTIVATE → ROUTE → SYNTHESIZE. "
            "Element 145 (Admin Sphere) coordinates cross-domain analysis, identifies "
            "blind spots, contradictions, cascade chains, and emergent connections. "
            "This is the primary tool for multi-domain analysis."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Input text to analyze through the full 144+1 lattice."
                },
                "scaffold_mode": {
                    "type": "string",
                    "enum": ["compact", "orchestrator", "sphere_agent"],
                    "description": "Prompt scaffold to generate. Default 'compact'.",
                    "default": "compact"
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "lattice_get_house",
        "description": (
            "Get detailed information about a specific House: name, description, "
            "all 12 Spheres with keywords, and connections to other Houses."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_id": {
                    "type": "string",
                    "description": "House ID (e.g., 'H1', 'H12')."
                }
            },
            "required": ["house_id"]
        }
    },
    {
        "name": "lattice_get_connections",
        "description": (
            "Get all inter-House connections for a given House. Returns connection "
            "types, strengths, and descriptions for all edges."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "house_id": {
                    "type": "string",
                    "description": "House ID to get connections for (e.g., 'H4')."
                },
                "min_strength": {
                    "type": "number",
                    "description": "Minimum connection strength to include. Default 0.0.",
                    "default": 0.0
                }
            },
            "required": ["house_id"]
        }
    }
]


# ═══════════════════════════════════════════════════════════════
# MCP SERVER HANDLER
# ═══════════════════════════════════════════════════════════════

class LatticeMCPServer:
    """
    MCP Server implementation for the 144+1 Lattice.

    Handles the MCP JSON-RPC protocol over stdio, exposing
    lattice operations as callable tools.
    """

    def __init__(self, ontology_path: Optional[str] = None):
        """
        Initialize the MCP server with lattice engine.

        Parameters
        ----------
        ontology_path : str, optional
            Path to lattice_ontology.yaml. Uses bundled default.
        """
        from element145.core.lcp import create_engine
        self.engine = create_engine(ontology_path)
        self.tools = {t["name"]: t for t in MCP_TOOLS}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a single MCP JSON-RPC request.

        Parameters
        ----------
        request : dict
            MCP request with method, params, id.

        Returns
        -------
        dict
            MCP response.
        """
        method = request.get("method", "")
        req_id = request.get("id")
        params = request.get("params", {})

        if method == "initialize":
            return self._handle_initialize(req_id, params)
        elif method == "tools/list":
            return self._handle_tools_list(req_id)
        elif method == "tools/call":
            return self._handle_tools_call(req_id, params)
        else:
            return self._error(req_id, -32601, f"Method not found: {method}")

    def _handle_initialize(self, req_id: Any, params: Dict) -> Dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "element145-lattice",
                    "version": "0.1.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }

    def _handle_tools_list(self, req_id: Any) -> Dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }

    def _handle_tools_call(self, req_id: Any, params: Dict) -> Dict:
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})

        try:
            result = self._execute_tool(tool_name, tool_args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(result, indent=2)}
                    ]
                }
            }
        except Exception as e:
            return self._error(req_id, -32000, str(e))

    def _execute_tool(self, name: str, args: Dict) -> Dict:
        """Execute a lattice tool and return results."""
        if name == "lattice_ingest":
            return self._tool_ingest(args)
        elif name == "lattice_activate":
            return self._tool_activate(args)
        elif name == "lattice_route":
            return self._tool_route(args)
        elif name == "lattice_synthesize":
            return self._tool_synthesize(args)
        elif name == "lattice_get_house":
            return self._tool_get_house(args)
        elif name == "lattice_get_connections":
            return self._tool_get_connections(args)
        else:
            raise ValueError(f"Unknown tool: {name}")

    # ─── Tool implementations ───────────────────────────────

    def _tool_ingest(self, args: Dict) -> Dict:
        text = args["text"]
        max_spheres = args.get("max_spheres", 15)

        results = self.engine.ontology.search_spheres(text)[:max_spheres]

        activated_spheres = []
        activated_houses = set()
        for sphere, score in results:
            activated_spheres.append({
                "id": sphere.id,
                "name": sphere.name,
                "house": sphere.house_id,
                "score": score
            })
            activated_houses.add(sphere.house_id)

        # Auto-expand if too few houses
        min_houses = args.get("min_houses", 3)
        if len(activated_houses) < min_houses and activated_houses:
            for h_id in list(activated_houses):
                edges = self.engine.ontology.get_edges_for_house(h_id)
                for edge in edges:
                    other = edge.target if edge.source != h_id else edge.source
                    activated_houses.add(other)
                    if len(activated_houses) >= min_houses:
                        break

        return {
            "activated_spheres": activated_spheres,
            "activated_houses": sorted(activated_houses),
            "num_spheres": len(activated_spheres),
            "num_houses": len(activated_houses),
            "blind_spots": [
                f"H{i}" for i in range(1, 13)
                if f"H{i}" not in activated_houses
            ]
        }

    def _tool_activate(self, args: Dict) -> Dict:
        house_ids = args["house_ids"]
        min_strength = args.get("min_strength", 0.3)

        houses = []
        connections = []
        seen_connections = set()

        for h_id in house_ids:
            house_data = self.engine.ontology.get_house_data(h_id)
            if house_data:
                houses.append(house_data)

            edges = self.engine.ontology.get_edges_for_house(h_id)
            for edge in edges:
                if edge.strength >= min_strength:
                    key = tuple(sorted([edge.source, edge.target]))
                    if key not in seen_connections:
                        seen_connections.add(key)
                        connections.append({
                            "source": edge.source,
                            "target": edge.target,
                            "type": edge.connection_type,
                            "strength": edge.strength,
                        })

        return {
            "houses": houses,
            "connections": connections,
            "num_active_connections": len(connections)
        }

    def _tool_route(self, args: Dict) -> Dict:
        house_ids = args["house_ids"]
        max_hops = args.get("max_hops", 3)

        # BFS to find paths between activated houses
        paths = []
        for i, start in enumerate(house_ids):
            for end in house_ids[i+1:]:
                path = self._bfs_path(start, end, max_hops)
                if path:
                    paths.append(path)

        return {
            "routing_paths": paths,
            "num_paths": len(paths)
        }

    def _bfs_path(self, start: str, end: str, max_hops: int) -> Optional[Dict]:
        """BFS shortest path between two Houses."""
        from collections import deque

        queue = deque([(start, [start], 1.0)])
        visited = {start}

        while queue:
            current, path, strength = queue.popleft()

            if current == end:
                return {
                    "from": start,
                    "to": end,
                    "path": path,
                    "hops": len(path) - 1,
                    "total_strength": round(strength, 4)
                }

            if len(path) > max_hops:
                continue

            edges = self.engine.ontology.get_edges_for_house(current)
            for edge in edges:
                neighbor = edge.target if edge.source == current else edge.source
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((
                        neighbor,
                        path + [neighbor],
                        strength * edge.strength
                    ))

        return None

    def _tool_synthesize(self, args: Dict) -> Dict:
        text = args["text"]
        mode = args.get("scaffold_mode", "compact")

        result = self.engine.analyze(text)

        return {
            "activated_houses": [
                {"id": h, "name": self.engine.ontology.houses.get(h, {}).get("name", "")}
                for h in result.activated_houses
            ],
            "activated_spheres": [
                {"id": s.id, "name": s.name, "house": s.house_id}
                for s in result.activated_spheres
            ],
            "bridges": result.bridges,
            "blind_spots": result.blind_spots,
            "cascade_chains": result.cascade_chains,
            "coherence_score": result.coherence_score,
            "element_145_synthesis": result.synthesis_notes,
            "scaffold_prompt": self.engine.generate_prompt(result, mode=mode)
        }

    def _tool_get_house(self, args: Dict) -> Dict:
        house_id = args["house_id"]
        house_data = self.engine.ontology.get_house_data(house_id)
        if not house_data:
            raise ValueError(f"Unknown House: {house_id}")

        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        connections = self.engine.ontology.get_edges_for_house(house_id)

        return {
            "house": house_data,
            "spheres": [{"id": s.id, "name": s.name, "keywords": list(s.keywords)} for s in spheres],
            "connections": [
                {
                    "to": e.target if e.source == house_id else e.source,
                    "type": e.connection_type,
                    "strength": e.strength
                }
                for e in connections
            ]
        }

    def _tool_get_connections(self, args: Dict) -> Dict:
        house_id = args["house_id"]
        min_strength = args.get("min_strength", 0.0)

        connections = self.engine.ontology.get_edges_for_house(house_id)
        filtered = [
            {
                "source": e.source,
                "target": e.target,
                "type": e.connection_type,
                "strength": e.strength,
            }
            for e in connections
            if e.strength >= min_strength
        ]

        return {
            "house_id": house_id,
            "connections": filtered,
            "num_connections": len(filtered)
        }

    def _error(self, req_id: Any, code: int, message: str) -> Dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message}
        }

    # ─── Stdio transport ────────────────────────────────────

    def run_stdio(self):
        """Run the MCP server over stdio (standard MCP transport)."""
        print(json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }), flush=True)

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_resp = self._error(None, -32700, "Parse error")
                print(json.dumps(error_resp), flush=True)


# ═══════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    """Run the Element 145 MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Element 145 Lattice MCP Server")
    parser.add_argument("--ontology", type=str, default=None,
                        help="Path to lattice_ontology.yaml")
    parser.add_argument("--transport", choices=["stdio"], default="stdio",
                        help="Transport protocol (currently only stdio)")
    args = parser.parse_args()

    server = LatticeMCPServer(ontology_path=args.ontology)

    if args.transport == "stdio":
        server.run_stdio()


if __name__ == "__main__":
    main()
