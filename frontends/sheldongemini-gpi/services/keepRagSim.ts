
/**
 * GOOGLE KEEP RAG INTEGRATION (SIMULATED)
 *
 * Simulates a Read/Write interface with Google Keep to serve as a 
 * Retrieval-Augmented Generation (RAG) layer for the Resident Node.
 */

interface KeepNote {
    id: string;
    title: string;
    content: string;
    labels: string[];
    timestamp: string;
}

// Initial "Sheldon-esque" dataset
// This persists in memory during the session (until page refresh)
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

export const runKeepRagSimulation = (query: string): string => {
    const qLower = query.toLowerCase();
    
    // --- 1. WRITE OPERATION ---
    // Trigger keywords: "save to keep", "create note", "add note", "remember:"
    if (qLower.includes("save to keep") || qLower.includes("add note") || qLower.includes("create note") || qLower.startsWith("remember:")) {
        // Extract content - simplistic extraction logic
        let content = query;
        const triggers = ["save to keep", "add note", "create note", "remember:"];
        for (const t of triggers) {
            const idx = qLower.indexOf(t);
            if (idx !== -1) {
                // Get everything after the trigger
                content = query.substring(idx + t.length);
                break;
            }
        }
        
        // Cleanup content
        content = content.replace(/^[:\s-]+/, '').trim();
        if (!content) content = "Empty Note";

        const newNote: KeepNote = {
            id: `note_${Date.now().toString().slice(-4)}`,
            title: "User Entry (Session)",
            content: content,
            labels: ["user-input", "rag-memory"],
            timestamp: new Date().toISOString()
        };
        
        // "Persist" to simulation store
        MOCK_KEEP_STORE.push(newNote);

        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: WRITE_NOTE
Status: SUCCESS
Note ID: ${newNote.id}
Timestamp: ${newNote.timestamp}
Content: "${content.substring(0, 50)}${content.length > 50 ? '...' : ''}"
Labels: [${newNote.labels.join(', ')}]
Message: Data fragment successfully encoded into external memory (Google Keep). RAG Index updated.`;
    }

    // --- 2. READ/SEARCH OPERATION (RAG) ---
    // Explicit triggers: "search keep", "check notes", "my notes"
    const isExplicitSearch = qLower.includes("search keep") || qLower.includes("check notes") || qLower.includes("read note") || qLower.includes("what did i save");

    // Implicit Search: Tokenize query and check against note content/titles
    // We only return implicit matches if the relevance is high to avoid noise.
    const queryTokens = qLower.split(/\s+/).filter(t => t.length > 3);
    
    const hits = MOCK_KEEP_STORE.filter(note => {
        // 1. Explicit search always matches everything to let LLM filter, or maybe just keyword match
        if (isExplicitSearch) {
             // If user just says "check notes", return everything (limit 3)
             if (queryTokens.length === 0) return true; 
             // Otherwise match keywords
             return queryTokens.some(t => note.content.toLowerCase().includes(t) || note.title.toLowerCase().includes(t) || note.labels.includes(t));
        }

        // 2. Implicit RAG: Only match if significant keywords exist in the note
        // e.g. "Who are my enemies?" matches "enemies" label/content
        return queryTokens.some(t => note.content.toLowerCase().includes(t) || note.title.toLowerCase().includes(t) || note.labels.includes(t));
    });

    if (hits.length > 0) {
        // Limit to top 3 matching notes
        const topHits = hits.slice(0, 3);
        const results = topHits.map(h => 
            `-- ID: ${h.id} | Title: "${h.title}" --\n   "${h.content}"\n   Labels: [${h.labels.join(', ')}]`
        ).join('\n\n');

        return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: READ_QUERY (Vector Search Simulated)
Query: "${query}"
Matches Found: ${hits.length} (Showing top ${topHits.length})

RETRIEVED CONTEXT FROM NOTES:
${results}

[SYSTEM] These notes have been retrieved from Google Keep and injected into your working memory.`;
    } else if (isExplicitSearch) {
         return `[GOOGLE KEEP RAG INTERFACE]
>>> OPERATION: SEARCH
Status: COMPLETED
Result: No matching entries found in the persistent Keep storage for query: "${query}".`;
    }

    // No action triggered
    return "";
};
