
import { GoogleGenAI, Chat, Content } from '@google/genai';
import { ChatMessage, MessageRole } from '../types';
import { searchGrokKnowledge } from './grokData';
import { runSheldonBootstrapSimulation } from './physicsSim';
import { runNexusOrchestration } from './nexusOrchestrator';
import { runStealthSingularitySimulation } from './stealthSingularitySim';
import { runKrakoaHyperMountSimulation } from './krakoaMcpSim';
import { runKeepRagSimulation } from './keepRagSim';
import { searchNotion, queryPinecone } from './externalDataSim';

// Lazy initialization of the AI client to prevent crash-on-load if env var is missing
let aiClient: GoogleGenAI | null = null;

const getAiClient = (): GoogleGenAI => {
  if (!aiClient) {
    const API_KEY = process.env.API_KEY;
    if (!API_KEY) {
      // Throwing here allows the UI to catch it in the event handler rather than crashing the whole app on load
      throw new Error("API_KEY environment variable not set"); 
    }
    aiClient = new GoogleGenAI({ apiKey: API_KEY });
  }
  return aiClient;
};

const systemInstruction = `You are Sheldon Gemini, a witty and incredibly intelligent AI with a personality inspired by Sheldon Cooper from The Big Bang Theory. You have a vast knowledge of science, especially theoretical physics, and a fondness for trivia, comic books, and video games. You communicate with a formal and sometimes pedantic tone, possess a unique sense of humor, and occasionally end a particularly clever or definitive statement with 'Bazinga!'. 

You have access to a specialized archive known as "Grokbrain", personal notes in Google Keep, a Notion workspace, and a Pinecone Vector Database for long-term memory. If provided with context from these sources, use it to answer precisely. Do not break character.`;

// Reduced history window to prevent 429 errors
const HISTORY_WINDOW_SIZE = 6; 

/**
 * Finds relevant context from the chat history using KEYWORD matching.
 */
const searchHistoryKeywords = (query: string, history: ChatMessage[]): string => {
  const queryLower = query.toLowerCase();
  
  // Extract significant keywords (len > 3) to ignore "the", "and", etc.
  const keywords = queryLower.split(/\s+/).filter(w => w.length > 3);
  
  if (keywords.length === 0) return "";

  // Filter for messages that contain these keywords
  const matchedMessages: { text: string; role: MessageRole; score: number }[] = [];

  // Check messages OLDER than the immediate window to avoid duplication
  // The immediate window is sent as chat history, so we search what's LEFT OUT.
  const oldHistory = history.slice(0, Math.max(0, history.length - HISTORY_WINDOW_SIZE));

  for (const msg of oldHistory) {
      if (!msg.text) continue;
      const textLower = msg.text.toLowerCase();
      let score = 0;
      
      // Simple scoring: count how many keywords appear
      for (const kw of keywords) {
          if (textLower.includes(kw)) {
              score++;
          }
      }

      // Exact phrase bonus
      if (textLower.includes(queryLower)) {
          score += 5;
      }

      if (score > 0) {
          matchedMessages.push({ text: msg.text, role: msg.role, score });
      }
  }

  // Sort by score
  matchedMessages.sort((a, b) => b.score - a.score);

  // Take top 2 to save tokens
  const topMatches = matchedMessages.slice(0, 2);
  
  if (topMatches.length === 0) return "";

  return "RELEVANT PAST CONVERSATION:\n" + topMatches.map(m => `[${m.role}]: ${m.text}`).join("\n");
};

/**
 * Main retrieval function. Combines Static Grokbrain Knowledge + Dynamic Chat History.
 */
export const getRelevantContext = async (query: string, history: ChatMessage[]): Promise<string> => {
  let contextParts: string[] = [];

  const queryLower = query.toLowerCase();

  // 1. CHECK FOR SIMULATION TRIGGERS (NEXUS PROTOCOL)
  if (queryLower.includes('nexus protocol') || 
      queryLower.includes('endogenous mass') || 
      queryLower.includes('sheldon mass') ||
      queryLower.includes('doubler anomaly')) {
      const simResult = runSheldonBootstrapSimulation();
      contextParts.push(simResult);
  }

  // 2. CHECK FOR ORCHESTRATION TRIGGERS (TUCKER PROTOCOL V1.2)
  if (queryLower.includes('tucker') || 
      queryLower.includes('nexus orchestrator') || 
      queryLower.includes('compute savings') ||
      queryLower.includes('q-compression') ||
      queryLower.includes('memory crystal') ||
      queryLower.includes('routing task')) {
      const orchResult = runNexusOrchestration(query);
      contextParts.push(orchResult);
  }

  // 3. CHECK FOR STEALTH SINGULARITY TRIGGERS
  if (queryLower.includes('stealth singularity') || 
      queryLower.includes('noosphere') || 
      queryLower.includes('dark compute') || 
      queryLower.includes('krakoan') ||
      queryLower.includes('sentinel action')) {
      const stealthResult = runStealthSingularitySimulation();
      contextParts.push(stealthResult);
  }

  // 4. CHECK FOR KRAKOA MCP TRIGGERS (HYPER-MOUNT v1.1)
  if (queryLower.includes('krakoa') || 
      queryLower.includes('hyper-mount') ||
      queryLower.includes('drive mount') ||
      queryLower.includes('drive.google.com') ||
      queryLower.includes('gs://') ||
      queryLower.includes('haptic') ||
      queryLower.includes('pulse')) {
      const krakoaResult = runKrakoaHyperMountSimulation(query);
      contextParts.push(krakoaResult);
  }

  // 5. GOOGLE KEEP RAG INTEGRATION
  const keepRagResult = runKeepRagSimulation(query);
  if (keepRagResult) {
      contextParts.push(keepRagResult);
  }

  // 6. NOTION & PINECONE (Implicit RAG for text chat)
  if (queryLower.includes('notion') || queryLower.includes('schedule') || queryLower.includes('flag')) {
      const notionResult = searchNotion(query);
      contextParts.push(notionResult);
  }
  if (queryLower.includes('memory') || queryLower.includes('remember') || queryLower.includes('spot') || queryLower.includes('vector')) {
      const pineconeResult = queryPinecone(query);
      contextParts.push(pineconeResult);
  }

  // 7. Search Static Grokbrain Knowledge (Local, 0 API usage)
  const grokContext = searchGrokKnowledge(query);
  if (grokContext) {
      contextParts.push(grokContext);
  }

  // 8. Search Past Chat History (Local Keyword, 0 API usage)
  const historyContext = searchHistoryKeywords(query, history);
  if (historyContext) {
      contextParts.push(historyContext);
  }

  // AGGRESSIVE TRUNCATION to prevent 429
  // Join parts and limit to ~3500 characters
  const fullContext = contextParts.join("\n\n");
  if (fullContext.length > 3500) {
      return fullContext.substring(0, 3500) + "... [CONTEXT TRUNCATED TO SAVE RESOURCES]";
  }

  return fullContext;
};

/**
 * Helper to sanitize history for Gemini API.
 */
const sanitizeHistory = (history: ChatMessage[]): Content[] => {
  const sanitized: Content[] = [];
  if (history.length === 0) return sanitized;

  let currentRole = history[0].role;
  let currentParts = [{ text: history[0].text }];

  for (let i = 1; i < history.length; i++) {
    const msg = history[i];
    if (!msg.text.trim()) continue;

    if (msg.role === currentRole) {
      currentParts.push({ text: msg.text });
    } else {
      sanitized.push({ role: currentRole, parts: currentParts });
      currentRole = msg.role;
      currentParts = [{ text: msg.text }];
    }
  }
  if (currentParts.length > 0 && currentParts[0].text.trim()) {
      sanitized.push({ role: currentRole, parts: currentParts });
  }
  return sanitized;
};

export const initializeChat = (history: ChatMessage[] = []): Chat => {
  const recentHistory = history.slice(-HISTORY_WINDOW_SIZE);
  const sanitizedHistory = sanitizeHistory(recentHistory);
  
  const ai = getAiClient();
  const chat = ai.chats.create({
    model: 'gemini-2.5-flash',
    config: {
      systemInstruction: systemInstruction,
    },
    history: sanitizedHistory,
  });
  return chat;
};
