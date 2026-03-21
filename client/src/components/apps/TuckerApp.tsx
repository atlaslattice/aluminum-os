import { useState, useRef, useEffect } from 'react';
import {
  MessageCircle, Send, Bot, User, Zap, Brain, Cpu, Globe,
  ChevronDown, RefreshCw, Settings2, Sparkles, Star,
  AlertCircle, CheckCircle, Copy, Trash2, Download,
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════
// TUCKER V4 — Constitutional Chatbot
// Co-designed with GPT-4 and Gemini Pro
// Source repo: splitmerge420/tucker-gemini-GPT-
// Integrated into Aluminum OS: ALUM-INT-008
// All conversations routed through Pantheon Council constitutional layer.
// Model: GPT-4.1 (primary) + Gemini 2.5 Pro (synthesis) + Claude (oversight)
// ═══════════════════════════════════════════════════════════════

type ModelId = 'gpt4' | 'gemini' | 'claude' | 'grok' | 'auto';
type MessageRole = 'user' | 'tucker' | 'system';
type TabId = 'chat' | 'config' | 'history' | 'council' | 'about';

interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  model?: ModelId;
  timestamp: Date;
  constitutional?: boolean;
  tokens?: number;
}

interface TuckerConfig {
  model: ModelId;
  temperature: number;
  maxTokens: number;
  constitutionalMode: boolean;
  councilMode: boolean;
  systemPrompt: string;
  persona: string;
}

interface CouncilVote {
  member: string;
  color: string;
  icon: string;
  vote: 'approve' | 'flag' | 'abstain';
  note: string;
}

// ─── Tucker personas (v3 + v4 combined) ───
const PERSONAS = [
  { id: 'default', name: 'Tucker V4 (Default)', description: 'Balanced — GPT+Gemini synthesis, constitutional oversight' },
  { id: 'explorer', name: 'Tucker V3 Explorer', description: 'Deep research mode — DeerFlow style, multi-source synthesis' },
  { id: 'coder', name: 'Tucker Coder', description: 'Code-first — Aluminum OS architecture aware, Rust+Python+TypeScript' },
  { id: 'sovereign', name: 'Tucker Sovereign', description: 'Constitutional mode — Atlas Lattice governance, Kintsugi policies' },
  { id: 'health', name: 'Tucker Health', description: 'Healthcare focus — HIPAA-aware, FHIR R4, One Medical integration' },
];

const MODELS: { id: ModelId; name: string; color: string; icon: string; description: string }[] = [
  { id: 'auto', name: 'Auto-Route', color: '#00ff88', icon: '⚡', description: '3-tier router — cost + quality + constitutional' },
  { id: 'gpt4', name: 'GPT-4.1', color: '#ffd700', icon: '🧠', description: 'Primary — co-designed with Tucker' },
  { id: 'gemini', name: 'Gemini 2.5 Pro', color: '#4fc3f7', icon: '✨', description: 'Synthesis layer — scale + multimodal' },
  { id: 'claude', name: 'Claude (Oversight)', color: '#ff6b35', icon: '🛡️', description: 'Constitutional oversight + safety' },
  { id: 'grok', name: 'Grok (Truth)', color: '#ff4444', icon: '⚡', description: 'Contrarian verification + stress test' },
];

// ─── Sample constitutional conversations ───
const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: 'sys-1',
    role: 'system',
    content: 'Tucker V4 initialized. Constitutional substrate active. Pantheon Council oversight enabled. Model routing: Auto (GPT-4.1 primary → Gemini synthesis → Claude oversight).',
    timestamp: new Date(),
    constitutional: true,
  },
  {
    id: 'tucker-1',
    role: 'tucker',
    model: 'gpt4',
    content: "Hey! I'm Tucker — your Aluminum OS constitutional chatbot, co-designed with GPT and Gemini. I'm wired into the Pantheon Council and the Kintsugi policy layer, so everything I say goes through constitutional review.\n\nWhat are we working on today? I can help with code (Rust, Python, TypeScript), Atlas Lattice governance, healthcare integrations, research synthesis, or just a conversation.",
    timestamp: new Date(),
    constitutional: true,
    tokens: 87,
  },
];

const COUNCIL_VOTES: CouncilVote[] = [
  { member: 'Claude', color: '#ff6b35', icon: '🛡️', vote: 'approve', note: 'Constitutional alignment verified' },
  { member: 'GPT-4.1', color: '#ffd700', icon: '🧠', vote: 'approve', note: 'Response quality: high' },
  { member: 'Gemini', color: '#4fc3f7', icon: '✨', vote: 'approve', note: 'Synthesis layer coherent' },
  { member: 'Grok', color: '#ff4444', icon: '⚡', vote: 'abstain', note: 'Stress test pending' },
];

const DEFAULT_CONFIG: TuckerConfig = {
  model: 'auto',
  temperature: 0.7,
  maxTokens: 2048,
  constitutionalMode: true,
  councilMode: false,
  systemPrompt: 'You are Tucker, the Aluminum OS constitutional chatbot. You are co-designed with GPT and Gemini. You operate under Atlas Lattice Foundation constitutional principles. You have access to the Pantheon Council for oversight. You are helpful, honest, and constitutionally aligned.',
  persona: 'default',
};

function formatTime(d: Date) {
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function ModelBadge({ model, size = 'sm' }: { model?: ModelId; size?: 'sm' | 'xs' }) {
  const m = MODELS.find(x => x.id === model) ?? MODELS[0];
  const cls = size === 'xs' ? 'text-[9px] px-1 py-0 rounded' : 'text-[10px] px-1.5 py-0.5 rounded';
  return (
    <span className={`${cls} font-mono font-bold`} style={{ background: m.color + '22', color: m.color, border: `1px solid ${m.color}44` }}>
      {m.icon} {m.name}
    </span>
  );
}

export default function TuckerApp() {
  const [tab, setTab] = useState<TabId>('chat');
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState('');
  const [config, setConfig] = useState<TuckerConfig>(DEFAULT_CONFIG);
  const [isTyping, setIsTyping] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Simulate Tucker response (constitutional routing)
    await new Promise(r => setTimeout(r, 900 + Math.random() * 600));
    const tuckerMsg: ChatMessage = {
      id: `tucker-${Date.now()}`,
      role: 'tucker',
      model: config.model === 'auto' ? 'gpt4' : config.model,
      content: generateTuckerResponse(userMsg.content, config),
      timestamp: new Date(),
      constitutional: config.constitutionalMode,
      tokens: Math.floor(50 + Math.random() * 200),
    };
    setIsTyping(false);
    setMessages(prev => [...prev, tuckerMsg]);
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const copyMsg = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 1500);
  };

  const clearChat = () => setMessages(INITIAL_MESSAGES);

  return (
    <div className="flex flex-col h-full bg-[#0a0a0f] text-gray-100 font-sans overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#1a1a2e] bg-[#0d0d1a]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg font-bold shadow-lg"
            style={{ background: 'linear-gradient(135deg, #ffd700 0%, #ff6b35 50%, #4fc3f7 100%)' }}>
            T
          </div>
          <div>
            <div className="text-sm font-bold tracking-wide">Tucker V4</div>
            <div className="text-[10px] text-gray-400">GPT+Gemini · Constitutional · ALUM-INT-008</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {config.constitutionalMode && (
            <span className="text-[9px] px-2 py-0.5 rounded-full font-bold" style={{ background: '#00ff8822', color: '#00ff88', border: '1px solid #00ff8844' }}>
              ⚖ CONST
            </span>
          )}
          {config.councilMode && (
            <span className="text-[9px] px-2 py-0.5 rounded-full font-bold" style={{ background: '#9b59b622', color: '#9b59b6', border: '1px solid #9b59b644' }}>
              👁 COUNCIL
            </span>
          )}
          <ModelBadge model={config.model} />
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-[#1a1a2e] bg-[#0d0d1a] overflow-x-auto">
        {(['chat', 'config', 'history', 'council', 'about'] as TabId[]).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-xs font-medium transition-colors whitespace-nowrap ${
              tab === t ? 'text-white border-b-2 border-[#ffd700]' : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {t === 'chat' && '💬 Chat'}
            {t === 'config' && '⚙️ Config'}
            {t === 'history' && '📜 History'}
            {t === 'council' && '👁 Council'}
            {t === 'about' && 'ℹ️ About'}
          </button>
        ))}
      </div>

      {/* Tab: Chat */}
      {tab === 'chat' && (
        <div className="flex flex-col flex-1 overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-4">
            {messages.map(msg => (
              <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {msg.role !== 'system' && (
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${
                    msg.role === 'user'
                      ? 'bg-[#1a1a2e] text-gray-300'
                      : 'text-white shadow-lg'
                  }`} style={msg.role === 'tucker' ? { background: 'linear-gradient(135deg, #ffd700, #ff6b35)' } : {}}>
                    {msg.role === 'user' ? <User className="w-4 h-4" /> : 'T'}
                  </div>
                )}
                <div className={`flex-1 max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
                  {msg.role === 'system' ? (
                    <div className="w-full px-3 py-2 rounded-lg text-xs font-mono" style={{ background: '#00ff8811', color: '#00ff88', border: '1px solid #00ff8822' }}>
                      <AlertCircle className="w-3 h-3 inline mr-1" />{msg.content}
                    </div>
                  ) : (
                    <>
                      <div className={`px-3 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                        msg.role === 'user'
                          ? 'bg-[#1a2744] text-gray-100 rounded-tr-sm'
                          : 'bg-[#141428] text-gray-100 rounded-tl-sm border border-[#2a2a4a]'
                      }`}>
                        {msg.content}
                      </div>
                      <div className="flex items-center gap-2">
                        {msg.role === 'tucker' && msg.model && <ModelBadge model={msg.model} size="xs" />}
                        {msg.constitutional && (
                          <span className="text-[9px] text-green-400 flex items-center gap-0.5">
                            <CheckCircle className="w-2.5 h-2.5" /> const
                          </span>
                        )}
                        {msg.tokens && <span className="text-[9px] text-gray-600">{msg.tokens}tok</span>}
                        <span className="text-[9px] text-gray-600">{formatTime(msg.timestamp)}</span>
                        {msg.role === 'tucker' && (
                          <button
                            onClick={() => copyMsg(msg.id, msg.content)}
                            className="text-[9px] text-gray-600 hover:text-gray-300 transition-colors"
                          >
                            {copied === msg.id ? <CheckCircle className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
                          </button>
                        )}
                      </div>
                    </>
                  )}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm text-white shadow-lg" style={{ background: 'linear-gradient(135deg, #ffd700, #ff6b35)' }}>T</div>
                <div className="px-3 py-2.5 rounded-2xl rounded-tl-sm bg-[#141428] border border-[#2a2a4a]">
                  <div className="flex gap-1 items-center h-4">
                    {[0, 1, 2].map(i => (
                      <div key={i} className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: `${i * 150}ms` }} />
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-[#1a1a2e] p-3 bg-[#0d0d1a]">
            <div className="flex items-end gap-2">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Message Tucker... (Enter to send, Shift+Enter for newline)"
                  rows={2}
                  className="w-full bg-[#141428] border border-[#2a2a4a] rounded-xl px-3 py-2.5 text-sm text-gray-100 placeholder-gray-600 resize-none focus:outline-none focus:border-[#ffd70066] transition-colors"
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <button
                  onClick={sendMessage}
                  disabled={!input.trim() || isTyping}
                  className="w-9 h-9 rounded-xl flex items-center justify-center transition-all disabled:opacity-30"
                  style={{ background: 'linear-gradient(135deg, #ffd700, #ff6b35)' }}
                >
                  <Send className="w-4 h-4 text-black" />
                </button>
                <button onClick={clearChat} className="w-9 h-9 rounded-xl flex items-center justify-center bg-[#1a1a2e] hover:bg-[#2a2a4e] transition-colors">
                  <Trash2 className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Config */}
      {tab === 'config' && (
        <div className="flex-1 overflow-y-auto p-4 space-y-5">
          <h3 className="text-sm font-bold text-gray-200">Tucker V4 Configuration</h3>

          {/* Model selection */}
          <div>
            <label className="text-xs text-gray-400 mb-2 block">Primary Model</label>
            <div className="grid grid-cols-1 gap-2">
              {MODELS.map(m => (
                <button
                  key={m.id}
                  onClick={() => setConfig(c => ({ ...c, model: m.id }))}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all text-left"
                  style={{
                    background: config.model === m.id ? m.color + '18' : '#141428',
                    borderColor: config.model === m.id ? m.color + '66' : '#2a2a4a',
                  }}
                >
                  <span className="text-lg">{m.icon}</span>
                  <div className="flex-1">
                    <div className="text-xs font-bold" style={{ color: config.model === m.id ? m.color : '#e2e8f0' }}>{m.name}</div>
                    <div className="text-[10px] text-gray-500">{m.description}</div>
                  </div>
                  {config.model === m.id && <CheckCircle className="w-4 h-4" style={{ color: m.color }} />}
                </button>
              ))}
            </div>
          </div>

          {/* Persona */}
          <div>
            <label className="text-xs text-gray-400 mb-2 block">Tucker Persona</label>
            <div className="space-y-2">
              {PERSONAS.map(p => (
                <button
                  key={p.id}
                  onClick={() => setConfig(c => ({ ...c, persona: p.id }))}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all text-left"
                  style={{
                    background: config.persona === p.id ? '#ffd70018' : '#141428',
                    borderColor: config.persona === p.id ? '#ffd70066' : '#2a2a4a',
                  }}
                >
                  <Sparkles className="w-4 h-4" style={{ color: config.persona === p.id ? '#ffd700' : '#6b7280' }} />
                  <div>
                    <div className="text-xs font-bold" style={{ color: config.persona === p.id ? '#ffd700' : '#e2e8f0' }}>{p.name}</div>
                    <div className="text-[10px] text-gray-500">{p.description}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Toggles */}
          <div className="space-y-3">
            {[
              { key: 'constitutionalMode', label: 'Constitutional Mode', desc: 'Route all responses through Atlas Lattice governance', color: '#00ff88' },
              { key: 'councilMode', label: 'Council Oversight', desc: 'Show Pantheon Council votes on each response', color: '#9b59b6' },
            ].map(({ key, label, desc, color }) => (
              <div key={key} className="flex items-center justify-between px-3 py-2.5 rounded-xl bg-[#141428] border border-[#2a2a4a]">
                <div>
                  <div className="text-xs font-bold text-gray-200">{label}</div>
                  <div className="text-[10px] text-gray-500">{desc}</div>
                </div>
                <button
                  onClick={() => setConfig(c => ({ ...c, [key]: !c[key as keyof TuckerConfig] }))}
                  className="w-10 h-5 rounded-full relative transition-colors"
                  style={{ background: (config[key as keyof TuckerConfig] as boolean) ? color + '88' : '#2a2a4a' }}
                >
                  <div className={`w-4 h-4 rounded-full bg-white absolute top-0.5 transition-transform ${(config[key as keyof TuckerConfig] as boolean) ? 'translate-x-5' : 'translate-x-0.5'}`} />
                </button>
              </div>
            ))}
          </div>

          {/* Temperature */}
          <div>
            <label className="text-xs text-gray-400 mb-2 block">Temperature: {config.temperature.toFixed(1)}</label>
            <input
              type="range" min="0" max="1" step="0.1"
              value={config.temperature}
              onChange={e => setConfig(c => ({ ...c, temperature: parseFloat(e.target.value) }))}
              className="w-full accent-[#ffd700]"
            />
            <div className="flex justify-between text-[9px] text-gray-600 mt-1">
              <span>Focused (0.0)</span><span>Balanced (0.7)</span><span>Creative (1.0)</span>
            </div>
          </div>

          {/* System prompt */}
          <div>
            <label className="text-xs text-gray-400 mb-2 block">System Prompt</label>
            <textarea
              value={config.systemPrompt}
              onChange={e => setConfig(c => ({ ...c, systemPrompt: e.target.value }))}
              rows={5}
              className="w-full bg-[#141428] border border-[#2a2a4a] rounded-xl px-3 py-2.5 text-xs text-gray-300 resize-none focus:outline-none focus:border-[#ffd70066] font-mono"
            />
          </div>
        </div>
      )}

      {/* Tab: History */}
      {tab === 'history' && (
        <div className="flex-1 overflow-y-auto p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-gray-200">Conversation History</h3>
            <span className="text-xs text-gray-500">{messages.filter(m => m.role !== 'system').length} messages</span>
          </div>
          <div className="space-y-2">
            {messages.filter(m => m.role !== 'system').map(msg => (
              <div key={msg.id} className="px-3 py-2 rounded-xl bg-[#141428] border border-[#1a1a2e]">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-bold" style={{ color: msg.role === 'user' ? '#4fc3f7' : '#ffd700' }}>
                    {msg.role === 'user' ? '👤 You' : '🤖 Tucker'}
                  </span>
                  <div className="flex items-center gap-2">
                    {msg.model && <ModelBadge model={msg.model} size="xs" />}
                    <span className="text-[9px] text-gray-600">{formatTime(msg.timestamp)}</span>
                  </div>
                </div>
                <p className="text-xs text-gray-400 line-clamp-2">{msg.content}</p>
              </div>
            ))}
          </div>
          <button
            onClick={() => {
              const txt = messages.filter(m => m.role !== 'system').map(m => `[${m.role.toUpperCase()}] ${m.content}`).join('\n\n');
              const blob = new Blob([txt], { type: 'text/plain' });
              const a = document.createElement('a');
              a.href = URL.createObjectURL(blob);
              a.download = `tucker-chat-${new Date().toISOString().slice(0, 10)}.txt`;
              a.click();
            }}
            className="mt-4 w-full px-3 py-2 rounded-xl bg-[#141428] border border-[#2a2a4a] text-xs text-gray-400 hover:text-gray-200 flex items-center justify-center gap-2 transition-colors"
          >
            <Download className="w-3.5 h-3.5" /> Export conversation
          </button>
        </div>
      )}

      {/* Tab: Council */}
      {tab === 'council' && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <h3 className="text-sm font-bold text-gray-200">Pantheon Council — Tucker Review</h3>
          <p className="text-xs text-gray-500">Council votes on Tucker's last response. Constitutional alignment status per member.</p>
          <div className="space-y-3">
            {COUNCIL_VOTES.map(v => (
              <div key={v.member} className="flex items-center gap-3 px-3 py-3 rounded-xl bg-[#141428] border border-[#1a1a2e]">
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0" style={{ background: v.color + '22', border: `1px solid ${v.color}44` }}>
                  {v.icon}
                </div>
                <div className="flex-1">
                  <div className="text-xs font-bold text-gray-200">{v.member}</div>
                  <div className="text-[10px] text-gray-500">{v.note}</div>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                  v.vote === 'approve' ? 'bg-green-900/30 text-green-400 border border-green-800' :
                  v.vote === 'flag' ? 'bg-red-900/30 text-red-400 border border-red-800' :
                  'bg-gray-800 text-gray-400 border border-gray-700'
                }`}>
                  {v.vote === 'approve' ? '✓ APPROVE' : v.vote === 'flag' ? '⚠ FLAG' : '— ABSTAIN'}
                </span>
              </div>
            ))}
          </div>
          <div className="px-3 py-3 rounded-xl border" style={{ background: '#00ff8811', borderColor: '#00ff8833' }}>
            <div className="text-xs font-bold text-green-400 mb-1">⚖ Constitutional Verdict</div>
            <p className="text-[10px] text-gray-400">3/4 council members approve. Constitutional alignment confirmed. Tucker V4 response cleared for delivery. Grok stress test deferred to next review cycle.</p>
          </div>
        </div>
      )}

      {/* Tab: About */}
      {tab === 'about' && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg"
              style={{ background: 'linear-gradient(135deg, #ffd700 0%, #ff6b35 50%, #4fc3f7 100%)' }}>
              T
            </div>
            <div>
              <h2 className="text-base font-bold">Tucker V4 Configurator</h2>
              <p className="text-xs text-gray-400">Co-designed with GPT-4.1 and Gemini 2.5 Pro</p>
            </div>
          </div>

          <div className="space-y-2 text-xs text-gray-400">
            {[
              ['Source Repo', 'splitmerge420/tucker-gemini-GPT-'],
              ['Aluminum OS Integration', 'ALUM-INT-008'],
              ['Primary Model', 'GPT-4.1 (Tucker co-design)'],
              ['Synthesis Layer', 'Gemini 2.5 Pro'],
              ['Constitutional Oversight', 'Claude + Kintsugi policies'],
              ['Truth Layer', 'Grok (stress testing)'],
              ['Governance', 'Atlas Lattice Foundation'],
              ['Version', 'V4 (V3 Explorer also available)'],
              ['Origin', 'Google AI Studio → aluminum-os migration'],
              ['Status', '🟡 IN PROGRESS — code migration pending'],
            ].map(([k, v]) => (
              <div key={k} className="flex justify-between py-1.5 border-b border-[#1a1a2e]">
                <span className="text-gray-500">{k}</span>
                <span className="text-gray-300 text-right max-w-[60%]">{v}</span>
              </div>
            ))}
          </div>

          <div className="px-3 py-3 rounded-xl border border-[#2a2a4a] bg-[#141428]">
            <div className="text-xs font-bold text-gray-300 mb-2">Migration Status</div>
            <p className="text-[10px] text-gray-500 leading-relaxed">
              Tucker V4 was co-designed in Google AI Studio with GPT and Gemini. The source repo
              (tucker-gemini-GPT-) was created 2026-03-21 and is being migrated into Aluminum OS.
              Full chatbot source code integration is in progress. Constitutional substrate and
              Pantheon Council integration complete. Kintsugi policy bindings pending code review.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-[10px]">
            {[
              { label: 'Tucker V3 Explorer', status: 'PENDING', color: '#ff9900' },
              { label: 'Tucker V4 Configurator', status: 'IN PROGRESS', color: '#ffd700' },
              { label: 'Constitutional Binding', status: 'ACTIVE', color: '#00ff88' },
              { label: 'Council Integration', status: 'ACTIVE', color: '#00ff88' },
              { label: 'Kintsugi Policies', status: 'PENDING', color: '#ff9900' },
              { label: 'Gemini API Bridge', status: 'PENDING', color: '#ff9900' },
            ].map(({ label, status, color }) => (
              <div key={label} className="px-2.5 py-2 rounded-lg bg-[#141428] border border-[#1a1a2e]">
                <div className="text-gray-400 mb-1">{label}</div>
                <span className="font-bold text-[9px]" style={{ color }}>{status}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Response generator (placeholder until Tucker source is migrated) ───
function generateTuckerResponse(input: string, config: TuckerConfig): string {
  const lc = input.toLowerCase();

  if (lc.includes('aluminum os') || lc.includes('architecture')) {
    return "Aluminum OS runs on a 5-ring constitutional architecture:\n\n• **Ring 0** — Forge Core (Rust kernel: BuddyAllocator, AgentRegistry, IntentScheduler)\n• **Ring 1** — Inference Engine (10 models, 3-tier routing)\n• **Ring 2** — SHELDONBRAIN (25.2 GB memory: Working + Long-Term + Swarm)\n• **Ring 3** — Pantheon Council (10+1 members, quorum governance)\n• **Ring 4** — Noosphere (35 apps, 120 artifacts, constitutional substrate)\n\nI'm wired into Ring 3 (Council oversight) and Ring 4 (app layer). What aspect do you want to dig into?";
  }

  if (lc.includes('tucker') || lc.includes('chatbot') || lc.includes('who are you')) {
    return "I'm Tucker — a constitutional chatbot co-designed with GPT-4.1 and Gemini 2.5 Pro in Google AI Studio.\n\nV4 is the canonical build. V3 Explorer is the research mode. Both are now being integrated into Aluminum OS as ALUM-INT-008.\n\nMy constitutional layer means every response I generate goes through Kintsugi policy checks and Pantheon Council oversight. I'm not just a chatbot — I'm a governed AI interface.";
  }

  if (lc.includes('code') || lc.includes('rust') || lc.includes('python') || lc.includes('typescript')) {
    return "Happy to help with code. I'm aware of the Aluminum OS codebase:\n\n```\naluminum-os/\n├── src/           # Rust Ring 0 kernel\n├── python/core/   # Python Ring 1 (manus_core, health_layer)\n├── client/src/    # TypeScript React desktop\n├── kintsugi/      # OPA policy engine\n└── janus/         # Constitutional continuity system\n```\n\nWhat are you building?";
  }

  if (lc.includes('health') || lc.includes('hipaa') || lc.includes('fhir')) {
    return "Healthcare is a core domain in Aluminum OS — I have full awareness of the Health Layer:\n\n• **HIPAA** compliance: 100% (7 modules)\n• **FHIR R4**: Online with PQC signatures\n• **Constitutional rules**: KINTSUGI-009 through KINTSUGI-016\n• **Health connectors**: One Medical, MyChart, Teams (via Layer 5)\n\nI can help with clinical data flows, amendment policies, or the AHCEP escalation protocol. What's the use case?";
  }

  if (lc.includes('janus')) {
    return "Janus is the constitutional continuity system — it keeps every agent instance synchronized with the environment so new spawns don't need manual context loading.\n\nJanus V2 (active) layers:\n1. **Boot Layer** — hardcoded pointers in userMemories\n2. **Warm Layer** — Notion pull on spawn\n3. **Hot Layer** — GitHub pull on demand\n4. **Heartbeat Layer** — daily Chrome scheduled task\n\nThe `janus_boot.py` script is the executable implementation. Want to walk through it?";
  }

  if (lc.includes('kintsugi')) {
    return "Kintsugi is the Aluminum OS constitutional governance layer — built on OPA (Open Policy Agent).\n\n**16 policy rules** (KINTSUGI-001 → KINTSUGI-016):\n- KINTSUGI-001 through KINTSUGI-014: Core OS rules\n- KINTSUGI-015 through KINTSUGI-016: Healthcare rules\n\nAll agent actions are pre-screened against Kintsugi. Violations are logged with PQC signatures for audit. The `golden_trace.py` SDK makes policy checks programmatic.\n\nWhat policy area are you looking at?";
  }

  if (lc.includes('gemini') || lc.includes('gpt') || lc.includes('model')) {
    const model = MODELS.find(m => m.id === config.model) ?? MODELS[0];
    return `Currently routing through **${model.name}** ${model.icon}.\n\nThe Aluminum OS model stack:\n• **GPT-4.1** — Tucker's co-designer, primary reasoning\n• **Gemini 2.5 Pro** — synthesis + scale + multimodal\n• **Claude** — constitutional oversight, safety audit\n• **Grok** — truth verification, contrarian stress test\n• **DeepSeek** — specialist memory + sovereign tasks\n\nAuto-routing picks the best model per request based on cost, quality, and constitutional constraints. Want to switch to a specific model?`;
  }

  // Default thoughtful response
  return `Got it. Let me think through that constitutionally.\n\nYou said: "${input}"\n\nMy take: this intersects with ${config.constitutionalMode ? 'constitutional governance (active oversight)' : 'standard reasoning (constitutional mode off)'} and the current Aluminum OS architecture context.\n\nCould you be more specific about what you're trying to accomplish? I can route this to the right Council member (GPT for architecture, Gemini for synthesis, Claude for constitutional review, Grok for stress testing) depending on the domain.`;
}
