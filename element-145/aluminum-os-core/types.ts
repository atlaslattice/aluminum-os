
export enum ModuleType {
  SYNAPTIC_FORGE = 'SynapticForge',
  CEREBELLUM = 'Cerebellum',
  THALAMUS = 'Thalamus',
  CHRONOS = 'Chronos',
  NOSTR = 'NostrClient'
}

export interface NeuralEvent {
  id: string;
  timestamp: number;
  type: 'thought' | 'action' | 'relay' | 'memory';
  content: string;
  metadata?: any;
}

export interface MemoryNode {
  id: string;
  label: string;
  strength: number;
  connections: string[];
}

export interface NostrEvent {
  id: string;
  pubkey: string;
  created_at: number;
  kind: number;
  tags: string[][];
  content: string;
  sig: string;
}
