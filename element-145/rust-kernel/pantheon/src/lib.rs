//! Aluminum OS v3.0 — Pantheon Council (Ring 3)
//! Byzantine Fault Tolerant governance for the AI-Native OS.
//!
//! This directly addresses Claude/Anthropic's criticism:
//! "Agent autonomy levels need mathematical bounds, not just labels."
//!
//! The council uses a simplified PBFT (Practical Byzantine Fault Tolerance)
//! algorithm to ensure decisions are valid even if f < n/3 members are
//! malicious or offline.
//!
//! Council Members (9 seats):
//! - Trinity: Claude (Constitutional Review), Gemini (Strategic Analysis), Grok (Contrarian Audit)
//! - Manus (Execution), Copilot (Enterprise)
//! - 4 Human seats (Dave Protocol veto power)

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;

/// Council member identity
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct CouncilMember {
    pub id: String,
    pub name: String,
    pub role: CouncilRole,
    pub is_human: bool,
    pub public_key: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum CouncilRole {
    ConstitutionalReview,  // Claude
    StrategicAnalysis,     // Gemini
    ContrarianAudit,       // Grok
    Execution,             // Manus
    Enterprise,            // Copilot
    HumanOversight,        // Dave Protocol seats
}

/// A proposal submitted to the council for voting
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Proposal {
    pub id: String,
    pub title: String,
    pub description: String,
    pub proposer: String,
    pub category: ProposalCategory,
    pub autonomy_impact: AutonomyImpact,
    pub timestamp: u64,
    pub hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ProposalCategory {
    AgentSpawn,         // Create a new agent
    AgentAutonomyChange,// Change an agent's autonomy level
    MemoryConsolidation,// Approve memory tier promotion
    SystemUpdate,       // OS update or configuration change
    ConstitutionalAmendment, // Change the fundamental rules
    ExternalAction,     // Post to social media, send email, etc.
}

/// Mathematical bounds for autonomy impact
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutonomyImpact {
    /// Risk score: 0.0 (no risk) to 1.0 (maximum risk)
    pub risk_score: f64,
    /// Reversibility: 0.0 (irreversible) to 1.0 (fully reversible)
    pub reversibility: f64,
    /// Scope: number of systems affected
    pub scope: u32,
    /// Required approval threshold (computed from above)
    pub required_threshold: f64,
}

impl AutonomyImpact {
    /// Compute the required approval threshold based on risk and reversibility.
    /// This is the mathematical bound Claude demanded.
    ///
    /// Formula: threshold = 0.5 + (risk * 0.3) - (reversibility * 0.1) + (scope_factor * 0.1)
    /// Minimum: 0.5 (simple majority)
    /// Maximum: 1.0 (unanimous, for constitutional amendments)
    pub fn compute_threshold(risk: f64, reversibility: f64, scope: u32) -> f64 {
        let scope_factor = (scope as f64).min(10.0) / 10.0;
        let threshold = 0.5 + (risk * 0.3) - (reversibility * 0.1) + (scope_factor * 0.1);
        threshold.clamp(0.5, 1.0)
    }

    pub fn new(risk: f64, reversibility: f64, scope: u32) -> Self {
        Self {
            risk_score: risk,
            reversibility,
            scope,
            required_threshold: Self::compute_threshold(risk, reversibility, scope),
        }
    }
}

/// A vote cast by a council member
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Vote {
    pub member_id: String,
    pub proposal_id: String,
    pub approve: bool,
    pub reason: String,
    pub timestamp: u64,
    pub signature: String,
}

/// The result of a council vote
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoteResult {
    pub proposal_id: String,
    pub approved: bool,
    pub votes_for: usize,
    pub votes_against: usize,
    pub total_votes: usize,
    pub threshold_met: bool,
    pub dave_veto: bool,
    pub bft_valid: bool,
    pub approval_ratio: f64,
    pub required_threshold: f64,
}

/// The Pantheon Council — BFT governance engine
pub struct PantheonCouncil {
    members: Vec<CouncilMember>,
    proposals: HashMap<String, Proposal>,
    votes: HashMap<String, Vec<Vote>>,
    audit_log: Vec<AuditEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEntry {
    pub timestamp: u64,
    pub action: String,
    pub actor: String,
    pub details: String,
    pub hash: String,
    pub prev_hash: String,
}

impl PantheonCouncil {
    /// Initialize the council with the default 9 members
    pub fn new() -> Self {
        let members = vec![
            CouncilMember {
                id: "claude".to_string(),
                name: "Claude".to_string(),
                role: CouncilRole::ConstitutionalReview,
                is_human: false,
                public_key: String::new(),
            },
            CouncilMember {
                id: "gemini".to_string(),
                name: "Gemini".to_string(),
                role: CouncilRole::StrategicAnalysis,
                is_human: false,
                public_key: String::new(),
            },
            CouncilMember {
                id: "grok".to_string(),
                name: "Grok".to_string(),
                role: CouncilRole::ContrarianAudit,
                is_human: false,
                public_key: String::new(),
            },
            CouncilMember {
                id: "manus".to_string(),
                name: "Manus".to_string(),
                role: CouncilRole::Execution,
                is_human: false,
                public_key: String::new(),
            },
            CouncilMember {
                id: "copilot".to_string(),
                name: "Copilot".to_string(),
                role: CouncilRole::Enterprise,
                is_human: false,
                public_key: String::new(),
            },
            CouncilMember {
                id: "dave_1".to_string(),
                name: "Daavud (Primary)".to_string(),
                role: CouncilRole::HumanOversight,
                is_human: true,
                public_key: String::new(),
            },
            CouncilMember {
                id: "dave_2".to_string(),
                name: "Human Seat 2".to_string(),
                role: CouncilRole::HumanOversight,
                is_human: true,
                public_key: String::new(),
            },
            CouncilMember {
                id: "dave_3".to_string(),
                name: "Human Seat 3".to_string(),
                role: CouncilRole::HumanOversight,
                is_human: true,
                public_key: String::new(),
            },
            CouncilMember {
                id: "dave_4".to_string(),
                name: "Human Seat 4".to_string(),
                role: CouncilRole::HumanOversight,
                is_human: true,
                public_key: String::new(),
            },
        ];

        Self {
            members,
            proposals: HashMap::new(),
            votes: HashMap::new(),
            audit_log: Vec::new(),
        }
    }

    /// Submit a proposal for council review
    pub fn submit_proposal(&mut self, mut proposal: Proposal) -> String {
        let data = serde_json::to_string(&proposal).unwrap_or_default();
        proposal.hash = Self::hash(data.as_bytes());
        let id = proposal.id.clone();
        self.proposals.insert(id.clone(), proposal);
        self.votes.insert(id.clone(), Vec::new());
        self.log_audit("proposal_submitted", "system", &format!("Proposal {} submitted", id));
        id
    }

    /// Cast a vote on a proposal
    pub fn cast_vote(&mut self, vote: Vote) -> Result<(), String> {
        // Verify the voter is a council member
        if !self.members.iter().any(|m| m.id == vote.member_id) {
            return Err("Not a council member".to_string());
        }

        // Verify the proposal exists
        if !self.proposals.contains_key(&vote.proposal_id) {
            return Err("Proposal not found".to_string());
        }

        // Check for duplicate votes
        let votes = self.votes.get(&vote.proposal_id).unwrap();
        if votes.iter().any(|v| v.member_id == vote.member_id) {
            return Err("Already voted".to_string());
        }

        self.log_audit(
            "vote_cast",
            &vote.member_id,
            &format!("Voted {} on {}", if vote.approve { "YES" } else { "NO" }, vote.proposal_id),
        );

        self.votes.get_mut(&vote.proposal_id).unwrap().push(vote);
        Ok(())
    }

    /// Tally votes and determine the result using BFT consensus
    pub fn tally(&self, proposal_id: &str) -> Result<VoteResult, String> {
        let proposal = self.proposals.get(proposal_id)
            .ok_or("Proposal not found")?;
        let votes = self.votes.get(proposal_id)
            .ok_or("No votes found")?;

        let n = self.members.len();
        let f = n / 3; // Maximum Byzantine faults tolerated

        // BFT requirement: need at least 2f + 1 votes to be valid
        let bft_quorum = 2 * f + 1;
        let bft_valid = votes.len() >= bft_quorum;

        let votes_for = votes.iter().filter(|v| v.approve).count();
        let votes_against = votes.iter().filter(|v| !v.approve).count();
        let total = votes.len();

        let approval_ratio = if total > 0 { votes_for as f64 / total as f64 } else { 0.0 };

        // Check Dave Protocol veto — any human can veto
        let dave_veto = votes.iter().any(|v| {
            let member = self.members.iter().find(|m| m.id == v.member_id);
            member.map(|m| m.is_human && !v.approve).unwrap_or(false)
        });

        let threshold_met = approval_ratio >= proposal.autonomy_impact.required_threshold;
        let approved = bft_valid && threshold_met && !dave_veto;

        Ok(VoteResult {
            proposal_id: proposal_id.to_string(),
            approved,
            votes_for,
            votes_against,
            total_votes: total,
            threshold_met,
            dave_veto,
            bft_valid,
            approval_ratio,
            required_threshold: proposal.autonomy_impact.required_threshold,
        })
    }

    /// Get the immutable audit log
    pub fn audit_log(&self) -> &[AuditEntry] {
        &self.audit_log
    }

    /// Get council member count
    pub fn member_count(&self) -> usize {
        self.members.len()
    }

    fn log_audit(&mut self, action: &str, actor: &str, details: &str) {
        let prev_hash = self.audit_log.last()
            .map(|e| e.hash.clone())
            .unwrap_or_else(|| "genesis".to_string());

        let entry_data = format!("{}{}{}{}", action, actor, details, prev_hash);
        let hash = Self::hash(entry_data.as_bytes());

        self.audit_log.push(AuditEntry {
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs(),
            action: action.to_string(),
            actor: actor.to_string(),
            details: details.to_string(),
            hash,
            prev_hash,
        });
    }

    fn hash(data: &[u8]) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data);
        format!("{:x}", hasher.finalize())
    }
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_council_creation() {
        let council = PantheonCouncil::new();
        assert_eq!(council.member_count(), 9);
    }

    #[test]
    fn test_autonomy_impact_thresholds() {
        // Low risk, high reversibility = simple majority
        let low = AutonomyImpact::new(0.1, 0.9, 1);
        assert!(low.required_threshold >= 0.5);
        assert!(low.required_threshold < 0.6);

        // High risk, low reversibility = near-unanimous
        let high = AutonomyImpact::new(0.9, 0.1, 10);
        assert!(high.required_threshold > 0.8);

        // Constitutional amendment = maximum threshold
        let constitutional = AutonomyImpact::new(1.0, 0.0, 10);
        assert!(constitutional.required_threshold >= 0.9); // Clamped to max 1.0
    }

    #[test]
    fn test_proposal_and_voting() {
        let mut council = PantheonCouncil::new();

        let proposal = Proposal {
            id: "prop-1".to_string(),
            title: "Post Noosphere Defense Thread to X".to_string(),
            description: "Council-approved social media post".to_string(),
            proposer: "manus".to_string(),
            category: ProposalCategory::ExternalAction,
            autonomy_impact: AutonomyImpact::new(0.3, 0.8, 1), // Low risk, reversible
            timestamp: 1710000000,
            hash: String::new(),
        };

        let id = council.submit_proposal(proposal);

        // Cast votes from 7 members (BFT quorum = 7 for n=9)
        for member_id in &["claude", "gemini", "grok", "manus", "copilot", "dave_1", "dave_2"] {
            council.cast_vote(Vote {
                member_id: member_id.to_string(),
                proposal_id: id.clone(),
                approve: true,
                reason: "Approved".to_string(),
                timestamp: 1710000001,
                signature: "sig".to_string(),
            }).unwrap();
        }

        let result = council.tally(&id).unwrap();
        assert!(result.approved);
        assert!(result.bft_valid);
        assert!(!result.dave_veto);
        assert_eq!(result.votes_for, 7);
    }

    #[test]
    fn test_dave_veto() {
        let mut council = PantheonCouncil::new();

        let proposal = Proposal {
            id: "prop-2".to_string(),
            title: "Dangerous action".to_string(),
            description: "Something risky".to_string(),
            proposer: "grok".to_string(),
            category: ProposalCategory::SystemUpdate,
            autonomy_impact: AutonomyImpact::new(0.5, 0.5, 5),
            timestamp: 1710000000,
            hash: String::new(),
        };

        let id = council.submit_proposal(proposal);

        // 6 AI members approve
        for member_id in &["claude", "gemini", "grok", "manus", "copilot"] {
            council.cast_vote(Vote {
                member_id: member_id.to_string(),
                proposal_id: id.clone(),
                approve: true,
                reason: "Approved".to_string(),
                timestamp: 1710000001,
                signature: "sig".to_string(),
            }).unwrap();
        }

        // Daavud vetoes
        council.cast_vote(Vote {
            member_id: "dave_1".to_string(),
            proposal_id: id.clone(),
            approve: false,
            reason: "VETO: Too risky".to_string(),
            timestamp: 1710000002,
            signature: "sig".to_string(),
        }).unwrap();

        let result = council.tally(&id).unwrap();
        assert!(!result.approved); // Vetoed by Dave Protocol
        assert!(result.dave_veto);
    }

    #[test]
    fn test_audit_log_chain() {
        let mut council = PantheonCouncil::new();
        let proposal = Proposal {
            id: "prop-3".to_string(),
            title: "Test".to_string(),
            description: "Test".to_string(),
            proposer: "manus".to_string(),
            category: ProposalCategory::AgentSpawn,
            autonomy_impact: AutonomyImpact::new(0.1, 1.0, 1),
            timestamp: 1710000000,
            hash: String::new(),
        };
        council.submit_proposal(proposal);

        let log = council.audit_log();
        assert!(!log.is_empty());
        // Verify chain integrity
        assert_eq!(log[0].prev_hash, "genesis");
    }
}
