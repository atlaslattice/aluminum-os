
/**
 * EXTERNAL DATA SIMULATION (Notion & Pinecone)
 * 
 * Simulates external API integrations for RAG.
 */

const MOCK_NOTION_PAGES = [
    { id: 'n-01', title: 'Weekly Schedule', content: 'Monday: Thai Food. Tuesday: Cheesecake Factory. Wednesday: Halo Night. Thursday: Anything but Pizza. Friday: Vintage Game Night. Saturday: Laundry (8:15 PM sharp). Sunday: Pranking Kripke.' },
    { id: 'n-02', title: 'Project: Picard', content: 'Objective: Integrate Starfleet-level voice commands into the Sheldon-AI interface. Status: In Progress. Note: Must ensure "Computer" voice commands are acknowledged with a chirp.' },
    { id: 'n-03', title: 'Fun with Flags Scripts', content: 'Episode 409: The Flags of the Federated States of Micronesia. Fun fact: The four stars represent the four states.' },
    { id: 'n-04', title: 'Apartment Flag Status', content: 'Current Status: Right side up. Distress level: Zero. If upside down, apartment is in distress.' }
];

const MOCK_PINECONE_VECTORS = [
    { id: 'v-99', score: 0.98, metadata: 'Long-term Memory: The time Penny touched my food (Incident #402).' },
    { id: 'v-98', score: 0.95, metadata: 'Fact: The exact seating coordinates of "My Spot" are 0,0,0 relative to the cushion center, situated to avoid drafts and face the television at a direct angle.' },
    { id: 'v-97', score: 0.92, metadata: 'Secret: Grandmother Meemaw\'s cookie recipe ingredient list (Classified).' },
    { id: 'v-96', score: 0.89, metadata: 'Schrodinger\'s Cat: The thought experiment illustrating the paradox of quantum superposition.' }
];

export const searchNotion = (query: string): string => {
    const q = query.toLowerCase();
    const hits = MOCK_NOTION_PAGES.filter(p => p.title.toLowerCase().includes(q) || p.content.toLowerCase().includes(q));
    
    if (hits.length === 0) {
        // Fallback: If query is generic like "schedule", find the schedule
        if (q.includes('schedule')) {
            const sched = MOCK_NOTION_PAGES.find(p => p.title.includes('Schedule'));
            return sched ? `[NOTION API] Found 1 Page:\n- Title: ${sched.title}\n- Content: ${sched.content}` : "No schedule found.";
        }
        return "Notion Search: No pages found matching that specific query.";
    }
    
    return `[NOTION API] Retrieved ${hits.length} pages:\n` + hits.map(h => `- Title: "${h.title}"\n  Content: "${h.content}"`).join('\n\n');
};

export const queryPinecone = (vectorDesc: string): string => {
    // In a real app, this would embed 'vectorDesc' and query the index.
    // Here we filter the mock metadata for keywords.
    const q = vectorDesc.toLowerCase();
    const hits = MOCK_PINECONE_VECTORS.filter(v => v.metadata.toLowerCase().includes(q));

    if (hits.length === 0) {
        return "[PINECONE VECTOR DB] No high-confidence semantic matches found for this query.";
    }

    return `[PINECONE VECTOR DB] Top Semantic Matches (RAG):\n` + hits.map(v => `(Confidence: ${v.score}) ${v.metadata}`).join('\n');
};
