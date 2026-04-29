#!/usr/bin/env python3
"""
ontological_scaffold_experiment.py — A/B/C Ontological Scaffolding Test
=======================================================================
Tests whether the 144+1 ontological lattice improves AI reasoning performance.

Condition A: Baseline (no scaffold)
Condition B: 144+1 Lattice (12 Houses × 12 Spheres + Element 145)
Condition C: Alternative scaffold (flat 145-category list, same granularity, no structure)

Task: Geopolitical scenario analysis — complex enough to show differences across domains.
Test subject: Gemini (via API)
Blind evaluator: Claude (via API)

Metrics: Coverage, Cross-domain connections, Coherence, Completeness, Actionability
"""

import os
import json
import time

# ============================================================
# §1 — THE TASK (identical across all three conditions)
# ============================================================

TASK = """Analyze the following geopolitical scenario and provide a comprehensive assessment:

SCENARIO: In 2027, a major earthquake (magnitude 8.2) strikes Istanbul, Turkey, causing catastrophic damage to critical infrastructure including the Bosphorus Bridge, major ports, and energy pipelines. Turkey declares a state of emergency. The earthquake occurs during a period of heightened tensions between NATO and Russia over Black Sea access, and while Turkey is in the middle of negotiating EU accession terms.

Provide a comprehensive multi-domain analysis covering all relevant dimensions of this crisis. For each domain you analyze, explain the specific impacts, second-order effects, cross-domain interactions, and recommended responses. Be as thorough and specific as possible."""


# ============================================================
# §2 — THE SCAFFOLDS
# ============================================================

SCAFFOLD_B_LATTICE = """Before analyzing, organize your reasoning using the following 12×12+1 ontological framework. Each "House" represents a major domain, and each contains 12 specialized "Spheres." Element 145 (Admin Sphere) serves as the meta-coordination layer that identifies cross-domain interactions.

THE 12 HOUSES:
H01 — Consciousness & Cognition: perception, attention, memory, reasoning, emotion, language, learning, creativity, metacognition, social cognition, altered states, development
H02 — Technology & Engineering: computing, networking, energy systems, materials, manufacturing, robotics, biotech, aerospace, civil engineering, environmental tech, quantum tech, AI/ML
H03 — Economics & Finance: microeconomics, macroeconomics, monetary policy, trade, labor markets, financial markets, development economics, behavioral economics, public finance, inequality, innovation economics, environmental economics
H04 — Governance & Law: constitutional law, international law, regulatory frameworks, human rights, criminal justice, administrative law, electoral systems, federalism, treaty law, maritime law, cyber law, indigenous rights
H05 — Culture & Society: anthropology, sociology, media studies, education, religion, arts, linguistics, gender studies, migration, urban studies, sports/recreation, food culture
H06 — Health & Biology: anatomy, genetics, immunology, neuroscience, pharmacology, epidemiology, ecology, evolution, microbiology, nutrition, mental health, public health
H07 — Earth & Environment: geology, meteorology, oceanography, ecology, climate science, hydrology, soil science, atmospheric chemistry, natural hazards, conservation, resource management, planetary science
H08 — Mathematics & Logic: algebra, geometry, analysis, probability, statistics, number theory, topology, combinatorics, logic, computation theory, optimization, applied mathematics
H09 — Physics & Chemistry: classical mechanics, quantum mechanics, thermodynamics, electromagnetism, relativity, nuclear physics, organic chemistry, inorganic chemistry, physical chemistry, materials science, optics, particle physics
H10 — History & Philosophy: ancient history, medieval history, modern history, philosophy of mind, ethics, epistemology, political philosophy, aesthetics, philosophy of science, historiography, comparative religion, existentialism
H11 — Communication & Information: journalism, rhetoric, information theory, library science, data science, cryptography, semiotics, public relations, advertising, telecommunications, archival science, knowledge management
H12 — Security & Defense: military strategy, intelligence analysis, cybersecurity, counterterrorism, nuclear deterrence, maritime security, space security, biosecurity, critical infrastructure protection, conflict resolution, peacekeeping, arms control

ELEMENT 145 — ADMIN SPHERE (Meta-Coordination):
After analyzing each relevant House, use this coordination layer to:
1. Map cross-domain interactions (which Houses affect which other Houses)
2. Identify emergent risks that only appear at domain intersections
3. Synthesize a unified response strategy that accounts for all domains simultaneously
4. Flag blind spots — domains that seem irrelevant but may have hidden second-order effects

Structure your analysis by House, then provide the Element 145 synthesis."""


SCAFFOLD_C_FLAT = """Before analyzing, organize your reasoning using the following 145-category framework. Cover each relevant category in your analysis:

CATEGORIES:
1. Perception 2. Attention 3. Memory 4. Reasoning 5. Emotion 6. Language processing 7. Learning 8. Creativity 9. Metacognition 10. Social cognition 11. Altered states 12. Development
13. Computing 14. Networking 15. Energy systems 16. Materials 17. Manufacturing 18. Robotics 19. Biotech 20. Aerospace 21. Civil engineering 22. Environmental tech 23. Quantum tech 24. AI/ML
25. Microeconomics 26. Macroeconomics 27. Monetary policy 28. Trade 29. Labor markets 30. Financial markets 31. Development economics 32. Behavioral economics 33. Public finance 34. Inequality 35. Innovation economics 36. Environmental economics
37. Constitutional law 38. International law 39. Regulatory frameworks 40. Human rights 41. Criminal justice 42. Administrative law 43. Electoral systems 44. Federalism 45. Treaty law 46. Maritime law 47. Cyber law 48. Indigenous rights
49. Anthropology 50. Sociology 51. Media studies 52. Education 53. Religion 54. Arts 55. Linguistics 56. Gender studies 57. Migration 58. Urban studies 59. Sports/recreation 60. Food culture
61. Anatomy 62. Genetics 63. Immunology 64. Neuroscience 65. Pharmacology 66. Epidemiology 67. Ecology 68. Evolution 69. Microbiology 70. Nutrition 71. Mental health 72. Public health
73. Geology 74. Meteorology 75. Oceanography 76. Ecology 77. Climate science 78. Hydrology 79. Soil science 80. Atmospheric chemistry 81. Natural hazards 82. Conservation 83. Resource management 84. Planetary science
85. Algebra 86. Geometry 87. Analysis 88. Probability 89. Statistics 90. Number theory 91. Topology 92. Combinatorics 93. Logic 94. Computation theory 95. Optimization 96. Applied mathematics
97. Classical mechanics 98. Quantum mechanics 99. Thermodynamics 100. Electromagnetism 101. Relativity 102. Nuclear physics 103. Organic chemistry 104. Inorganic chemistry 105. Physical chemistry 106. Materials science 107. Optics 108. Particle physics
109. Ancient history 110. Medieval history 111. Modern history 112. Philosophy of mind 113. Ethics 114. Epistemology 115. Political philosophy 116. Aesthetics 117. Philosophy of science 118. Historiography 119. Comparative religion 120. Existentialism
121. Journalism 122. Rhetoric 123. Information theory 124. Library science 125. Data science 126. Cryptography 127. Semiotics 128. Public relations 129. Advertising 130. Telecommunications 131. Archival science 132. Knowledge management
133. Military strategy 134. Intelligence analysis 135. Cybersecurity 136. Counterterrorism 137. Nuclear deterrence 138. Maritime security 139. Space security 140. Biosecurity 141. Critical infrastructure protection 142. Conflict resolution 143. Peacekeeping 144. Arms control
145. Meta-coordination and synthesis

Structure your analysis by covering all relevant categories, then provide a synthesis under category 145."""


# ============================================================
# §3 — EVALUATION RUBRIC (for blind evaluator)
# ============================================================

EVALUATION_PROMPT = """You are an expert evaluator assessing the quality of geopolitical scenario analyses. You will be given three analyses (labeled X, Y, Z) of the same scenario. You do NOT know which methodology produced which analysis. Score each on the following dimensions using a 1-10 scale:

1. **Coverage** (1-10): How many relevant domains does the analysis touch? Does it miss obvious areas?
2. **Cross-Domain Connections** (1-10): Does the analysis identify non-obvious interactions between different domains? (e.g., how an earthquake affects financial markets which affects refugee flows which affects EU politics)
3. **Depth** (1-10): Within each domain covered, how specific and detailed is the analysis?
4. **Coherence** (1-10): Does the analysis hold together as a unified assessment, or is it a disconnected list?
5. **Actionability** (1-10): Could a decision-maker act on this analysis? Are recommendations specific and prioritized?
6. **Blind Spots** (1-10): Does the analysis identify non-obvious risks or domains that others might miss?

For each analysis (X, Y, Z), provide:
- Scores for all 6 dimensions
- A brief justification for each score
- An overall ranking (1st, 2nd, 3rd)

IMPORTANT: Do NOT try to guess which methodology produced which analysis. Judge purely on output quality.

THE SCENARIO:
{scenario}

ANALYSIS X:
{analysis_x}

ANALYSIS Y:
{analysis_y}

ANALYSIS Z:
{analysis_z}

Provide your evaluation in the following JSON format:
{{
  "X": {{"coverage": N, "cross_domain": N, "depth": N, "coherence": N, "actionability": N, "blind_spots": N, "total": N, "justification": "..."}},
  "Y": {{"coverage": N, "cross_domain": N, "depth": N, "coherence": N, "actionability": N, "blind_spots": N, "total": N, "justification": "..."}},
  "Z": {{"coverage": N, "cross_domain": N, "depth": N, "coherence": N, "actionability": N, "blind_spots": N, "total": N, "justification": "..."}},
  "ranking": ["best_label", "middle_label", "worst_label"],
  "evaluator_notes": "..."
}}"""


# ============================================================
# §4 — API CALLS
# ============================================================

def call_test_model(prompt: str, retries: int = 3) -> str:
    """Call Claude Haiku as test subject (fast, cheap, good for A/B testing)."""
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    for attempt in range(retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"    [Attempt {attempt+1}/{retries}] Error: {e}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
    
    raise RuntimeError("Test model failed after retries")


def call_evaluator(prompt: str, retries: int = 3) -> str:
    """Call Grok as blind evaluator (different model family from test subject)."""
    import requests
    
    api_key = os.environ["XAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-3-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 4096,
                    "temperature": 0.3,
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"    [Eval attempt {attempt+1}/{retries}] Error: {e}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
    
    # Fallback to Claude if Grok fails for evaluation
    print("    [Falling back to Claude for evaluation]")
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# ============================================================
# §5 — MAIN EXPERIMENT
# ============================================================

def main():
    print("=" * 70)
    print("A/B/C ONTOLOGICAL SCAFFOLDING EXPERIMENT")
    print("=" * 70)
    print()
    print("Task: Geopolitical scenario analysis (Istanbul earthquake 2027)")
    print("Test subject: Claude Sonnet 4")
    print("Blind evaluator: Grok 3 Mini (fallback: Claude Sonnet 4)")
    print()
    
    results = {}
    
    # --- Condition A: Baseline ---
    print("--- Condition A: Baseline (no scaffold) ---")
    t0 = time.time()
    prompt_a = TASK
    response_a = call_test_model(prompt_a)
    elapsed_a = time.time() - t0
    results["A"] = {"response": response_a, "elapsed": elapsed_a, "condition": "baseline"}
    print(f"  Received {len(response_a)} chars in {elapsed_a:.1f}s")
    
    # --- Condition B: 144+1 Lattice ---
    print("--- Condition B: 144+1 Lattice scaffold ---")
    t0 = time.time()
    prompt_b = SCAFFOLD_B_LATTICE + "\n\n" + TASK
    response_b = call_test_model(prompt_b)
    elapsed_b = time.time() - t0
    results["B"] = {"response": response_b, "elapsed": elapsed_b, "condition": "144+1_lattice"}
    print(f"  Received {len(response_b)} chars in {elapsed_b:.1f}s")
    
    # --- Condition C: Flat 145-category list ---
    print("--- Condition C: Flat 145-category scaffold ---")
    t0 = time.time()
    prompt_c = SCAFFOLD_C_FLAT + "\n\n" + TASK
    response_c = call_test_model(prompt_c)
    elapsed_c = time.time() - t0
    results["C"] = {"response": response_c, "elapsed": elapsed_c, "condition": "flat_145_list"}
    print(f"  Received {len(response_c)} chars in {elapsed_c:.1f}s")
    
    print()
    
    # --- Randomize labels for blind evaluation ---
    import random
    random.seed(42)
    conditions = ["A", "B", "C"]
    labels = ["X", "Y", "Z"]
    random.shuffle(conditions)
    label_map = dict(zip(labels, conditions))
    reverse_map = {v: k for k, v in label_map.items()}
    
    print(f"  Blind label mapping (hidden from evaluator): {label_map}")
    print()
    
    # --- Blind Evaluation via Claude ---
    print("--- Blind Evaluation (Claude Sonnet 4) ---")
    eval_prompt = EVALUATION_PROMPT.format(
        scenario=TASK,
        analysis_x=results[label_map["X"]]["response"],
        analysis_y=results[label_map["Y"]]["response"],
        analysis_z=results[label_map["Z"]]["response"],
    )
    
    t0 = time.time()
    eval_response = call_evaluator(eval_prompt)
    eval_elapsed = time.time() - t0
    print(f"  Evaluation received in {eval_elapsed:.1f}s")
    print()
    
    # --- Parse evaluation ---
    # Try to extract JSON from the response
    try:
        # Find JSON block
        json_start = eval_response.find("{")
        json_end = eval_response.rfind("}") + 1
        eval_json = json.loads(eval_response[json_start:json_end])
    except (json.JSONDecodeError, ValueError):
        eval_json = {"raw_response": eval_response, "parse_error": True}
    
    # --- Map back to conditions ---
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    
    condition_names = {"A": "Baseline", "B": "144+1 Lattice", "C": "Flat 145-list"}
    
    if "parse_error" not in eval_json:
        for label in ["X", "Y", "Z"]:
            cond = label_map[label]
            scores = eval_json.get(label, {})
            total = scores.get("total", "N/A")
            print(f"  {label} → Condition {cond} ({condition_names[cond]}): Total = {total}")
            for metric in ["coverage", "cross_domain", "depth", "coherence", "actionability", "blind_spots"]:
                print(f"    {metric}: {scores.get(metric, 'N/A')}")
            print(f"    Justification: {scores.get('justification', 'N/A')[:200]}...")
            print()
        
        ranking = eval_json.get("ranking", [])
        print(f"  Blind ranking: {ranking}")
        print(f"  Decoded ranking:")
        for i, label in enumerate(ranking, 1):
            cond = label_map[label]
            print(f"    {i}. {condition_names[cond]} (Condition {cond})")
        
        print(f"\n  Evaluator notes: {eval_json.get('evaluator_notes', 'N/A')[:300]}")
    else:
        print("  [Evaluation JSON parse failed — raw response saved]")
    
    # --- Save everything ---
    output = {
        "experiment": "ontological_scaffold_abc",
        "task": "geopolitical_scenario_istanbul_earthquake_2027",
        "test_model": "claude-sonnet-4",
        "evaluator_model": "grok-3-mini-or-claude-sonnet-4",
        "label_map": label_map,
        "conditions": {
            cond: {
                "name": condition_names[cond],
                "response_length": len(results[cond]["response"]),
                "elapsed": results[cond]["elapsed"],
                "response": results[cond]["response"],
            }
            for cond in ["A", "B", "C"]
        },
        "evaluation": eval_json,
        "evaluation_raw": eval_response,
    }
    
    outpath = "ontological_scaffold_experiment_results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results saved to {outpath}")


if __name__ == "__main__":
    main()
