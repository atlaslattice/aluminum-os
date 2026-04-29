#!/usr/bin/env python3
"""
Google Drive to Notion Sync Script
Processes Google Drive modified files and creates entries in AI-Native OS System RAM database
"""

import json
import hashlib
import subprocess
from datetime import datetime

# Database configuration
DATA_SOURCE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

# Google Drive files modified in last 24 hours
drive_files = [
    {
        "path": "Sheldonbrain/Capital_Factory_Jan28/warm_intro_templates.md",
        "size": 4080,
        "modified": "2026-01-23 06:41:31"
    },
    {
        "path": "Sheldonbrain/Capital_Factory_Jan28/atlas_lattice_one_pager.md",
        "size": 2801,
        "modified": "2026-01-23 06:41:29"
    },
    {
        "path": "Sheldonbrain/Capital_Factory_Jan28/capital_factory_prep.md",
        "size": 6315,
        "modified": "2026-01-23 06:41:27"
    }
]

def create_memory_hash(path, modified):
    """Create a unique hash for deduplication"""
    content = f"{path}|{modified}"
    return hashlib.md5(content.encode()).hexdigest()

def classify_file(path, size):
    """Classify file based on path and properties"""
    path_lower = path.lower()
    
    # Determine Entity Type based on file extension and path
    if any(ext in path_lower for ext in ['.md', '.doc', '.pdf', '.txt']):
        entity_type = "Project"
    else:
        entity_type = "Action"
    
    # Determine Priority based on folder structure and file name
    if 'capital_factory' in path_lower or 'atlas_lattice' in path_lower:
        priority = "High"
    elif 'sheldonbrain' in path_lower:
        priority = "Medium"
    else:
        priority = "Low"
    
    # All drive files are active
    state = "Active"
    
    return state, entity_type, priority

def create_notion_entry(file_data):
    """Create a Notion database entry for a Drive file"""
    path = file_data['path']
    size = file_data['size']
    modified = file_data['modified']
    
    # Extract filename from path
    filename = path.split('/')[-1]
    
    # Create memory hash for deduplication
    memory_hash = create_memory_hash(path, modified)
    
    # Classify file
    state, entity_type, priority = classify_file(path, size)
    
    # Create context stream
    size_kb = size / 1024
    context_stream = f"Path: {path}\nSize: {size_kb:.2f} KB\nModified: {modified}"
    
    # Prepare Notion entry data
    notion_data = {
        "parent": {
            "data_source_id": DATA_SOURCE_ID
        },
        "pages": [
            {
                "properties": {
                    "Entity/Task": f"Drive: {filename}",
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
            print(f"✓ Created entry: Drive: {filename}")
            return True
        else:
            print(f"✗ Failed to create entry: Drive: {filename}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception creating entry: Drive: {filename}")
        print(f"  Error: {str(e)}")
        return False

# Process Drive files
print(f"Processing {len(drive_files)} Google Drive files...")
success_count = 0

for file_data in drive_files:
    if create_notion_entry(file_data):
        success_count += 1

print(f"\n=== Google Drive Sync Complete ===")
print(f"Total files: {len(drive_files)}")
print(f"Created: {success_count}")
