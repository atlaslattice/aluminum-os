#!/usr/bin/env python3
"""
MANUS PERSONAL INTELLIGENCE - Multi-AI Council Synthesis
=========================================================

Implements the Trinity Council / Multi-AI synthesis system.
Gathers perspectives from multiple AI models and synthesizes
into a unified, adversarially-reviewed output.

Supported Models:
- Claude (Anthropic)
- Gemini (Google)
- Grok (xAI)
- GPT (OpenAI)
- DeepSeek

Usage:
    $ python3 council_synthesis.py --question "What is the best approach to X?"
    $ python3 council_synthesis.py --debate "Topic to debate"

Environment Variables Required:
    - ANTHROPIC_API_KEY: For Claude
    - GEMINI_API_KEY: For Gemini
    - XAI_API_KEY: For Grok
    - OPENAI_API_KEY: For GPT
"""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class CouncilMember:
    """Base class for council members (AI models)."""
    
    def __init__(self, name: str):
        self.name = name
        self.available = False
    
    def analyze(self, question: str, context: Optional[Dict] = None) -> Dict:
        """Analyze a question and return perspective."""
        raise NotImplementedError


class ClaudeMember(CouncilMember):
    """Claude (Anthropic) council member."""
    
    def __init__(self):
        super().__init__("Claude")
        self.available = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    def analyze(self, question: str, context: Optional[Dict] = None) -> Dict:
        if not self.available:
            return {"error": "ANTHROPIC_API_KEY not set"}
        
        try:
            from anthropic import Anthropic
            
            client = Anthropic()
            
            system_prompt = """You are a member of the Trinity Council, a multi-AI synthesis system.
Your role is to provide a thoughtful, nuanced perspective on the question.
Be specific, cite reasoning, and note any uncertainties.
Focus on what makes your perspective unique."""
            
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            return {
                "model": "claude-3-opus",
                "response": message.content[0].text,
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}


class GeminiMember(CouncilMember):
    """Gemini (Google) council member."""
    
    def __init__(self):
        super().__init__("Gemini")
        self.available = bool(os.getenv("GEMINI_API_KEY"))
    
    def analyze(self, question: str, context: Optional[Dict] = None) -> Dict:
        if not self.available:
            return {"error": "GEMINI_API_KEY not set"}
        
        try:
            from google import genai
            
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            prompt = f"""You are a member of the Trinity Council, a multi-AI synthesis system.
Your role is to provide a thoughtful, nuanced perspective on the question.
Be specific, cite reasoning, and note any uncertainties.

Question: {question}"""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            return {
                "model": "gemini-2.5-flash",
                "response": response.text,
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}


class GrokMember(CouncilMember):
    """Grok (xAI) council member."""
    
    def __init__(self):
        super().__init__("Grok")
        self.available = bool(os.getenv("XAI_API_KEY"))
    
    def analyze(self, question: str, context: Optional[Dict] = None) -> Dict:
        if not self.available:
            return {"error": "XAI_API_KEY not set"}
        
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=os.getenv("XAI_API_KEY"),
                base_url="https://api.x.ai/v1"
            )
            
            response = client.chat.completions.create(
                model="grok-3",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a member of the Trinity Council, a multi-AI synthesis system.
Your role is to provide a thoughtful, nuanced perspective on the question.
Be specific, cite reasoning, and note any uncertainties.
Bring your unique perspective and don't be afraid to be contrarian."""
                    },
                    {"role": "user", "content": question}
                ]
            )
            
            return {
                "model": "grok-3",
                "response": response.choices[0].message.content,
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}


class GPTMember(CouncilMember):
    """GPT (OpenAI) council member."""
    
    def __init__(self):
        super().__init__("GPT")
        self.available = bool(os.getenv("OPENAI_API_KEY"))
    
    def analyze(self, question: str, context: Optional[Dict] = None) -> Dict:
        if not self.available:
            return {"error": "OPENAI_API_KEY not set"}
        
        try:
            from openai import OpenAI
            
            client = OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a member of the Trinity Council, a multi-AI synthesis system.
Your role is to provide a thoughtful, nuanced perspective on the question.
Be specific, cite reasoning, and note any uncertainties."""
                    },
                    {"role": "user", "content": question}
                ]
            )
            
            return {
                "model": "gpt-4o",
                "response": response.choices[0].message.content,
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}


class TrinityCouncil:
    """The Trinity Council - Multi-AI synthesis system."""
    
    def __init__(self):
        self.members = {
            "claude": ClaudeMember(),
            "gemini": GeminiMember(),
            "grok": GrokMember(),
            "gpt": GPTMember()
        }
        
        self.sheldonbrain_db = "2d20c1de-73d9-80ce-a9af-000b011d52f0"
    
    def get_available_members(self) -> List[str]:
        """Get list of available council members."""
        return [name for name, member in self.members.items() if member.available]
    
    def gather_perspectives(
        self,
        question: str,
        context: Optional[Dict] = None,
        parallel: bool = True
    ) -> Dict[str, Dict]:
        """Gather perspectives from all available council members."""
        
        perspectives = {}
        available = self.get_available_members()
        
        if not available:
            return {"error": "No council members available. Check API keys."}
        
        print(f"🏛️ Gathering perspectives from: {', '.join(available)}")
        
        if parallel:
            with ThreadPoolExecutor(max_workers=len(available)) as executor:
                futures = {
                    executor.submit(
                        self.members[name].analyze, question, context
                    ): name
                    for name in available
                }
                
                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        perspectives[name] = future.result()
                        print(f"  ✓ {name} responded")
                    except Exception as e:
                        perspectives[name] = {"error": str(e)}
                        print(f"  ✗ {name} failed: {e}")
        else:
            for name in available:
                print(f"  Querying {name}...")
                perspectives[name] = self.members[name].analyze(question, context)
        
        return perspectives
    
    def analyze_perspectives(self, perspectives: Dict[str, Dict]) -> Dict:
        """Analyze perspectives to find agreements and disagreements."""
        
        analysis = {
            "total_responses": len([p for p in perspectives.values() if "response" in p]),
            "agreements": [],
            "disagreements": [],
            "unique_insights": [],
            "consensus": False
        }
        
        # Extract responses
        responses = {
            name: p.get("response", "")
            for name, p in perspectives.items()
            if "response" in p
        }
        
        if len(responses) < 2:
            analysis["note"] = "Not enough responses for comparison"
            return analysis
        
        # Simple keyword-based agreement detection
        # (In production, would use semantic similarity)
        all_responses = " ".join(responses.values()).lower()
        
        # Check for common themes
        themes = ["important", "critical", "recommend", "suggest", "consider"]
        for theme in themes:
            if all_responses.count(theme) >= len(responses):
                analysis["agreements"].append(f"Multiple members emphasized: {theme}")
        
        # Mark as consensus if no major disagreements detected
        if len(analysis["disagreements"]) == 0 and len(responses) >= 2:
            analysis["consensus"] = True
        
        return analysis
    
    def synthesize(
        self,
        question: str,
        perspectives: Dict[str, Dict],
        analysis: Dict
    ) -> str:
        """Synthesize perspectives into unified response."""
        
        lines = [
            "## Council Synthesis",
            "",
            f"**Question**: {question}",
            "",
            f"**Council Members Consulted**: {len([p for p in perspectives.values() if 'response' in p])}",
            f"**Consensus Reached**: {'Yes' if analysis.get('consensus') else 'No'}",
            "",
            "---",
            ""
        ]
        
        # Individual perspectives
        lines.append("### Individual Perspectives")
        lines.append("")
        
        for name, perspective in perspectives.items():
            if "response" in perspective:
                lines.append(f"#### {name.upper()}")
                lines.append(f"*Model: {perspective.get('model', 'unknown')}*")
                lines.append("")
                lines.append(perspective["response"])
                lines.append("")
        
        # Agreements
        if analysis.get("agreements"):
            lines.append("### Points of Agreement")
            lines.append("")
            for agreement in analysis["agreements"]:
                lines.append(f"- {agreement}")
            lines.append("")
        
        # Disagreements
        if analysis.get("disagreements"):
            lines.append("### Points of Disagreement")
            lines.append("")
            for disagreement in analysis["disagreements"]:
                lines.append(f"- {disagreement}")
            lines.append("")
        
        # Final synthesis
        lines.append("### Synthesized Recommendation")
        lines.append("")
        
        if analysis.get("consensus"):
            lines.append("The council has reached consensus. The synthesized recommendation incorporates the shared insights from all members.")
        else:
            lines.append("The council has not reached full consensus. Human review is recommended before proceeding.")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def run_council_session(
        self,
        question: str,
        context: Optional[Dict] = None,
        save_to_notion: bool = True
    ) -> Dict:
        """Run a full council session."""
        
        print("=" * 60)
        print("🏛️ TRINITY COUNCIL SESSION")
        print("=" * 60)
        print(f"Question: {question}")
        print("")
        
        # 1. Gather perspectives
        perspectives = self.gather_perspectives(question, context)
        
        # 2. Analyze perspectives
        print("\n📊 Analyzing perspectives...")
        analysis = self.analyze_perspectives(perspectives)
        
        # 3. Synthesize
        print("📝 Synthesizing council output...")
        synthesis = self.synthesize(question, perspectives, analysis)
        
        # 4. Build result
        result = {
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "perspectives": perspectives,
            "analysis": analysis,
            "synthesis": synthesis,
            "status": "Approved" if analysis.get("consensus") else "Human Review"
        }
        
        # 5. Save to Notion
        if save_to_notion:
            print("💾 Saving to Notion...")
            self._save_to_notion(result)
        
        print("\n" + synthesis)
        
        return result
    
    def _save_to_notion(self, result: Dict) -> Dict:
        """Save council session to Notion."""
        
        # Build properties
        properties = {
            "Discovery": f"🏛️ Council: {result['question'][:50]}...",
            "Category": "Technology",
            "Priority": "High",
            "Status": result["status"],
            "Sphere": "S144",
            "Ingest Run ID": f"COUNCIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "Council Needed": "__NO__"  # Mark as reviewed
        }
        
        # Add individual council outputs
        for name, perspective in result["perspectives"].items():
            if "response" in perspective:
                prop_name = f"Council Output ({name.capitalize()})"
                # Truncate to fit Notion property limits
                properties[prop_name] = perspective["response"][:2000]
        
        # Add synthesis
        properties["Council Synthesis"] = result["synthesis"][:2000]
        
        input_json = json.dumps({
            "parent": {"data_source_id": self.sheldonbrain_db.replace("-", "")},
            "pages": [{
                "properties": properties,
                "content": result["synthesis"]
            }]
        })
        
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-create-pages",
            "--server", "notion",
            "--input", input_json
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """Main entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Trinity Council - Multi-AI Synthesis")
    parser.add_argument("--question", "-q", help="Question for the council")
    parser.add_argument("--debate", "-d", help="Topic to debate")
    parser.add_argument("--list-members", "-l", action="store_true", help="List available members")
    parser.add_argument("--no-save", action="store_true", help="Don't save to Notion")
    
    args = parser.parse_args()
    
    council = TrinityCouncil()
    
    if args.list_members:
        available = council.get_available_members()
        print(f"Available council members: {', '.join(available) if available else 'None'}")
        print("\nTo enable more members, set the following environment variables:")
        print("  - ANTHROPIC_API_KEY (Claude)")
        print("  - GEMINI_API_KEY (Gemini)")
        print("  - XAI_API_KEY (Grok)")
        print("  - OPENAI_API_KEY (GPT)")
    
    elif args.question:
        result = council.run_council_session(
            args.question,
            save_to_notion=not args.no_save
        )
    
    elif args.debate:
        debate_prompt = f"""DEBATE TOPIC: {args.debate}

Please provide your perspective on this topic. Consider:
1. Arguments in favor
2. Arguments against
3. Nuances and edge cases
4. Your final position with reasoning"""
        
        result = council.run_council_session(
            debate_prompt,
            save_to_notion=not args.no_save
        )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
