#!/usr/bin/env python3
"""
Pinecone RAG Integration Script
Stores AI-Native OS knowledge in Pinecone vector database for semantic search and retrieval
"""

import json
import hashlib
import subprocess
from datetime import datetime, timezone
import sys
import os

DATA_SOURCE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

# Check if pinecone is installed
try:
    from pinecone import Pinecone, ServerlessSpec
except ImportError:
    print("Installing pinecone-client library...")
    subprocess.run(["sudo", "pip3", "install", "pinecone-client"], check=True)
    from pinecone import Pinecone, ServerlessSpec

def setup_pinecone_rag():
    """
    Set up Pinecone RAG integration for AI-Native OS knowledge storage
    
    Requirements:
    1. Pinecone API key (from pinecone.io console)
    2. Index name for knowledge storage
    3. Embedding model (OpenAI, Cohere, or custom)
    
    Architecture:
    - Notion entries → Generate embeddings → Store in Pinecone
    - Query → Generate query embedding → Search Pinecone → Retrieve relevant entries
    - Claude RAG → Use Pinecone results for context-aware responses
    """
    
    print("=== Pinecone RAG Integration ===")
    print("\nPinecone Configuration Required:")
    print("1. API Key: Get from https://app.pinecone.io/")
    print("2. Environment: Specify cloud region (e.g., 'us-east-1-aws')")
    print("3. Index Name: Choose a name for your knowledge base")
    print("4. Embedding Model: OpenAI ada-002, Cohere, or custom")
    
    # Create configuration entry in Notion
    config_content = """
# Pinecone RAG Integration Configuration

## Status: Pending API Key Setup

Pinecone vector database integration enables semantic search and retrieval across all AI-Native OS knowledge.

### Architecture Overview

**Data Flow:**
1. **Ingestion**: Notion entries → Text extraction → Chunking
2. **Embedding**: Text chunks → Embedding model → Vectors (1536-dim for OpenAI)
3. **Storage**: Vectors + metadata → Pinecone index
4. **Retrieval**: Query → Query embedding → Similarity search → Top-K results
5. **RAG**: Retrieved context → Claude/LLM → Enhanced responses

### Configuration Steps

#### 1. Create Pinecone Account
- Sign up at https://www.pinecone.io/
- Create new project
- Generate API key from console

#### 2. Create Index
```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="YOUR_API_KEY")

# Create serverless index
pc.create_index(
    name="ai-native-os-knowledge",
    dimension=1536,  # OpenAI ada-002 dimension
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
```

#### 3. Data Mapping

**Pinecone Vector Structure:**
- **id**: Unique identifier (Memory Hash or Notion page ID)
- **values**: Embedding vector (1536-dim array)
- **metadata**: {
    - entity_task: str
    - context_stream: str (truncated for metadata size limits)
    - state: str
    - entity_type: str
    - priority: str
    - notion_url: str
    - created_at: timestamp
    - last_sync: timestamp
  }

#### 4. Embedding Models

**Option A: OpenAI (Recommended)**
- Model: text-embedding-ada-002
- Dimension: 1536
- Cost: $0.0001 per 1K tokens
- Quality: High

**Option B: Cohere**
- Model: embed-english-v3.0
- Dimension: 1024
- Cost: Free tier available
- Quality: High

**Option C: Open Source**
- Model: sentence-transformers/all-MiniLM-L6-v2
- Dimension: 384
- Cost: Free (local)
- Quality: Good

### Implementation Plan

1. **Phase 1: Setup**
   - Configure Pinecone API key
   - Create index with appropriate dimensions
   - Set up embedding model

2. **Phase 2: Initial Load**
   - Query all Notion entries
   - Generate embeddings for existing data
   - Bulk upsert to Pinecone (batches of 100)

3. **Phase 3: Incremental Sync**
   - Sync new/updated Notion entries daily
   - Update Pinecone vectors for modified entries
   - Delete vectors for removed entries

4. **Phase 4: Query Interface**
   - Implement semantic search API
   - Integrate with Claude for RAG responses
   - Add to web dashboard

### Usage Examples

**Semantic Search:**
```python
# Query: "What emails did I receive about payments?"
query_embedding = get_embedding("payment emails recent")
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    filter={"entity_type": "Action"}
)
```

**RAG with Claude:**
```python
# Retrieve relevant context
context = retrieve_from_pinecone(user_query)

# Augment Claude prompt
prompt = f\"\"\"
Context from knowledge base:
{context}

User question: {user_query}

Please answer based on the context above.
\"\"\"

response = claude.generate(prompt)
```

### Cost Estimation

**For 10,000 entries:**
- Storage: ~$0.10/month (Pinecone serverless)
- Embeddings: ~$0.50 one-time (OpenAI)
- Queries: ~$0.01/1000 queries

### Next Steps

1. Obtain Pinecone API key
2. Choose embedding model
3. Run initial data load
4. Test semantic search
5. Integrate with Claude RAG
"""
    
    memory_hash = hashlib.md5(f"pinecone_rag_config|{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()
    
    notion_data = {
        "parent": {
            "data_source_id": DATA_SOURCE_ID
        },
        "pages": [
            {
                "properties": {
                    "Entity/Task": "Pinecone RAG Integration - Configuration Required",
                    "Context Stream": config_content,
                    "State": "Blocked",
                    "Entity Type": "System",
                    "Priority": "High",
                    "Memory Hash": memory_hash
                }
            }
        ]
    }
    
    json_input = json.dumps(notion_data)
    cmd = [
        'manus-mcp-cli', 'tool', 'call', 'notion-create-pages',
        '--server', 'notion',
        '--input', json_input
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("\n✓ Created Pinecone RAG configuration entry in Notion")
            print("\nNext steps:")
            print("1. Sign up at https://www.pinecone.io/")
            print("2. Create API key")
            print("3. Configure embedding model (OpenAI recommended)")
            print("4. Run initial data load script")
            return True
        else:
            print(f"\n✗ Failed to create configuration entry")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    setup_pinecone_rag()
