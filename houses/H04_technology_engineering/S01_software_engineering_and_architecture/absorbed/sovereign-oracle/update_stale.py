import json

with open("/home/ubuntu/stale_entries.json") as f:
    data = json.load(f)

stale = data["stale_entries"]

# Extract page IDs from URLs
# URL format: https://www.notion.so/30c0c1de73d981cc8b4be1e5519c1a7d
page_ids = []
for entry in stale:
    url = entry["url"]
    page_id = url.split("/")[-1]
    # Format as UUID
    if len(page_id) == 32:
        page_id = f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"
    page_ids.append(page_id)

print(f"Total stale entries to update: {len(page_ids)}")
for pid in page_ids:
    print(f"  {pid}")

with open("/home/ubuntu/stale_page_ids.json", "w") as f:
    json.dump(page_ids, f, indent=2)
