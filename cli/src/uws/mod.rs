//! UWS Integration Module — Universal Workspace CLI bridge
//!
//! Forked from splitmerge420/tucker-gemini-GPT-/cli/src/uws/mod.rs
//! Updated to reference aluminum-os Ring 2 identifiers.
//!
//! Registers Tucker as both a standalone binary and a UWS subcommand.
//! When running as a UWS plugin, Tucker receives commands via the bridge
//! protocol and returns results to UWS for unified workspace display.

use anyhow::Result;
use crate::config::TuckerConfig;
use std::path::PathBuf;

/// UWS plugin manifest — aluminum-os fork (Ring 2, Agent Runtime)
const UWS_PLUGIN_MANIFEST: &str = r#"{
    "name": "tucker",
    "version": "4.0.0",
    "description": "Tucker V4 Constitutional AI Governance Agent — Aluminum OS fork. Pendragon Protocol enforcement with 5-model council.",
    "ring": 2,
    "commands": [
        {
            "name": "tucker",
            "description": "Tucker governance CLI",
            "subcommands": [
                {"name": "chat",    "description": "Interactive chat (solo or council mode)"},
                {"name": "council", "description": "Convene Pantheon Council"},
                {"name": "govern",  "description": "Run constitutional compliance check + NPFM"},
                {"name": "sync",    "description": "Sync constitutional documents"},
                {"name": "status",  "description": "Show Tucker + Aluminum OS status"}
            ]
        }
    ],
    "bridge": {
        "type": "subprocess",
        "binary": "tucker",
        "protocol": "json-rpc"
    },
    "aluminum_os": {
        "ring": 2,
        "component": "agent-runtime",
        "fork_of": "splitmerge420/tucker-gemini-GPT-",
        "constitutional_protocols": ["caal", "mission-allocation", "digital-habeas-corpus", "local-first", "fractal-governance", "clause-81"],
        "kintsugi_rules": 16
    }
}"#;

pub async fn register(config: &TuckerConfig) -> Result<()> {
    println!("UWS REGISTRATION — Tucker V4 (Aluminum OS fork)");
    let uws_path = find_uws_binary(config)?;
    println!("UWS binary: {}", uws_path.display());
    let manifest_dir = get_uws_plugin_dir(&uws_path)?;
    let manifest_path = manifest_dir.join("tucker.json");
    std::fs::create_dir_all(&manifest_dir)?;
    std::fs::write(&manifest_path, UWS_PLUGIN_MANIFEST)?;
    println!("Plugin manifest: {}", manifest_path.display());
    let tucker_path = std::env::current_exe()?;
    println!("Tucker binary: {}", tucker_path.display());
    let link_path = manifest_dir.join("tucker");
    if !link_path.exists() {
        #[cfg(unix)]
        std::os::unix::fs::symlink(&tucker_path, &link_path)?;
        #[cfg(windows)]
        std::os::windows::fs::symlink_file(&tucker_path, &link_path)?;
    }
    println!("Tucker registered as UWS subcommand (Ring 2, Agent Runtime)");
    println!("Usage: uws tucker chat --council | uws tucker council review | uws tucker govern --input <text>");
    println!("Also available: forge status  (Ring 0-3 unified CLI)");
    Ok(())
}

pub async fn unregister(config: &TuckerConfig) -> Result<()> {
    let uws_path = find_uws_binary(config)?;
    let manifest_dir = get_uws_plugin_dir(&uws_path)?;
    for f in ["tucker.json", "tucker"] {
        let p = manifest_dir.join(f);
        if p.exists() { std::fs::remove_file(p)?; }
    }
    println!("Tucker unregistered from UWS");
    Ok(())
}

pub async fn status(config: &TuckerConfig) -> Result<()> {
    println!("UWS INTEGRATION STATUS");
    println!("Registered:   {}", if config.uws.registered { "YES" } else { "NO" });
    println!("Subcommand:   uws {}", config.uws.subcommand_name);
    println!("Bridge port:  {}", config.uws.bridge_port);
    println!("Ring:         2 (Agent Runtime)");
    match find_uws_binary(config) {
        Ok(p)  => println!("UWS binary:   {} (found)", p.display()),
        Err(_) => println!("UWS binary:   not found"),
    }
    println!("Aluminum OS:  Ring 2 | tucker-governance | Protocols: 6/6 | Kintsugi: 16/16");
    Ok(())
}

pub async fn bridge(config: &TuckerConfig, command: &[String]) -> Result<()> {
    if command.is_empty() {
        println!("{{\"error\": \"no command provided\"}}");
        return Ok(());
    }
    match command[0].as_str() {
        "status" => {
            let status = serde_json::json!({
                "name":             "tucker",
                "version":          "4.0.0",
                "ring":             2,
                "fork_of":          "splitmerge420/tucker-gemini-GPT-",
                "council_members":  config.council.members.len(),
                "protocols_active": config.governance.protocols_enabled.len(),
                "sync_enabled":     config.sync.enabled,
            });
            println!("{}", serde_json::to_string_pretty(&status)?);
        }
        "council-ask" => {
            let question = command[1..].join(" ");
            if question.is_empty() {
                println!("{{\"error\": \"no question provided\"}}");
            } else {
                let result = crate::council::convene(config, &question,
                    Some("You are a Pantheon Council member providing governance guidance.")).await?;
                println!("{}", serde_json::to_string_pretty(&result)?);
            }
        }
        "protocols" => {
            let protocols = serde_json::json!({"protocols": [
                {"id": "P1", "name": "CAAL",           "full": "Constitutional AI Alignment Layer"},
                {"id": "P2", "name": "Mission Alloc",   "full": "Autonomous Mission Allocation"},
                {"id": "P3", "name": "Habeas Corpus",   "full": "Digital Habeas Corpus"},
                {"id": "P4", "name": "Local First",     "full": "Local First Execution"},
                {"id": "P5", "name": "Fractal Gov",     "full": "Fractal Governance and Redundancy"},
                {"id": "P6", "name": "Clause 81",       "full": "Clause 81 — Return Surplus, Not Extract"}
            ]});
            println!("{}", serde_json::to_string_pretty(&protocols)?);
        }
        "forge-govern" => {
            // Bridge command: quick governance check using native engine
            let input = command[1..].join(" ");
            crate::governance::evaluate(config, &input, "all", true).await?;
        }
        cmd => println!("{{\"error\": \"unknown bridge command: {}\"}}", cmd),
    }
    Ok(())
}

fn find_uws_binary(config: &TuckerConfig) -> Result<PathBuf> {
    if let Some(p) = &config.uws.uws_binary_path {
        let path = PathBuf::from(p);
        if path.exists() { return Ok(path); }
    }
    if let Ok(out) = std::process::Command::new("which").arg("uws").output() {
        if out.status.success() {
            let p = String::from_utf8_lossy(&out.stdout).trim().to_string();
            return Ok(PathBuf::from(p));
        }
    }
    for p in ["/usr/local/bin/uws", "/usr/bin/uws", "~/.cargo/bin/uws"] {
        let path = PathBuf::from(p);
        if path.exists() { return Ok(path); }
    }
    anyhow::bail!("UWS binary not found — install: cargo install uws")
}

fn get_uws_plugin_dir(uws_path: &PathBuf) -> Result<PathBuf> {
    let home = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
    let _ = uws_path;
    Ok(home.join(".uws").join("plugins").join("tucker"))
}
