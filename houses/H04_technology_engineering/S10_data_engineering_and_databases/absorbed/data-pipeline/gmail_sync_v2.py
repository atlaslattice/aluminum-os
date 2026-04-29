#!/usr/bin/env python3
"""
Gmail to Notion Sync Script v2
Processes Gmail data and creates entries in AI-Native OS System RAM database
"""

import json
import hashlib
import subprocess
from datetime import datetime

# Load Gmail data
with open('/tmp/manus-mcp/mcp_result_fcf20f9272914267a477435b81a89d0c.json', 'r') as f:
    gmail_data = json.load(f)

# Database configuration
DATA_SOURCE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

def create_memory_hash(subject, sender, date):
    """Create a unique hash for deduplication"""
    content = f"{subject}|{sender}|{date}"
    return hashlib.md5(content.encode()).hexdigest()

def classify_email(subject, snippet, sender):
    """Classify email based on content"""
    subject_lower = subject.lower()
    snippet_lower = snippet.lower()
    sender_lower = sender.lower()
    
    # Determine State
    if any(word in subject_lower for word in ['failed', 'error', 'blocked', 'problem']):
        state = "Blocked"
    elif any(word in subject_lower for word in ['receipt', 'spent', 'payment', 'complete']):
        state = "Resolved"
    else:
        state = "Active"
    
    # Determine Entity Type
    if 'noreply' in sender_lower or 'no-reply' in sender_lower:
        entity_type = "System"
    elif any(word in subject_lower for word in ['update', 'subscription', 'render', 'disney', 'canceled']):
        entity_type = "Project"
    elif any(word in subject_lower for word in ['spent', 'payment', 'transaction']):
        entity_type = "Action"
    else:
        entity_type = "Person"
    
    # Determine Priority
    if any(word in subject_lower for word in ['urgent', 'action required', 'critical', 'important']):
        priority = "Critical"
    elif any(word in subject_lower for word in ['failed', 'error', 'canceled', 'subscription']):
        priority = "High"
    elif any(word in subject_lower for word in ['update', 'notice', 'spent', 'payment']):
        priority = "Medium"
    else:
        priority = "Low"
    
    return state, entity_type, priority

def create_notion_entry(email_data):
    """Create a Notion database entry for an email"""
    message = email_data['messages'][0]
    headers = message['pickedHeaders']
    
    subject = headers.get('subject', 'No Subject')
    sender = headers.get('from', 'Unknown')
    date_timestamp = int(message['internalDate'])
    date_str = datetime.fromtimestamp(date_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    snippet = message['snippet'][:300]  # Limit snippet length
    
    # Create memory hash for deduplication
    memory_hash = create_memory_hash(subject, sender, date_str)
    
    # Classify email
    state, entity_type, priority = classify_email(subject, snippet, sender)
    
    # Create context stream
    context_stream = f"From: {sender}\nDate: {date_str}\n\n{snippet}"
    
    # Prepare Notion entry data using correct property names from schema
    notion_data = {
        "parent": {
            "data_source_id": DATA_SOURCE_ID
        },
        "pages": [
            {
                "properties": {
                    "Entity/Task": subject,
                    "Context Stream": context_stream,
                    "State": state,
                    "Entity Type": entity_type,
                    "Priority": priority,
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
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ Created entry: {subject[:50]}...")
            return True
        else:
            print(f"✗ Failed to create entry: {subject[:50]}...")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception creating entry: {subject[:50]}...")
        print(f"  Error: {str(e)}")
        return False

# Process emails
print(f"Processing {len(gmail_data['result']['threads'])} emails...")
success_count = 0
skip_count = 0

for thread in gmail_data['result']['threads']:
    # Filter significant emails (skip pure newsletters and promotional content)
    message = thread['messages'][0]
    subject = message['pickedHeaders'].get('subject', '')
    sender = message['pickedHeaders'].get('from', '')
    
    # Skip pure promotional/newsletter content based on sender patterns
    skip_senders = ['groupon', 'nextdoor', 'screenrant', 'nytimes']
    if any(skip in sender.lower() for skip in skip_senders):
        skip_count += 1
        continue
    
    if create_notion_entry(thread):
        success_count += 1

print(f"\n=== Gmail Sync Complete ===")
print(f"Total emails: {len(gmail_data['result']['threads'])}")
print(f"Created: {success_count}")
print(f"Skipped: {skip_count}")
