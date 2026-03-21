//! Interactive chat — solo and council modes
//! Full async chat requires API keys configured in environment.

use anyhow::Result;
use crate::config::TuckerConfig;

pub async fn interactive_chat(config: &TuckerConfig, model: &str, topic: Option<&str>) -> Result<()> {
    println!("Tucker Chat — Solo mode ({model})");
    if let Some(t) = topic { println!("Topic: {t}"); }
    println!();
    println!("Configure API keys for live chat:");
    println!("  ANTHROPIC_API_KEY  → Claude (default)");
    println!("  OPENAI_API_KEY     → GPT-4o");
    println!("  GOOGLE_API_KEY     → Gemini 2.5");
    println!();
    println!("For constitutional governance chat, run: forge council");
    println!("(forge provides immediate constitutional scoring without API keys)");
    let _ = config;
    Ok(())
}

pub async fn interactive_council_chat(config: &TuckerConfig, topic: Option<&str>) -> Result<()> {
    println!("Tucker Chat — Council mode (5 models)");
    if let Some(t) = topic { println!("Topic: {t}"); }
    println!();
    let active = config.council.members.iter().filter(|m| m.enabled).count();
    println!("Active council members: {active}/5");
    println!();
    for m in config.council.members.iter().filter(|m| m.enabled) {
        let key = match m.provider.as_str() {
            "anthropic" => std::env::var("ANTHROPIC_API_KEY").map(|_| "✓").unwrap_or("✗ ANTHROPIC_API_KEY required"),
            "openai"    => std::env::var("OPENAI_API_KEY").map(|_| "✓").unwrap_or("✗ OPENAI_API_KEY required"),
            "google"    => std::env::var("GOOGLE_API_KEY").map(|_| "✓").unwrap_or("✗ GOOGLE_API_KEY required"),
            "deepseek"  => std::env::var("DEEPSEEK_API_KEY").map(|_| "✓").unwrap_or("✗ DEEPSEEK_API_KEY required"),
            "xai"       => std::env::var("XAI_API_KEY").map(|_| "✓").unwrap_or("✗ XAI_API_KEY required"),
            _           => "✗",
        };
        println!("  {} {}", key, m.name);
    }
    Ok(())
}
