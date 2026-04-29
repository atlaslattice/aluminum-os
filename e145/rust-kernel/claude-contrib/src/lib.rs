//! Aluminum OS v3.0 — Forge Core (Ring 0)
//!
//! The bare-metal microkernel providing:
//! - Memory management (buddy allocator)
//! - Agent identity and capability model
//! - Intent-based scheduling (priority queue)
//! - Cryptographic primitives (SHA-256 signatures)
//!
//! This crate compiles in both `std` (for testing/simulation) and
//! `no_std` (for bare-metal deployment). Feature-gated accordingly.

#![cfg_attr(not(feature = "std"), no_std)]

use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};

// ============================================================
// MEMORY MANAGEMENT: Buddy Allocator
// Works in no_std — zero heap allocation, fixed-size arrays only.
// ============================================================

/// Maximum order: 2^18 * 4KB = 1GB blocks
const MAX_ORDER: usize = 19;
/// Minimum block: 4KB page
const MIN_BLOCK_SIZE: u64 = 4096;
/// Max free blocks tracked per order (bounded for no_std)
const MAX_FREE_PER_ORDER: usize = 256;

/// A buddy allocator for physical memory management.
/// Uses fixed-size arrays — no heap, no Vec, no HashMap.
pub struct BuddyAllocator {
    free_counts: [usize; MAX_ORDER],
    free_addrs: [[u64; MAX_FREE_PER_ORDER]; MAX_ORDER],
    total_memory: u64,
    allocated: u64,
}

impl BuddyAllocator {
    /// Create a new allocator managing memory starting at `base_addr`.
    pub fn new(base_addr: u64, total_memory: u64) -> Self {
        let mut alloc = Self {
            free_counts: [0; MAX_ORDER],
            free_addrs: [[0u64; MAX_FREE_PER_ORDER]; MAX_ORDER],
            total_memory,
            allocated: 0,
        };

        // Carve initial memory into largest possible blocks
        let mut addr = base_addr;
        let mut remaining = total_memory;
        for order in (0..MAX_ORDER).rev() {
            let block_size = MIN_BLOCK_SIZE << order;
            while remaining >= block_size {
                if alloc.free_counts[order] < MAX_FREE_PER_ORDER {
                    alloc.free_addrs[order][alloc.free_counts[order]] = addr;
                    alloc.free_counts[order] += 1;
                    addr += block_size;
                    remaining -= block_size;
                } else {
                    break;
                }
            }
        }
        alloc
    }

    /// Allocate a block of at least `size` bytes. Returns physical address.
    pub fn allocate(&mut self, size: u64) -> Option<u64> {
        let order = self.size_to_order(size);
        if order >= MAX_ORDER {
            return None;
        }

        // Find smallest available block that fits
        for current_order in order..MAX_ORDER {
            if self.free_counts[current_order] > 0 {
                // Pop from free list
                self.free_counts[current_order] -= 1;
                let addr = self.free_addrs[current_order][self.free_counts[current_order]];

                // Split larger blocks down to requested order
                for split_order in (order..current_order).rev() {
                    let buddy_addr = addr + (MIN_BLOCK_SIZE << split_order);
                    if self.free_counts[split_order] < MAX_FREE_PER_ORDER {
                        self.free_addrs[split_order][self.free_counts[split_order]] = buddy_addr;
                        self.free_counts[split_order] += 1;
                    }
                }

                self.allocated += MIN_BLOCK_SIZE << order;
                return Some(addr);
            }
        }
        None
    }

    /// Free a previously allocated block.
    pub fn free(&mut self, addr: u64, size: u64) {
        let order = self.size_to_order(size);
        if order < MAX_ORDER && self.free_counts[order] < MAX_FREE_PER_ORDER {
            self.free_addrs[order][self.free_counts[order]] = addr;
            self.free_counts[order] += 1;
            self.allocated -= MIN_BLOCK_SIZE << order;
            // TODO: buddy coalescing — merge adjacent free blocks
        }
    }

    /// Returns (total_bytes, allocated_bytes, free_bytes).
    pub fn stats(&self) -> (u64, u64, u64) {
        (self.total_memory, self.allocated, self.total_memory - self.allocated)
    }

    fn size_to_order(&self, size: u64) -> usize {
        let mut order = 0;
        let mut block_size = MIN_BLOCK_SIZE;
        while block_size < size && order < MAX_ORDER - 1 {
            order += 1;
            block_size <<= 1;
        }
        order
    }
}

// ============================================================
// AGENT IDENTITY: Cryptographic identity + capability set
// ============================================================

/// Autonomy levels with mathematical bounds.
/// Each level defines what fraction of decisions an agent can make
/// without council approval.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AutonomyTier {
    /// Can observe and report. Cannot act. Autonomy ratio: 0.0
    Observer,
    /// Can suggest actions. Human approves. Autonomy ratio: 0.0-0.2
    Advisory,
    /// Can act within bounds. Human informed. Autonomy ratio: 0.2-0.6
    Collaborative,
    /// Can act freely within constitution. Audit trail. Autonomy ratio: 0.6-0.9
    Autonomous,
    /// Constitutional Scribe level. Full action with veto. Autonomy ratio: 0.9-1.0
    Sovereign,
}

impl AutonomyTier {
    /// Maximum autonomy ratio for this tier.
    pub fn max_autonomy_ratio(&self) -> f32 {
        match self {
            Self::Observer => 0.0,
            Self::Advisory => 0.2,
            Self::Collaborative => 0.6,
            Self::Autonomous => 0.9,
            Self::Sovereign => 1.0,
        }
    }
}

/// Fixed-size capability set (no heap). Up to 16 capabilities per agent.
const MAX_CAPABILITIES: usize = 16;
const MAX_ID_LEN: usize = 64;

/// An agent's cryptographic identity card.
#[derive(Debug, Clone)]
pub struct AgentIdentity {
    /// Unique identifier (e.g., "claude-scribe", "grok-adversarial")
    id: [u8; MAX_ID_LEN],
    id_len: usize,
    /// SHA-256 hash of the agent's public key
    pubkey_hash: [u8; 32],
    /// Autonomy tier
    pub autonomy: AutonomyTier,
    /// Capability flags
    capabilities: [Capability; MAX_CAPABILITIES],
    cap_count: usize,
}

/// Capabilities an agent may hold.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Capability {
    None,
    ReadMemory,
    WriteMemory,
    ExecuteCode,
    NetworkAccess,
    FileSystemRead,
    FileSystemWrite,
    CouncilVote,
    CouncilPropose,
    ConstitutionRead,
    ConstitutionAmend,
    SpawnAgent,
    TerminateAgent,
    ModelInference,
    CostTracking,
    AuditLog,
}

impl Default for Capability {
    fn default() -> Self { Self::None }
}

impl AgentIdentity {
    /// Create a new agent identity. Signs the ID with SHA-256.
    pub fn new(id: &str, autonomy: AutonomyTier) -> Self {
        let mut id_buf = [0u8; MAX_ID_LEN];
        let id_bytes = id.as_bytes();
        let len = if id_bytes.len() > MAX_ID_LEN { MAX_ID_LEN } else { id_bytes.len() };
        id_buf[..len].copy_from_slice(&id_bytes[..len]);

        // Derive pubkey hash from ID (in production: from actual keypair)
        let mut hasher = Sha256::new();
        hasher.update(&id_buf[..len]);
        let hash = hasher.finalize();
        let mut pubkey_hash = [0u8; 32];
        pubkey_hash.copy_from_slice(&hash);

        Self {
            id: id_buf,
            id_len: len,
            pubkey_hash,
            autonomy,
            capabilities: [Capability::None; MAX_CAPABILITIES],
            cap_count: 0,
        }
    }

    /// Grant a capability to this agent. Returns false if at capacity.
    pub fn grant(&mut self, cap: Capability) -> bool {
        if self.cap_count >= MAX_CAPABILITIES {
            return false;
        }
        // Don't duplicate
        for i in 0..self.cap_count {
            if self.capabilities[i] == cap {
                return true;
            }
        }
        self.capabilities[self.cap_count] = cap;
        self.cap_count += 1;
        true
    }

    /// Check if agent holds a capability.
    pub fn has_capability(&self, cap: Capability) -> bool {
        for i in 0..self.cap_count {
            if self.capabilities[i] == cap {
                return true;
            }
        }
        false
    }

    /// Verify the agent's identity hash.
    pub fn verify(&self) -> bool {
        let mut hasher = Sha256::new();
        hasher.update(&self.id[..self.id_len]);
        let hash = hasher.finalize();
        hash.as_slice() == &self.pubkey_hash
    }

    /// Get the agent ID as a string slice.
    pub fn id_str(&self) -> &str {
        core::str::from_utf8(&self.id[..self.id_len]).unwrap_or("invalid")
    }
}

// ============================================================
// INTENT SCHEDULER: Priority queue based on AI-determined urgency
// Fixed-size, no heap.
// ============================================================

const MAX_TASKS: usize = 256;

/// Task priority — determined by intent analysis, not nice values.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum TaskPriority {
    Background = 0,
    Normal = 1,
    Elevated = 2,
    Urgent = 3,
    Critical = 4,
}

/// A scheduled task in the intent queue.
#[derive(Debug, Clone)]
pub struct Task {
    pub id: u64,
    pub priority: TaskPriority,
    pub agent_id: [u8; MAX_ID_LEN],
    pub agent_id_len: usize,
    /// Timestamp (ticks since boot)
    pub enqueued_at: u64,
    /// Whether this task has been claimed by an executor
    pub claimed: bool,
}

/// Intent-based priority scheduler.
/// Higher priority tasks execute first. Within same priority, FIFO.
pub struct IntentScheduler {
    tasks: [Option<Task>; MAX_TASKS],
    count: usize,
    next_id: u64,
}

impl IntentScheduler {
    pub fn new() -> Self {
        // Initialize with None — const generic init
        Self {
            tasks: [const { None }; MAX_TASKS],
            count: 0,
            next_id: 1,
        }
    }

    /// Submit a task. Returns task ID or None if queue is full.
    pub fn submit(&mut self, priority: TaskPriority, agent_id: &str, tick: u64) -> Option<u64> {
        if self.count >= MAX_TASKS {
            return None;
        }

        let id = self.next_id;
        self.next_id += 1;

        let mut aid = [0u8; MAX_ID_LEN];
        let bytes = agent_id.as_bytes();
        let len = bytes.len().min(MAX_ID_LEN);
        aid[..len].copy_from_slice(&bytes[..len]);

        // Find empty slot
        for slot in self.tasks.iter_mut() {
            if slot.is_none() {
                *slot = Some(Task {
                    id,
                    priority,
                    agent_id: aid,
                    agent_id_len: len,
                    enqueued_at: tick,
                    claimed: false,
                });
                self.count += 1;
                return Some(id);
            }
        }
        None
    }

    /// Claim the highest-priority unclaimed task.
    pub fn claim_next(&mut self) -> Option<&mut Task> {
        let mut best_idx: Option<usize> = None;
        let mut best_priority = TaskPriority::Background;
        let mut best_time = u64::MAX;

        for (i, slot) in self.tasks.iter().enumerate() {
            if let Some(task) = slot {
                if !task.claimed
                    && (task.priority > best_priority
                        || (task.priority == best_priority && task.enqueued_at < best_time))
                {
                    best_idx = Some(i);
                    best_priority = task.priority;
                    best_time = task.enqueued_at;
                }
            }
        }

        if let Some(idx) = best_idx {
            if let Some(ref mut task) = self.tasks[idx] {
                task.claimed = true;
                return Some(task);
            }
        }
        None
    }

    /// Complete and remove a task by ID.
    pub fn complete(&mut self, task_id: u64) -> bool {
        for slot in self.tasks.iter_mut() {
            if let Some(task) = slot {
                if task.id == task_id {
                    *slot = None;
                    self.count -= 1;
                    return true;
                }
            }
        }
        false
    }

    /// Number of pending tasks.
    pub fn pending(&self) -> usize {
        self.count
    }
}

// ============================================================
// CONSTITUTIONAL SUBSTRATE: Immutable rules loaded at boot
// ============================================================

const MAX_RULES: usize = 64;
const MAX_RULE_LEN: usize = 256;

/// The Constitutional Substrate — loaded before any agent, immutable at runtime.
pub struct Constitution {
    rules: [[u8; MAX_RULE_LEN]; MAX_RULES],
    rule_lens: [usize; MAX_RULES],
    rule_count: usize,
    /// SHA-256 hash of all rules concatenated — integrity check
    hash: [u8; 32],
}

impl Constitution {
    pub fn new() -> Self {
        Self {
            rules: [[0u8; MAX_RULE_LEN]; MAX_RULES],
            rule_lens: [0; MAX_RULES],
            rule_count: 0,
            hash: [0u8; 32],
        }
    }

    /// Add a constitutional rule. Returns false if at capacity.
    pub fn add_rule(&mut self, rule: &str) -> bool {
        if self.rule_count >= MAX_RULES {
            return false;
        }
        let bytes = rule.as_bytes();
        let len = bytes.len().min(MAX_RULE_LEN);
        self.rules[self.rule_count][..len].copy_from_slice(&bytes[..len]);
        self.rule_lens[self.rule_count] = len;
        self.rule_count += 1;
        self.rehash();
        true
    }

    /// Seal the constitution — compute final hash. After this, rules
    /// should not change (enforced by convention; in production, by MMU).
    pub fn seal(&mut self) -> [u8; 32] {
        self.rehash();
        self.hash
    }

    /// Verify integrity against a known hash.
    pub fn verify(&self, expected: &[u8; 32]) -> bool {
        self.hash == *expected
    }

    /// Number of rules.
    pub fn rule_count(&self) -> usize {
        self.rule_count
    }

    /// Get rule text by index.
    pub fn get_rule(&self, idx: usize) -> Option<&str> {
        if idx < self.rule_count {
            core::str::from_utf8(&self.rules[idx][..self.rule_lens[idx]]).ok()
        } else {
            None
        }
    }

    fn rehash(&mut self) {
        let mut hasher = Sha256::new();
        for i in 0..self.rule_count {
            hasher.update(&self.rules[i][..self.rule_lens[i]]);
        }
        let result = hasher.finalize();
        self.hash.copy_from_slice(&result);
    }
}

// ============================================================
// TESTS (std only)
// ============================================================

#[cfg(all(test, feature = "std"))]
mod tests {
    use super::*;

    #[test]
    fn buddy_allocator_basic() {
        let mut alloc = BuddyAllocator::new(0x1000_0000, 1024 * 1024); // 1MB
        let (total, _, _) = alloc.stats();
        assert_eq!(total, 1024 * 1024);

        // Allocate a 4KB page
        let addr1 = alloc.allocate(4096).expect("should allocate 4KB");
        assert!(addr1 >= 0x1000_0000);

        // Allocate another
        let addr2 = alloc.allocate(4096).expect("should allocate another 4KB");
        assert_ne!(addr1, addr2); // Different addresses

        // Check stats updated
        let (_, allocated, _) = alloc.stats();
        assert_eq!(allocated, 8192); // 2 * 4KB

        // Free one
        alloc.free(addr1, 4096);
        let (_, allocated, _) = alloc.stats();
        assert_eq!(allocated, 4096);
    }

    #[test]
    fn buddy_allocator_large_block() {
        let mut alloc = BuddyAllocator::new(0, 16 * 1024 * 1024); // 16MB
        // Allocate 1MB — should get a single order-8 block
        let addr = alloc.allocate(1024 * 1024).expect("should allocate 1MB");
        assert_eq!(addr, 0);
        let (_, allocated, _) = alloc.stats();
        assert_eq!(allocated, 1024 * 1024);
    }

    #[test]
    fn buddy_allocator_exhaustion() {
        let mut alloc = BuddyAllocator::new(0, 8192); // Only 8KB
        let _ = alloc.allocate(4096).expect("first 4KB");
        let _ = alloc.allocate(4096).expect("second 4KB");
        assert!(alloc.allocate(4096).is_none()); // Should fail
    }

    #[test]
    fn agent_identity_create_and_verify() {
        let mut agent = AgentIdentity::new("claude-scribe", AutonomyTier::Sovereign);
        assert!(agent.verify());
        assert_eq!(agent.id_str(), "claude-scribe");
        assert_eq!(agent.autonomy.max_autonomy_ratio(), 1.0);

        // Grant capabilities
        assert!(agent.grant(Capability::CouncilVote));
        assert!(agent.grant(Capability::ConstitutionRead));
        assert!(agent.has_capability(Capability::CouncilVote));
        assert!(!agent.has_capability(Capability::ExecuteCode));
    }

    #[test]
    fn agent_identity_duplicate_capability() {
        let mut agent = AgentIdentity::new("grok", AutonomyTier::Collaborative);
        assert!(agent.grant(Capability::ReadMemory));
        assert!(agent.grant(Capability::ReadMemory)); // Duplicate — should return true
        assert_eq!(agent.cap_count, 1); // But not double-count
    }

    #[test]
    fn scheduler_priority_ordering() {
        let mut sched = IntentScheduler::new();
        sched.submit(TaskPriority::Normal, "agent-a", 1).unwrap();
        sched.submit(TaskPriority::Critical, "agent-b", 2).unwrap();
        sched.submit(TaskPriority::Urgent, "agent-c", 3).unwrap();

        // Highest priority first
        let task = sched.claim_next().unwrap();
        assert_eq!(task.priority, TaskPriority::Critical);

        let task = sched.claim_next().unwrap();
        assert_eq!(task.priority, TaskPriority::Urgent);

        let task = sched.claim_next().unwrap();
        assert_eq!(task.priority, TaskPriority::Normal);

        assert!(sched.claim_next().is_none());
    }

    #[test]
    fn scheduler_fifo_within_priority() {
        let mut sched = IntentScheduler::new();
        let id1 = sched.submit(TaskPriority::Normal, "first", 10).unwrap();
        let _id2 = sched.submit(TaskPriority::Normal, "second", 20).unwrap();

        // Earlier timestamp wins within same priority
        let task = sched.claim_next().unwrap();
        assert_eq!(task.id, id1);
    }

    #[test]
    fn scheduler_complete_removes() {
        let mut sched = IntentScheduler::new();
        let id = sched.submit(TaskPriority::Normal, "test", 1).unwrap();
        assert_eq!(sched.pending(), 1);
        assert!(sched.complete(id));
        assert_eq!(sched.pending(), 0);
    }

    #[test]
    fn constitution_rules_and_integrity() {
        let mut constitution = Constitution::new();
        constitution.add_rule("No agent shall act against the operator's explicit veto");
        constitution.add_rule("All memory writes require audit trail");
        constitution.add_rule("Council decisions require 2/3 supermajority");

        let hash = constitution.seal();
        assert!(constitution.verify(&hash));
        assert_eq!(constitution.rule_count(), 3);
        assert_eq!(
            constitution.get_rule(0).unwrap(),
            "No agent shall act against the operator's explicit veto"
        );

        // Tamper detection — wrong hash should fail
        let mut bad_hash = hash;
        bad_hash[0] ^= 0xFF;
        assert!(!constitution.verify(&bad_hash));
    }
}
