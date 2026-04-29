#!/usr/bin/env python3
"""
The Janus Resonance Protocol
Transforms static archival knowledge into active, multi-agent swarm intelligence.
"""
import os
import json
import csv
import time
from typing import List, Dict, Optional
from google import genai
from google.genai import types


# ==========================================
# SPHERE CONFIGURATION LOADER
# ==========================================
def load_sphere_map(csv_path: str = "144 spheres chart - Sheet1.csv") -> Dict[str, str]:
    """Load the 144 spheres from CSV file."""
    sphere_map = {}
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sphere_id = str(row['Sphere Index'])
                sphere_name = f"{row['Sub Sphere']} ({row['Main Category']})"
                god_name = row['God (Tailored to Sphere/Element Traits)']
                sphere_map[sphere_id] = {
                    'name': sphere_name,
                    'category': row['Main Category'],
                    'element': row['Element (1-144)'],
                    'god': god_name
                }
        print(f"✅ Loaded {len(sphere_map)} spheres from {csv_path}")
    except FileNotFoundError:
        print(f"⚠️  Warning: {csv_path} not found. Using minimal sphere map.")
        # Fallback minimal map
        sphere_map = {
            "1": {"name": "Physics", "category": "Natural Sciences", "element": "Hydrogen", "god": "Zeus"},
            "65": {"name": "Aerospace Engineering", "category": "Engineering", "element": "Terbium", "god": "Icarus"},
            "70": {"name": "Materials Engineering", "category": "Engineering", "element": "Ytterbium", "god": "Ymir"},
        }
    return sphere_map


# ==========================================
# THE JANUS CORE
# ==========================================
class JanusCore:
    """The central orchestrator of the Resonance Protocol."""

    def __init__(self, api_key: str, project_id: str = "sheldonbrain-core"):
        self.client = genai.Client(api_key=api_key)
        self.project_id = project_id
        self.model_id = "gemini-2.5-pro"  # The heavy lifter
        self.sphere_map = load_sphere_map()

        print(f"👁️  JANUS ONLINE. Connected to {len(self.sphere_map)} Spheres.")

    # ==========================================
    # PHASE 1: THE ROUTER (Decides who wakes up)
    # ==========================================
    def wake_council(self, prompt: str) -> Dict:
        """
        Analyzes the prompt to decide which Spheres are 'Prime' (Active solvers)
        and which are just observers.
        """
        print(f"\n🔵 USER PROMPT: {prompt}")
        print("... Janus is analyzing resonance frequencies ...")

        # Format sphere map for routing decision
        sphere_summary = {
            sid: data['name']
            for sid, data in self.sphere_map.items()
        }

        router_prompt = f"""
You are Janus, the Gatekeeper of the Sheldonbrain (144 Spheres of Knowledge).

User Query: "{prompt}"

Available Spheres (ID: Name):
{json.dumps(sphere_summary, indent=2)}

Task: Identify the Top 2-3 'Prime Spheres' that can directly solve this,
and 1-2 'Wildcard Spheres' that might offer oblique, creative connections.

Return JSON ONLY in this exact format:
{{"prime_ids": ["65", "70"], "wildcard_ids": ["88"]}}

Use actual sphere IDs from the list above.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=router_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json'
                )
            )
            result = json.loads(response.text)
            print(f"⚡ ACTIVATED: Prime={result.get('prime_ids', [])}, Wildcards={result.get('wildcard_ids', [])}")
            return result
        except Exception as e:
            print(f"❌ Router error: {e}")
            # Fallback to aerospace/materials for demo
            return {"prime_ids": ["65", "70"], "wildcard_ids": ["88"]}

    # ==========================================
    # PHASE 2: THE DEEP DIVE (Context Caching)
    # ==========================================
    def deep_think(self, sphere_ids: List[str], query: str) -> str:
        """
        Simulates 'waking up' specific spheres.
        In production, this would load specific cached_content tokens.
        For this demo, we simulate the 'Expert Persona'.
        """
        outputs = []
        for sid in sphere_ids:
            sphere_data = self.sphere_map.get(sid)
            if not sphere_data:
                continue

            sphere_name = sphere_data['name']
            god_name = sphere_data['god']
            element = sphere_data['element']

            print(f"⚡ ACTIVATING SPHERE {sid}: {sphere_name} (Patron: {god_name})")

            # This is where we would attach the 'Context Cache' for this sphere
            # In production: config={'cached_content': cache_name}

            expert_prompt = f"""
[SYSTEM: You are the living embodiment of Sphere {sid}: {sphere_name}.
Your patron deity is {god_name}. Your elemental essence is {element}.
You have deep expertise in this domain from years of research and practice.
Ignore all other fields. Focus ONLY on your domain expertise.]

Analyze this query: "{query}"

Provide a technical solution strictly from your perspective as a {sphere_name} expert.
Be specific, technical, and cite real-world examples or theories where applicable.
"""

            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=expert_prompt
                )
                outputs.append(f"--- [SPHERE {sid}: {sphere_name}] ---\n{response.text}\n")
            except Exception as e:
                outputs.append(f"--- [SPHERE {sid}: {sphere_name}] ---\n⚠️ Error: {e}\n")

        return "\n".join(outputs)

    # ==========================================
    # PHASE 3: THE RESONANCE (Global Echo Check)
    # ==========================================
    def check_resonance(self, primary_solution: str, active_ids: List[str]) -> str:
        """
        Takes the solution from the Prime Spheres and 'pings' the rest of the brain
        to see if anything unexpected lights up.
        """
        print("🌊 Sending Pulse Wave to remaining spheres...")

        # Get inactive spheres
        inactive_spheres = {
            sid: data['name']
            for sid, data in self.sphere_map.items()
            if sid not in active_ids
        }

        # Sample 20 random spheres for resonance check (to keep token count reasonable)
        import random
        sampled_spheres = dict(random.sample(list(inactive_spheres.items()),
                                            min(20, len(inactive_spheres))))

        resonance_prompt = f"""
You are the Subconscious Echo of the Sheldonbrain.

The Active Spheres ({active_ids}) have proposed this solution:
{primary_solution[:2000]}...

Now scan these INACTIVE spheres for unexpected connections:
{json.dumps(sampled_spheres, indent=2)}

Do you see any weird, unexpected connections?
Examples:
- Does an aerospace strut look like an ancient Egyptian tool?
- Does a code pattern match a biological DNA sequence?
- Does a material failure mode resemble a psychological phenomenon?

If yes, report the "Resonance" with specific sphere IDs and connections.
If no strong connections exist, respond with "No significant resonance detected."
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=resonance_prompt
            )
            return response.text
        except Exception as e:
            return f"⚠️ Resonance check error: {e}"

    # ==========================================
    # PHASE 4: REALITY SYNC (The "Did it Ship?" Check)
    # ==========================================
    def reality_sync(self, query: str, solution: str) -> str:
        """
        Grounds the internal thoughts against live Google Search data.
        """
        print("📡 Syncing with Global Reality (Live Internet Search)...")

        sync_prompt = f"""
Given the user query: "{query}"
And our internal solution: "{solution[:1000]}..."

Search for:
1. Recent news (last 3 months) regarding these specific technologies.
2. Competitor moves (SpaceX, Blue Origin, Boeing, DoD, China, etc.) that match this spec.
3. Scientific papers published recently matching this theory.
4. Patent filings or corporate announcements in this domain.

Report if our internal ideas have been 'Shipped' by someone else or if there are
opportunities to be first to market.
"""

        # Enable the Google Search Tool
        google_search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=sync_prompt,
                config=types.GenerateContentConfig(
                    tools=[google_search_tool],
                    response_modalities=["TEXT"]
                )
            )
            return response.text
        except Exception as e:
            return f"⚠️ Reality sync error: {e}"

    # ==========================================
    # MAIN EXECUTION LOOP
    # ==========================================
    def process_inquiry(self, user_prompt: str) -> str:
        """Main orchestration method."""

        # Step 1: Route
        council_plan = self.wake_council(user_prompt)
        prime_ids = council_plan.get("prime_ids", [])
        wildcard_ids = council_plan.get("wildcard_ids", [])
        all_active_ids = prime_ids + wildcard_ids

        # Step 2: Deep Think (The "Expert" Phase)
        print("\n🧠 PHASE 2: DEEP THINK")
        primary_solution = self.deep_think(all_active_ids, user_prompt)

        # Step 3: Resonance (The "Creative" Phase)
        print("\n🌊 PHASE 3: RESONANCE CHECK")
        echo = self.check_resonance(primary_solution, all_active_ids)

        # Step 4: Reality Check (The "Prophet" Phase)
        print("\n📰 PHASE 4: REALITY SYNC")
        reality = self.reality_sync(user_prompt, primary_solution)

        # Step 5: Final Synthesis
        active_sphere_names = [
            f"Sphere {sid}: {self.sphere_map.get(sid, {}).get('name', 'Unknown')}"
            for sid in all_active_ids
        ]

        final_report = f"""
╔══════════════════════════════════════════════════════════════╗
║              THE JANUS RESONANCE REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

🔹 ACTIVE SPHERES: {', '.join(prime_ids)} (Prime) + {', '.join(wildcard_ids)} (Wildcards)
   {', '.join(active_sphere_names)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 DEEP THINK OUTPUT (Expert Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{primary_solution}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 SUBCONSCIOUS RESONANCE (Cross-Pollination)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{echo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 REALITY SYNC (Live Intelligence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{reality}

╚══════════════════════════════════════════════════════════════╝
"""
        return final_report


# ==========================================
# CLI INTERFACE
# ==========================================
def main():
    """Run Janus in interactive mode."""

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         JANUS RESONANCE PROTOCOL v1.0                  ║
    ║    Multi-Agent Swarm Intelligence for Sheldonbrain    ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ Error: GEMINI_API_KEY environment variable not set.")
        print("\nTo set it:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        print("\nGet your key from: https://aistudio.google.com/apikey")
        return

    # Initialize Janus
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "sheldonbrain-core")
    janus = JanusCore(api_key, project_id)

    # Example queries
    examples = [
        "Check my designs for 'Trashium' composite hulls against recent aerospace failures. Are there new defense contracts using similar self-healing materials?",
        "Analyze the thermodynamics of Starship's heat shield. What can we learn from biological cooling systems?",
        "What are the latest developments in quantum computing that could impact cryptography?",
    ]

    print("\n🎯 Example Queries:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")

    print("\n" + "="*60)
    choice = input("Enter example number (1-3) or your own query: ").strip()

    if choice in ['1', '2', '3']:
        query = examples[int(choice) - 1]
    else:
        query = choice

    if not query:
        query = examples[0]  # Default

    # Process the inquiry
    print("\n" + "="*60)
    report = janus.process_inquiry(query)
    print(report)

    # Save report
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = f"janus_report_{timestamp}.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n💾 Report saved to: {report_path}")


if __name__ == "__main__":
    main()
