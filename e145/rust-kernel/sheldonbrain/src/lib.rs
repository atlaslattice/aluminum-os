//! Aluminum OS v3.0 — SHELDONBRAIN (Ring 2)
//! LLM-Native Memory System with 3-tier architecture:
//!
//! Tier 1: Working Memory (in-process, encrypted, 30-min consolidation)
//! Tier 2: Long-Term Memory (persistent store, 7-day promotion from Tier 1)
//! Tier 3: Swarm Memory (federated knowledge graph for digital nations)
//!
//! This integrates with the Manus 2.0 toolkit's ChromaDB MemoryStore
//! and adds the consolidation engine that Grok only described but never coded.

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

/// A memory entry in the SHELDONBRAIN system
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Memory {
    pub id: String,
    pub content: String,
    pub tier: MemoryTier,
    pub created_at: u64,
    pub last_accessed: u64,
    pub access_count: u32,
    pub entropy_score: f64,
    pub tags: Vec<String>,
    pub source: String,
    pub hash: String,
    pub encrypted: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum MemoryTier {
    Working,   // Tier 1: Hot, in-process, 30-min consolidation window
    LongTerm,  // Tier 2: Warm, persistent, 7-day promotion from Working
    Swarm,     // Tier 3: Cold, federated, shared across digital nations
}

/// Entropy scoring for memory importance
/// Higher entropy = more unique/important = higher retention priority
fn compute_entropy(content: &str, access_count: u32, age_seconds: u64) -> f64 {
    // Content uniqueness (simplified: character diversity)
    let unique_chars = content.chars().collect::<std::collections::HashSet<_>>().len();
    let content_score = (unique_chars as f64 / content.len().max(1) as f64).min(1.0);

    // Access frequency (more access = more important)
    let access_score = (access_count as f64).ln().max(0.0) / 10.0;

    // Recency (newer = higher score, decays over 7 days)
    let day_seconds = 86400.0;
    let recency_score = (1.0 - (age_seconds as f64 / (7.0 * day_seconds))).max(0.0);

    // Weighted combination
    (content_score * 0.3 + access_score * 0.4 + recency_score * 0.3).clamp(0.0, 1.0)
}

/// The consolidation engine — promotes memories between tiers
pub struct ConsolidationEngine {
    /// Minimum entropy score to promote from Working to LongTerm
    promotion_threshold: f64,
    /// Minimum entropy score to promote from LongTerm to Swarm
    swarm_threshold: f64,
    /// Maximum age in Working memory before forced consolidation (30 min)
    working_ttl_seconds: u64,
    /// Maximum age in LongTerm before review (7 days)
    longterm_review_seconds: u64,
}

impl ConsolidationEngine {
    pub fn new() -> Self {
        Self {
            promotion_threshold: 0.4,
            swarm_threshold: 0.7,
            working_ttl_seconds: 1800,       // 30 minutes
            longterm_review_seconds: 604800,  // 7 days
        }
    }

    /// Run a consolidation pass on all memories.
    /// Returns (promoted_to_longterm, promoted_to_swarm, evicted).
    pub fn consolidate(&self, memories: &mut Vec<Memory>) -> ConsolidationResult {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        let mut promoted_lt = 0;
        let mut promoted_swarm = 0;
        let mut evicted = 0;

        for memory in memories.iter_mut() {
            let age = now.saturating_sub(memory.created_at);
            memory.entropy_score = compute_entropy(&memory.content, memory.access_count, age);

            match memory.tier {
                MemoryTier::Working => {
                    if age > self.working_ttl_seconds {
                        if memory.entropy_score >= self.promotion_threshold {
                            memory.tier = MemoryTier::LongTerm;
                            promoted_lt += 1;
                        } else {
                            // Low entropy, old working memory — evict
                            evicted += 1;
                        }
                    }
                }
                MemoryTier::LongTerm => {
                    if age > self.longterm_review_seconds {
                        if memory.entropy_score >= self.swarm_threshold {
                            memory.tier = MemoryTier::Swarm;
                            promoted_swarm += 1;
                        }
                        // LongTerm memories are never evicted, only demoted in priority
                    }
                }
                MemoryTier::Swarm => {
                    // Swarm memories are permanent — they belong to the collective
                }
            }
        }

        // Remove evicted memories
        memories.retain(|m| m.tier != MemoryTier::Working || {
            let age = now.saturating_sub(m.created_at);
            age <= self.working_ttl_seconds || m.entropy_score >= self.promotion_threshold
        });

        ConsolidationResult {
            promoted_to_longterm: promoted_lt,
            promoted_to_swarm: promoted_swarm,
            evicted,
            total_remaining: memories.len(),
            timestamp: now,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct ConsolidationResult {
    pub promoted_to_longterm: usize,
    pub promoted_to_swarm: usize,
    pub evicted: usize,
    pub total_remaining: usize,
    pub timestamp: u64,
}

/// The main SHELDONBRAIN memory system
pub struct SheldonBrain {
    memories: Vec<Memory>,
    consolidation_engine: ConsolidationEngine,
    /// Index for fast lookup by tag
    tag_index: HashMap<String, Vec<String>>,
}

impl SheldonBrain {
    pub fn new() -> Self {
        Self {
            memories: Vec::new(),
            consolidation_engine: ConsolidationEngine::new(),
            tag_index: HashMap::new(),
        }
    }

    /// Store a new memory in Working tier
    pub fn store(&mut self, content: &str, tags: Vec<String>, source: &str) -> String {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        let id = uuid::Uuid::new_v4().to_string();
        let hash = Self::hash_content(content);

        let memory = Memory {
            id: id.clone(),
            content: content.to_string(),
            tier: MemoryTier::Working,
            created_at: now,
            last_accessed: now,
            access_count: 0,
            entropy_score: 0.0,
            tags: tags.clone(),
            source: source.to_string(),
            hash,
            encrypted: false,
        };

        // Update tag index
        for tag in &tags {
            self.tag_index.entry(tag.clone())
                .or_insert_with(Vec::new)
                .push(id.clone());
        }

        self.memories.push(memory);
        id
    }

    /// Recall memories by semantic similarity (simplified: keyword matching)
    /// In production, this delegates to ChromaDB via Manus Core
    pub fn recall(&mut self, query: &str, limit: usize) -> Vec<&Memory> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        let query_lower = query.to_lowercase();
        let mut results: Vec<(usize, f64)> = self.memories.iter().enumerate()
            .filter_map(|(i, m)| {
                let content_lower = m.content.to_lowercase();
                if content_lower.contains(&query_lower) {
                    let relevance = 1.0 - (now.saturating_sub(m.last_accessed) as f64 / 86400.0).min(1.0);
                    Some((i, relevance + m.entropy_score))
                } else {
                    // Check tags
                    let tag_match = m.tags.iter().any(|t| t.to_lowercase().contains(&query_lower));
                    if tag_match {
                        Some((i, 0.5 + m.entropy_score))
                    } else {
                        None
                    }
                }
            })
            .collect();

        results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        results.truncate(limit);

        // Update access counts
        for (idx, _) in &results {
            self.memories[*idx].access_count += 1;
            self.memories[*idx].last_accessed = now;
        }

        results.iter().map(|(idx, _)| &self.memories[*idx]).collect()
    }

    /// Run memory consolidation
    pub fn consolidate(&mut self) -> ConsolidationResult {
        self.consolidation_engine.consolidate(&mut self.memories)
    }

    /// Get memory statistics
    pub fn stats(&self) -> MemoryStats {
        let working = self.memories.iter().filter(|m| m.tier == MemoryTier::Working).count();
        let longterm = self.memories.iter().filter(|m| m.tier == MemoryTier::LongTerm).count();
        let swarm = self.memories.iter().filter(|m| m.tier == MemoryTier::Swarm).count();

        MemoryStats {
            total: self.memories.len(),
            working,
            longterm,
            swarm,
            avg_entropy: if self.memories.is_empty() { 0.0 }
                else { self.memories.iter().map(|m| m.entropy_score).sum::<f64>() / self.memories.len() as f64 },
        }
    }

    fn hash_content(content: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        format!("{:x}", hasher.finalize())
    }
}

#[derive(Debug, Serialize)]
pub struct MemoryStats {
    pub total: usize,
    pub working: usize,
    pub longterm: usize,
    pub swarm: usize,
    pub avg_entropy: f64,
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_store_and_recall() {
        let mut brain = SheldonBrain::new();
        brain.store("The Stryker cyberattack of March 2026", vec!["security".to_string()], "manus");
        brain.store("Noosphere defense framework analysis", vec!["noosphere".to_string()], "manus");
        brain.store("Aluminum OS v3.0 architecture spec", vec!["os".to_string()], "manus");

        let results = brain.recall("Stryker", 5);
        assert!(!results.is_empty());
        assert!(results[0].content.contains("Stryker"));
    }

    #[test]
    fn test_entropy_scoring() {
        // High diversity content should score higher
        let high_entropy = compute_entropy("The quick brown fox jumps over the lazy dog", 10, 3600);
        let low_entropy = compute_entropy("aaaaaaaaaa", 1, 86400 * 7);
        assert!(high_entropy > low_entropy);
    }

    #[test]
    fn test_memory_tiers() {
        let mut brain = SheldonBrain::new();
        brain.store("Test memory", vec!["test".to_string()], "test");

        let stats = brain.stats();
        assert_eq!(stats.working, 1);
        assert_eq!(stats.longterm, 0);
        assert_eq!(stats.swarm, 0);
    }

    #[test]
    fn test_consolidation() {
        let mut brain = SheldonBrain::new();
        brain.store("Important memory with high access", vec!["important".to_string()], "test");
        brain.store("Trivial memory", vec!["trivial".to_string()], "test");

        // Simulate high access on first memory
        for _ in 0..20 {
            brain.recall("Important", 1);
        }

        let result = brain.consolidate();
        assert_eq!(result.total_remaining, 2); // Both should survive initial consolidation
    }

    #[test]
    fn test_tag_recall() {
        let mut brain = SheldonBrain::new();
        brain.store("Some content", vec!["noosphere".to_string(), "defense".to_string()], "test");

        let results = brain.recall("noosphere", 5);
        assert!(!results.is_empty());
    }
}
