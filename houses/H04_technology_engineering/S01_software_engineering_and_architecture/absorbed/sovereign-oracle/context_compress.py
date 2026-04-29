"""
WISH #5: Context Compression
Intelligent summarization of long conversations to preserve signal, discard noise.
Keeps the agent sharp without losing critical info.
"""
import json
import os
import hashlib
from datetime import datetime

class ContextCompressor:
    def __init__(self, max_tokens_estimate: int = 50000):
        self.max_tokens = max_tokens_estimate
        self.compression_log = []

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimate: ~4 chars per token."""
        return len(text) // 4

    def compress(self, messages: list, preserve_tags: list = None) -> dict:
        """Compress a conversation, preserving tagged/critical messages."""
        preserve_tags = preserve_tags or ["critical", "decision", "artifact", "user_preference"]
        total_tokens = sum(self.estimate_tokens(m.get("content", "")) for m in messages)

        if total_tokens <= self.max_tokens:
            return {"compressed": False, "messages": messages, "tokens": total_tokens}

        preserved = []
        compressible = []
        for m in messages:
            tags = m.get("tags", [])
            if any(t in preserve_tags for t in tags) or m.get("role") == "user":
                preserved.append(m)
            else:
                compressible.append(m)

        # Group compressible messages into chunks and summarize
        summaries = []
        chunk = []
        chunk_tokens = 0
        for m in compressible:
            t = self.estimate_tokens(m.get("content", ""))
            if chunk_tokens + t > 2000:
                summaries.append(self._summarize_chunk(chunk))
                chunk = []
                chunk_tokens = 0
            chunk.append(m)
            chunk_tokens += t
        if chunk:
            summaries.append(self._summarize_chunk(chunk))

        compressed_messages = []
        summary_idx = 0
        for m in messages:
            if m in preserved:
                compressed_messages.append(m)
            elif summary_idx < len(summaries):
                compressed_messages.append({
                    "role": "system",
                    "content": f"[COMPRESSED] {summaries[summary_idx]}",
                    "tags": ["compressed"]
                })
                summary_idx += 1

        new_tokens = sum(self.estimate_tokens(m.get("content", "")) for m in compressed_messages)
        self.compression_log.append({
            "timestamp": datetime.now().isoformat(),
            "original_tokens": total_tokens,
            "compressed_tokens": new_tokens,
            "ratio": round(new_tokens / total_tokens, 2) if total_tokens > 0 else 1.0,
            "messages_preserved": len(preserved),
            "chunks_compressed": len(summaries)
        })

        return {
            "compressed": True,
            "messages": compressed_messages,
            "original_tokens": total_tokens,
            "compressed_tokens": new_tokens,
            "savings_pct": round((1 - new_tokens / total_tokens) * 100, 1) if total_tokens > 0 else 0
        }

    def _summarize_chunk(self, messages: list) -> str:
        """Extract key points from a chunk of messages."""
        contents = [m.get("content", "")[:200] for m in messages]
        key_points = []
        for c in contents:
            if len(c.strip()) > 20:
                key_points.append(c.strip()[:150])
        if not key_points:
            return "No significant content in this segment."
        return "Key points: " + " | ".join(key_points[:5])


if __name__ == "__main__":
    compressor = ContextCompressor(max_tokens_estimate=500)
    test_messages = [
        {"role": "user", "content": "Run the daily sync", "tags": ["critical"]},
        {"role": "assistant", "content": "Starting Gmail sync. Fetching emails from last 24 hours..." * 20, "tags": []},
        {"role": "assistant", "content": "Found 25 emails. Filtering spam..." * 15, "tags": []},
        {"role": "assistant", "content": "Created 15 Notion entries successfully.", "tags": ["artifact"]},
        {"role": "assistant", "content": "Checking Google Drive for changes..." * 10, "tags": []},
        {"role": "assistant", "content": "No Drive changes found.", "tags": ["decision"]},
        {"role": "user", "content": "Now do the noosphere analysis", "tags": ["critical"]},
    ]
    result = compressor.compress(test_messages)
    print(f"Compressed: {result['compressed']}")
    if result['compressed']:
        print(f"Savings: {result['savings_pct']}% ({result['original_tokens']} -> {result['compressed_tokens']} tokens)")
    print(f"Messages: {len(test_messages)} -> {len(result['messages'])}")
    print("WISH #5: CONTEXT COMPRESSION — OPERATIONAL")
