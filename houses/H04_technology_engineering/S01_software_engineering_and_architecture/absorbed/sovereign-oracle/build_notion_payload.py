import json

with open("/home/ubuntu/emails_to_sync.json") as f:
    emails = json.load(f)

# Deduplicate the 3 "Action Item from Paraag Kumar" - keep the most recent one
seen_subjects = {}
deduped = []
for e in emails:
    key = e["subject"]
    if key in seen_subjects:
        # Keep the one already added (first = most recent since sorted by date desc)
        continue
    seen_subjects[key] = True
    deduped.append(e)

emails = deduped
print(f"After subject dedup: {len(emails)} emails")

pages = []
for e in emails:
    page = {
        "properties": {
            "Entity/Task": e["subject"],
            "Context Stream": e["context"],
            "Entity Type": e["entity_type"],
            "State": e["state"],
            "Priority": e["priority"],
            "Memory Hash": e["memory_hash"],
            "date:Last Sync:start": "2026-02-19",
            "date:Last Sync:is_datetime": 0
        }
    }
    pages.append(page)

payload = {
    "parent": {"data_source_id": "add65d86-00d0-46c6-b97b-c0924a94512f"},
    "pages": pages
}

with open("/home/ubuntu/gmail_notion_payload.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"Payload created with {len(pages)} pages")
for p in pages:
    print(f"  - {p['properties']['Entity/Task']} [{p['properties']['State']}] [{p['properties']['Priority']}]")
