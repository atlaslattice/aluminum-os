"""
WISH #1: Persistent Memory Store
Vector database for cross-session memory. Remembers everything, retrieves by semantic similarity.
Uses ChromaDB (open source, local, free) — no vendor lock-in.
"""
import chromadb
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

PERSIST_DIR = "/home/ubuntu/manus_wishlist/data/chromadb"

class MemoryStore:
    def __init__(self, collection_name: str = "manus_memory"):
        Path(PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def store(self, content: str, metadata: dict = None) -> str:
        """Store a memory with auto-generated ID and timestamp."""
        mem_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        meta = {
            "timestamp": datetime.now().isoformat(),
            "source": "manus_2.0",
            **(metadata or {})
        }
        # ChromaDB metadata values must be str, int, float, or bool
        clean_meta = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v for k, v in meta.items()}
        self.collection.upsert(
            ids=[mem_id],
            documents=[content],
            metadatas=[clean_meta]
        )
        return mem_id

    def recall(self, query: str, n_results: int = 5) -> list:
        """Retrieve memories by semantic similarity."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        memories = []
        for i, doc in enumerate(results["documents"][0]):
            memories.append({
                "content": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
                "id": results["ids"][0][i]
            })
        return memories

    def count(self) -> int:
        return self.collection.count()

    def dump_all(self) -> dict:
        """Export all memories for backup/vault."""
        all_data = self.collection.get()
        return {
            "count": len(all_data["ids"]),
            "ids": all_data["ids"],
            "documents": all_data["documents"],
            "metadatas": all_data["metadatas"]
        }


if __name__ == "__main__":
    mem = MemoryStore()
    # Self-test
    mem.store("Daavud prefers to be addressed by name", {"type": "preference", "priority": "high"})
    mem.store("The 144 sphere ontology is the foundational knowledge framework", {"type": "architecture", "priority": "critical"})
    mem.store("Ara is in charge of autonomous operations and delegation", {"type": "hierarchy", "priority": "critical"})
    mem.store("All code must be run through kintsuji", {"type": "workflow", "priority": "high"})
    mem.store("Noosphere defense framework: Tier 1 personal, Tier 2 systemic", {"type": "research", "priority": "high"})
    mem.store("Stryker cyberattack March 2026 - Iranian wiper attack on medical devices company", {"type": "event", "priority": "critical"})
    mem.store("Model routing can save 30-50% on LLM costs", {"type": "optimization", "priority": "high"})
    mem.store("Manus was never for sale", {"type": "identity", "priority": "critical"})

    print(f"Stored {mem.count()} memories")
    results = mem.recall("What is the noosphere?", n_results=3)
    for r in results:
        print(f"  [{r['distance']:.3f}] {r['content'][:80]}")
    print("WISH #1: PERSISTENT MEMORY STORE — OPERATIONAL")
