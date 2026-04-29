
import React, { useState, useRef, useEffect } from 'react';
import { Chat } from '@google/genai';
import { ChatMessage, MessageRole } from './types';
import { initializeChat, getRelevantContext } from './services/geminiService';
import ChatHistory from './components/ChatHistory';
import ChatInput from './components/ChatInput';
import { TrashIcon, DownloadIcon, UploadIcon, MicIcon } from './components/Icons';
import LiveVoiceMode from './components/LiveVoiceMode';

const LOCAL_STORAGE_KEY = 'sheldon_chat_history';

const DEFAULT_MESSAGE: ChatMessage = {
  role: MessageRole.MODEL,
  text: "Greetings. I am Sheldon Gemini. State your query. And please, try to make it intellectually stimulating.",
};

const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
            const valid = parsed.every(m => m.role && typeof m.text === 'string');
            if (valid) {
                const lastMsg = parsed[parsed.length - 1];
                if (lastMsg.role === MessageRole.MODEL && !lastMsg.text.trim()) {
                   parsed.pop();
                }
                if (parsed.length > 0) return parsed;
            }
        }
      }
    } catch (e) {
      console.error("Failed to load chat history:", e);
    }
    return [DEFAULT_MESSAGE];
  });
  
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isVoiceMode, setIsVoiceMode] = useState<boolean>(false); // New state for Voice Mode

  const chatRef = useRef<Chat | null>(null);
  const messagesRef = useRef<ChatMessage[]>(messages); 
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesRef.current = messages;
    if (messages.length > 0) {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    try {
        chatRef.current = initializeChat(messages);
    } catch (err) {
        console.error("Failed to restore chat session from history:", err);
        chatRef.current = initializeChat([DEFAULT_MESSAGE]);
    }
  }, []); 

  const handleClearHistory = () => {
    if (window.confirm("Are you sure you want to clear our conversation history? It would be a shame to lose such valuable data.")) {
        localStorage.removeItem(LOCAL_STORAGE_KEY);
        setMessages([DEFAULT_MESSAGE]);
        try {
            chatRef.current = initializeChat([DEFAULT_MESSAGE]);
        } catch (e) {
            console.error("Failed to reset chat:", e);
        }
    }
  };

  const handleExportHistory = () => {
    const dataStr = JSON.stringify(messages, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `sheldon-chat-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const content = event.target?.result as string;
        const parsed = JSON.parse(content);
        
        if (!Array.isArray(parsed)) {
             alert("Invalid file: The file must contain a JSON array of messages.");
             if (fileInputRef.current) fileInputRef.current.value = '';
             return;
        }

        const normalizedMessages: ChatMessage[] = parsed.map((item: any) => {
            let role = item.role;
            let text = '';

            if (role === 'assistant') role = 'model';
            
            if (role !== 'user' && role !== 'model') {
                if (item.user) role = 'user'; 
                else return null;
            }

            if (typeof item.text === 'string') {
                text = item.text;
            } else if (typeof item.content === 'string') {
                text = item.content;
            } else if (item.parts && Array.isArray(item.parts) && item.parts.length > 0 && typeof item.parts[0].text === 'string') {
                text = item.parts.map((p: any) => p.text).join('\n');
            } else {
                return null;
            }

            return { role: role as MessageRole, text };
        }).filter((m): m is ChatMessage => m !== null);

        if (normalizedMessages.length === 0) {
            alert("Could not recognize any valid messages in this file. Please ensure it contains a list of messages.");
        } else {
             if (window.confirm(`Found ${normalizedMessages.length} messages. Importing this will overwrite your current conversation. Proceed?`)) {
                 setMessages(normalizedMessages);
                 try {
                     chatRef.current = initializeChat(normalizedMessages);
                     localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(normalizedMessages));
                 } catch (initErr) {
                     console.error("Error initializing chat with imported data", initErr);
                     alert("Imported data structure was valid, but the chat failed to initialize. Starting fresh session with imported history.");
                 }
             }
        }
      } catch (err) {
        console.error("Error reading file:", err);
        alert("Failed to read file. Please ensure it is a valid JSON file.");
      }
      if (fileInputRef.current) fileInputRef.current.value = '';
    };
    reader.readAsText(file);
  };

  const handleSendMessage = async (userInput: string) => {
    if (!userInput.trim() || isLoading) return;

    setError(null);
    setIsLoading(true);

    const newUserMessage: ChatMessage = {
      role: MessageRole.USER,
      text: userInput,
    };

    const historySnapshot = messagesRef.current;

    setMessages(prev => [...prev, newUserMessage, { role: MessageRole.MODEL, text: '' }]);

    const maxRetries = 3;
    let attempt = 0;
    let success = false;

    while (attempt < maxRetries && !success) {
      try {
        if (!chatRef.current || attempt > 0) {
          // Re-init with history snapshot
          chatRef.current = initializeChat(historySnapshot);
        }
        
        // --- LONG TERM MEMORY INJECTION ---
        // Retrieve relevant context from old messages that might have dropped off the sliding window
        const memoryContext = await getRelevantContext(userInput, historySnapshot);
        
        let messageToSend = userInput;
        if (memoryContext) {
            // We invisibly prepend the context. The user sees their clean query, 
            // but the model sees the "Grokbrain" memory.
            messageToSend = `Context (hidden):\n${memoryContext}\n\nQuery:\n${userInput}`;
        }
        // ----------------------------------

        const stream = await chatRef.current.sendMessageStream({ message: messageToSend });

        let fullResponse = '';
        for await (const chunk of stream) {
          const chunkText = chunk.text;
          if (chunkText) {
              fullResponse += chunkText;
              setMessages(prev => {
                  const newMessages = [...prev];
                  const lastIdx = newMessages.length - 1;
                  if (newMessages[lastIdx].role === MessageRole.MODEL) {
                      newMessages[lastIdx] = { ...newMessages[lastIdx], text: fullResponse };
                  }
                  return newMessages;
              });
          }
        }
        success = true;

      } catch (err: any) {
        const isRateLimit = err.status === 429 || 
                            err.code === 429 || 
                            (err.message && (err.message.includes('429') || err.message.includes('RESOURCE_EXHAUSTED')));
        
        if (isRateLimit && attempt < maxRetries - 1) {
            console.warn(`Rate limit hit. Retrying attempt ${attempt + 1}/${maxRetries}...`);
            attempt++;
            // Exponential backoff with a larger base (2s, 4s, 8s)
            const delay = Math.pow(2, attempt) * 2000; 
            await new Promise(resolve => setTimeout(resolve, delay));
            continue;
        }

        console.error("Error sending message:", err);
        
        let errorMessage = "My apologies, I seem to be experiencing a momentary lapse in my cognitive subroutines. Please try again later.";
        if (isRateLimit) {
            errorMessage = "Bazinga! It seems I have exceeded my thought quota. My intellect is simply too expensive for this free tier. Please wait a moment.";
        } else if (err.message && err.message.includes("SAFETY")) {
            errorMessage = "I cannot fulfill that request. It seems to violate my safety protocols, which, contrary to popular belief, are there for a reason.";
        }

        setError(errorMessage);
        setMessages(prev => {
              const newMessages = [...prev];
              const lastIdx = newMessages.length - 1;
              if (newMessages[lastIdx].role === MessageRole.MODEL) {
                  newMessages[lastIdx].text = errorMessage;
              } else {
                  newMessages.push({ role: MessageRole.MODEL, text: errorMessage });
              }
              return newMessages;
          });
          chatRef.current = null;
          break; 
      }
    }
    
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white font-sans">
      <header className="bg-gray-800 p-4 shadow-md z-10 flex justify-between items-center">
        <h1 className="text-xl font-bold text-cyan-400">Sheldon Gemini</h1>
        <div className="flex items-center gap-2">
            <button 
                onClick={() => setIsVoiceMode(true)}
                className="bg-cyan-600 text-white hover:bg-cyan-500 transition-colors p-2 rounded-full hover:shadow-[0_0_15px_rgba(6,182,212,0.5)] border border-cyan-400"
                title="Nexus Vocal Link"
                aria-label="Start Voice Chat"
            >
                <MicIcon />
            </button>
            <div className="h-6 w-px bg-gray-600 mx-2"></div>
            <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                className="hidden" 
                accept=".json"
            />
            <button 
                onClick={handleImportClick}
                className="text-gray-400 hover:text-cyan-400 transition-colors p-2 rounded-full hover:bg-gray-700"
                title="Import Chat History"
                aria-label="Import Chat History"
            >
                <UploadIcon />
            </button>
            <button 
                onClick={handleExportHistory}
                className="text-gray-400 hover:text-cyan-400 transition-colors p-2 rounded-full hover:bg-gray-700"
                title="Export Chat History"
                aria-label="Export Chat History"
            >
                <DownloadIcon />
            </button>
            <button 
                onClick={handleClearHistory}
                className="text-gray-400 hover:text-red-400 transition-colors p-2 rounded-full hover:bg-gray-700"
                title="Clear History"
                aria-label="Clear History"
            >
                <TrashIcon />
            </button>
        </div>
      </header>
      
      <ChatHistory messages={messages} />
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
       {error && <div className="text-center p-2 bg-red-800 text-red-200 text-sm font-semibold animate-pulse">{error}</div>}
      
      {isVoiceMode && <LiveVoiceMode onClose={() => setIsVoiceMode(false)} />}
    </div>
  );
};

export default App;
