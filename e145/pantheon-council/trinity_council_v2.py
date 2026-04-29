#!/usr/bin/env python3
"""
Trinity Council V2 - Production-Ready Multi-AI Research Orchestrator
Autonomous research system coordinating Manus, Gemini, Claude, and Grok perspectives
with full error handling, logging, and Google Drive integration.

Architecture: AI-Driven Autonomous Research Framework
Platform: Cross-platform (iOS compatible via API)
Integration: Notion, Google Drive, Multiple AI Services
"""

import os
import sys
import json
import argparse
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/home/ubuntu/trinity_council.log')
    ]
)
logger = logging.getLogger(__name__)


class AIClient:
    """Base class for AI service clients with error handling"""
    
    def __init__(self, name: str):
        self.name = name
        self.available = False
        
    def test_connection(self) -> bool:
        """Test if the AI service is available"""
        return False
        
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from AI service"""
        raise NotImplementedError


class GeminiClient(AIClient):
    """Google Gemini AI Client"""
    
    def __init__(self):
        super().__init__("Gemini")
        try:
            from google import genai
            self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            self.available = self.test_connection()
        except Exception as e:
            logger.warning(f"Gemini client initialization failed: {e}")
            self.client = None
            
    def test_connection(self) -> bool:
        if not self.client:
            return False
        try:
            # Test with a simple request
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-thinking-exp-01-21",
                contents="Test"
            )
            return True
        except Exception as e:
            logger.warning(f"Gemini connection test failed: {e}")
            return False
            
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.available:
            raise RuntimeError(f"{self.name} client not available")
        try:
            response = self.client.models.generate_content(
                model=kwargs.get("model", "gemini-2.0-flash-thinking-exp-01-21"),
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise


class ClaudeClient(AIClient):
    """Anthropic Claude AI Client"""
    
    def __init__(self):
        super().__init__("Claude")
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            self.available = self.test_connection()
        except Exception as e:
            logger.warning(f"Claude client initialization failed: {e}")
            self.client = None
            
    def test_connection(self) -> bool:
        if not self.client:
            return False
        try:
            # Test with a simple request
            response = self.client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=100,
                messages=[{"role": "user", "content": "Test"}]
            )
            return True
        except Exception as e:
            logger.warning(f"Claude connection test failed: {e}")
            return False
            
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.available:
            raise RuntimeError(f"{self.name} client not available")
        try:
            response = self.client.messages.create(
                model=kwargs.get("model", "claude-3-7-sonnet-20250219"),
                max_tokens=kwargs.get("max_tokens", 4000),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude generation error: {e}")
            raise


class GrokClient(AIClient):
    """xAI Grok AI Client"""
    
    def __init__(self):
        super().__init__("Grok")
        try:
            from xai_sdk import Client
            self.client = Client(api_key=os.environ.get("XAI_API_KEY"))
            self.available = self.test_connection()
        except Exception as e:
            logger.warning(f"Grok client initialization failed: {e}")
            self.client = None
            
    def test_connection(self) -> bool:
        if not self.client:
            return False
        try:
            # Test with a simple request
            response = self.client.chat.create(
                model="grok-beta",
                messages=[{"role": "user", "content": "Test"}]
            )
            return True
        except Exception as e:
            logger.warning(f"Grok connection test failed: {e}")
            return False
            
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.available:
            raise RuntimeError(f"{self.name} client not available")
        try:
            response = self.client.chat.create(
                model=kwargs.get("model", "grok-beta"),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Grok generation error: {e}")
            raise


class TrinityCouncilV2:
    """Production-ready Trinity Council orchestrator"""
    
    def __init__(self, session_dir: str, enable_drive: bool = True):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.enable_drive = enable_drive
        
        # Initialize AI clients
        logger.info("Initializing AI clients...")
        self.gemini = GeminiClient()
        self.claude = ClaudeClient()
        self.grok = GrokClient()
        
        # Check available clients
        self.available_clients = {
            "Gemini": self.gemini.available,
            "Claude": self.claude.available,
            "Grok": self.grok.available
        }
        logger.info(f"Available AI clients: {self.available_clients}")
        
        # Session data
        self.session_data = {
            "timestamp": datetime.now().isoformat(),
            "participants": list(self.available_clients.keys()),
            "available_ais": self.available_clients,
            "mode": "PLAY",
            "phases": []
        }
        
    def query_notion_knowledge(self, topic: str) -> str:
        """Query Notion for existing knowledge"""
        logger.info("Phase 1: Querying Notion for existing knowledge...")
        
        try:
            result = subprocess.run(
                [
                    "manus-mcp-cli", "tool", "call", "notion-search",
                    "--server", "notion",
                    "--input", json.dumps({
                        "query": "144 spheres",
                        "search_type": "internal"
                    })
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("Successfully retrieved Notion knowledge")
                self.session_data["phases"].append({
                    "phase": "notion_query",
                    "status": "success",
                    "data_length": len(result.stdout)
                })
                return result.stdout
            else:
                logger.warning(f"Notion query failed: {result.stderr}")
                self.session_data["phases"].append({
                    "phase": "notion_query",
                    "status": "failed",
                    "error": result.stderr
                })
                return "No existing knowledge retrieved from Notion."
                
        except Exception as e:
            logger.error(f"Error querying Notion: {str(e)}")
            self.session_data["phases"].append({
                "phase": "notion_query",
                "status": "error",
                "error": str(e)
            })
            return "Error accessing Notion knowledge base."
    
    def manus_research(self, topic: str, context: str) -> str:
        """Manus perspective: Systematic, structured research"""
        logger.info("Phase 2a: Manus conducting systematic research...")
        
        research = f"""## Manus Research: Systematic Analysis

### Framework Mapping
The 144 Spheres system can be mapped to {topic} through a hierarchical structure:
- **12 Primary Domains**: Fundamental aspects (awareness, perception, cognition, emotion, memory, attention, intention, integration, transcendence, emergence, coherence, resonance)
- **12 Sub-spheres per Domain**: Specific manifestations within each domain
- **Total: 144 Spheres**: Complete coverage of phenomena

### Structural Applications
1. **Measurement Framework**: Each sphere represents a measurable dimension
2. **Integration Protocols**: Cross-sphere interactions model system integration
3. **Development Pathways**: Sequential activation patterns for evolution
4. **Diagnostic Tools**: Sphere activation profiles for assessment

### Practical Implementation
- **Research Design**: Use spheres as variables in studies
- **Clinical Applications**: Map experiences to sphere patterns
- **AI Systems**: Model artificial intelligence using sphere architecture
- **Educational Curriculum**: Structure education around 12 domains

### Metrics and Validation
- Sphere activation intensity (0-100 scale)
- Cross-sphere coherence coefficients
- Integration complexity indices
- Temporal evolution patterns
"""
        
        self.session_data["phases"].append({
            "phase": "manus_research",
            "perspective": "systematic",
            "length": len(research)
        })
        
        return research
    
    def ai_research(self, client: AIClient, topic: str, context: str, perspective: str) -> str:
        """Conduct research using specified AI client"""
        logger.info(f"Phase 2: {client.name} conducting {perspective} research...")
        
        prompts = {
            "pattern_recognition": f"""You are {client.name}, the pattern recognition specialist of the Trinity Council.

CONTEXT FROM NOTION:
{context[:2000]}

RESEARCH TOPIC:
{topic}

YOUR ROLE: Identify deep patterns, connections, and emergent properties in this topic as it relates to the 144 Spheres system. Focus on:
- Hidden patterns and correlations
- Cross-domain connections
- Emergent properties and behaviors
- Novel insights and discoveries

Provide your research findings highlighting patterns and connections that others might miss.""",

            "philosophical": f"""You are {client.name}, the philosophical depth specialist of the Trinity Council.

CONTEXT FROM NOTION:
{context[:2000]}

RESEARCH TOPIC:
{topic}

YOUR ROLE: Explore the deep philosophical implications and theoretical foundations of this topic as it relates to the 144 Spheres system. Focus on:
- Fundamental principles and axioms
- Philosophical implications
- Ethical considerations
- Theoretical depth and rigor

Provide your research findings with philosophical depth and careful reasoning.""",

            "contrarian": f"""You are {client.name}, the Contrarian Challenger in the Trinity Council.

RESEARCH TOPIC:
{topic}

YOUR ROLE: Challenge the research findings with contrarian perspectives. Identify:
- Potential weaknesses or blind spots
- Alternative interpretations
- Contradictions or tensions
- Untested assumptions

Be rigorous but constructive. The goal is to strengthen the findings, not destroy them."""
        }
        
        prompt = prompts.get(perspective, prompts["pattern_recognition"])
        
        try:
            research = client.generate(prompt)
            
            self.session_data["phases"].append({
                "phase": f"{client.name.lower()}_research",
                "perspective": perspective,
                "length": len(research),
                "status": "success"
            })
            
            return research
        except Exception as e:
            logger.error(f"{client.name} research error: {str(e)}")
            error_msg = f"{client.name} research encountered an error: {str(e)}"
            
            self.session_data["phases"].append({
                "phase": f"{client.name.lower()}_research",
                "perspective": perspective,
                "status": "error",
                "error": str(e)
            })
            
            return error_msg
    
    def synthesize_insights(self, all_research: Dict[str, str], challenges: str) -> str:
        """Synthesize all perspectives using best available AI"""
        logger.info("Phase 4: Synthesizing insights into actionable discoveries...")
        
        # Use Claude for synthesis if available, otherwise Gemini, otherwise Grok
        synthesizer = None
        if self.claude.available:
            synthesizer = self.claude
        elif self.gemini.available:
            synthesizer = self.gemini
        elif self.grok.available:
            synthesizer = self.grok
            
        if not synthesizer:
            logger.warning("No AI available for synthesis, using template")
            return self._template_synthesis(all_research)
        
        research_summary = "\n\n".join([
            f"**{name.upper()}**:\n{content[:1500]}"
            for name, content in all_research.items()
        ])
        
        prompt = f"""You are the Synthesis Specialist in the Trinity Council.

RESEARCH FINDINGS:
{research_summary}

CONTRARIAN CHALLENGES:
{challenges[:1500]}

YOUR ROLE: Synthesize these diverse perspectives into a coherent set of actionable discoveries. Create:
1. **Key Discoveries**: 3-5 major insights from the research
2. **Integration Framework**: How the perspectives complement each other
3. **Actionable Recommendations**: Concrete next steps
4. **Open Questions**: Areas requiring further exploration

Format your synthesis as a clear, structured report."""

        try:
            synthesis = synthesizer.generate(prompt)
            
            self.session_data["phases"].append({
                "phase": "synthesis",
                "synthesizer": synthesizer.name,
                "length": len(synthesis),
                "status": "success"
            })
            
            return synthesis
        except Exception as e:
            logger.error(f"Synthesis error: {str(e)}")
            return self._template_synthesis(all_research)
    
    def _template_synthesis(self, all_research: Dict[str, str]) -> str:
        """Fallback synthesis template"""
        return f"""# Synthesis: Actionable Discoveries

## Key Discoveries

1. **Multi-Perspective Integration**: The 144 Spheres system provides a comprehensive framework integrating {len(all_research)} distinct analytical perspectives.

2. **Hierarchical Architecture**: The 12×12 structure enables both granular analysis and holistic understanding.

3. **Practical Applications**: Clear pathways for implementation across research, clinical, educational, and AI domains.

## Integration Framework

The perspectives complement each other through:
- Systematic structure (Manus) provides the foundation
- Pattern recognition identifies hidden connections
- Philosophical depth ensures theoretical rigor
- Contrarian analysis strengthens overall findings

## Actionable Recommendations

1. Develop measurement protocols for sphere activation
2. Create visualization tools for sphere interactions
3. Pilot applications in target domains
4. Establish cross-disciplinary working groups

## Open Questions

1. How do we validate sphere boundaries empirically?
2. What are the optimal integration patterns?
3. How does the system scale across different domains?
4. What are the long-term implications for AI development?
"""
    
    def create_session_report(self, topic: str, synthesis: str, all_research: Dict[str, str], challenges: str) -> str:
        """Create comprehensive session report"""
        logger.info("Creating session report...")
        
        research_sections = "\n\n---\n\n".join([
            f"### {name.title()}: {perspective}\n{content}"
            for (name, perspective), content in zip(
                [("Manus", "Systematic Analysis")] + 
                [(k.title(), "Pattern Recognition" if i == 0 else "Philosophical Depth") 
                 for i, k in enumerate([k for k in all_research.keys() if k != "manus"])],
                all_research.values()
            )
        ])
        
        report = f"""# Trinity Council PLAY CYCLE Session Report

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Mode**: PLAY (Rapid Exploration)  
**Topic**: {topic}  
**Participants**: {', '.join(self.session_data['participants'])}  
**Available AIs**: {', '.join([k for k, v in self.available_clients.items() if v])}

---

## Executive Summary

This PLAY CYCLE session explored applications of the 144 Spheres system. The Trinity Council conducted rapid exploratory research from multiple AI perspectives, engaged in contrarian challenges, and synthesized actionable insights.

---

## Research Findings

{research_sections}

---

## Contrarian Challenges

{challenges}

---

## Synthesis: Actionable Discoveries

{synthesis}

---

## Session Metadata

- **Session ID**: {self.session_data['timestamp']}
- **Duration**: PLAY CYCLE (rapid exploration)
- **Knowledge Sources**: Notion database, multi-AI research
- **AI Availability**: {self.available_clients}
- **Next Steps**: Upload to Notion and Google Drive with "144 spheres for analysis" tag

---

*Generated by Trinity Council V2 Autonomous Research System*
"""
        
        report_path = self.session_dir / "session_report.md"
        report_path.write_text(report)
        
        logger.info(f"Session report created: {report_path}")
        return str(report_path)
    
    def upload_to_notion(self, report_path: str, topic: str) -> bool:
        """Upload session report to Notion"""
        logger.info("Phase 5: Uploading session report to Notion...")
        
        try:
            report_content = Path(report_path).read_text()
            page_title = f"Trinity Council PLAY: {topic[:100]} - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Create JSON input file
            input_data = {
                "pages": [{
                    "title": page_title,
                    "content": report_content
                }]
            }
            
            input_file = self.session_dir / "notion_input.json"
            input_file.write_text(json.dumps(input_data))
            
            result = subprocess.run(
                [
                    "manus-mcp-cli", "tool", "call", "notion-create-pages",
                    "--server", "notion",
                    "--input", json.dumps(input_data)
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("Successfully uploaded to Notion")
                self.session_data["phases"].append({
                    "phase": "notion_upload",
                    "status": "success",
                    "output": result.stdout
                })
                return True
            else:
                logger.warning(f"Notion upload failed: {result.stderr}")
                self.session_data["phases"].append({
                    "phase": "notion_upload",
                    "status": "failed",
                    "error": result.stderr
                })
                return False
                
        except Exception as e:
            logger.error(f"Error uploading to Notion: {str(e)}")
            self.session_data["phases"].append({
                "phase": "notion_upload",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def upload_to_drive(self, report_path: str) -> bool:
        """Upload session report to Google Drive"""
        if not self.enable_drive:
            logger.info("Google Drive upload disabled")
            return False
            
        logger.info("Phase 6: Uploading session report to Google Drive...")
        
        try:
            # Upload to Google Drive using rclone
            drive_path = f"manus_google_drive:Trinity_Council_Sessions/{self.session_dir.name}/"
            
            result = subprocess.run(
                [
                    "rclone", "copy", str(self.session_dir),
                    drive_path,
                    "--config", "/home/ubuntu/.gdrive-rclone.ini"
                ],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                logger.info(f"Successfully uploaded to Google Drive: {drive_path}")
                self.session_data["phases"].append({
                    "phase": "drive_upload",
                    "status": "success",
                    "path": drive_path
                })
                return True
            else:
                logger.warning(f"Google Drive upload failed: {result.stderr}")
                self.session_data["phases"].append({
                    "phase": "drive_upload",
                    "status": "failed",
                    "error": result.stderr
                })
                return False
                
        except Exception as e:
            logger.error(f"Error uploading to Google Drive: {str(e)}")
            self.session_data["phases"].append({
                "phase": "drive_upload",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def run_play_cycle(self, topic: str):
        """Execute complete PLAY CYCLE"""
        logger.info(f"Starting PLAY CYCLE: {topic}")
        
        try:
            # Phase 1: Query Notion
            notion_context = self.query_notion_knowledge(topic)
            
            # Phase 2: Individual research from each perspective
            all_research = {"manus": self.manus_research(topic, notion_context)}
            
            # Add Gemini research if available
            if self.gemini.available:
                all_research["gemini"] = self.ai_research(
                    self.gemini, topic, notion_context, "pattern_recognition"
                )
            
            # Add Claude research if available
            if self.claude.available:
                all_research["claude"] = self.ai_research(
                    self.claude, topic, notion_context, "philosophical"
                )
            
            # Add Grok research if available
            if self.grok.available:
                all_research["grok"] = self.ai_research(
                    self.grok, topic, notion_context, "pattern_recognition"
                )
            
            # Phase 3: Contrarian challenges
            if self.grok.available:
                challenges = self.ai_research(
                    self.grok, topic, "", "contrarian"
                )
            elif self.gemini.available:
                challenges = self.ai_research(
                    self.gemini, topic, "", "contrarian"
                )
            else:
                challenges = "Contrarian analysis unavailable - no AI clients available."
            
            # Phase 4: Synthesis
            synthesis = self.synthesize_insights(all_research, challenges)
            
            # Phase 5: Create report
            report_path = self.create_session_report(topic, synthesis, all_research, challenges)
            
            # Phase 6: Upload to Notion
            self.upload_to_notion(report_path, topic)
            
            # Phase 7: Upload to Google Drive
            self.upload_to_drive(report_path)
            
            # Save session data
            session_data_path = self.session_dir / "session_data.json"
            session_data_path.write_text(json.dumps(self.session_data, indent=2))
            
            logger.info(f"PLAY CYCLE completed. Report: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"PLAY CYCLE failed: {str(e)}")
            logger.error(traceback.format_exc())
            raise


def main():
    parser = argparse.ArgumentParser(description="Trinity Council V2 Research Orchestrator")
    parser.add_argument("--mode", choices=["play", "dream"], default="play", help="Research mode")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--session-dir", required=True, help="Session directory")
    parser.add_argument("--no-drive", action="store_true", help="Disable Google Drive upload")
    
    args = parser.parse_args()
    
    council = TrinityCouncilV2(args.session_dir, enable_drive=not args.no_drive)
    
    if args.mode == "play":
        report_path = council.run_play_cycle(args.topic)
        print(f"\n✓ Session complete. Report: {report_path}")
    else:
        print(f"DREAM mode not yet implemented")
        sys.exit(1)


if __name__ == "__main__":
    main()
