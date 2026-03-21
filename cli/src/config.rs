//! Tucker configuration — fork of tucker-gemini-GPT-/cli/src/config.rs
//! Adapted to use aluminum-os council member names.

use anyhow::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TuckerConfig {
    pub council:    CouncilConfig,
    pub sync:       SyncConfig,
    pub uws:        UwsConfig,
    pub governance: GovernanceConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouncilConfig {
    pub members: Vec<CouncilMember>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouncilMember {
    pub name:     String,
    pub provider: String,
    pub weight:   f32,
    pub enabled:  bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncConfig { pub enabled: bool }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UwsConfig {
    pub registered:       bool,
    pub subcommand_name:  String,
    pub bridge_port:      u16,
    pub uws_binary_path:  Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceConfig {
    pub protocols_enabled: Vec<String>,
}

impl Default for TuckerConfig {
    fn default() -> Self {
        Self {
            council: CouncilConfig {
                members: vec![
                    CouncilMember { name: "Tucker (Claude)".into(), provider: "anthropic".into(), weight: 1.0, enabled: true  },
                    CouncilMember { name: "GPT-4o".into(),           provider: "openai".into(),   weight: 1.0, enabled: true  },
                    CouncilMember { name: "Gemini 2.5".into(),       provider: "google".into(),   weight: 0.9, enabled: true  },
                    CouncilMember { name: "DeepSeek".into(),         provider: "deepseek".into(), weight: 0.7, enabled: true  },
                    CouncilMember { name: "Grok".into(),             provider: "xai".into(),      weight: 0.7, enabled: true  },
                ],
            },
            sync: SyncConfig { enabled: false },
            uws: UwsConfig {
                registered:      false,
                subcommand_name: "tucker".into(),
                bridge_port:     3737,
                uws_binary_path: None,
            },
            governance: GovernanceConfig {
                protocols_enabled: vec![
                    "caal".into(), "mission-allocation".into(), "digital-habeas-corpus".into(),
                    "local-first".into(), "fractal-governance".into(), "clause-81".into(),
                ],
            },
        }
    }
}

/// Load config from TOML file or return defaults.
/// Path resolution order: explicit arg → TUCKER_CONFIG env → ~/.tucker/config.toml → defaults
pub fn load_config(path: Option<&str>) -> Result<TuckerConfig> {
    let config_path = path
        .map(|p| p.to_string())
        .or_else(|| std::env::var("TUCKER_CONFIG").ok())
        .or_else(|| {
            dirs::home_dir().map(|h| h.join(".tucker").join("config.toml").to_string_lossy().into_owned())
        });

    if let Some(p) = config_path {
        if std::path::Path::new(&p).exists() {
            let raw = std::fs::read_to_string(&p)?;
            return Ok(toml::from_str(&raw)?);
        }
    }
    Ok(TuckerConfig::default())
}

pub async fn init_config() -> Result<()> {
    let config_dir = dirs::home_dir()
        .ok_or_else(|| anyhow::anyhow!("Cannot determine home directory"))?
        .join(".tucker");
    std::fs::create_dir_all(&config_dir)?;

    let config_path = config_dir.join("config.toml");
    if config_path.exists() {
        println!("Config already exists: {}", config_path.display());
        return Ok(());
    }

    let default = TuckerConfig::default();
    std::fs::write(&config_path, toml::to_string_pretty(&default)?)?;

    println!("Tucker configuration initialized: {}", config_path.display());
    println!();
    println!("Set API keys in environment variables:");
    println!("  export ANTHROPIC_API_KEY=sk-ant-...");
    println!("  export OPENAI_API_KEY=sk-...");
    println!("  export GOOGLE_API_KEY=...");
    println!("  export DEEPSEEK_API_KEY=...");
    println!("  export XAI_API_KEY=...");
    println!();
    println!("Or run: tucker chat --council   to activate full council mode");
    Ok(())
}
