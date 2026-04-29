#!/usr/bin/env python3
"""
MANUS PERSONAL INTELLIGENCE - Session Context Loader
=====================================================

This script loads relevant context at the start of every Manus session,
providing persistent memory and cross-session continuity.

Usage:
    Called automatically at session start, or manually:
    $ python3 session_context_loader.py

Environment Variables Required:
    - NOTION_API_KEY: Notion integration token
    - PINECONE_API_KEY: Pinecone API key (optional, for semantic search)
    - OPENAI_API_KEY: For embeddings (optional)
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SessionContextLoader:
    """Load and compile session context from multiple sources."""
    
    def __init__(self):
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "recent_sessions": [],
            "active_projects": [],
            "pending_actions": [],
            "urgent_items": [],
            "relevant_knowledge": [],
            "user_preferences": [],
            "recommendations": []
        }
        
        # Sheldonbrain OS database ID
        self.sheldonbrain_db = "2d20c1de-73d9-80ce-a9af-000b011d52f0"
        self.data_source = "collection://2d20c1de-73d9-80ce-a9af-000b011d52f0"
    
    def load_recent_sessions(self, limit: int = 5) -> List[Dict]:
        """Load recent JANUS checkpoints from Notion."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere, Summary 
                    FROM "{self.data_source}" 
                    WHERE Discovery LIKE '%JANUS%' 
                    ORDER BY rowid DESC 
                    LIMIT {limit}'''
        
        try:
            result = self._notion_query(query)
            self.context["recent_sessions"] = result
            return result
        except Exception as e:
            print(f"Warning: Could not load recent sessions: {e}")
            return []
    
    def load_active_projects(self, limit: int = 20) -> List[Dict]:
        """Load active/pending projects from Sheldonbrain OS."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere, Actions 
                    FROM "{self.data_source}" 
                    WHERE Status IN ('Pending', 'In Progress', 'Feast Mode') 
                    LIMIT {limit}'''
        
        try:
            result = self._notion_query(query)
            self.context["active_projects"] = result
            return result
        except Exception as e:
            print(f"Warning: Could not load active projects: {e}")
            return []
    
    def load_urgent_items(self) -> List[Dict]:
        """Load items in Feast Mode or requiring council review."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere, Actions 
                    FROM "{self.data_source}" 
                    WHERE "Feast Mode" = '__YES__' OR "Council Needed" = '__YES__'
                    LIMIT 10'''
        
        try:
            result = self._notion_query(query)
            self.context["urgent_items"] = result
            return result
        except Exception as e:
            print(f"Warning: Could not load urgent items: {e}")
            return []
    
    def load_high_priority_pending(self) -> List[Dict]:
        """Load high-priority pending items."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere, Actions 
                    FROM "{self.data_source}" 
                    WHERE Priority = 'High' AND Status = 'Pending'
                    LIMIT 10'''
        
        try:
            result = self._notion_query(query)
            self.context["pending_actions"] = result
            return result
        except Exception as e:
            print(f"Warning: Could not load pending actions: {e}")
            return []
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate proactive recommendations based on loaded context."""
        
        recommendations = []
        
        # Check for urgent items
        if self.context["urgent_items"]:
            recommendations.append({
                "type": "urgent",
                "priority": "HIGH",
                "message": f"You have {len(self.context['urgent_items'])} items in Feast Mode or needing Council review",
                "items": [item.get("Discovery", "Unknown") for item in self.context["urgent_items"][:3]]
            })
        
        # Check for high-priority pending
        if self.context["pending_actions"]:
            recommendations.append({
                "type": "pending",
                "priority": "MEDIUM",
                "message": f"You have {len(self.context['pending_actions'])} high-priority pending items",
                "items": [item.get("Discovery", "Unknown") for item in self.context["pending_actions"][:3]]
            })
        
        # Time-based recommendations
        now = datetime.now()
        if now.weekday() == 0:  # Monday
            recommendations.append({
                "type": "weekly_review",
                "priority": "LOW",
                "message": "It's Monday - consider reviewing last week's progress"
            })
        
        if now.hour >= 17:  # Evening
            recommendations.append({
                "type": "daily_checkpoint",
                "priority": "LOW",
                "message": "End of day - consider creating a JANUS checkpoint"
            })
        
        self.context["recommendations"] = recommendations
        return recommendations
    
    def _notion_query(self, query: str) -> List[Dict]:
        """Execute a Notion query via MCP CLI."""
        
        input_json = json.dumps({
            "data": {
                "data_source_urls": [self.data_source],
                "query": query
            }
        })
        
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-query-data-sources",
            "--server", "notion",
            "--input", input_json
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"Query failed: {result.stderr}")
        
        # Parse the output
        output = result.stdout
        
        # Find JSON in output
        try:
            # Look for the results array
            if '"results":' in output:
                import re
                match = re.search(r'"results":\s*(\[.*?\])', output, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
        
        return []
    
    def compile_context(self) -> Dict:
        """Compile full session context."""
        
        print("🧠 Loading session context...")
        
        # Load all context sources
        print("  📖 Loading recent sessions...")
        self.load_recent_sessions()
        
        print("  📋 Loading active projects...")
        self.load_active_projects()
        
        print("  🔥 Loading urgent items...")
        self.load_urgent_items()
        
        print("  ⚡ Loading high-priority pending...")
        self.load_high_priority_pending()
        
        print("  💡 Generating recommendations...")
        self.generate_recommendations()
        
        return self.context
    
    def format_briefing(self) -> str:
        """Format context as a human-readable briefing."""
        
        lines = [
            "=" * 60,
            "🧠 MANUS PERSONAL INTELLIGENCE - SESSION BRIEFING",
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            ""
        ]
        
        # Recommendations
        if self.context["recommendations"]:
            lines.append("📌 RECOMMENDATIONS:")
            for rec in self.context["recommendations"]:
                priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(rec.get("priority", "LOW"), "⚪")
                lines.append(f"  {priority_emoji} {rec['message']}")
            lines.append("")
        
        # Urgent items
        if self.context["urgent_items"]:
            lines.append("🔥 URGENT ITEMS (Feast Mode / Council Needed):")
            for item in self.context["urgent_items"][:5]:
                lines.append(f"  • {item.get('Discovery', 'Unknown')}")
            lines.append("")
        
        # Active projects
        if self.context["active_projects"]:
            lines.append(f"📋 ACTIVE PROJECTS ({len(self.context['active_projects'])} total):")
            for item in self.context["active_projects"][:5]:
                status = item.get("Status", "Unknown")
                lines.append(f"  • [{status}] {item.get('Discovery', 'Unknown')}")
            lines.append("")
        
        # Recent sessions
        if self.context["recent_sessions"]:
            lines.append("📖 RECENT SESSIONS:")
            for item in self.context["recent_sessions"][:3]:
                lines.append(f"  • {item.get('Discovery', 'Unknown')}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("Ready for your instructions.")
        lines.append("")
        
        return "\n".join(lines)
    
    def save_context(self, filepath: str = "/home/ubuntu/manus_pi/current_context.json"):
        """Save context to file for reference."""
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(self.context, f, indent=2, default=str)
        
        print(f"💾 Context saved to {filepath}")


def main():
    """Main entry point."""
    
    loader = SessionContextLoader()
    context = loader.compile_context()
    
    # Print briefing
    print(loader.format_briefing())
    
    # Save context
    loader.save_context()
    
    return context


if __name__ == "__main__":
    main()
