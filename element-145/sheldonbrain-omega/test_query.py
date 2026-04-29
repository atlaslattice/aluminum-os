#!/usr/bin/env python3
"""Quick test of vector database queries"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.vector_store_adapter import get_vector_store
from langchain_huggingface import HuggingFaceEmbeddings

print("=" * 70)
print("VECTOR DATABASE QUERY TEST")
print("=" * 70)
print()

# Initialize
print("🔧 Initializing...")
vector_store = get_vector_store(use_vertex=False)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Check stats
stats = vector_store.get_stats()
print(f"📊 Vector Store Stats:")
print(f"   Total vectors: {stats.get('total_vectors', 'unknown')}")
print(f"   Collection: {stats.get('collection', 'unknown')}")
print()

# Test queries
test_queries = [
    "quantum computing algorithms",
    "machine learning models",
    "ancient history",
    "music theory"
]

for query in test_queries:
    print(f"🔍 Query: '{query}'")

    # Generate query embedding
    query_vector = embeddings.embed_query(query)

    # Search
    results = vector_store.search(query_vector, limit=3)

    print(f"   Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        score = result.get('score', 0)
        content_preview = result.get('content', '')[:100]
        metadata = result.get('metadata', {})

        print(f"   {i}. Score: {score:.3f}")
        print(f"      Content: {content_preview}...")
        if metadata.get('title'):
            print(f"      Title: {metadata['title']}")
        if metadata.get('sphere_name'):
            print(f"      Sphere: {metadata['sphere_name']}")
    print()

print("=" * 70)
print("✅ QUERY TEST COMPLETE")
print("=" * 70)
