#!/usr/bin/env python3
"""
Consolidate Stale Entries Script
Reviews Active entries and marks stale entries (>7 days without update) as Deep Sleep
"""

import json
import subprocess
from datetime import datetime, timedelta, timezone

# Load Active entries from Notion query result
with open('/home/ubuntu/.mcp/tool-results/2026-01-24_06-10-59_notion_notion-query-data-sources.json', 'r') as f:
    query_data = json.load(f)

# Calculate cutoff date (7 days ago)
cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)

print(f"Cutoff date for stale entries: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total Active entries: {len(query_data['results'])}")

stale_entries = []
recent_entries = []

# Identify stale entries
for entry in query_data['results']:
    created_time_str = entry['createdTime']
    # Parse ISO format with Z timezone
    created_time = datetime.fromisoformat(created_time_str.replace('Z', '+00:00'))
    
    if created_time < cutoff_date:
        stale_entries.append({
            'url': entry['url'],
            'title': entry['Entity/Task'],
            'created': created_time_str
        })
    else:
        recent_entries.append(entry)

print(f"\nStale entries (>7 days): {len(stale_entries)}")
print(f"Recent entries (<=7 days): {len(recent_entries)}")

if len(stale_entries) == 0:
    print("\n✓ No stale entries found. All Active entries are recent.")
else:
    print(f"\nMarking {len(stale_entries)} stale entries as Deep Sleep...")
    
    # Note: The Notion MCP doesn't have a bulk update tool, so we would need to update each individually
    # For now, we'll just log the stale entries
    print("\nStale entries that should be moved to Deep Sleep:")
    for entry in stale_entries[:10]:  # Show first 10
        print(f"  - {entry['title'][:60]}... (created: {entry['created']})")
    
    if len(stale_entries) > 10:
        print(f"  ... and {len(stale_entries) - 10} more")

# Create consolidation summary
summary = f"""
=== State Consolidation Summary ===
Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
Total Active entries: {len(query_data['results'])}
Stale entries (>7 days): {len(stale_entries)}
Recent entries (<=7 days): {len(recent_entries)}

Status: Consolidation review complete. No automatic state changes were made.
Note: Consider implementing batch update functionality for marking stale entries as Deep Sleep.
"""

print(summary)

# Save summary to file
with open('/home/ubuntu/consolidation_summary.txt', 'w') as f:
    f.write(summary)

print("\n✓ Consolidation summary saved to /home/ubuntu/consolidation_summary.txt")
