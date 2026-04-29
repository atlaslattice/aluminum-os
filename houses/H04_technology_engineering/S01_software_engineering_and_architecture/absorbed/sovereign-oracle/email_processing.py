import hashlib
import json

# Raw emails from the last 24 hours
emails = [
    {"subject": "Your ride with Andilay on February 19", "from": "Lyft Receipts", "date": "Thu, 19 Feb 2026 07:43:27 +0000", "body_snippet": "Lyft", "message_id": "19c74da95677999f"},
    {"subject": "Payment sent", "from": "Cash App", "date": "Thu, 19 Feb 2026 07:43:09 +0000", "body_snippet": "You paid Andilay torres Pereira $20 for a", "message_id": "19c74da4f6979e91"},
    {"subject": "Your ride with Eliana on February 18", "from": "Lyft Receipts", "date": "Thu, 19 Feb 2026 06:56:03 +0000", "body_snippet": "Lyft", "message_id": "19c74af31ab43c8f"},
    {"subject": "You paid off your Pay Over Time plan for a purchase on card (...3271)", "from": "Chase", "date": "Thu, 19 Feb 2026 05:47:29 +0000", "body_snippet": "MCP Completion", "message_id": "19c74706f95e85c8"},
    {"subject": "Your family order from Best Buy is confirmed for February 19", "from": "Instacart", "date": "Thu, 19 Feb 2026 03:34:21 +0000", "body_snippet": "Hi Dave, your family order from Best Buy is all set.", "message_id": "19c73f68c012437d"},
    {"subject": "Tell us how we did", "from": "Instacart", "date": "Thu, 19 Feb 2026 03:29:56 +0000", "body_snippet": "How was your order on February 18th?", "message_id": "19c73f27f2600592"},
    {"subject": "Goldenvoice Presents April 2026 is here", "from": "Goldenvoice", "date": "Wed, 18 Feb 2026 20:37:56 -0600", "body_snippet": "", "message_id": "19c73c7ca1dd51d0"},
    {"subject": "Michael Sitarzewski recently posted", "from": "LinkedIn", "date": "Thu, 19 Feb 2026 02:15:27 +0000", "body_snippet": "LinkedIn network conversations", "message_id": "19c73ae593f78636"},
    {"subject": "You have 2 new messages", "from": "LinkedIn", "date": "Thu, 19 Feb 2026 01:08:23 +0000", "body_snippet": "You have 2 new messages", "message_id": "19c7370e9938ae29"},
    {"subject": "Action Item from Paraag Kumar at One Medical", "from": "One Medical", "date": "Wed, 18 Feb 2026 16:47:32 -0800", "body_snippet": "Hi David,", "message_id": "19c735dce52cf532"},
    {"subject": "Run hundreds of agents in parallel", "from": "Petra from Warp", "date": "Thu, 19 Feb 2026 00:46:35 +0000", "body_snippet": "Run hundreds of agents in parallel", "message_id": "19c735cee483e4cd"},
    {"subject": "Your Instacart family order receipt", "from": "Instacart", "date": "Thu, 19 Feb 2026 00:35:01 +0000", "body_snippet": "Thanks for ordering from Instacart!", "message_id": "19c73525d69ec8e7"},
    {"subject": "Action Item from Paraag Kumar at One Medical", "from": "One Medical", "date": "Wed, 18 Feb 2026 16:26:27 -0800", "body_snippet": "Hi David,", "message_id": "19c734a81a09695c"},
    {"subject": "Jeremy Moreland posted an update", "from": "Jeremy on Facebook", "date": "Wed, 18 Feb 2026 16:24:06 -0800", "body_snippet": "Hi David,", "message_id": "19c73486f0e9e6fe"},
    {"subject": "Your ride with Jorge on February 18", "from": "Lyft Receipts", "date": "Thu, 19 Feb 2026 00:17:26 +0000", "body_snippet": "Lyft", "message_id": "19c734242bb5b5d4"},
    {"subject": "You spent $140.50 at Smoking Depot Lama", "from": "Cash App", "date": "Thu, 19 Feb 2026 00:03:33 +0000", "body_snippet": "You spent $140.50 at Smoking Depot Lama.", "message_id": "19c73358879311da"},
    {"subject": "Your ride with Alexis on February 18", "from": "Lyft Receipts", "date": "Wed, 18 Feb 2026 23:47:41 +0000", "body_snippet": "Lyft", "message_id": "19c732701c54be65"},
    {"subject": "Action Item from Paraag Kumar at One Medical", "from": "One Medical", "date": "Wed, 18 Feb 2026 15:28:41 -0800", "body_snippet": "Hi David,", "message_id": "19c73159ea4343c3"},
    {"subject": "New Online Account: Welcome, Dave Sheldon!", "from": "Greater Austin YMCA", "date": "Wed, 18 Feb 2026 22:39:49 +0000", "body_snippet": "Your Receipt", "message_id": "19c72e8e38446f13"},
    {"subject": "Your family order from Costco is confirmed for February 18", "from": "Instacart", "date": "Wed, 18 Feb 2026 22:29:55 +0000", "body_snippet": "Hi Dave, your family order from Costco is all set.", "message_id": "19c72dfd4d321729"},
    {"subject": "David, is it time to lower your 79% credit usage?", "from": "Experian", "date": "Wed, 18 Feb 2026 16:29:22 -0600", "body_snippet": "Experian", "message_id": "19c72df5df5a8dab"},
    {"subject": "The total for your transaction at Lime Ride has been updated from $2.81 to $17.89", "from": "Cash App", "date": "Wed, 18 Feb 2026 22:22:21 +0000", "body_snippet": "The total for your transaction at Lime Ride has been updated from $2.81 to $17.89.", "message_id": "19c72d8defbddfb6"},
    {"subject": "We've updated our user agreements", "from": "Lyft", "date": "Wed, 18 Feb 2026 22:06:17 +0000", "body_snippet": "Lyft", "message_id": "19c72ca2a9f98428"},
    {"subject": "Reminder: Advanced Website and CRO Training Tomorrow", "from": "SuperCool", "date": "Wed, 18 Feb 2026 22:05:28 +0000", "body_snippet": "February 19th Bootcamp", "message_id": "19c72c96fc91748d"},
    {"subject": "Google Calendar mentioned you in #Google Calendar", "from": "Slack", "date": "Wed, 18 Feb 2026 21:48:55 +0000", "body_snippet": "Hi therealdavesheldon,", "message_id": "19c72ba431ac54e4"},
]

# Filter: Remove marketing/spam/newsletters per user preference
# Keep: directly relevant, personally addressed, actionable emails
# Remove: LinkedIn digests, Facebook updates, marketing promos, newsletter-style, generic surveys, user agreement updates

SPAM_KEYWORDS = ["recently posted", "posted an update", "is it time to lower", "updated our user agreements", "run hundreds of agents"]
SPAM_SENDERS = ["LinkedIn", "Jeremy on Facebook", "Experian", "Petra from Warp", "Goldenvoice"]

def is_spam(email):
    if email["from"] in SPAM_SENDERS:
        return True
    for kw in SPAM_KEYWORDS:
        if kw.lower() in email["subject"].lower():
            return True
    return False

# Filter out feedback surveys too
def is_survey(email):
    return "tell us how we did" in email["subject"].lower() or "how was your" in email["body_snippet"].lower()

# Load existing hashes
with open("/home/ubuntu/existing_hashes.txt") as f:
    existing_hashes = set(line.strip() for line in f if line.strip())

# Process significant emails
significant_emails = []
for email in emails:
    if is_spam(email) or is_survey(email):
        continue
    
    # Generate memory hash from message_id
    raw = f"{email['message_id']}"
    mem_hash = hashlib.md5(raw.encode()).hexdigest()
    
    # Check dedup
    if mem_hash in existing_hashes:
        continue
    
    # Classify state
    subject_lower = email["subject"].lower()
    body_lower = email["body_snippet"].lower()
    combined = subject_lower + " " + body_lower
    
    if any(kw in combined for kw in ["receipt", "paid off", "confirmed", "welcome", "payment received"]):
        state = "Resolved"
    elif any(kw in combined for kw in ["failed", "declined", "blocked", "negative", "canceled"]):
        state = "Blocked"
    else:
        state = "Active"
    
    # Classify entity type
    if any(kw in combined for kw in ["action item", "reminder", "mentioned you", "new messages"]):
        entity_type = "Action"
    elif any(kw in combined for kw in ["ride", "order", "transaction", "payment", "spent", "receipt", "account"]):
        entity_type = "System"
    elif any(kw in combined for kw in ["from paraag", "from jonathan"]):
        entity_type = "Person"
    else:
        entity_type = "System"
    
    # Classify priority
    if any(kw in combined for kw in ["urgent", "action required", "action item", "critical"]):
        priority = "Critical"
    elif any(kw in combined for kw in ["important", "failed", "declined", "blocked", "negative"]):
        priority = "High"
    elif any(kw in combined for kw in ["update", "confirmed", "reminder", "mentioned"]):
        priority = "Medium"
    else:
        priority = "Low"
    
    # Build context stream
    context = f"From: {email['from']} | Date: {email['date']} | Snippet: {email['body_snippet'][:100]}"
    
    significant_emails.append({
        "subject": email["subject"],
        "context": context,
        "state": state,
        "entity_type": entity_type,
        "priority": priority,
        "memory_hash": mem_hash,
        "message_id": email["message_id"]
    })

print(f"Total emails: {len(emails)}")
print(f"Filtered (spam/survey): {sum(1 for e in emails if is_spam(e) or is_survey(e))}")
print(f"Significant emails to sync: {len(significant_emails)}")
print()

for i, e in enumerate(significant_emails):
    print(f"{i+1}. [{e['state']}] [{e['priority']}] [{e['entity_type']}] {e['subject']}")
    print(f"   Hash: {e['memory_hash']}")

# Save for use in next step
with open("/home/ubuntu/emails_to_sync.json", "w") as f:
    json.dump(significant_emails, f, indent=2)
