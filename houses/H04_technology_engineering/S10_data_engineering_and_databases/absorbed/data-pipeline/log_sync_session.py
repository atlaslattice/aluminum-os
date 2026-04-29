#!/usr/bin/env python3
"""
Log Sync Session Script
Creates a sync session entry in the AI-Native OS System RAM database
"""

import json
import hashlib
import subprocess
from datetime import datetime, timezone

# Database configuration
DATA_SOURCE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

# Sync session data
sync_date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Create session summary
session_summary = f"""
AI-Native OS Daily Sync Session
Date: {sync_date}

GMAIL SYNC:
- Total emails processed: 100
- Entries created: 83
- Promotional emails skipped: 17
- Status: ✓ Complete

GOOGLE DRIVE SYNC:
- Files modified (last 24h): 3
- Entries created: 3
- Files synced:
  * warm_intro_templates.md (4.0 KB)
  * atlas_lattice_one_pager.md (2.7 KB)
  * capital_factory_prep.md (6.2 KB)
- Status: ✓ Complete

STATE CONSOLIDATION:
- Total Active entries reviewed: 71
- Stale entries (>7 days): 0
- Recent entries (<=7 days): 71
- Status: ✓ Complete (No stale entries found)

SYNC SESSION STATUS: ✓ SUCCESSFUL
All synchronization tasks completed successfully.
"""

# Create memory hash for session
memory_hash = hashlib.md5(f"sync_session|{sync_date}".encode()).hexdigest()

# Prepare Notion entry data
notion_data = {
    "parent": {
        "data_source_id": DATA_SOURCE_ID
    },
    "pages": [
        {
            "properties": {
                "Entity/Task": f"Daily Sync Session - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
                "Context Stream": session_summary,
                "State": "Resolved",
                "Entity Type": "System",
                "Priority": "Medium",
                "Memory Hash": memory_hash
            }
        }
    ]
}

# Call Notion MCP to create entry
json_input = json.dumps(notion_data)
cmd = [
    'manus-mcp-cli', 'tool', 'call', 'notion-create-pages',
    '--server', 'notion',
    '--input', json_input
]

print("Logging sync session to Notion database...")
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("✓ Sync session logged successfully")
        print(f"\nSession Summary:")
        print(session_summary)
    else:
        print("✗ Failed to log sync session")
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"✗ Exception logging sync session")
    print(f"Error: {str(e)}")
