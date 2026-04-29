/**
 * LATTICE API CLIENT
 * Replaces all simulated services with real endpoint calls.
 * 
 * Endpoints:
 * - sheldonbrain-rag-api (Cloud Run): /query, /classify, /lattice, /spheres
 * - krakoa MCP server: WebSocket connection for GDrive mount + haptics
 * - bridge_v2 (via API): model routing and synthesis
 * 
 * Configuration is loaded from environment or falls back to defaults.
 */

// ─── Configuration ───────────────────────────────────────────────────────────

interface LatticeConfig {
  ragApiUrl: string;
  krakoaMcpUrl: string;
  bridgeApiUrl: string;
  geminiApiKey: string;
}

const getConfig = (): LatticeConfig => ({
  ragApiUrl: import.meta.env?.VITE_RAG_API_URL || "https://sheldonbrain-rag-api-HASH.run.app",
  krakoaMcpUrl: import.meta.env?.VITE_KRAKOA_MCP_URL || "ws://localhost:8765",
  bridgeApiUrl: import.meta.env?.VITE_BRIDGE_API_URL || "http://localhost:8080",
  geminiApiKey: import.meta.env?.VITE_GEMINI_API_KEY || "",
});

// ─── Types ───────────────────────────────────────────────────────────────────

export interface RagQueryResult {
  answer: string;
  sources: Array<{ title: string; content: string; score: number }>;
  namespace: string;
  latency_ms: number;
}

export interface ClassifyResult {
  house: string;
  sphere: string;
  confidence: number;
  house_name: string;
  sphere_name: string;
}

export interface LatticeNode {
  house_id: string;
  house_name: string;
  spheres: Array<{
    sphere_id: string;
    sphere_name: string;
    module_count: number;
  }>;
}

export interface SphereInfo {
  id: string;
  name: string;
  house: string;
  house_name: string;
}

export interface BridgeRouteResult {
  model: string;
  response: string;
  route_path: string;
  tokens_used: number;
  cost_estimate: number;
}

// ─── RAG API (replaces externalDataSim.ts + keepRagSim.ts) ──────────────────

export const queryRag = async (
  query: string,
  namespace: string = "default"
): Promise<RagQueryResult> => {
  const config = getConfig();
  try {
    const response = await fetch(`${config.ragApiUrl}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, namespace, top_k: 5 }),
    });
    if (!response.ok) throw new Error(`RAG API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    // Graceful fallback — return formatted error as result
    return {
      answer: `[RAG API OFFLINE] Query: "${query}" (namespace: ${namespace}). Connect sheldonbrain-rag-api to enable live retrieval.`,
      sources: [],
      namespace,
      latency_ms: 0,
    };
  }
};

/**
 * Replaces externalDataSim.ts queryNotion + queryPinecone
 */
export const queryNotionRag = (query: string): Promise<RagQueryResult> =>
  queryRag(query, "notion");

/**
 * Replaces keepRagSim.ts readKeepNotes + writeKeepNote
 */
export const queryKeepRag = (query: string): Promise<RagQueryResult> =>
  queryRag(query, "keep");

// ─── Classification API (replaces grokData.ts sphere routing) ────────────────

export const classifyText = async (text: string): Promise<ClassifyResult> => {
  const config = getConfig();
  try {
    const response = await fetch(`${config.ragApiUrl}/classify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!response.ok) throw new Error(`Classify API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    return {
      house: "H02",
      sphere: "S03",
      confidence: 0.0,
      house_name: "Formal Sciences",
      sphere_name: "Computer Science (fallback)",
    };
  }
};

// ─── Lattice Structure API (replaces grokData.ts SPHERES constant) ───────────

export const getLatticeStructure = async (): Promise<LatticeNode[]> => {
  const config = getConfig();
  try {
    const response = await fetch(`${config.ragApiUrl}/lattice`);
    if (!response.ok) throw new Error(`Lattice API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    // Return minimal fallback structure
    return [
      { house_id: "H01", house_name: "Philosophy & Logic", spheres: [] },
      { house_id: "H02", house_name: "Formal Sciences", spheres: [] },
      { house_id: "H03", house_name: "Natural Sciences", spheres: [] },
      { house_id: "H04", house_name: "Technology & Engineering", spheres: [] },
      { house_id: "H05", house_name: "Arts & Creative Expression", spheres: [] },
      { house_id: "H06", house_name: "Humanities & Culture", spheres: [] },
      { house_id: "H07", house_name: "Applied Sciences", spheres: [] },
      { house_id: "H08", house_name: "Education & Pedagogy", spheres: [] },
      { house_id: "H09", house_name: "Life Sciences", spheres: [] },
      { house_id: "H10", house_name: "Health & Medicine", spheres: [] },
      { house_id: "H11", house_name: "Social Sciences", spheres: [] },
      { house_id: "H12", house_name: "Law & Governance", spheres: [] },
    ];
  }
};

export const getSpheres = async (): Promise<SphereInfo[]> => {
  const config = getConfig();
  try {
    const response = await fetch(`${config.ragApiUrl}/spheres`);
    if (!response.ok) throw new Error(`Spheres API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    return [];
  }
};

// ─── Krakoa MCP (replaces krakoaMcpSim.ts) ──────────────────────────────────

export interface McpToolResult {
  tool: string;
  status: string;
  output: string;
  latency_ms: number;
}

export const callKrakoaMcp = async (
  tool: string,
  params: Record<string, unknown>
): Promise<McpToolResult> => {
  const config = getConfig();
  try {
    // MCP over HTTP fallback (WebSocket preferred but HTTP works for simple calls)
    const response = await fetch(`${config.krakoaMcpUrl}/tool`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool, params }),
    });
    if (!response.ok) throw new Error(`MCP error: ${response.status}`);
    return await response.json();
  } catch (error) {
    return {
      tool,
      status: "SIMULATED",
      output: `[KRAKOA MCP OFFLINE] Tool: ${tool}, Params: ${JSON.stringify(params)}. Connect krakoa_mcp_server for live execution.`,
      latency_ms: 0,
    };
  }
};

/**
 * Replaces krakoaMcpSim.ts runKrakoaHyperMountSimulation
 */
export const hyperMount = (uri: string, mode: string = "READ_ONLY") =>
  callKrakoaMcp("krakoa_drive_mount", { uri, mode });

export const hapticPulse = (pattern: string = "SHORT", target: string = "pixel_watch") =>
  callKrakoaMcp("krakoa_haptic_pulse", { pattern, target });

// ─── Bridge / Nexus (replaces nexusOrchestrator.ts routing) ──────────────────

export const routeViaBridge = async (
  query: string,
  context: string = ""
): Promise<BridgeRouteResult> => {
  const config = getConfig();
  try {
    const response = await fetch(`${config.bridgeApiUrl}/route`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, context, strategy: "optimal" }),
    });
    if (!response.ok) throw new Error(`Bridge API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    return {
      model: "gemini-2.5-flash (fallback)",
      response: "",
      route_path: "LOCAL → FALLBACK",
      tokens_used: 0,
      cost_estimate: 0,
    };
  }
};

// ─── Unified Interface ───────────────────────────────────────────────────────

/**
 * Master query function that classifies intent and routes to appropriate service.
 * Replaces the scattered sim calls throughout the frontend.
 */
export const latticeQuery = async (
  input: string,
  options: { namespace?: string; useBridge?: boolean } = {}
): Promise<{
  classification: ClassifyResult;
  ragResult: RagQueryResult;
  bridgeResult?: BridgeRouteResult;
}> => {
  const [classification, ragResult] = await Promise.all([
    classifyText(input),
    queryRag(input, options.namespace || "default"),
  ]);

  let bridgeResult: BridgeRouteResult | undefined;
  if (options.useBridge) {
    bridgeResult = await routeViaBridge(input, ragResult.answer);
  }

  return { classification, ragResult, bridgeResult };
};
