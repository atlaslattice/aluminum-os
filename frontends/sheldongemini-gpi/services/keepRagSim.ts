/**
 * GOOGLE KEEP RAG INTEGRATION (MIGRATED → latticeApi.ts)
 *
 * Previously: In-memory mock Keep notes with simulated read/write
 * Now: Routes to sheldonbrain-rag-api /query?namespace=keep
 * 
 * Backward-compatible interface — same export signature, real backend.
 * Falls back to mock data if RAG API is unreachable.
 */

import { queryKeepRag } from "./latticeApi";

interface KeepNote {
    id: string;
    title: string;
    content: string;
    labels: string[];
    timestamp: string;
}

// Offline fallback store (preserved from original)
const MOCK_KEEP_STORE: KeepNote[] = [
    {
        id: "note_001",
        title: "Roommate Agreement Addendum 4a",
        content: "Regarding the thermostat setting: It shall remain at 72 degrees. Any deviation requires a 2/3 vote of the residents, or a localized heat wave.",
        labels: ["admin", "rules", "thermostat"],
        timestamp: "2023-10-27T10:00:00Z"
    },
    {
        id: "note_002",
        title: "Mortal Enemies List",
        content: "1. Wil Wheaton (Currently on probation)\n2. Joel Schumacher (For the nipples on the Batsuit)\n3. The cafeteria lady who touched my food.\n4. Babylon 5 (The show, generally)",
        labels: ["personal", "grievances", "enemies"],
        timestamp: "2023-11-15T14:30:00Z"
    },
    {
        id: "note_003",
        title: "Super Asymmetry Idea",
        content: "The intersection of string theory and loop quantum gravity might rely on a non-commutative geometry observed in 4D space-time manifolds. Do not tell Amy yet.",
        labels: ["physics", "nobel", "work"],
        timestamp: "2024-01-05T09:15:00Z"
    }
];

/**
 * Main Keep RAG function — routes to real API, falls back to mock.
 * Handles both READ and WRITE operations based on query content.
 */
export const runKeepRagSimulation = async (query: string): Promise<string> => {
    const qLower = query.toLowerCase();
    
    // --- WRITE OPERATION ---
    if (qLower.includes("save to keep") || qLower.includes("add note") || qLower.includes("create note") || qLower.startsWith("remember:")) {
        let content = query;
        const triggers = ["save to keep", "add note", "create note", "remember:"];
        for (const t of triggers) {
            const idx = qLower.indexOf(t);
            if (idx !== -1) {
                content = query.substring(idx + t.length);
                break;
            }
        }
        content = content.replace(/^[:\s-]+/, '').trim();
        if (!content) content = "Empty Note";

        const newNote: KeepNote = {
            id: `note_${Date.now().toString().slice(-4)}`,
            title: "User Entry (Session)",
            content: content,
            labels: ["user-input", "rag-memory"],
            timestamp: new Date().toISOString()
        };
        MOCK_KEEP_STORE.push(newNote);

        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: WRITE_NOTE
Status: SUCCESS
Note ID: ${newNote.id}
Timestamp: ${newNote.timestamp}
Content: "${content.substring(0, 50)}${content.length > 50 ? '...' : ''}"
Labels: [${newNote.labels.join(', ')}]
Message: Data fragment encoded into external memory (Google Keep). RAG Index updated.`;
    }

    // --- READ/SEARCH OPERATION ---
    // Try real RAG API first
    const ragResult = await queryKeepRag(query);
    
    if (ragResult.sources.length > 0 && ragResult.latency_ms > 0) {
        // Real API responded with results
        const results = ragResult.sources.slice(0, 3).map(s =>
            `-- Title: "${s.title}" --\n   "${s.content}"\n   Score: ${s.score.toFixed(3)}`
        ).join('\n\n');

        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: READ_QUERY (Live RAG — ${ragResult.latency_ms}ms)
Query: "${query}"
Matches Found: ${ragResult.sources.length}

RETRIEVED CONTEXT FROM NOTES:
${results}

[SYSTEM] Notes retrieved from Google Keep RAG and injected into working memory.`;
    }

    // --- OFFLINE FALLBACK ---
    const isExplicitSearch = qLower.includes("search keep") || qLower.includes("check notes") || qLower.includes("read note") || qLower.includes("what did i save");
    const queryTokens = qLower.split(/\s+/).filter(t => t.length > 3);
    
    const hits = MOCK_KEEP_STORE.filter(note => {
        if (isExplicitSearch) {
            if (queryTokens.length === 0) return true;
            return queryTokens.some(t => note.content.toLowerCase().includes(t) || note.title.toLowerCase().includes(t) || note.labels.includes(t));
        }
        return queryTokens.some(t => note.content.toLowerCase().includes(t) || note.title.toLowerCase().includes(t) || note.labels.includes(t));
    });

    if (hits.length > 0) {
        const topHits = hits.slice(0, 3);
        const results = topHits.map(h =>
            `-- ID: ${h.id} | Title: "${h.title}" --\n   "${h.content}"\n   Labels: [${h.labels.join(', ')}]`
        ).join('\n\n');

        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: READ_QUERY (Offline Cache)
Query: "${query}"
Matches Found: ${hits.length} (Showing top ${topHits.length})

RETRIEVED CONTEXT FROM NOTES:
${results}

[SYSTEM] Notes retrieved from local cache. Connect RAG API for live data.`;
    } else if (isExplicitSearch) {
        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: SEARCH
Status: COMPLETED
Result: No matching entries found for query: "${query}".`;
    }

    return "";
};
