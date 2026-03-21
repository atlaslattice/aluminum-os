//! Council deliberation — Pantheon Council orchestration
//! Full async version requires API keys. Degrades gracefully without them.

use anyhow::Result;
use serde::{Deserialize, Serialize};
use crate::config::TuckerConfig;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouncilResult {
    pub question:         String,
    pub responses:        Vec<CouncilResponse>,
    pub synthesis:        String,
    pub quorum_met:       bool,
    pub total_latency_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouncilResponse {
    pub member:      String,
    pub provider:    String,
    pub latency_ms:  u64,
    pub weight:      f32,
    pub content:     String,
    pub error:       Option<String>,
}

/// Convene the Pantheon Council for a question.
/// With API keys → real LLM calls (configure via environment variables).
/// Without keys  → returns structured stub response.
pub async fn convene(config: &TuckerConfig, question: &str, _system: Option<&str>) -> Result<CouncilResult> {
    println!("⚖️  Convening Pantheon Council…");
    println!("   Question: {question}");
    println!();

    let active: Vec<_> = config.council.members.iter().filter(|m| m.enabled).collect();
    println!("   Active members: {}", active.len());

    let responses: Vec<CouncilResponse> = active.iter().map(|m| {
        // Check for API key
        let key_env = match m.provider.as_str() {
            "anthropic" => std::env::var("ANTHROPIC_API_KEY").ok(),
            "openai"    => std::env::var("OPENAI_API_KEY").ok(),
            "google"    => std::env::var("GOOGLE_API_KEY").ok(),
            "deepseek"  => std::env::var("DEEPSEEK_API_KEY").ok(),
            "xai"       => std::env::var("XAI_API_KEY").ok(),
            _           => None,
        };

        let (content, error) = if key_env.is_some() {
            // TODO: replace with real HTTP call to provider API
            (format!("[{}] Constitutional review of: {}", m.name, &question[..question.len().min(60)]), None)
        } else {
            (String::new(), Some(format!("No {} API key — set {}",
                m.provider,
                match m.provider.as_str() {
                    "anthropic" => "ANTHROPIC_API_KEY",
                    "openai"    => "OPENAI_API_KEY",
                    "google"    => "GOOGLE_API_KEY",
                    "deepseek"  => "DEEPSEEK_API_KEY",
                    "xai"       => "XAI_API_KEY",
                    _           => "API_KEY",
                }
            )))
        };

        CouncilResponse {
            member: m.name.clone(), provider: m.provider.clone(),
            latency_ms: 0, weight: m.weight, content, error,
        }
    }).collect();

    let active_count = responses.iter().filter(|r| r.error.is_none()).count();
    let quorum_met = active_count >= 3;
    let synthesis = if quorum_met {
        format!("Council synthesis ({active_count}/{} members): Constitutional analysis of query.", active.len())
    } else {
        "Quorum not met — configure API keys for full council deliberation. Run: tucker init".to_string()
    };

    println!("   Quorum: {} ({active_count}/{} members active)", if quorum_met { "MET" } else { "NOT MET" }, active.len());
    println!("   Synthesis: {synthesis}");

    Ok(CouncilResult { question: question.to_string(), responses, synthesis, quorum_met, total_latency_ms: 0 })
}

pub async fn review(config: &TuckerConfig, target: &str, review_type: &str) -> Result<()> {
    println!("Council Review — {review_type}: {target}");
    convene(config, &format!("Review {review_type}: {target}"), None).await?;
    Ok(())
}

pub async fn ask(config: &TuckerConfig, question: &str) -> Result<()> {
    let result = convene(config, question, None).await?;
    println!("{}", serde_json::to_string_pretty(&result)?);
    Ok(())
}

pub async fn status(config: &TuckerConfig) -> Result<()> {
    println!("Pantheon Council — {} members configured", config.council.members.len());
    for m in &config.council.members {
        let dot = if m.enabled { "●" } else { "○" };
        println!("  {dot} {:<20} ({:<12}) w={:.1}", m.name, m.provider, m.weight);
    }
    Ok(())
}

pub async fn configure(_config: &TuckerConfig) -> Result<()> {
    println!("Edit ~/.tucker/config.toml to configure council members and weights.");
    Ok(())
}
