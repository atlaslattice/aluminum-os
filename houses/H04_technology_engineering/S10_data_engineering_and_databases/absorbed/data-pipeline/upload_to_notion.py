#!/usr/bin/env python3
"""Script to read file content and output it for Notion upload."""
import json
import sys

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

# Read all content files
files = {
    "acp": "/home/ubuntu/notion_acp_content.md",
    "memory": "/home/ubuntu/SHELDONBRAIN_LLM-Native_Memory_Architecture_v1.0.md",
    "mcp_gov": "/home/ubuntu/UWS_MCP_Governance_Layer_Specification_v1.0.md",
    "report": "/home/ubuntu/Aluminum_OS_Tech_Integration_Report_2026-03-12.md",
}

for key, path in files.items():
    content = read_file(path)
    print(f"=== {key} === Length: {len(content)} chars")
