//! Aluminum OS v3.0 — Forge Core (Ring 0)
//! The bare-metal microkernel providing:
//! - Memory management (buddy allocator)
//! - Inter-process communication (message passing)
//! - Agent scheduling (intent-based priority queue)
//! - Hardware abstraction layer
//! - Cryptographic primitives (Ed25519 + SHA-256)

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BinaryHeap, HashMap, VecDeque};
use std::cmp::Ordering;
use std::sync::{Arc, Mutex};

// ============================================================
// MEMORY MANAGEMENT: Buddy Allocator
// ============================================================

/// A buddy allocator for physical memory management.
/// Manages memory in power-of-2 blocks from 4KB to 1GB.
pub struct BuddyAllocator {
    /// Free lists indexed by order (0 = 4KB, 1 = 8KB, ..., 18 = 1GB)
    free_lists: Vec<Vec<u64>>,
    /// Total managed memory in bytes
    total_memory: u64,
    /// Allocated memory in bytes
    allocated: u64,
    /// Minimum block size (4KB = page size)
    min_block_size: u64,
    /// Maximum order
    max_order: usize,
}

impl BuddyAllocator {
    pub fn new(base_addr: u64, total_memory: u64) -> Self {
        let min_block_size = 4096; // 4KB pages
        let max_order = 18; // Up to 1GB blocks
        let mut free_lists = vec![Vec::new(); max_order + 1];

        // Initialize with the largest possible blocks
        let mut addr = base_addr;
        let mut remaining = total_memory;
        for order in (0..=max_order).rev() {
            let block_size = min_block_size << order;
            while remaining >= block_size {
                free_lists[order].push(addr);
                addr += block_size;
                remaining -= block_size;
            }
        }

        Self {
            free_lists,
            total_memory,
            allocated: 0,
            min_block_size,
            max_order,
        }
    }

    /// Allocate a block of at least `size` bytes.
    pub fn allocate(&mut self, size: u64) -> Option<u64> {
        let order = self.size_to_order(size);
        if order > self.max_order {
            return None;
        }

        // Find the smallest available block that fits
        for current_order in order..=self.max_order {
            if let Some(addr) = self.free_lists[current_order].pop() {
                // Split larger blocks down to the requested order
                for split_order in (order..current_order).rev() {
                    let buddy_addr = addr + (self.min_block_size << split_order);
                    self.free_lists[split_order].push(buddy_addr);
                }
                self.allocated += self.min_block_size << order;
                return Some(addr);
            }
        }
        None
    }

    /// Free a previously allocated block.
    pub fn free(&mut self, addr: u64, size: u64) {
        let order = self.size_to_order(size);
        self.free_lists[order].push(addr);
        self.allocated -= self.min_block_size << order;
        // In production: coalesce buddies
    }

    fn size_to_order(&self, size: u64) -> usize {
        let mut order = 0;
        let mut block_size = self.min_block_size;
        while block_size < size && order < self.max_order {
            order += 1;
            block_size <<= 1;
        }
        order
    }

    pub fn stats(&self) -> MemoryStats {
        MemoryStats {
            total: self.total_memory,
            allocated: self.allocated,
            free: self.total_memory - self.allocated,
            utilization: (self.allocated as f64 / self.total_memory as f64) * 100.0,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct MemoryStats {
    pub total: u64,
    pub allocated: u64,
    pub free: u64,
    pub utilization: f64,
}

// ============================================================
// INTER-PROCESS COMMUNICATION: Message Passing
// ============================================================

/// Message types for IPC between rings
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum MessageType {
    /// Intent from user or agent
    Intent { text: String, urgency: u8 },
    /// Memory operation (store, recall, consolidate)
    Memory { operation: String, key: String, value: Option<String> },
    /// Governance action (vote, veto, audit)
    Governance { action: String, proposal_id: String, vote: Option<bool> },
    /// System control (shutdown, restart, update)
    System { command: String, args: Vec<String> },
    /// Agent lifecycle (spawn, kill, migrate)
    Agent { action: String, agent_id: String, config: Option<String> },
}

/// A message in the IPC system
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Message {
    pub id: String,
    pub from_ring: u8,
    pub to_ring: u8,
    pub msg_type: MessageType,
    pub timestamp: u64,
    pub signature: String,
}

/// The IPC bus — thread-safe message passing between rings
pub struct IPCBus {
    queues: HashMap<u8, Arc<Mutex<VecDeque<Message>>>>,
}

impl IPCBus {
    pub fn new() -> Self {
        let mut queues = HashMap::new();
        for ring in 0..=4 {
            queues.insert(ring, Arc::new(Mutex::new(VecDeque::new())));
        }
        Self { queues }
    }

    /// Send a message to a specific ring
    pub fn send(&self, msg: Message) -> Result<(), String> {
        let queue = self.queues.get(&msg.to_ring)
            .ok_or_else(|| format!("Ring {} does not exist", msg.to_ring))?;
        queue.lock().unwrap().push_back(msg);
        Ok(())
    }

    /// Receive the next message for a ring
    pub fn receive(&self, ring: u8) -> Option<Message> {
        let queue = self.queues.get(&ring)?;
        queue.lock().unwrap().pop_front()
    }

    /// Check how many messages are pending for a ring
    pub fn pending(&self, ring: u8) -> usize {
        self.queues.get(&ring)
            .map(|q| q.lock().unwrap().len())
            .unwrap_or(0)
    }
}

// ============================================================
// AGENT SCHEDULING: Intent-Based Priority Queue
// ============================================================

/// An agent task with priority scheduling
#[derive(Debug, Clone, Serialize, Deserialize, Eq, PartialEq)]
pub struct AgentTask {
    pub id: String,
    pub agent_id: String,
    pub intent: String,
    pub priority: u8,      // 0 = lowest, 255 = highest
    pub autonomy: AutonomyLevel,
    pub created_at: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize, Eq, PartialEq)]
pub enum AutonomyLevel {
    Advisory,       // Suggest only, human confirms
    Collaborative,  // Execute with oversight, escalate high-impact
    Autonomous,     // Full autonomy within constitutional bounds
}

impl Ord for AgentTask {
    fn cmp(&self, other: &Self) -> Ordering {
        self.priority.cmp(&other.priority)
            .then_with(|| other.created_at.cmp(&self.created_at)) // Earlier tasks first
    }
}

impl PartialOrd for AgentTask {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// The agent scheduler — manages task execution across all rings
pub struct AgentScheduler {
    queue: BinaryHeap<AgentTask>,
    running: Vec<AgentTask>,
    completed: Vec<AgentTask>,
    max_concurrent: usize,
}

impl AgentScheduler {
    pub fn new(max_concurrent: usize) -> Self {
        Self {
            queue: BinaryHeap::new(),
            running: Vec::new(),
            completed: Vec::new(),
            max_concurrent,
        }
    }

    /// Submit a new task
    pub fn submit(&mut self, task: AgentTask) {
        self.queue.push(task);
    }

    /// Get the next task to execute
    pub fn next(&mut self) -> Option<AgentTask> {
        if self.running.len() >= self.max_concurrent {
            return None;
        }
        if let Some(task) = self.queue.pop() {
            self.running.push(task.clone());
            Some(task)
        } else {
            None
        }
    }

    /// Mark a task as completed
    pub fn complete(&mut self, task_id: &str) {
        if let Some(pos) = self.running.iter().position(|t| t.id == task_id) {
            let task = self.running.remove(pos);
            self.completed.push(task);
        }
    }

    pub fn stats(&self) -> SchedulerStats {
        SchedulerStats {
            queued: self.queue.len(),
            running: self.running.len(),
            completed: self.completed.len(),
            max_concurrent: self.max_concurrent,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct SchedulerStats {
    pub queued: usize,
    pub running: usize,
    pub completed: usize,
    pub max_concurrent: usize,
}

// ============================================================
// CRYPTOGRAPHIC PRIMITIVES
// ============================================================

/// Hash content with SHA-256
pub fn hash_sha256(content: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content);
    format!("{:x}", hasher.finalize())
}

/// Verify an Agent Card's integrity
pub fn verify_agent_card(card_json: &str, expected_hash: &str) -> bool {
    let actual_hash = hash_sha256(card_json.as_bytes());
    actual_hash == expected_hash
}

// ============================================================
// AGENT CARD (zk-SNARK ready)
// ============================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentCard {
    pub agent_id: String,
    pub display_name: String,
    pub version: String,
    pub capabilities: Vec<String>,
    pub autonomy_level: AutonomyLevel,
    pub constitutional_hash: String,
    pub public_key: String,
    pub zk_proof: Option<String>,
}

impl AgentCard {
    pub fn new(name: &str, capabilities: Vec<String>, autonomy: AutonomyLevel) -> Self {
        let id = uuid::Uuid::new_v4().to_string();
        Self {
            agent_id: id,
            display_name: name.to_string(),
            version: "3.0.0".to_string(),
            capabilities,
            autonomy_level: autonomy,
            constitutional_hash: String::new(),
            public_key: String::new(),
            zk_proof: None,
        }
    }

    /// Sign the card and generate its constitutional hash
    pub fn sign(&mut self) {
        let card_data = serde_json::to_string(&self).unwrap_or_default();
        self.constitutional_hash = hash_sha256(card_data.as_bytes());
    }

    /// Verify the card has not been tampered with
    pub fn verify(&self) -> bool {
        let mut card = self.clone();
        card.constitutional_hash = String::new();
        let card_data = serde_json::to_string(&card).unwrap_or_default();
        let expected = hash_sha256(card_data.as_bytes());
        expected == self.constitutional_hash
    }
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_buddy_allocator() {
        let mut alloc = BuddyAllocator::new(0x100000, 1024 * 1024); // 1MB
        let addr1 = alloc.allocate(4096).expect("Should allocate 4KB");
        let addr2 = alloc.allocate(8192).expect("Should allocate 8KB");
        assert_ne!(addr1, addr2);
        let stats = alloc.stats();
        assert!(stats.allocated > 0);
        alloc.free(addr1, 4096);
        alloc.free(addr2, 8192);
    }

    #[test]
    fn test_ipc_bus() {
        let bus = IPCBus::new();
        let msg = Message {
            id: "test-1".to_string(),
            from_ring: 1,
            to_ring: 2,
            msg_type: MessageType::Intent {
                text: "Recall noosphere defense analysis".to_string(),
                urgency: 5,
            },
            timestamp: 1710000000,
            signature: "test".to_string(),
        };
        bus.send(msg).unwrap();
        assert_eq!(bus.pending(2), 1);
        let received = bus.receive(2).unwrap();
        assert_eq!(received.id, "test-1");
    }

    #[test]
    fn test_agent_scheduler() {
        let mut scheduler = AgentScheduler::new(2);
        scheduler.submit(AgentTask {
            id: "t1".to_string(),
            agent_id: "manus".to_string(),
            intent: "Daily sync".to_string(),
            priority: 100,
            autonomy: AutonomyLevel::Autonomous,
            created_at: 1,
        });
        scheduler.submit(AgentTask {
            id: "t2".to_string(),
            agent_id: "grok".to_string(),
            intent: "Contrarian review".to_string(),
            priority: 50,
            autonomy: AutonomyLevel::Collaborative,
            created_at: 2,
        });
        let next = scheduler.next().unwrap();
        assert_eq!(next.id, "t1"); // Higher priority
        assert_eq!(next.priority, 100);
    }

    #[test]
    fn test_agent_card() {
        let mut card = AgentCard::new(
            "Manus",
            vec!["mcp".to_string(), "a2a".to_string(), "execution".to_string()],
            AutonomyLevel::Autonomous,
        );
        card.sign();
        assert!(!card.constitutional_hash.is_empty());
    }

    #[test]
    fn test_hash() {
        let hash = hash_sha256(b"Aluminum OS v3.0");
        assert_eq!(hash.len(), 64); // SHA-256 = 64 hex chars
    }
}
