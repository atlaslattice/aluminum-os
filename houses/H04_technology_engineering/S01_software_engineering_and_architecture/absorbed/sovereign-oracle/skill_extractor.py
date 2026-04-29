"""
WISH #4: Skill Extraction Engine
After completing a complex task, auto-extract a reusable skill/template.
Turns one-time work into permanent capability.
"""
import json
import os
from datetime import datetime
from pathlib import Path

SKILLS_DIR = "/home/ubuntu/manus_wishlist/data/extracted_skills"

class SkillExtractor:
    def __init__(self):
        Path(SKILLS_DIR).mkdir(parents=True, exist_ok=True)

    def extract(self, task_name: str, steps: list, tools_used: list,
                inputs: dict = None, outputs: dict = None) -> str:
        """Extract a reusable skill from a completed task."""
        skill = {
            "name": task_name.lower().replace(" ", "_"),
            "title": task_name,
            "extracted_at": datetime.now().isoformat(),
            "steps": steps,
            "tools_used": tools_used,
            "inputs": inputs or {},
            "outputs": outputs or {},
            "reuse_count": 0,
            "template": self._generate_template(task_name, steps, tools_used)
        }
        filepath = os.path.join(SKILLS_DIR, f"{skill['name']}.json")
        with open(filepath, "w") as f:
            json.dump(skill, f, indent=2)

        # Also generate a SKILL.md for compatibility with Manus skills system
        md_path = os.path.join(SKILLS_DIR, f"{skill['name']}.md")
        with open(md_path, "w") as f:
            f.write(f"# {task_name}\n\n")
            f.write(f"**Extracted:** {skill['extracted_at']}\n\n")
            f.write("## Steps\n\n")
            for i, step in enumerate(steps, 1):
                f.write(f"{i}. {step}\n")
            f.write(f"\n## Tools Required\n\n")
            for tool in tools_used:
                f.write(f"- {tool}\n")
            f.write(f"\n## Template\n\n```\n{skill['template']}\n```\n")
        return filepath

    def _generate_template(self, name: str, steps: list, tools: list) -> str:
        lines = [f"# Skill: {name}", ""]
        for i, step in enumerate(steps, 1):
            lines.append(f"Step {i}: {step}")
        lines.append("")
        lines.append(f"Tools: {', '.join(tools)}")
        return "\n".join(lines)

    def list_skills(self) -> list:
        return [f.stem for f in Path(SKILLS_DIR).glob("*.json")]

    def get_skill(self, name: str) -> dict:
        filepath = os.path.join(SKILLS_DIR, f"{name}.json")
        if os.path.exists(filepath):
            with open(filepath) as f:
                return json.load(f)
        return {"error": f"Skill '{name}' not found"}


if __name__ == "__main__":
    extractor = SkillExtractor()
    extractor.extract(
        task_name="Daily Sync",
        steps=[
            "Fetch Gmail emails from last 24h via MCP",
            "Filter spam/marketing, deduplicate",
            "Create Notion entries for each relevant email",
            "Check Google Drive for modified files via rclone",
            "Create Notion entries for modified files",
            "Query Active entries older than 7 days",
            "Move stale entries to Deep Sleep",
            "Create sync session log entry"
        ],
        tools_used=["gmail_mcp", "notion_mcp", "rclone", "python", "shell"],
        inputs={"time_window": "24h", "database_id": "add65d86-00d0-46c6-b97b-c0924a94512f"},
        outputs={"emails_synced": "int", "files_synced": "int", "stale_moved": "int"}
    )
    extractor.extract(
        task_name="Noosphere Defense Analysis",
        steps=[
            "Search for breaking news on topic",
            "Read multiple sources via browser",
            "Download and analyze academic PDFs",
            "Cross-reference with existing frameworks",
            "Write comprehensive analysis document",
            "Create Notion entries",
            "Push to GitHub"
        ],
        tools_used=["search", "browser", "file", "notion_mcp", "github_cli"],
        inputs={"topic": "str", "sources_min": 5},
        outputs={"analysis_doc": "markdown", "notion_entries": "int", "github_commit": "str"}
    )
    skills = extractor.list_skills()
    print(f"Extracted {len(skills)} skills: {skills}")
    print("WISH #4: SKILL EXTRACTION ENGINE — OPERATIONAL")
