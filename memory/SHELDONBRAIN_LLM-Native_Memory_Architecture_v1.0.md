# SHELDONBRAIN LLM-Native Memory Consolidation Architecture v1.0

**Author:** Manus AI for Daavud
**Date:** March 12, 2026
**Status:** DRAFT
**Classification:** Tier 1 Implementation Artifact

---

## 1. Executive Summary

The persistence and recall of memory are fundamental to any intelligent agent. The current memory architecture for SHELDONBRAIN, while robust, relies heavily on a traditional RAG (Retrieval-Augmented Generation) pipeline with Pinecone for vector storage. Recent industry developments, most notably Google's open-sourcing of the "Always On Memory Agent" [1] and Microsoft Research's "PlugMem" framework [2], have revealed a more efficient, lightweight, and powerful paradigm: **LLM-Native Memory Consolidation**.

This document specifies a new, hybrid memory architecture for SHELDONBRAIN that embraces this paradigm. We will supplement our existing RAG/Pinecone infrastructure with a new LLM-native memory layer for personal, device-level context. This new layer will handle the high-velocity, ephemeral data of daily user interactions, while the RAG system will continue to serve as the long-term, archival knowledge base for enterprise-scale information.

This evolution will significantly reduce latency for personal context recall, lower operational costs, and align SHELDONBRAIN with the cutting edge of agent memory design.

---

## 2. The Problem with Pure RAG for Personal Memory

A pure RAG architecture, while excellent for querying large, static document corpuses, presents several challenges when used as the primary memory system for a personal AI agent:

-   **Context Bloat**: As noted by Microsoft's PlugMem research, raw interaction logs quickly overwhelm the context window of an LLM, leading to noisy and irrelevant retrievals.
-   **High Latency & Cost**: The process of embedding, indexing, and querying a vector database for every single interaction is computationally expensive and introduces significant latency, making real-time conversational recall difficult.
-   **Loss of Nuance**: Vector search is optimized for semantic similarity, but often misses the causal, temporal, and relational nuances of conversational history.

---

## 3. The Hybrid Architecture: LLM-Native + RAG

To address these challenges, we will implement a two-tiered memory system:

| Tier | Name | Technology | Scope | Use Case |
|---|---|---|---|---|
| **Tier 1** | **Working Memory** | LLM-Native Consolidation (SQLite) | Personal, Device-Local | High-velocity conversational history, short-term tasks, immediate context. |
| **Tier 2** | **Long-Term Memory** | RAG (Pinecone/Vector DB) | Cross-Device, Archival | Enterprise knowledge, documents, web pages, permanent records. |

**SHELDONBRAIN** will now interact with both tiers, using the Working Memory for immediate recall and the Long-Term Memory for deep research or retrieval of archived information.

![Hybrid Memory Architecture Diagram](https://i.imgur.com/example.png)  *Placeholder for architecture diagram to be created*

---

## 4. Tier 1: LLM-Native Working Memory

This tier is directly inspired by Google's Always On Memory Agent, using an LLM to manage its own structured memory in a simple, local database.

### 4.1. Components

-   **Ingestion Agent**: A specialist sub-agent that captures all user interactions (text, voice, UI interactions, etc.) and stores them as raw logs in a temporary buffer.
-   **Consolidation Agent**: The core of the system. This agent runs on a scheduled interval (default: every 30 minutes) and performs the following actions:
    1.  Reads the raw interaction logs from the buffer.
    2.  Uses a low-latency LLM (e.g., Gemini 3.1 Flash-Lite) to "think" about the recent interactions.
    3.  Extracts key entities, facts, relationships, tasks, and user preferences.
    4.  Transforms this information into a structured format (e.g., JSON or key-value pairs).
    5.  Writes the structured memories to a local SQLite database.
    6.  Archives the raw logs and clears the buffer.
-   **Query Agent**: When SHELDONBRAIN needs to recall recent context, this agent queries the SQLite database using natural language, which is then translated to SQL, or by directly retrieving structured data.

### 4.2. Database Schema (SQLite)

The SQLite database will have a simple but flexible schema:

-   `memories` table: `id`, `timestamp`, `type` (e.g., 'fact', 'preference', 'task'), `content` (JSON blob), `source_interaction_id`.
-   `entities` table: `id`, `name`, `type` (e.g., 'person', 'place', 'project').
-   `relationships` table: `id`, `source_entity_id`, `target_entity_id`, `type`.

This structured format allows for much more precise and efficient querying than a vector search over raw text.

---

## 5. The Consolidation Process: From Raw Log to Reusable Knowledge

The magic of this system lies in the consolidation process, which mirrors the approach of Microsoft's PlugMem.

**Prompt for the Consolidation Agent:**

> You are the Consolidation Agent for SHELDONBRAIN. Your task is to review the following raw interaction logs and transform them into structured, reusable knowledge. Extract key facts, user preferences, new tasks, and relationships between entities. Discard conversational filler. Output the result as a JSON object with keys for 'new_facts', 'updated_preferences', 'new_tasks', and 'new_relationships'.
>
> Raw Logs:
> ```
> {{raw_logs}}
> ```

This process effectively uses the LLM's own reasoning capabilities to perform the summarization and structuring that would otherwise require a complex and brittle data processing pipeline.

---

## 6. Integration with Tier 2 (RAG)

The two tiers are not isolated. The Consolidation Agent will also be responsible for identifying memories that have long-term significance and should be promoted to the archival RAG layer.

-   **Promotion Trigger**: After a certain period (e.g., 7 days), or when a project is marked as "complete," the Consolidation Agent can flag memories for promotion.
-   **Summarization for RAG**: Before sending to the RAG pipeline, the agent will generate a high-quality, narrative summary of the relevant memories. This summary, not the raw data, is then embedded and indexed in Pinecone.

This ensures that the Long-Term Memory layer remains a curated, high-signal knowledge base, free from the noise of ephemeral interactions.

---

## 7. Implementation Roadmap

1.  **[Week 1]** Set up the local SQLite database and define the final schema.
2.  **[Week 1]** Develop the Ingestion Agent to capture and buffer raw interaction logs.
3.  **[Week 2]** Develop the Consolidation Agent, including the prompting logic and the process for writing to SQLite. Schedule it to run every 30 minutes.
4.  **[Week 2]** Develop the Query Agent and integrate it into SHELDONBRAIN's main reasoning loop.
5.  **[Week 3]** Implement the promotion logic for moving significant memories from Tier 1 to Tier 2.
6.  **[Week 4]** Begin benchmarking the new hybrid system against the pure RAG architecture for latency, cost, and quality of recall.

---

## 8. References

[1] Franzen, Carl. "Google PM open-sources Always On Memory Agent, ditching vector databases for LLM-driven persistent memory." VentureBeat, March 6, 2026.
[2] Microsoft Research. "From raw interaction to reusable knowledge: Rethinking memory for AI agents." Microsoft Research Blog, March 10, 2026.
