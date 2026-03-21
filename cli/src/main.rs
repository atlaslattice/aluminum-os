//! Tucker V4 — Aluminum OS Fork
//! Constitutional AI Governance CLI
//!
//! Upstream: splitmerge420/tucker-gemini-GPT- / cli/
//! Fork additions:
//!   - aluminum_os integration for Ring 0 constitutional types
//!   - governance module uses aluminum_os::Constitution directly
//!   - ring 2 agent registration aligns with aluminum-os AgentRegistry
//!
//! Build: cargo build -p tucker --release
//! Requires `cargo update` on first build to download async deps.

use anyhow::Result;
use clap::{Parser, Subcommand};

pub mod chat;
pub mod config;
pub mod council;
pub mod governance;
pub mod sync;
pub mod uws;

#[derive(Parser)]
#[command(
    name = "tucker",
    version = "4.0.0",
    about = "Tucker V4 — Constitutional AI Governance CLI\n\
             Aluminum OS fork · Pendragon Protocol enforcement · 5-model council.",
    long_about = "Tucker V4 is a constitutional compliance enforcement agent operating as both \
    a standalone CLI and a UWS subcommand. It orchestrates a 5-model Pantheon Council \
    (GPT-4o, Gemini 2.5, Claude, DeepSeek, Grok) for governance decisions and maintains \
    sync with Aluminum OS constitutional documents. This fork integrates with the \
    Aluminum OS Ring 0 kernel for native constitutional veto enforcement."
)]
struct Cli {
    #[command(subcommand)]
    command: Commands,

    /// Config file path (default: ~/.tucker/config.toml)
    #[arg(short, long, env = "TUCKER_CONFIG")]
    config: Option<String>,

    /// Verbose output
    #[arg(short, long, default_value_t = false)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Start interactive chat (council-aware)
    Chat {
        #[arg(short = 'C', long, default_value_t = false)]
        council: bool,
        #[arg(short, long, default_value = "claude")]
        model: String,
        #[arg(short, long)]
        topic: Option<String>,
    },
    /// Convene the Pantheon Council for governance review
    Council {
        #[command(subcommand)]
        action: CouncilAction,
    },
    /// Run constitutional compliance check (6 Pendragon protocols + NPFM)
    Govern {
        #[arg(short, long)]
        input: String,
        #[arg(short, long, default_value = "all")]
        protocol: String,
        /// Output governance verdict as JSON
        #[arg(long, default_value_t = false)]
        json: bool,
    },
    /// Sync constitutional documents
    Sync {
        #[command(subcommand)]
        action: SyncAction,
    },
    /// UWS integration management
    Uws {
        #[command(subcommand)]
        action: UwsAction,
    },
    /// Show Tucker + Aluminum OS system status
    Status,
    /// Initialize Tucker configuration
    Init,
}

#[derive(Subcommand)]
enum CouncilAction {
    Review { #[arg(short, long)] target: String, #[arg(short, long, default_value = "general")] review_type: String },
    Ask    { question: String },
    Status,
    Config,
}

#[derive(Subcommand)]
enum SyncAction {
    Pull, Push, Status,
    Full,
    Schedule { #[arg(short, long, default_value = "daily")] interval: String },
}

#[derive(Subcommand)]
enum UwsAction {
    Register, Unregister, Status,
    Bridge { command: Vec<String> },
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    let filter = if cli.verbose { "tucker=debug" } else { "tucker=info" };
    tracing_subscriber::fmt().with_env_filter(filter).with_target(false).init();
    tracing::info!("Tucker V4 — Aluminum OS Fork — Pendragon Protocol enforcement");

    let cfg = config::load_config(cli.config.as_deref())?;

    match cli.command {
        Commands::Chat { council, model, topic } => {
            if council {
                tracing::info!("Council mode — all models deliberate");
                chat::interactive_council_chat(&cfg, topic.as_deref()).await?;
            } else {
                chat::interactive_chat(&cfg, &model, topic.as_deref()).await?;
            }
        }
        Commands::Council { action } => match action {
            CouncilAction::Review { target, review_type } =>
                council::review(&cfg, &target, &review_type).await?,
            CouncilAction::Ask { question } =>
                council::ask(&cfg, &question).await?,
            CouncilAction::Status => council::status(&cfg).await?,
            CouncilAction::Config => council::configure(&cfg).await?,
        },
        Commands::Govern { input, protocol, json } =>
            governance::evaluate(&cfg, &input, &protocol, json).await?,
        Commands::Sync { action } => match action {
            SyncAction::Pull               => sync::pull(&cfg).await?,
            SyncAction::Push               => sync::push(&cfg).await?,
            SyncAction::Status             => sync::status(&cfg).await?,
            SyncAction::Full               => sync::full_cycle(&cfg).await?,
            SyncAction::Schedule {interval}=> sync::schedule(&cfg, &interval).await?,
        },
        Commands::Uws { action } => match action {
            UwsAction::Register            => uws::register(&cfg).await?,
            UwsAction::Unregister          => uws::unregister(&cfg).await?,
            UwsAction::Status              => uws::status(&cfg).await?,
            UwsAction::Bridge { command }  => uws::bridge(&cfg, &command).await?,
        },
        Commands::Status => print_status(&cfg),
        Commands::Init   => config::init_config().await?,
    }
    Ok(())
}

fn print_status(config: &config::TuckerConfig) {
    println!("╔══════════════════════════════════════════════════╗");
    println!("║  TUCKER V4 — Aluminum OS Fork                    ║");
    println!("║  Constitutional Governance CLI · Ring 2          ║");
    println!("╠══════════════════════════════════════════════════╣");
    println!("║  Version:    4.0.0 (aluminum-os fork)            ║");
    println!("║  Council:    5 models configured                 ║");
    println!("║  Protocols:  6 Pendragon + Kintsugi-016          ║");
    println!("║  Sync:       {} ║",
        if config.sync.enabled { "Enabled                             " }
        else                   { "Disabled                            " });
    println!("║  UWS:        {} ║",
        if config.uws.registered { "Registered                          " }
        else                     { "Not registered                      " });
    println!("╠══════════════════════════════════════════════════╣");
    println!("║  Council Members:                                ║");
    for m in &config.council.members {
        let dot = if m.enabled { "●" } else { "○" };
        println!("║    {dot} {:<14} ({:<12}) w={:.1}          ║",
            m.name, m.provider, m.weight);
    }
    println!("╠══════════════════════════════════════════════════╣");
    println!("║  Pendragon Protocols:                            ║");
    let protos = ["CAAL", "Mission Alloc", "Habeas Corpus", "Local First", "Fractal Gov", "Clause 81"];
    for p in &protos {
        println!("║    ● {p:<45}║");
    }
    println!("╚══════════════════════════════════════════════════╝");
}
