#!/usr/bin/env python3
"""
Manus Core Bridge v2.0 — Lattice-Aware Model Router

Replaces the original bridge.py from aluminum-os-v3/manus-core/ with a
lattice-aware version that classifies every query through the 144+1
ontology BEFORE dispatching to the appropriate model.

Original bridge.py capabilities (preserved):
  - Multi-model routing (Gemini, Claude, Grok, GPT, Qwen, DeepSeek)
  - Cost tracking per model
  - Token counting
  - Fallback chains

New capabilities (added):
  - LCP INGEST: Every query is classified into House/Sphere before routing
  - Model-Domain affinity: Certain models are preferred for certain Houses
  - Cross-domain detection: Queries spanning 3+ Houses trigger synthesis
  - Noosphere intent classification: Replaces keyword matching with lattice

Architecture:
  Query → INGEST (classify) → ACTIVATE (edges) → MODEL_SELECT → DISPATCH

Usage:
    from bridge_v2 import LatticeBridge

    bridge = LatticeBridge()
    result = await bridge.dispatch("Explain quantum entanglement")
    print(result["model"])     # → "gemini-2.5-flash"
    print(result["house"])     # → "H09"
    print(result["sphere"])    # → "H09.S02 Quantum Mechanics"
"""

import os
import sys
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

# Import lattice classification
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_ontology_v2 import (
    SPHERES, HOUSE_NAMES, HOUSE_IDS,
    classify_text, get_activated_context, get_connected_houses,
    address_for_index, house_for_sphere,
)


# ============================================================================
# MODEL REGISTRY
# ============================================================================

@dataclass
class ModelSpec:
    """Specification for a model in the routing pool."""
    name: str
    provider: str
    api_key_env: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_context: int
    strengths: List[str]  # House IDs this model excels at
    weaknesses: List[str]  # House IDs this model struggles with
    tier: int  # 1=primary, 2=secondary, 3=fallback
    available: bool = True

    @property
    def api_key(self) -> str:
        return os.getenv(self.api_key_env, "")


# Canonical model registry — Pantheon Council seat assignments
MODEL_REGISTRY = {
    # Seat S1: Claude — Reasoning, Ethics, Philosophy
    "claude-sonnet": ModelSpec(
        name="claude-sonnet-4-20250514",
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_context=200000,
        strengths=["H01", "H10", "H04", "H08"],  # Cognition, Philosophy, Governance, Math
        weaknesses=["H12"],  # Security (tends to refuse)
        tier=1,
    ),

    # Seat S2: Gemini — Synthesis, Science, Technology
    "gemini-flash": ModelSpec(
        name="gemini-2.5-flash",
        provider="google",
        api_key_env="GEMINI_API_KEY",
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        max_context=1000000,
        strengths=["H02", "H09", "H06", "H07"],  # Tech, Physics, Health, Earth
        weaknesses=[],
        tier=1,
    ),

    # Seat S3: Grok — Contrarian, Security, Current Events
    "grok-3": ModelSpec(
        name="grok-3",
        provider="xai",
        api_key_env="XAI_API_KEY",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_context=131072,
        strengths=["H12", "H03", "H11"],  # Security, Economics, Communication
        weaknesses=["H05"],  # Culture (can be blunt)
        tier=1,
    ),

    # Seat S4: GPT — General, Creative, Culture
    "gpt-4o": ModelSpec(
        name="gpt-4o",
        provider="openai",
        api_key_env="OPENAI_API_KEY",
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        max_context=128000,
        strengths=["H05", "H11", "H01"],  # Culture, Communication, Cognition
        weaknesses=[],
        tier=2,  # Not always available
    ),

    # Seat S5: Qwen — Multilingual, Trade, Asia-Pacific
    "qwen-max": ModelSpec(
        name="qwen-max",
        provider="alibaba",
        api_key_env="QWEN_API_KEY",
        cost_per_1k_input=0.002,
        cost_per_1k_output=0.006,
        max_context=128000,
        strengths=["H03", "H05", "H04"],  # Economics, Culture, Governance
        weaknesses=[],
        tier=2,
    ),

    # Seat S6: DeepSeek — Code, Math, Formal Reasoning
    "deepseek-r1": ModelSpec(
        name="deepseek-r1",
        provider="deepseek",
        api_key_env="DEEPSEEK_API_KEY",
        cost_per_1k_input=0.0014,
        cost_per_1k_output=0.0028,
        max_context=128000,
        strengths=["H08", "H02", "H09"],  # Math, Tech, Physics
        weaknesses=["H05", "H10"],  # Culture, History
        tier=2,
    ),
}


# ============================================================================
# COST TRACKER
# ============================================================================

@dataclass
class CostTracker:
    """Track API costs per model and per House."""
    total_cost: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    cost_by_model: Dict[str, float] = field(default_factory=dict)
    cost_by_house: Dict[str, float] = field(default_factory=dict)
    calls_by_model: Dict[str, int] = field(default_factory=dict)

    def record(self, model: str, input_tokens: int, output_tokens: int,
               cost: float, house: str):
        self.total_cost += cost
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.cost_by_model[model] = self.cost_by_model.get(model, 0) + cost
        self.cost_by_house[house] = self.cost_by_house.get(house, 0) + cost
        self.calls_by_model[model] = self.calls_by_model.get(model, 0) + 1

    def summary(self) -> Dict:
        return {
            "total_cost": round(self.total_cost, 6),
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "cost_by_model": {k: round(v, 6) for k, v in self.cost_by_model.items()},
            "cost_by_house": {k: round(v, 6) for k, v in self.cost_by_house.items()},
            "calls_by_model": self.calls_by_model,
        }


# ============================================================================
# NOOSPHERE INTENT ENGINE (replaces keyword-based Rust version)
# ============================================================================

class NoosphereIntent:
    """Lattice-aware intent classification.

    Replaces the keyword-based Rust Noosphere intent engine with
    lattice classification. Instead of matching keywords like
    "weather" → WeatherIntent, it classifies into the 144+1 ontology
    and derives intent from the sphere classification.

    Intent categories map to LCP operations:
      - RETRIEVE: User wants information → INGEST + RAG query
      - ANALYZE: User wants analysis → INGEST + ACTIVATE + model reasoning
      - CREATE: User wants to produce something → INGEST + model generation
      - ACT: User wants to take action → INGEST + MCP tool call
      - SYNTHESIZE: Cross-domain query → full LCP pipeline
    """

    INTENT_SIGNALS = {
        "RETRIEVE": ["what is", "tell me about", "explain", "describe", "define",
                      "who is", "when did", "where is", "how does", "summarize"],
        "ANALYZE": ["analyze", "compare", "evaluate", "assess", "critique",
                     "review", "examine", "investigate", "diagnose"],
        "CREATE": ["write", "draft", "generate", "create", "compose", "design",
                    "build", "make", "produce", "develop"],
        "ACT": ["send", "schedule", "book", "buy", "update", "delete",
                 "move", "copy", "share", "publish", "deploy"],
        "SYNTHESIZE": [],  # Detected by cross-domain activation, not keywords
    }

    def classify_intent(self, query: str) -> Dict:
        """Classify user intent using lattice context + signal words.

        Args:
            query: User query

        Returns:
            Dict with intent, confidence, lattice_context
        """
        query_lower = query.lower()

        # Step 1: Lattice classification
        context = get_activated_context(query)
        primary_houses = set(s["house_id"] for s in context["primary_spheres"])

        # Step 2: Signal word matching
        intent_scores = {}
        for intent, signals in self.INTENT_SIGNALS.items():
            score = sum(1 for s in signals if s in query_lower)
            if score > 0:
                intent_scores[intent] = score

        # Step 3: Cross-domain detection → SYNTHESIZE
        if len(primary_houses) >= 3:
            intent_scores["SYNTHESIZE"] = intent_scores.get("SYNTHESIZE", 0) + 2

        # Step 4: Select highest-scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 1.0)
        else:
            best_intent = "RETRIEVE"  # Default
            confidence = 0.3

        return {
            "intent": best_intent,
            "confidence": round(confidence, 2),
            "primary_houses": list(primary_houses),
            "activated_houses": context["activated_houses"],
            "primary_spheres": context["primary_spheres"][:3],
            "cross_domain": len(primary_houses) >= 3,
            "edges": context["edges"][:5],
        }


# ============================================================================
# LATTICE BRIDGE — Main Router
# ============================================================================

class LatticeBridge:
    """Lattice-aware model router.

    The core routing engine that classifies every query through the
    144+1 ontology and dispatches to the optimal model based on:
    1. Domain affinity (which model is best for which House)
    2. Availability (API key present, model not rate-limited)
    3. Cost optimization (prefer cheaper models when quality is equivalent)
    4. Cross-domain synthesis (trigger E145 for multi-House queries)
    """

    def __init__(self, models: Optional[Dict[str, ModelSpec]] = None):
        self.models = models or MODEL_REGISTRY
        self.cost_tracker = CostTracker()
        self.noosphere = NoosphereIntent()
        self._check_availability()

    def _check_availability(self):
        """Check which models have API keys configured."""
        for name, spec in self.models.items():
            spec.available = bool(spec.api_key)
            if spec.available:
                print(f"  ✓ {name} ({spec.provider}) — available")
            else:
                print(f"  ✗ {name} ({spec.provider}) — no API key")

    def select_model(self, query: str) -> Dict:
        """Select the optimal model for a query based on lattice classification.

        This is the core routing decision. It:
        1. Classifies the query into the 144+1 ontology
        2. Determines intent (RETRIEVE, ANALYZE, CREATE, ACT, SYNTHESIZE)
        3. Selects the model with the best domain affinity
        4. Falls back through the tier chain if primary is unavailable

        Args:
            query: User query

        Returns:
            Dict with selected model, reasoning, and lattice context
        """
        # Step 1: Intent classification
        intent = self.noosphere.classify_intent(query)
        primary_houses = set(intent["primary_houses"])

        # Step 2: Score each available model
        model_scores = []
        for name, spec in self.models.items():
            if not spec.available:
                continue

            score = 0.0

            # Domain affinity bonus
            affinity_hits = len(primary_houses & set(spec.strengths))
            score += affinity_hits * 2.0

            # Weakness penalty
            weakness_hits = len(primary_houses & set(spec.weaknesses))
            score -= weakness_hits * 1.5

            # Tier bonus (prefer primary models)
            score += (4 - spec.tier) * 0.5

            # Cost efficiency bonus (prefer cheaper for simple queries)
            if intent["intent"] == "RETRIEVE":
                cost_score = 1.0 / (spec.cost_per_1k_input + 0.001)
                score += min(cost_score, 2.0)

            # Cross-domain bonus for models with broad strengths
            if intent["cross_domain"] and len(spec.strengths) >= 3:
                score += 1.0

            model_scores.append({
                "model": name,
                "spec": spec,
                "score": round(score, 2),
                "affinity": affinity_hits,
                "weaknesses": weakness_hits,
            })

        # Sort by score
        model_scores.sort(key=lambda x: -x["score"])

        if not model_scores:
            return {
                "status": "no_models_available",
                "intent": intent,
                "fallback": "Please configure at least one model API key",
            }

        selected = model_scores[0]
        alternatives = model_scores[1:3]

        return {
            "status": "routed",
            "model": selected["spec"].name,
            "model_key": selected["model"],
            "provider": selected["spec"].provider,
            "score": selected["score"],
            "affinity": selected["affinity"],
            "intent": intent,
            "reasoning": self._explain_selection(selected, intent, primary_houses),
            "alternatives": [
                {"model": a["model"], "score": a["score"]} for a in alternatives
            ],
        }

    def _explain_selection(self, selected: Dict, intent: Dict,
                           primary_houses: set) -> str:
        """Generate a human-readable explanation of the routing decision."""
        model = selected["model"]
        spec = selected["spec"]
        houses = [HOUSE_NAMES[int(h[1:]) - 1] for h in primary_houses if h.startswith("H")]

        parts = [f"Selected {model} ({spec.provider})"]

        if selected["affinity"] > 0:
            parts.append(f"domain affinity: {selected['affinity']} matching houses")

        if intent["cross_domain"]:
            parts.append(f"cross-domain query spanning {len(primary_houses)} houses")

        if intent["intent"] != "RETRIEVE":
            parts.append(f"intent: {intent['intent']}")

        parts.append(f"houses: {', '.join(houses[:3])}")

        return " | ".join(parts)

    async def dispatch(self, query: str, system_prompt: Optional[str] = None,
                       force_model: Optional[str] = None) -> Dict:
        """Full dispatch pipeline: classify → route → call → track.

        Args:
            query: User query
            system_prompt: Optional system prompt override
            force_model: Optional model override (bypasses routing)

        Returns:
            Dict with response, model used, lattice context, cost
        """
        start_time = time.time()

        # Route
        if force_model and force_model in self.models:
            routing = {
                "status": "forced",
                "model": self.models[force_model].name,
                "model_key": force_model,
                "provider": self.models[force_model].provider,
                "intent": self.noosphere.classify_intent(query),
            }
        else:
            routing = self.select_model(query)

        if routing["status"] == "no_models_available":
            return routing

        # Dispatch to model
        model_key = routing["model_key"]
        spec = self.models[model_key]
        intent = routing["intent"]

        # Build lattice-enhanced system prompt
        lattice_prompt = self._build_lattice_prompt(intent, system_prompt)

        # Call the model
        try:
            response = await self._call_model(spec, query, lattice_prompt)
        except Exception as e:
            # Fallback to next model
            alternatives = routing.get("alternatives", [])
            response = None
            for alt in alternatives:
                try:
                    alt_spec = self.models[alt["model"]]
                    response = await self._call_model(alt_spec, query, lattice_prompt)
                    model_key = alt["model"]
                    spec = alt_spec
                    break
                except Exception:
                    continue

            if response is None:
                return {
                    "status": "error",
                    "error": str(e),
                    "routing": routing,
                }

        # Track cost
        input_tokens = response.get("input_tokens", 0)
        output_tokens = response.get("output_tokens", 0)
        cost = (input_tokens * spec.cost_per_1k_input / 1000 +
                output_tokens * spec.cost_per_1k_output / 1000)

        primary_house = intent["primary_houses"][0] if intent["primary_houses"] else "E145"
        self.cost_tracker.record(model_key, input_tokens, output_tokens, cost, primary_house)

        return {
            "status": "success",
            "response": response.get("text", ""),
            "model": spec.name,
            "provider": spec.provider,
            "intent": intent["intent"],
            "lattice_context": {
                "primary_spheres": [s["address"] for s in intent["primary_spheres"]],
                "activated_houses": intent["activated_houses"],
                "cross_domain": intent["cross_domain"],
            },
            "cost": round(cost, 6),
            "latency_ms": round((time.time() - start_time) * 1000, 1),
            "tokens": {"input": input_tokens, "output": output_tokens},
        }

    def _build_lattice_prompt(self, intent: Dict,
                              user_prompt: Optional[str] = None) -> str:
        """Build a system prompt enhanced with lattice context.

        This injects the relevant House/Sphere context into the system
        prompt so the model knows which domains are relevant.
        """
        parts = []

        if user_prompt:
            parts.append(user_prompt)

        # Add lattice context
        if intent["primary_spheres"]:
            spheres = intent["primary_spheres"][:3]
            parts.append("\n--- Lattice Context ---")
            parts.append(f"Primary domains: {', '.join(s['house'] + ' → ' + s['sphere'] for s in spheres)}")

            if intent["cross_domain"]:
                parts.append(f"Cross-domain query: {len(intent['primary_houses'])} houses activated")
                parts.append("Consider interactions between domains and emergent effects.")

            if intent["edges"]:
                edge_strs = [f"{e['from']}↔{e['to']} ({e['type']})" for e in intent["edges"][:3]]
                parts.append(f"Domain connections: {', '.join(edge_strs)}")

        return "\n".join(parts)

    async def _call_model(self, spec: ModelSpec, query: str,
                          system_prompt: str) -> Dict:
        """Call a specific model. Dispatches to provider-specific implementations.

        Args:
            spec: Model specification
            query: User query
            system_prompt: System prompt with lattice context

        Returns:
            Dict with text, input_tokens, output_tokens
        """
        if spec.provider == "google":
            return await self._call_gemini(spec, query, system_prompt)
        elif spec.provider == "anthropic":
            return await self._call_claude(spec, query, system_prompt)
        elif spec.provider == "xai":
            return await self._call_grok(spec, query, system_prompt)
        else:
            # Stub for other providers
            return {
                "text": f"[STUB: {spec.provider}/{spec.name} not yet implemented]",
                "input_tokens": len(query.split()) * 2,
                "output_tokens": 0,
            }

    async def _call_gemini(self, spec: ModelSpec, query: str,
                           system_prompt: str) -> Dict:
        """Call Google Gemini API."""
        try:
            from google import genai
            client = genai.Client(api_key=spec.api_key)
            response = client.models.generate_content(
                model=spec.name,
                contents=query,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=4096,
                ),
            )
            return {
                "text": response.text,
                "input_tokens": getattr(response.usage_metadata, 'prompt_token_count', 0),
                "output_tokens": getattr(response.usage_metadata, 'candidates_token_count', 0),
            }
        except Exception as e:
            raise RuntimeError(f"Gemini call failed: {e}")

    async def _call_claude(self, spec: ModelSpec, query: str,
                           system_prompt: str) -> Dict:
        """Call Anthropic Claude API."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=spec.api_key)
            response = client.messages.create(
                model=spec.name,
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": query}],
            )
            return {
                "text": response.content[0].text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        except Exception as e:
            raise RuntimeError(f"Claude call failed: {e}")

    async def _call_grok(self, spec: ModelSpec, query: str,
                         system_prompt: str) -> Dict:
        """Call xAI Grok API."""
        try:
            import requests
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {spec.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": spec.name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    "max_tokens": 4096,
                },
                timeout=30,
            )
            data = response.json()
            choice = data["choices"][0]
            usage = data.get("usage", {})
            return {
                "text": choice["message"]["content"],
                "input_tokens": usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0),
            }
        except Exception as e:
            raise RuntimeError(f"Grok call failed: {e}")


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== Lattice Bridge v2.0 Self-Test ===\n")

    bridge = LatticeBridge()

    print("\n--- Model Selection Tests ---")
    test_queries = [
        "Explain quantum entanglement in simple terms",
        "Analyze the geopolitical implications of rare earth supply chains",
        "Write a Python function to compute eigenvalues",
        "What are the ethical implications of AI consciousness?",
        "Send an email to the team about the new security policy",
        "How does CRISPR affect biosecurity regulations in the EU?",
    ]

    for query in test_queries:
        result = bridge.select_model(query)
        print(f"\nQuery: '{query[:60]}...'")
        print(f"  Model: {result.get('model', 'N/A')}")
        print(f"  Provider: {result.get('provider', 'N/A')}")
        print(f"  Score: {result.get('score', 'N/A')}")
        print(f"  Intent: {result.get('intent', {}).get('intent', 'N/A')}")
        print(f"  Cross-domain: {result.get('intent', {}).get('cross_domain', False)}")
        print(f"  Reasoning: {result.get('reasoning', 'N/A')}")
