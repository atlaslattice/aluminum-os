
import React, { useEffect, useRef, useState } from 'react';
import { GoogleGenAI, LiveServerMessage, Modality, FunctionDeclaration, Type } from '@google/genai';
import { createPcmBlob, decodeAudioData, base64ToUint8Array } from '../services/audioUtils';
import { searchNotion, queryPinecone } from '../services/externalDataSim';
import { runKeepRagSimulation } from '../services/keepRagSim';
import LiveVoiceVisualizer from './LiveVoiceVisualizer';

interface LiveVoiceModeProps {
  onClose: () => void;
}

// --- FUNCTION DECLARATIONS (TOOLS) ---

const tool_accessNotion: FunctionDeclaration = {
  name: 'accessNotion',
  description: 'Search the Notion workspace for schedules, projects, or documents.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      query: { type: Type.STRING, description: 'The search term or topic (e.g., "Schedule", "Flags").' }
    },
    required: ['query']
  }
};

const tool_queryPinecone: FunctionDeclaration = {
  name: 'queryPinecone',
  description: 'Search long-term vector memory for facts, past incidents, or specific details like "My Spot".',
  parameters: {
    type: Type.OBJECT,
    properties: {
      memoryKey: { type: Type.STRING, description: 'Keywords describing the memory to retrieve.' }
    },
    required: ['memoryKey']
  }
};

const tool_accessKeep: FunctionDeclaration = {
  name: 'accessKeep',
  description: 'Read or search Google Keep notes.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      action: { type: Type.STRING, description: 'Either "read" or "write".' },
      content: { type: Type.STRING, description: 'For read: the search query. For write: the note content.' }
    },
    required: ['action', 'content']
  }
};

const LiveVoiceMode: React.FC<LiveVoiceModeProps> = ({ onClose }) => {
  const [status, setStatus] = useState<"connecting" | "connected" | "error" | "closed">("connecting");
  const [modelSpeaking, setModelSpeaking] = useState(false);
  const [activeTool, setActiveTool] = useState<string | null>(null);
  
  // Audio Refs
  const inputContextRef = useRef<AudioContext | null>(null);
  const outputContextRef = useRef<AudioContext | null>(null);
  const inputSourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const nextStartTimeRef = useRef<number>(0);
  const audioSourcesRef = useRef<Set<AudioBufferSourceNode>>(new Set());
  
  // Session Ref
  const sessionPromiseRef = useRef<Promise<any> | null>(null);

  useEffect(() => {
    let mounted = true;

    const startSession = async () => {
      try {
        const API_KEY = process.env.API_KEY;
        if (!API_KEY) throw new Error("API Key missing");

        const ai = new GoogleGenAI({ apiKey: API_KEY });

        const inputCtx = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 });
        const outputCtx = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
        
        inputContextRef.current = inputCtx;
        outputContextRef.current = outputCtx;

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        const sessionPromise = ai.live.connect({
          model: 'gemini-2.5-flash-native-audio-preview-12-2025',
          config: {
            responseModalities: [Modality.AUDIO],
            tools: [{ functionDeclarations: [tool_accessNotion, tool_queryPinecone, tool_accessKeep] }],
            systemInstruction: `You are Sheldon Gemini. You have access to "Enterprise Computer" capabilities via tools.
            You can access Notion, Pinecone Vector DB, and Google Keep.
            If the user asks to check a schedule, memories, or notes, USE THE TOOLS.
            When a tool returns data, incorporate it into your speech naturally, perhaps referencing your superior organizational skills.
            Voice: "Fenrir". Personality: Intellectual, witty, precise.`,
            speechConfig: {
              voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Fenrir' } },
            },
          },
          callbacks: {
            onopen: () => {
              if (mounted) setStatus("connected");
              
              const source = inputCtx.createMediaStreamSource(stream);
              const processor = inputCtx.createScriptProcessor(4096, 1, 1);
              
              processor.onaudioprocess = (e) => {
                const inputData = e.inputBuffer.getChannelData(0);
                const pcmBlob = createPcmBlob(inputData);
                sessionPromise.then((session) => {
                   session.sendRealtimeInput({ media: pcmBlob });
                });
              };

              source.connect(processor);
              processor.connect(inputCtx.destination);
              
              inputSourceRef.current = source;
              processorRef.current = processor;
            },
            onmessage: async (msg: LiveServerMessage) => {
              // 1. Handle Tool Calls
              if (msg.toolCall) {
                const responses = [];
                for (const fc of msg.toolCall.functionCalls) {
                  let result = "";
                  
                  if (mounted) setActiveTool(fc.name);

                  if (fc.name === 'accessNotion') {
                     const query = (fc.args as any).query;
                     result = searchNotion(query);
                  } else if (fc.name === 'queryPinecone') {
                     const key = (fc.args as any).memoryKey;
                     result = queryPinecone(key);
                  } else if (fc.name === 'accessKeep') {
                     const action = (fc.args as any).action;
                     const content = (fc.args as any).content;
                     // Reuse simulation logic which handles string commands
                     const cmd = action === 'write' ? `add note ${content}` : `search keep ${content}`;
                     result = runKeepRagSimulation(cmd);
                     if (!result) result = "Google Keep: No data found or operation failed.";
                  }

                  responses.push({
                    id: fc.id,
                    name: fc.name,
                    response: { result: result }
                  });
                }
                
                // Send response back
                sessionPromise.then(session => {
                  session.sendToolResponse({ functionResponses: responses });
                  if (mounted) setActiveTool(null);
                });
              }

              // 2. Handle Audio Output
              const audioData = msg.serverContent?.modelTurn?.parts?.[0]?.inlineData?.data;
              if (audioData) {
                if (mounted) setModelSpeaking(true);
                const bytes = base64ToUint8Array(audioData);
                const buffer = await decodeAudioData(bytes, outputCtx, 24000, 1);
                
                const source = outputCtx.createBufferSource();
                source.buffer = buffer;
                source.connect(outputCtx.destination);
                
                const currentTime = outputCtx.currentTime;
                if (nextStartTimeRef.current < currentTime) {
                    nextStartTimeRef.current = currentTime;
                }
                
                source.start(nextStartTimeRef.current);
                nextStartTimeRef.current += buffer.duration;
                
                audioSourcesRef.current.add(source);
                
                source.onended = () => {
                    audioSourcesRef.current.delete(source);
                    if (audioSourcesRef.current.size === 0) {
                        if (mounted) setModelSpeaking(false);
                    }
                };
              }

              if (msg.serverContent?.interrupted) {
                 audioSourcesRef.current.forEach(src => {
                     try { src.stop(); } catch(e) {}
                 });
                 audioSourcesRef.current.clear();
                 nextStartTimeRef.current = 0;
                 if (mounted) {
                     setModelSpeaking(false);
                     setActiveTool(null);
                 }
              }
            },
            onclose: () => {
              if (mounted) setStatus("closed");
            },
            onerror: (err) => {
              console.error("Live API Error:", err);
              if (mounted) setStatus("error");
            }
          }
        });

        sessionPromiseRef.current = sessionPromise;
      } catch (e) {
        console.error("Failed to start voice session", e);
        if (mounted) setStatus("error");
      }
    };

    startSession();

    return () => {
      mounted = false;
      inputSourceRef.current?.disconnect();
      processorRef.current?.disconnect();
      inputContextRef.current?.close();
      outputContextRef.current?.close();
      sessionPromiseRef.current?.then(session => {
          try { session.close(); } catch(e) {}
      });
    };
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-950/95 backdrop-blur-md">
      <div className="relative w-full max-w-lg p-6 flex flex-col items-center gap-6">
        
        {/* Header */}
        <div className="text-center">
            <h2 className="text-2xl font-bold text-cyan-400 tracking-widest uppercase">Nexus Vocal Link</h2>
            <p className="text-xs text-gray-500 mt-1">PROTOCOL: ARA-12 // RAG ENABLED</p>
        </div>

        {/* Visualizer */}
        <div className="w-full relative">
            <div className="absolute inset-0 bg-cyan-500/10 blur-xl rounded-full"></div>
            <LiveVoiceVisualizer isActive={status === 'connected'} isSpeaking={modelSpeaking} />
        </div>

        {/* Status Text & Tool Indicator */}
        <div className="h-12 text-center flex flex-col items-center justify-center">
            {status === 'connecting' && <span className="animate-pulse text-yellow-500">ESTABLISHING UPLINK...</span>}
            
            {status === 'connected' && !activeTool && (
                modelSpeaking 
                ? <span className="text-cyan-400 font-mono">SHELDON IS SPEAKING...</span>
                : <span className="text-gray-400 font-mono">LISTENING...</span>
            )}

            {activeTool && (
                 <div className="flex items-center gap-2 text-purple-400 font-mono text-sm animate-pulse border border-purple-500/50 px-3 py-1 rounded bg-purple-900/20">
                     <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
                     ACCESSING: {activeTool.replace('access', '').replace('query', '').toUpperCase()}
                 </div>
            )}

            {status === 'error' && <span className="text-red-500 font-bold">CONNECTION FAILURE</span>}
            {status === 'closed' && <span className="text-gray-500">LINK SEVERED</span>}
        </div>

        {/* Controls */}
        <button 
            onClick={onClose}
            className="px-8 py-3 bg-red-900/50 hover:bg-red-800 text-red-200 rounded-full border border-red-700 transition-all uppercase tracking-wider text-sm font-bold shadow-lg hover:shadow-red-900/50"
        >
            Terminate Session
        </button>
      </div>
    </div>
  );
};

export default LiveVoiceMode;
