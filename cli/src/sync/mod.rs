//! Sync — constitutional document sync (GitHub + Notion)

use anyhow::Result;
use crate::config::TuckerConfig;

pub async fn pull(config: &TuckerConfig) -> Result<()> {
    println!("Sync Pull — pulling latest constitutional documents…");
    println!("  Configure GITHUB_TOKEN for live sync");
    let _ = config;
    Ok(())
}

pub async fn push(config: &TuckerConfig) -> Result<()> {
    println!("Sync Push — pushing local changes…");
    let _ = config;
    Ok(())
}

pub async fn status(config: &TuckerConfig) -> Result<()> {
    println!("Sync Status:");
    println!("  Enabled: {}", config.sync.enabled);
    println!("  Set GITHUB_TOKEN and NOTION_TOKEN for live sync");
    Ok(())
}

pub async fn full_cycle(config: &TuckerConfig) -> Result<()> {
    pull(config).await?;
    push(config).await?;
    Ok(())
}

pub async fn schedule(config: &TuckerConfig, interval: &str) -> Result<()> {
    println!("Sync Schedule: {interval}");
    println!("  To run automatically: crontab -e");
    println!("  Or: ./janus/janus_heartbeat.sh {interval}");
    let _ = config;
    Ok(())
}
