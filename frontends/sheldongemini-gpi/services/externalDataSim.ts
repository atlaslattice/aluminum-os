/**
 * EXTERNAL DATA SERVICE (MIGRATED → latticeApi.ts)
 * 
 * Previously: Hardcoded mock Notion pages + Pinecone vectors
 * Now: Routes to sheldonbrain-rag-api via latticeApi.ts
 * 
 * Backward-compatible interface — same function signatures, real backend.
 * Falls back to mock data if API is unreachable.
 */

import { queryNotionRag, queryRag } from "./latticeApi";

// ─── Fallback mock data (preserved for offline mode) ─────────────────────────

const MOCK_NOTION_PAGES = [
    { id: 'n-01', title: 'Weekly Schedule', content: 'Monday: Thai Food. Tuesday: Cheesecake Factory. Wednesday: Halo Night. Thursday: Anything but Pizza. Friday: Vintage Game Night. Saturday: Laundry (8:15 PM sharp). Sunday: Pranking Kripke.' },
    { id: 'n-02', title: 'Project: Picard', content: 'Objective: Integrate Starfleet-level voice commands into the Sheldon-AI interface. Status: In Progress.' },
    { id: 'n-03', title: 'Fun with Flags Scripts', content: 'Episode 409: The Flags of the Federated States of Micronesia.' },
    { id: 'n-04', title: 'Apartment Flag Status', content: 'Current Status: Right side up. Distress level: Zero.' }
];

const MOCK_PINECONE_VECTORS = [
    { id: 'v-99', score: 0.98, metadata: 'Long-term Memory: The time Penny touched my food (Incident #402).' },
    { id: 'v-98', score: 0.95, metadata: 'Fact: The exact seating coordinates of "My Spot" are 0,0,0.' },
    { id: 'v-97', score: 0.92, metadata: "Secret: Grandmother Meemaw's cookie recipe (Classified)." },
    { id: 'v-96', score: 0.89, metadata: "Schrödinger's Cat: quantum superposition paradox." }
];

// ─── Migrated functions ──────────────────────────────────────────────────────

/**
 * Search Notion via RAG API. Falls back to mock if offline.
 */
export const searchNotion = async (query: string): Promise<string> => {
    const result = await queryNotionRag(query);
    
    // If API returned real results, format them
    if (result.sources.length > 0) {
        return `[NOTION RAG] Retrieved ${result.sources.length} results:\n` +
            result.sources.map(s => `- Title: "${s.title}"\n  Content: "${s.content}" (score: ${s.score.toFixed(2)})`).join('\n\n');
    }
    
    // Fallback to mock data for offline mode
    const q = query.toLowerCase();
    const hits = MOCK_NOTION_PAGES.filter(p => 
        p.title.toLowerCase().includes(q) || p.content.toLowerCase().includes(q)
    );
    
    if (hits.length === 0) {
        if (q.includes('schedule')) {
            const sched = MOCK_NOTION_PAGES.find(p => p.title.includes('Schedule'));
            return sched ? `[NOTION OFFLINE] Found 1 Page:\n- Title: ${sched.title}\n- Content: ${sched.content}` : "No schedule found.";
        }
        return "Notion Search: No pages found matching that specific query.";
    }
    
    return `[NOTION OFFLINE] Retrieved ${hits.length} pages:\n` + 
        hits.map(h => `- Title: "${h.title}"\n  Content: "${h.content}"`).join('\n\n');
};

/**
 * Query Pinecone via RAG API. Falls back to mock if offline.
 */
export const queryPinecone = async (vectorDesc: string): Promise<string> => {
    const result = await queryRag(vectorDesc, "pinecone");
    
    if (result.sources.length > 0) {
        return `[PINECONE RAG] Top ${result.sources.length} matches:\n` +
            result.sources.map((s, i) => `${i + 1}. "${s.title}" (score: ${s.score.toFixed(4)})`).join('\n');
    }
    
    // Fallback to mock
    const q = vectorDesc.toLowerCase();
    const hits = MOCK_PINECONE_VECTORS.filter(v => v.metadata.toLowerCase().includes(q));
    
    if (hits.length === 0) {
        return "[PINECONE OFFLINE] No high-confidence semantic matches found.";
    }
    
    return `[PINECONE OFFLINE] Top Semantic Matches:\n` + 
        hits.map(v => `(Confidence: ${v.score}) ${v.metadata}`).join('\n');
};
