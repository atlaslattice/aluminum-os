#!/usr/bin/env python3
"""
Claude RAG Integration Script
Integrates Claude with Pinecone vector database for context-aware retrieval and responses
"""

import json
import hashlib
import subprocess
from datetime import datetime, timezone
import os

DATA_SOURCE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

def setup_claude_rag():
    """
    Set up Claude RAG integration with Pinecone knowledge base
    
    Architecture:
    1. User query → Generate embedding
    2. Search Pinecone → Retrieve top-K relevant entries
    3. Format context from retrieved entries
    4. Send to Claude with augmented prompt
    5. Return context-aware response
    """
    
    print("=== Claude RAG Integration ===")
    print("\nClaude + Pinecone RAG enables context-aware AI responses")
    print("using your entire AI-Native OS knowledge base.")
    
    # Create configuration entry in Notion
    config_content = """
# Claude RAG Integration Configuration

## Status: Ready for Implementation

Claude RAG integration enables intelligent question-answering using your complete AI-Native OS knowledge base stored in Pinecone.

### Architecture

**RAG Pipeline:**
```
User Query
    ↓
Query Embedding (OpenAI/Cohere)
    ↓
Pinecone Similarity Search (top-K=5-10)
    ↓
Context Formatting
    ↓
Claude API Call (with augmented context)
    ↓
Context-Aware Response
```

### Implementation

#### 1. Query Processing
```python
def query_with_rag(user_query: str, top_k: int = 5):
    # Generate query embedding
    query_embedding = get_embedding(user_query)
    
    # Search Pinecone
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    # Format context
    context = format_context(results)
    
    # Call Claude with context
    response = call_claude_with_context(user_query, context)
    
    return response
```

#### 2. Context Formatting
```python
def format_context(pinecone_results):
    context_parts = []
    
    for match in pinecone_results.matches:
        metadata = match.metadata
        context_parts.append(f\"\"\"
Entry: {metadata['entity_task']}
Type: {metadata['entity_type']}
Priority: {metadata['priority']}
Content: {metadata['context_stream'][:500]}...
---
\"\"\")
    
    return "\\n".join(context_parts)
```

#### 3. Claude API Call
```python
import anthropic

def call_claude_with_context(query, context):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f\"\"\"
Based on the following context from my knowledge base, please answer my question.

Context:
{context}

Question: {query}

Please provide a detailed answer based on the context above. If the context doesn't contain relevant information, say so.
\"\"\"
        }]
    )
    
    return message.content[0].text
```

### Use Cases

#### 1. Email Search
**Query:** "What payment receipts did I receive yesterday?"
- Retrieves: Gmail sync entries with State=Resolved, Entity Type=Action
- Response: Detailed list of payment transactions with amounts and merchants

#### 2. Project Status
**Query:** "What's the status of the Capital Factory preparation?"
- Retrieves: Drive files and related entries about Capital Factory
- Response: Summary of prep materials, timeline, and action items

#### 3. System Operations
**Query:** "When was the last successful sync and what was synced?"
- Retrieves: Sync session logs and operation history
- Response: Detailed sync report with timestamps and entry counts

#### 4. Knowledge Discovery
**Query:** "What do I know about AI-Native OS architecture?"
- Retrieves: System documentation, scripts, and configuration entries
- Response: Comprehensive overview synthesized from all relevant sources

### Advanced Features

#### Hybrid Search (Semantic + Keyword)
```python
# Combine dense (semantic) and sparse (keyword) search
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    filter={
        "$and": [
            {"entity_type": {"$in": ["System", "Project"]}},
            {"priority": {"$in": ["High", "Critical"]}}
        ]
    }
)
```

#### Multi-Turn Conversations
```python
conversation_history = []

def chat_with_rag(user_message):
    # Retrieve relevant context
    context = retrieve_context(user_message)
    
    # Add to conversation
    conversation_history.append({
        "role": "user",
        "content": f"Context: {context}\\n\\nQuestion: {user_message}"
    })
    
    # Call Claude with full history
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=conversation_history
    )
    
    # Add response to history
    conversation_history.append({
        "role": "assistant",
        "content": response.content[0].text
    })
    
    return response.content[0].text
```

#### Citation and Sources
```python
def query_with_sources(user_query):
    results = retrieve_context(user_query)
    
    # Extract sources
    sources = [
        {
            "title": match.metadata['entity_task'],
            "url": match.metadata.get('notion_url'),
            "relevance_score": match.score
        }
        for match in results.matches
    ]
    
    # Generate response
    response = call_claude_with_context(user_query, results)
    
    return {
        "answer": response,
        "sources": sources
    }
```

### Integration Points

#### 1. Web Dashboard
- Add "Ask AI" chat interface
- Real-time RAG-powered responses
- Display source citations

#### 2. Slack/Discord Bot
- Deploy as chatbot
- Query knowledge base via chat
- Team-wide knowledge access

#### 3. API Endpoint
- REST API for RAG queries
- Integrate with other tools
- Programmatic knowledge access

#### 4. Scheduled Reports
- Daily digest of important entries
- Weekly summaries
- Automated insights

### Performance Optimization

**Caching:**
- Cache frequent queries
- Store embeddings for common questions
- Reduce API calls

**Batching:**
- Batch multiple queries
- Parallel Pinecone searches
- Concurrent Claude calls

**Filtering:**
- Pre-filter by entity type
- Time-based filtering
- Priority-based ranking

### Cost Estimation

**Per 1000 queries:**
- Pinecone queries: ~$0.01
- OpenAI embeddings: ~$0.10
- Claude API: ~$3.00 (assuming 1K tokens/response)
- **Total: ~$3.11 per 1000 queries**

### Next Steps

1. ✓ Pinecone index created and populated
2. ✓ Embedding model configured
3. ✓ Claude API key available (ANTHROPIC_API_KEY env var)
4. Implement RAG query function
5. Test with sample queries
6. Integrate into web dashboard
7. Deploy as API endpoint

### Environment Variables Required

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export PINECONE_API_KEY="..."
export OPENAI_API_KEY="..."  # For embeddings
```

### Example Integration

```python
# Simple RAG query
from claude_rag import query_with_rag

response = query_with_rag(
    "What sync operations happened today?",
    top_k=5
)

print(response)
# Output: "Based on your sync logs, today's operations included:
# 1. Gmail sync: 83 emails processed at 11:03 UTC
# 2. Google Drive sync: 3 files updated in Capital_Factory_Jan28 folder
# ..."
```
"""
    
    memory_hash = hashlib.md5(f"claude_rag_config|{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()
    
    notion_data = {
        "parent": {
            "data_source_id": DATA_SOURCE_ID
        },
        "pages": [
            {
                "properties": {
                    "Entity/Task": "Claude RAG Integration - Ready for Implementation",
                    "Context Stream": config_content,
                    "State": "Active",
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
            print("\n✓ Created Claude RAG configuration entry in Notion")
            print("\nClaude RAG is ready to implement!")
            print("\nPrerequisites:")
            print("  ✓ ANTHROPIC_API_KEY environment variable")
            print("  ✓ Pinecone index with knowledge base")
            print("  ✓ Embedding model (OpenAI/Cohere)")
            print("\nNext steps:")
            print("1. Implement RAG query function")
            print("2. Test with sample queries")
            print("3. Integrate into web dashboard")
            return True
        else:
            print(f"\n✗ Failed to create configuration entry")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    setup_claude_rag()
