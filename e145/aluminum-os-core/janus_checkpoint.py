#!/usr/bin/env python3
"""
MANUS PERSONAL INTELLIGENCE - JANUS Checkpoint System
======================================================

Creates session checkpoints for continuity across Manus sessions.
Named after Janus, the Roman god of beginnings, transitions, and endings.

Usage:
    Called at the end of each session, or manually:
    $ python3 janus_checkpoint.py --summary "Session summary here"

Environment Variables Required:
    - NOTION_API_KEY: Notion integration token
"""

import os
import json
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class JanusCheckpoint:
    """Create and manage session checkpoints."""
    
    def __init__(self):
        self.sheldonbrain_db = "2d20c1de-73d9-80ce-a9af-000b011d52f0"
        self.data_source = "collection://2d20c1de-73d9-80ce-a9af-000b011d52f0"
        self.drive_inbox = "Atlas Vault Inbox"
        
        self.checkpoint = {
            "id": self._generate_id(),
            "timestamp": datetime.now().isoformat(),
            "title": "",
            "summary": "",
            "key_topics": [],
            "decisions_made": [],
            "artifacts_created": [],
            "next_actions": [],
            "sphere": "S144",
            "status": "Completed"
        }
    
    def _generate_id(self) -> str:
        """Generate unique checkpoint ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
        return f"JANUS_{timestamp}_{hash_suffix}"
    
    def create_checkpoint(
        self,
        summary: str,
        key_topics: Optional[List[str]] = None,
        decisions: Optional[List[str]] = None,
        artifacts: Optional[List[str]] = None,
        next_actions: Optional[List[str]] = None,
        sphere: str = "S144"
    ) -> Dict:
        """Create a new JANUS checkpoint."""
        
        timestamp = datetime.now()
        
        self.checkpoint.update({
            "title": f"📖 JANUS CHECKPOINT - {timestamp.strftime('%Y-%m-%d %H:%M')}",
            "summary": summary,
            "key_topics": key_topics or [],
            "decisions_made": decisions or [],
            "artifacts_created": artifacts or [],
            "next_actions": next_actions or [],
            "sphere": sphere
        })
        
        return self.checkpoint
    
    def save_to_notion(self) -> Dict:
        """Save checkpoint to Sheldonbrain OS database."""
        
        # Build content markdown
        content_lines = [
            f"## Session Summary",
            f"",
            self.checkpoint["summary"],
            f"",
        ]
        
        if self.checkpoint["key_topics"]:
            content_lines.extend([
                f"## Key Topics",
                *[f"- {topic}" for topic in self.checkpoint["key_topics"]],
                ""
            ])
        
        if self.checkpoint["decisions_made"]:
            content_lines.extend([
                f"## Decisions Made",
                *[f"- {decision}" for decision in self.checkpoint["decisions_made"]],
                ""
            ])
        
        if self.checkpoint["artifacts_created"]:
            content_lines.extend([
                f"## Artifacts Created",
                *[f"- {artifact}" for artifact in self.checkpoint["artifacts_created"]],
                ""
            ])
        
        if self.checkpoint["next_actions"]:
            content_lines.extend([
                f"## Next Actions",
                *[f"- [ ] {action}" for action in self.checkpoint["next_actions"]],
                ""
            ])
        
        content_lines.extend([
            f"---",
            f"**Checkpoint ID**: `{self.checkpoint['id']}`",
            f"**Timestamp**: {self.checkpoint['timestamp']}",
            f"**Sphere**: {self.checkpoint['sphere']}"
        ])
        
        content = "\n".join(content_lines)
        
        # Create page in Notion
        input_json = json.dumps({
            "parent": {"data_source_id": self.sheldonbrain_db.replace("-", "")},
            "pages": [{
                "properties": {
                    "Discovery": self.checkpoint["title"],
                    "Category": "Technology",
                    "Priority": "High",
                    "Status": "Completed",
                    "Sphere": self.checkpoint["sphere"],
                    "Ingest Run ID": self.checkpoint["id"],
                    "Summary": self.checkpoint["summary"][:2000] if len(self.checkpoint["summary"]) > 2000 else self.checkpoint["summary"]
                },
                "content": content
            }]
        })
        
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-create-pages",
            "--server", "notion",
            "--input", input_json
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Checkpoint saved to Notion")
                # Parse result for URL
                if "url" in result.stdout:
                    import re
                    match = re.search(r'"url":\s*"([^"]+)"', result.stdout)
                    if match:
                        self.checkpoint["notion_url"] = match.group(1)
                        print(f"   URL: {self.checkpoint['notion_url']}")
                return {"success": True, "output": result.stdout}
            else:
                print(f"❌ Failed to save to Notion: {result.stderr}")
                return {"success": False, "error": result.stderr}
        except Exception as e:
            print(f"❌ Error saving to Notion: {e}")
            return {"success": False, "error": str(e)}
    
    def save_to_drive(self) -> Dict:
        """Save checkpoint to Google Drive."""
        
        # Create JSON file
        filename = f"JANUS_CHECKPOINT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/home/ubuntu/manus_pi/{filename}"
        
        with open(filepath, "w") as f:
            json.dump(self.checkpoint, f, indent=2, default=str)
        
        # Upload to Google Drive
        cmd = [
            "rclone", "copy", filepath,
            f"manus_google_drive:{self.drive_inbox}/",
            "--config", "/home/ubuntu/.gdrive-rclone.ini"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Checkpoint saved to Google Drive: {self.drive_inbox}/{filename}")
                self.checkpoint["drive_path"] = f"{self.drive_inbox}/{filename}"
                return {"success": True, "path": self.checkpoint["drive_path"]}
            else:
                print(f"❌ Failed to save to Drive: {result.stderr}")
                return {"success": False, "error": result.stderr}
        except Exception as e:
            print(f"❌ Error saving to Drive: {e}")
            return {"success": False, "error": str(e)}
    
    def save_local(self, filepath: str = None) -> str:
        """Save checkpoint to local file."""
        
        if filepath is None:
            filepath = f"/home/ubuntu/manus_pi/checkpoints/{self.checkpoint['id']}.json"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(self.checkpoint, f, indent=2, default=str)
        
        print(f"💾 Checkpoint saved locally: {filepath}")
        return filepath
    
    def save_all(self) -> Dict:
        """Save checkpoint to all destinations."""
        
        results = {
            "local": self.save_local(),
            "notion": self.save_to_notion(),
            "drive": self.save_to_drive()
        }
        
        return results
    
    def format_summary(self) -> str:
        """Format checkpoint as human-readable summary."""
        
        lines = [
            "=" * 60,
            f"📖 JANUS CHECKPOINT CREATED",
            "=" * 60,
            f"",
            f"ID: {self.checkpoint['id']}",
            f"Time: {self.checkpoint['timestamp']}",
            f"Sphere: {self.checkpoint['sphere']}",
            f"",
            f"SUMMARY:",
            self.checkpoint['summary'],
            f"",
        ]
        
        if self.checkpoint["key_topics"]:
            lines.append("KEY TOPICS:")
            for topic in self.checkpoint["key_topics"]:
                lines.append(f"  • {topic}")
            lines.append("")
        
        if self.checkpoint["next_actions"]:
            lines.append("NEXT ACTIONS:")
            for action in self.checkpoint["next_actions"]:
                lines.append(f"  □ {action}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(description="Create a JANUS checkpoint")
    parser.add_argument("--summary", "-s", required=True, help="Session summary")
    parser.add_argument("--topics", "-t", nargs="+", help="Key topics discussed")
    parser.add_argument("--decisions", "-d", nargs="+", help="Decisions made")
    parser.add_argument("--artifacts", "-a", nargs="+", help="Artifacts created")
    parser.add_argument("--next", "-n", nargs="+", help="Next actions")
    parser.add_argument("--sphere", default="S144", help="Sphere classification")
    parser.add_argument("--local-only", action="store_true", help="Only save locally")
    
    args = parser.parse_args()
    
    # Create checkpoint
    janus = JanusCheckpoint()
    janus.create_checkpoint(
        summary=args.summary,
        key_topics=args.topics,
        decisions=args.decisions,
        artifacts=args.artifacts,
        next_actions=args.next,
        sphere=args.sphere
    )
    
    # Save
    if args.local_only:
        janus.save_local()
    else:
        janus.save_all()
    
    # Print summary
    print(janus.format_summary())
    
    return janus.checkpoint


if __name__ == "__main__":
    main()
