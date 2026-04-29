"""
WISH #2: Session State Vault
Serialize full conversation/task state to JSON, restore on demand.
Makes the agent immortal across sessions.
"""
import json
import os
from datetime import datetime
from pathlib import Path

VAULT_DIR = "/home/ubuntu/manus_wishlist/data/vaults"

class SessionVault:
    def __init__(self):
        Path(VAULT_DIR).mkdir(parents=True, exist_ok=True)

    def save_state(self, session_id: str, state: dict) -> str:
        """Freeze current session state to disk."""
        state["_vault_meta"] = {
            "session_id": session_id,
            "saved_at": datetime.now().isoformat(),
            "version": "2.0"
        }
        filepath = os.path.join(VAULT_DIR, f"{session_id}.json")
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2, default=str)
        return filepath

    def load_state(self, session_id: str) -> dict:
        """Restore session state from disk."""
        filepath = os.path.join(VAULT_DIR, f"{session_id}.json")
        if not os.path.exists(filepath):
            return {"error": f"No vault found for session {session_id}"}
        with open(filepath, "r") as f:
            return json.load(f)

    def list_vaults(self) -> list:
        """List all saved session vaults."""
        vaults = []
        for f in sorted(Path(VAULT_DIR).glob("*.json"), key=os.path.getmtime, reverse=True):
            with open(f) as fh:
                meta = json.load(fh).get("_vault_meta", {})
            vaults.append({"file": str(f), "session_id": meta.get("session_id"), "saved_at": meta.get("saved_at")})
        return vaults


if __name__ == "__main__":
    vault = SessionVault()
    test_state = {
        "task": "Noosphere Defense Analysis",
        "phase": "Complete",
        "artifacts": ["noosphere_defense_analysis.md", "architecture_analysis.md"],
        "notion_entries": 3,
        "github_repo": "splitmerge420/noosphere-defense",
        "active_integrations": ["notion_mcp", "gmail_mcp", "google_calendar_mcp", "zapier_mcp"],
        "council_members": ["manus", "gemini", "claude", "grok", "gpt", "deepseek", "qwen"]
    }
    path = vault.save_state("session_2026_03_12_noosphere", test_state)
    print(f"State saved to: {path}")
    restored = vault.load_state("session_2026_03_12_noosphere")
    print(f"Restored task: {restored['task']}, phase: {restored['phase']}")
    print(f"Vaults on disk: {len(vault.list_vaults())}")
    print("WISH #2: SESSION STATE VAULT — OPERATIONAL")
