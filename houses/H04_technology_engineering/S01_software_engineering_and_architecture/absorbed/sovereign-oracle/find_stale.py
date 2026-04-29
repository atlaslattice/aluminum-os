import json
from datetime import datetime, timedelta

# Read the full query result
with open("/home/ubuntu/.mcp/tool-results/2026-02-19_06-14-00_notion_notion-query-data-sources.json") as f:
    data = json.load(f)

results = data["results"]
print(f"Total Active entries: {len(results)}")

# Current date
now = datetime.strptime("2026-02-19", "%Y-%m-%d")
cutoff = now - timedelta(days=7)  # 2026-02-12

stale_entries = []
fresh_entries = []

for entry in results:
    last_sync = entry.get("date:Last Sync:start", "")
    if last_sync:
        sync_date = datetime.strptime(last_sync, "%Y-%m-%d")
        if sync_date <= cutoff:
            stale_entries.append(entry)
        else:
            fresh_entries.append(entry)
    else:
        # No last sync date - consider stale
        stale_entries.append(entry)

print(f"Stale entries (>7 days, last sync <= 2026-02-12): {len(stale_entries)}")
print(f"Fresh entries: {len(fresh_entries)}")

# Save stale entry URLs for updating
stale_urls = [e["url"] for e in stale_entries]
with open("/home/ubuntu/stale_entries.json", "w") as f:
    json.dump({"stale_entries": stale_entries, "stale_urls": stale_urls, "count": len(stale_entries)}, f, indent=2)

print("\nStale entries to mark as Deep Sleep:")
for e in stale_entries[:10]:
    print(f"  - {e['Entity/Task']} (Last Sync: {e.get('date:Last Sync:start', 'N/A')})")
if len(stale_entries) > 10:
    print(f"  ... and {len(stale_entries) - 10} more")
