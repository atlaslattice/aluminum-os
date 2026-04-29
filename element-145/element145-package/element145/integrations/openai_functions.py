"""
OpenAI Function Calling — Schema definitions for the 144+1 Lattice
====================================================================
Provides OpenAI-compatible function/tool definitions that can be passed
directly to the OpenAI Chat Completions API (or any compatible provider).

Usage:
  from element145.integrations.openai_functions import OPENAI_TOOLS, handle_tool_call
  
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[...],
      tools=OPENAI_TOOLS,
  )

D-25 COI Disclosure: OpenAI is a Microsoft portfolio company (nonexclusive
license through 2032 per April 27, 2026 renegotiation). Azure OpenAI
Enterprise Agreement operates under Microsoft commercial terms.

Non-Microsoft alternatives for function calling:
  - Anthropic Claude: Tool use API (tools parameter)
  - Google Gemini: Function calling API
  - Mistral: Tool use API
  - Any MCP-compatible client: Use mcp_server.py instead

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List, Optional


# ═══════════════════════════════════════════════════════════════
# OPENAI TOOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════

OPENAI_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "lattice_analyze",
            "description": (
                "Run the full Lattice Context Protocol pipeline on input text. "
                "Maps the input across the Sheldonbrain 144+1 ontological lattice "
                "(12 Houses × 12 Spheres + Element 145 Admin Sphere). Returns "
                "activated Houses/Spheres, cross-domain connections, blind spots, "
                "cascade chains, and coherence score. Use this for any multi-domain "
                "analysis task."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The input text to analyze through the 144+1 lattice."
                    },
                    "scaffold_mode": {
                        "type": "string",
                        "enum": ["compact", "orchestrator", "sphere_agent"],
                        "description": "Prompt scaffold mode. 'compact' (~800 tokens), 'orchestrator' (~2000 tokens), 'sphere_agent' (~400 tokens per House).",
                        "default": "compact"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_ingest",
            "description": (
                "Classify input text into relevant Spheres and Houses without "
                "running the full synthesis pipeline. Lightweight — use for quick "
                "domain mapping."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Input text to classify."
                    },
                    "max_spheres": {
                        "type": "integer",
                        "description": "Maximum number of Spheres to return.",
                        "default": 15
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_get_house",
            "description": (
                "Get detailed information about a specific House in the lattice, "
                "including all 12 Spheres with keywords and inter-House connections."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "house_id": {
                        "type": "string",
                        "description": "House ID: H1 (Governance), H2 (Economics), H3 (Security), H4 (Technology), H5 (Arts), H6 (Philosophy), H7 (Health), H8 (Environment), H9 (Education), H10 (Society), H11 (Communication), H12 (Science)."
                    }
                },
                "required": ["house_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_get_connections",
            "description": (
                "Get all inter-House connections for a given House. Returns typed, "
                "weighted edges showing how domains relate to each other."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "house_id": {
                        "type": "string",
                        "description": "House ID to query connections for."
                    },
                    "min_strength": {
                        "type": "number",
                        "description": "Minimum connection strength to include (0.0-1.0).",
                        "default": 0.0
                    }
                },
                "required": ["house_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_blind_spots",
            "description": (
                "Given a list of activated Houses, identify which Houses were NOT "
                "considered. Element 145's blind spot detection."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "activated_houses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of House IDs that were activated in analysis."
                    }
                },
                "required": ["activated_houses"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lattice_route",
            "description": (
                "Find cross-domain reasoning paths between activated Houses. "
                "Returns cascade chains showing how insights propagate across "
                "the lattice topology."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source_house": {
                        "type": "string",
                        "description": "Starting House ID."
                    },
                    "target_house": {
                        "type": "string",
                        "description": "Destination House ID."
                    },
                    "max_hops": {
                        "type": "integer",
                        "description": "Maximum number of intermediate Houses.",
                        "default": 3
                    }
                },
                "required": ["source_house", "target_house"]
            }
        }
    }
]


# ═══════════════════════════════════════════════════════════════
# ANTHROPIC CLAUDE TOOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════

def get_anthropic_tools() -> List[Dict[str, Any]]:
    """
    Convert to Anthropic Claude tool format.

    Returns tool definitions compatible with the Anthropic Messages API.
    """
    tools = []
    for openai_tool in OPENAI_TOOLS:
        func = openai_tool["function"]
        tools.append({
            "name": func["name"],
            "description": func["description"],
            "input_schema": func["parameters"]
        })
    return tools


# ═══════════════════════════════════════════════════════════════
# TOOL CALL HANDLER
# ═══════════════════════════════════════════════════════════════

class LatticeToolHandler:
    """
    Handles function/tool calls from any LLM provider.

    Usage:
        handler = LatticeToolHandler()

        # OpenAI
        tool_call = response.choices[0].message.tool_calls[0]
        result = handler.handle(tool_call.function.name,
                                json.loads(tool_call.function.arguments))

        # Anthropic
        tool_use = response.content[0]  # ToolUseBlock
        result = handler.handle(tool_use.name, tool_use.input)
    """

    def __init__(self, ontology_path: Optional[str] = None):
        from element145.core.lcp import create_engine
        self.engine = create_engine(ontology_path)

    def handle(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a tool call to the appropriate handler.

        Parameters
        ----------
        function_name : str
            Name of the function being called.
        arguments : dict
            Function arguments.

        Returns
        -------
        dict
            Tool result to send back to the LLM.
        """
        handlers = {
            "lattice_analyze": self._analyze,
            "lattice_ingest": self._ingest,
            "lattice_get_house": self._get_house,
            "lattice_get_connections": self._get_connections,
            "lattice_blind_spots": self._blind_spots,
            "lattice_route": self._route,
        }

        handler = handlers.get(function_name)
        if handler is None:
            return {"error": f"Unknown function: {function_name}"}

        try:
            return handler(arguments)
        except Exception as e:
            return {"error": str(e)}

    def _analyze(self, args: Dict) -> Dict:
        result = self.engine.analyze(args["text"])
        mode = args.get("scaffold_mode", "compact")
        prompt = self.engine.generate_prompt(result, mode=mode)

        return {
            "activated_houses": result.activated_houses,
            "activated_spheres": [
                {"id": s.id, "name": s.name, "house": s.house_id}
                for s in result.activated_spheres
            ],
            "bridges": result.bridges,
            "blind_spots": result.blind_spots,
            "cascade_chains": result.cascade_chains,
            "coherence_score": result.coherence_score,
            "synthesis": result.synthesis_notes,
            "prompt": prompt,
        }

    def _ingest(self, args: Dict) -> Dict:
        max_spheres = args.get("max_spheres", 15)
        results = self.engine.ontology.search_spheres(args["text"])[:max_spheres]

        houses = set()
        spheres = []
        for sphere, score in results:
            spheres.append({"id": sphere.id, "name": sphere.name,
                          "house": sphere.house_id, "score": score})
            houses.add(sphere.house_id)

        return {
            "activated_spheres": spheres,
            "activated_houses": sorted(houses),
            "blind_spots": [f"H{i}" for i in range(1, 13) if f"H{i}" not in houses],
        }

    def _get_house(self, args: Dict) -> Dict:
        house_id = args["house_id"]
        data = self.engine.ontology.get_house_data(house_id)
        if not data:
            return {"error": f"Unknown House: {house_id}"}

        spheres = self.engine.ontology.get_spheres_for_house(house_id)
        return {
            "house": data,
            "spheres": [{"id": s.id, "name": s.name, "keywords": list(s.keywords)}
                       for s in spheres],
        }

    def _get_connections(self, args: Dict) -> Dict:
        house_id = args["house_id"]
        min_str = args.get("min_strength", 0.0)
        edges = self.engine.ontology.get_edges_for_house(house_id)

        return {
            "house_id": house_id,
            "connections": [
                {"source": e.source, "target": e.target,
                 "type": e.connection_type, "strength": e.strength}
                for e in edges if e.strength >= min_str
            ],
        }

    def _blind_spots(self, args: Dict) -> Dict:
        activated = set(args["activated_houses"])
        all_houses = {f"H{i}" for i in range(1, 13)}
        blind = sorted(all_houses - activated)

        return {
            "blind_spots": blind,
            "coverage": f"{len(activated)}/12",
            "coverage_pct": round(len(activated) / 12 * 100, 1),
        }

    def _route(self, args: Dict) -> Dict:
        source = args["source_house"]
        target = args["target_house"]
        max_hops = args.get("max_hops", 3)

        # BFS path finding
        from collections import deque
        queue = deque([(source, [source], 1.0)])
        visited = {source}

        while queue:
            current, path, strength = queue.popleft()
            if current == target:
                return {
                    "path": path,
                    "hops": len(path) - 1,
                    "cumulative_strength": round(strength, 4),
                }
            if len(path) > max_hops + 1:
                continue

            for edge in self.engine.ontology.get_edges_for_house(current):
                neighbor = edge.target if edge.source == current else edge.source
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], strength * edge.strength))

        return {"path": None, "error": f"No path found from {source} to {target} within {max_hops} hops"}


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE: OPENAI INTEGRATION EXAMPLE
# ═══════════════════════════════════════════════════════════════

OPENAI_USAGE_EXAMPLE = '''
# Example: Using Element 145 with OpenAI Chat Completions
# D-25: OpenAI is a Microsoft portfolio company

import openai
import json
from element145.integrations.openai_functions import OPENAI_TOOLS, LatticeToolHandler

client = openai.OpenAI()
handler = LatticeToolHandler()

messages = [
    {"role": "system", "content": "You are an analyst using the 144+1 ontological lattice."},
    {"role": "user", "content": "Analyze the implications of AI regulation on global trade."}
]

# First call — model decides to use lattice tools
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=OPENAI_TOOLS,
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = handler.handle(tool_call.function.name, args)
        messages.append({"role": "tool", "tool_call_id": tool_call.id,
                         "content": json.dumps(result)})
    
    # Second call with tool results
    final = client.chat.completions.create(
        model="gpt-4o", messages=messages, tools=OPENAI_TOOLS,
    )
    print(final.choices[0].message.content)
'''

ANTHROPIC_USAGE_EXAMPLE = '''
# Example: Using Element 145 with Anthropic Claude
# Provider-neutral alternative to OpenAI

import anthropic
from element145.integrations.openai_functions import get_anthropic_tools, LatticeToolHandler

client = anthropic.Anthropic()
handler = LatticeToolHandler()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="You are an analyst using the 144+1 ontological lattice.",
    messages=[{"role": "user", "content": "Analyze climate migration risks."}],
    tools=get_anthropic_tools(),
)

# Handle tool use blocks
for block in response.content:
    if block.type == "tool_use":
        result = handler.handle(block.name, block.input)
        # Continue conversation with tool result...
'''


if __name__ == "__main__":
    print("OpenAI Tool Definitions:")
    print(json.dumps(OPENAI_TOOLS, indent=2))
    print(f"\n{len(OPENAI_TOOLS)} tools defined.")
    print("\nAnthropic Tool Definitions:")
    print(json.dumps(get_anthropic_tools(), indent=2))
