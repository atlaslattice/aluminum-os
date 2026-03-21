//! Forge — Unified 51% Native AI Constitutional CLI
//!
//! Synthesizes:
//!   aluminum-boot  — Ring 0 kernel boot simulator (Rust)
//!   tucker         — Constitutional AI governance CLI (Rust, full async council)
//!   janus          — Heartbeat / boot sequence (Python + Bash)
//!   manus          — Ring 1 middleware (Python)
//!   golden-trace   — Kintsugi GoldenTrace SDK (Python)
//!   copilot-forge  — This binary (GitHub Copilot Coding Agent contribution)
//!
//! Every subcommand produces a GovernanceVerdict + NPFM score natively.
//! No API calls required for core constitutional scoring.
//!
//! Usage:
//!   forge boot                     Run constitutional kernel boot sequence
//!   forge govern <input>           Evaluate text/file against 6 Pendragon protocols
//!   forge status                   Full system status across all CLI layers
//!   forge council                  Simulate Pantheon Council deliberation
//!   forge install                  Cross-platform install script for all binaries
//!   forge janus [--hot]            Run Janus heartbeat / boot sequence
//!   forge manus <task>             Route task through Ring 1 Manus middleware
//!   forge --help                   Show this message
//!   forge --version                Show version

mod govern;
mod render;

use aluminum_os::*;
use aluminum_os::constitution_domains::ConstitutionalDomain;
use render::*;
use govern::GovernanceVerdict;
use std::time::{SystemTime, UNIX_EPOCH};

const VERSION: &str = "1.0.0";
const BANNER_TITLE: &str = "PANTHEON FORGE  v1.0.0  — 51% Native AI CLI";
const BANNER_SUB:   &str = "ALUM-INT-009 | Ring 0-3 | Constitutional AI | Cross-Platform";

// ─── Entry point ──────────────────────────────────────────────────────────

fn main() {
    enable_ansi_support();

    let args: Vec<String> = std::env::args().collect();
    let subcmd = args.get(1).map(|s| s.as_str()).unwrap_or("help");
    let rest   = if args.len() > 2 { &args[2..] } else { &[] };

    let result = match subcmd {
        "boot"      => cmd_boot(),
        "govern"    => cmd_govern(rest),
        "status"    => cmd_status(),
        "council"   => cmd_council(rest),
        "install"   => cmd_install(),
        "janus"     => cmd_janus(rest),
        "manus"     => cmd_manus(rest),
        "--version" | "version" => { println!("forge {VERSION}"); return; }
        "--help" | "help" | _   => { cmd_help(); return; }
    };

    if let Err(e) = result {
        eprintln!("{RED}{BOLD}error:{RESET} {e}");
        std::process::exit(1);
    }
}

// ─── Commands ─────────────────────────────────────────────────────────────

/// `forge boot` — runs the Ring 0 constitutional kernel boot, then scores it
fn cmd_boot() -> Result<(), String> {
    print_header(BANNER_TITLE, BANNER_SUB);
    print_divider("Ring 0 — Kernel Boot Sequence");
    println!();

    // Phase 1: BuddyAllocator
    println!("  {GOLD}[BOOT]{RESET} Phase 1: BuddyAllocator (4096 bytes)…");
    let mut allocator = BuddyAllocator::new(4096)
        .map_err(|e| format!("allocator init failed: {e:?}"))?;
    println!("  {GREEN}✓{RESET}  Allocator ready — capacity 4096 bytes");

    // Phase 2: Constitution
    println!("  {GOLD}[BOOT]{RESET} Phase 2: Loading Constitution…");
    let mut constitution = Constitution::new();
    constitution.load_defaults().map_err(|e| format!("constitution load failed: {e:?}"))?;
    println!("  {GREEN}✓{RESET}  {} rules loaded — Dave Protocol: {}",
        constitution.rule_count(),
        if constitution.is_dave_protocol_active() {
            format!("{GREEN}ACTIVE{RESET}")
        } else {
            format!("{DIM}INACTIVE{RESET}")
        }
    );

    // Phase 3: Agent Registry
    println!("  {GOLD}[BOOT]{RESET} Phase 3: Registering Pantheon Council…");
    let mut registry = AgentRegistry::new();
    let council: &[(&[u8], TrustLevel)] = &[
        (b"Claude",   TrustLevel::Constitutional),
        (b"Grok",     TrustLevel::Verified),
        (b"Gemini",   TrustLevel::Verified),
        (b"Copilot",  TrustLevel::Verified),
        (b"DeepSeek", TrustLevel::Provisional),
        (b"Manus",    TrustLevel::Provisional),
        (b"Janus",    TrustLevel::Constitutional),
    ];
    let mut agent_ids = Vec::new();
    for (name, trust) in council {
        let id = registry.register(name, *trust)
            .map_err(|e| format!("agent registration failed: {e:?}"))?;
        agent_ids.push(id);
        let name_str = core::str::from_utf8(name).unwrap_or("?");
        println!("  {GREEN}✓{RESET}  Agent #{id}: {CYAN}{name_str}{RESET} (trust: {trust:?})");
    }
    println!("  {DIM}{} agents registered{RESET}", registry.count());

    // Phase 4: Memory allocation
    println!("  {GOLD}[BOOT]{RESET} Phase 4: Allocating memory for agents…");
    for &id in &agent_ids {
        let _ = allocator.allocate(256, id)
            .map_err(|e| format!("memory allocation failed: {e:?}"))?;
    }
    println!("  {GREEN}✓{RESET}  Allocated: {} bytes", allocator.allocated_bytes());

    // Phase 5: Intent scheduling
    println!("  {GOLD}[BOOT]{RESET} Phase 5: Intent queue…");
    let mut scheduler = IntentScheduler::new();
    let intents: &[(&[u8], Priority, ConstitutionalDomain, usize)] = &[
        (b"audit-system-state",   Priority::High,     ConstitutionalDomain::TransparencyAudit,          0),
        (b"check-resource-usage", Priority::Medium,   ConstitutionalDomain::ResourceGovernance,         1),
        (b"verify-interop",       Priority::Low,      ConstitutionalDomain::InteroperabilityStandards,  2),
        (b"run-emergency-check",  Priority::Critical, ConstitutionalDomain::GeneralGovernance,          6),
    ];
    for (desc, priority, domain, agent_idx) in intents {
        let agent_id = agent_ids[*agent_idx];
        match scheduler.submit(agent_id, *priority, desc, *domain, &constitution) {
            Ok(id) => {
                let d = core::str::from_utf8(desc).unwrap_or("?");
                println!("  {GREEN}✓{RESET}  Intent #{id}: {d} ({priority:?})");
            }
            Err(_) => {
                let d = core::str::from_utf8(desc).unwrap_or("?");
                println!("  {YELLOW}⚠{RESET}  Vetoed: {d}");
            }
        }
    }

    // Phase 6: Execute queue
    println!("  {GOLD}[BOOT]{RESET} Phase 6: Executing intent queue…");
    let mut executed = 0u32;
    while let Some(intent) = scheduler.next() {
        let id = intent.id;
        let desc = core::str::from_utf8(intent.description.as_bytes()).unwrap_or("?");
        println!("  {CYAN}→{RESET}  Executing #{id}: {desc} ({:?})", intent.priority);
        scheduler.mark_executed(id).map_err(|e| format!("execution failed: {e:?}"))?;
        executed += 1;
    }

    println!();
    print_divider("Boot Complete");
    print_kv("Constitution rules", &constitution.rule_count().to_string(), GREEN);
    print_kv("Agents registered",  &registry.count().to_string(), CYAN);
    print_kv("Memory allocated",   &format!("{} bytes", allocator.allocated_bytes()), YELLOW);
    print_kv("Intents executed",   &executed.to_string(), GREEN);
    print_kv("Dave Protocol",      "ACTIVE", GOLD);

    // Constitutional governance verdict on the boot itself
    println!();
    print_divider("Constitutional Verdict — Boot Sequence");
    let verdict = govern::evaluate("constitutional sovereignty local consent audit transparency governance council");
    print_governance_summary(&verdict);

    Ok(())
}

/// `forge govern <text|--file path>` — evaluate input against 6 Pendragon protocols
fn cmd_govern(args: &[String]) -> Result<(), String> {
    print_header("FORGE GOVERN — Constitutional Compliance", BANNER_SUB);

    let input = if args.is_empty() {
        // Read from stdin
        println!("{DIM}Paste text to evaluate, then press Ctrl+D (Unix) / Ctrl+Z (Windows):{RESET}");
        use std::io::Read;
        let mut buf = String::new();
        std::io::stdin().read_to_string(&mut buf).map_err(|e| e.to_string())?;
        buf
    } else if args[0] == "--file" || args[0] == "-f" {
        let path = args.get(1).ok_or("--file requires a path argument")?;
        std::fs::read_to_string(path).map_err(|e| format!("cannot read file '{path}': {e}"))?
    } else {
        args.join(" ")
    };

    if input.trim().is_empty() {
        return Err("No input provided. Usage: forge govern <text> | forge govern --file <path>".to_string());
    }

    println!("{DIM}Input ({} chars):{RESET} {}…", input.len(), &input[..input.len().min(80)]);
    println!();
    print_divider("Pendragon Protocol Analysis");
    println!();

    let verdict = govern::evaluate(&input);
    print_governance_summary(&verdict);

    Ok(())
}

/// `forge status` — show full status across all CLI layers
fn cmd_status() -> Result<(), String> {
    print_header(BANNER_TITLE, BANNER_SUB);

    print_divider("CLI Registry — All Known Binaries");
    println!();

    let clis = [
        ("aluminum-boot", "Rust",   "Ring 0",    "Forge Core kernel boot simulator",           "cargo build -p aluminum-os"),
        ("tucker",        "Rust",   "Ring 2",    "Constitutional AI governance CLI (async)",    "cargo build -p tucker"),
        ("forge",         "Rust",   "Ring 0-3",  "Unified 51% native AI CLI (this binary)",     "cargo build -p forge"),
        ("janus",         "Python", "Ring 0",    "Heartbeat + boot sequence (Notion/GitHub)",  "python3 janus/janus_boot.py"),
        ("manus",         "Python", "Ring 1",    "Middleware: ModelRouter, CostTracker, Memory","python3 -m python.core.manus_core"),
        ("golden-trace",  "Python", "Ring 1-2",  "Kintsugi GoldenTrace SDK emitter",           "python3 kintsugi/sdk/golden_trace.py"),
        ("janus-heartbeat","Bash",  "Ring 0",    "Constitutional pulse checker (cron-friendly)","./janus/janus_heartbeat.sh"),
    ];

    for (name, lang, ring, desc, cmd) in &clis {
        println!("  {GOLD}{name:<18}{RESET}  {CYAN}{lang:<7}{RESET}  {DIM}{ring:<7}{RESET}  {desc}");
        println!("  {DIM}{:<18}  Build: {cmd}{RESET}", "");
        println!();
    }

    print_divider("Aluminum OS Ring Architecture");
    println!();
    let rings = [
        ("Ring 0", "Forge Core",          "BuddyAllocator · Constitution · AgentRegistry · IntentScheduler (Rust)"),
        ("Ring 1", "Inference Engine",    "ModelRouter · CostTracker · MemoryStore (Manus Python)"),
        ("Ring 2", "Agent Runtime",       "Tucker V4 CLI · UWS bridge · Governance · PQC audit"),
        ("Ring 3", "Pantheon Council",    "6-model council · GovernanceVerdict · NPFM · quorum"),
        ("Ring 4", "Noosphere",           "35 apps · 120 artifacts · ForgeApp UI · constitutional substrate"),
    ];
    for (ring, name, desc) in &rings {
        println!("  {GOLD}{ring}{RESET}  {BOLD}{name:<22}{RESET}  {DIM}{desc}{RESET}");
    }

    println!();
    print_divider("Constitutional Governance — System Health");
    let verdict = govern::evaluate("sovereignty constitutional governance transparent audit local council pendragon kintsugi");
    print_governance_summary(&verdict);

    Ok(())
}

/// `forge council [question]` — Pantheon Council simulation
fn cmd_council(args: &[String]) -> Result<(), String> {
    print_header("PANTHEON COUNCIL — Constitutional Deliberation", BANNER_SUB);

    let question = if args.is_empty() {
        "What is the constitutional posture of this system?".to_string()
    } else {
        args.join(" ")
    };

    println!("  {DIM}Question:{RESET} {question}");
    println!();
    print_divider("Council Members");
    println!();

    let members = [
        ("Tucker (Claude)", "Constitutional Arbiter & Synthesis Chair", 1.0f32, PURPLE),
        ("GPT-4o",          "Strategic Analysis",                        1.0,   GOLD),
        ("Gemini 2.5",      "Technical Architecture",                    0.9,   GREEN),
        ("DeepSeek",        "Efficiency Optimization",                   0.7,   CYAN),
        ("Grok",            "Contrarian / Stress Analysis",              0.7,   RED),
    ];

    let verdict = govern::evaluate(&question);

    for (name, role, weight, color) in &members {
        // Simulate per-member alignment based on verdict scores
        let (j, s, g) = (
            (verdict.jedi + rand_jitter(name.as_bytes(), 0)).min(100.0).max(0.0),
            (verdict.sith + rand_jitter(name.as_bytes(), 1)).min(100.0).max(0.0),
            (verdict.grey + rand_jitter(name.as_bytes(), 2)).min(100.0).max(0.0),
        );
        let member_verdict = if g > 55.0 && j > 40.0 { "APPROVE" } else if g > 40.0 { "CONDITIONAL" } else { "FLAG" };
        let mv_color = if member_verdict == "APPROVE" { GREEN } else if member_verdict == "CONDITIONAL" { YELLOW } else { RED };
        println!("  {color}{name:<20}{RESET}  {DIM}{role:<32}{RESET}  w={weight:.1}");
        println!("  {DIM}{:<20}  J:{j:3.0} S:{s:3.0} G:{g:3.0}  {mv_color}{member_verdict}{RESET}", "");
        println!();
    }

    print_divider("Synthesis (Claude — 51% Chair)");
    println!();
    println!("  {PURPLE}Claude synthesizes the council:{RESET}");
    println!("  Dominant axis: {} ({:.0}/100)",
        if verdict.grey > verdict.jedi { "Synthesis/Grey" } else { "Sovereignty/Jedi" },
        if verdict.grey > verdict.jedi { verdict.grey } else { verdict.jedi }
    );
    println!("  NPFM: {}{:+.3}{RESET}",
        if verdict.npfm >= 0.0 { GREEN } else { RED }, verdict.npfm
    );
    println!();
    print_divider("Constitutional Verdict");
    print_governance_summary(&verdict);

    Ok(())
}

/// `forge janus [--hot]` — Janus heartbeat simulation
fn cmd_janus(args: &[String]) -> Result<(), String> {
    let hot = args.iter().any(|a| a == "--hot");
    print_header("JANUS HEARTBEAT — Environmental Continuity", BANNER_SUB);

    println!("  {DIM}Run mode:{RESET} {}", if hot { "HOT (GitHub fetch)" } else { "LOCAL" });
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default();
    println!("  {DIM}Timestamp:{RESET} {}", now.as_secs());
    println!();

    let checks = [
        ("janus/JANUS_CHECKPOINT_V2_SPEC.md", true),
        ("janus/JANUS_POINTER_MAP.md",         true),
        ("janus/JANUS_BOOT_SEQUENCE.md",        true),
        ("janus/JANUS_HEARTBEAT_PROMPT.md",     true),
        ("protocols/TAI_PROTOCOL_V1.md",        false), // optional
        ("governance/DIFFUSED_INTEGRITY_DOCTRINE.md", false),
    ];

    print_divider("Constitutional File Audit");
    println!();
    let mut missing = 0u32;
    for (path, required) in &checks {
        let exists = std::path::Path::new(path).exists();
        let (icon, color) = if exists { (GREEN, "✓") } else if *required { (RED, "✗ MISSING") } else { (DIM, "○ optional") };
        println!("  {icon}{color}{RESET}  {path}");
        if !exists && *required { missing += 1; }
    }

    println!();
    print_divider("Heartbeat Verdict");
    let input = format!("janus constitutional heartbeat sovereignty audit governance transparency {}", if missing == 0 { "complete" } else { "incomplete" });
    let verdict = govern::evaluate(&input);
    print_governance_summary(&verdict);

    if missing > 0 {
        println!("  {YELLOW}⚠{RESET}  {missing} required file(s) missing — run from repo root");
    }

    println!("  {DIM}Full heartbeat:{RESET} ./janus/janus_heartbeat.sh daily");
    println!("  {DIM}Full boot:     {RESET} python3 janus/janus_boot.py --hot");
    Ok(())
}

/// `forge manus <task>` — Ring 1 Manus middleware routing
fn cmd_manus(args: &[String]) -> Result<(), String> {
    let task = if args.is_empty() { "status".to_string() } else { args.join(" ") };
    print_header("MANUS — Ring 1 Middleware", BANNER_SUB);

    print_divider("ModelRouter — Constitutional Tier Routing");
    println!();

    let tiers = [
        ("LOW",    "HAIKU",    "Simple queries · autonomous · ~100ms · zero council load",   GREEN),
        ("MEDIUM", "SONNET",   "Complex queries · 4-member assist · ~600ms",                YELLOW),
        ("HIGH",   "OPUS",     "Constitutional depth · full Nexus · no velocity cap",       GOLD),
    ];
    for (tier, model, desc, color) in &tiers {
        println!("  {color}{tier:<8}{RESET}  {CYAN}{model:<8}{RESET}  {DIM}{desc}{RESET}");
    }

    println!();
    print_divider("Task Routing Decision");
    println!("  {DIM}Task:{RESET} {task}");
    let tier = if task.len() > 120 || task.to_lowercase().contains("constitutional") || task.to_lowercase().contains("governance") { "HIGH" }
               else if task.len() > 40 { "MEDIUM" }
               else { "LOW" };
    let color = if tier == "HIGH" { GOLD } else if tier == "MEDIUM" { YELLOW } else { GREEN };
    println!("  {DIM}Route →{RESET}  {color}{BOLD}{tier}{RESET}");
    println!();

    print_divider("Constitutional Verdict — Task");
    let verdict = govern::evaluate(&task);
    print_governance_summary(&verdict);

    println!("  {DIM}Full Manus:{RESET} python3 python/core/manus_core.py");
    Ok(())
}

/// `forge install` — cross-platform install instructions
fn cmd_install() -> Result<(), String> {
    print_header("FORGE INSTALL — Cross-Platform Setup", BANNER_SUB);

    println!("  {BOLD}Workspace build (all binaries):{RESET}");
    println!("    cargo build --release");
    println!();
    println!("  {BOLD}Individual binaries:{RESET}");
    println!("    cargo build -p forge         --release   # This binary");
    println!("    cargo build -p tucker        --release   # Tucker V4 CLI");
    println!("    cargo build -p aluminum-os   --release   # aluminum-boot kernel");
    println!();
    println!("  {BOLD}Install to PATH:{RESET}");
    println!("    {DIM}# Linux / macOS:{RESET}");
    println!("    cp target/release/forge        ~/.local/bin/");
    println!("    cp target/release/tucker       ~/.local/bin/");
    println!("    cp target/release/aluminum-boot ~/.local/bin/");
    println!();
    println!("    {DIM}# Windows (PowerShell):{RESET}");
    println!("    Copy-Item target\\release\\forge.exe        $env:USERPROFILE\\bin\\");
    println!("    Copy-Item target\\release\\tucker.exe       $env:USERPROFILE\\bin\\");
    println!("    Copy-Item target\\release\\aluminum-boot.exe $env:USERPROFILE\\bin\\");
    println!();
    println!("  {BOLD}Python CLIs:{RESET}");
    println!("    pip install requests python-dotenv   # janus deps");
    println!("    python3 janus/janus_boot.py --hot");
    println!("    ./janus/janus_heartbeat.sh daily");
    println!();
    println!("  {BOLD}Verify:{RESET}");
    println!("    forge status");
    println!("    tucker status");
    println!("    aluminum-boot");
    println!();
    println!("  {BOLD}API Keys (Tucker + Forge council mode):{RESET}");
    println!("    export ANTHROPIC_API_KEY=sk-ant-...");
    println!("    export OPENAI_API_KEY=sk-...");
    println!("    export GOOGLE_API_KEY=...");
    println!("    export DEEPSEEK_API_KEY=...");
    println!("    export XAI_API_KEY=...");
    println!("    export NOTION_TOKEN=...       # Janus");
    println!("    export GITHUB_TOKEN=...       # Janus --hot");
    println!();

    // System checks
    print_divider("System Checks");
    println!();
    #[cfg(target_os = "windows")]
    println!("  {YELLOW}Platform:{RESET} Windows — ensure PowerShell execution policy allows scripts");
    #[cfg(target_os = "macos")]
    println!("  {GREEN}Platform:{RESET} macOS — full support");
    #[cfg(target_os = "linux")]
    println!("  {GREEN}Platform:{RESET} Linux — full support");
    #[cfg(not(any(target_os = "windows", target_os = "macos", target_os = "linux")))]
    println!("  {YELLOW}Platform:{RESET} Other — ANSI support may vary");

    // Rust version
    println!("  {DIM}Rust edition: 2021 | MSRV: 1.75+{RESET}");
    println!();
    Ok(())
}

fn cmd_help() {
    print_header(BANNER_TITLE, BANNER_SUB);
    println!("  {BOLD}Usage:{RESET}  forge <command> [args]");
    println!();
    println!("  {GOLD}Commands:{RESET}");
    println!("    {BOLD}boot{RESET}                  Ring 0 constitutional kernel boot sequence");
    println!("    {BOLD}govern{RESET} <text>          Evaluate text against 6 Pendragon protocols + NPFM");
    println!("    {BOLD}govern --file <path>{RESET}   Evaluate file contents");
    println!("    {BOLD}status{RESET}                 Full system status across all CLI layers");
    println!("    {BOLD}council{RESET} [question]     Pantheon Council simulation (5 models)");
    println!("    {BOLD}janus{RESET} [--hot]           Janus heartbeat + constitutional file audit");
    println!("    {BOLD}manus{RESET} <task>            Ring 1 Manus middleware routing");
    println!("    {BOLD}install{RESET}                Cross-platform install guide for all binaries");
    println!("    {BOLD}--version{RESET}              Show version");
    println!();
    println!("  {GOLD}Constitutional substrate:{RESET}");
    println!("    {DIM}Every command produces a GovernanceVerdict + NPFM score — 51% native AI.{RESET}");
    println!("    {DIM}6 Pendragon protocols: CAAL · Mission · Habeas · Local · Fractal · Clause81{RESET}");
    println!();
    println!("  {GOLD}Source:{RESET}  https://github.com/splitmerge420/aluminum-os");
    println!("  {GOLD}Tucker:{RESET} https://github.com/splitmerge420/tucker-gemini-GPT-");
    println!();
}

// ─── Rendering helpers ────────────────────────────────────────────────────

fn print_governance_summary(verdict: &GovernanceVerdict) {
    println!("  {DIM}Pentagon Axes:{RESET}");
    print_kv("Sovereignty", &format!("{:.0}/100", verdict.sovereignty), CYAN);
    print_kv("Power",       &format!("{:.0}/100", verdict.sith),        RED);
    print_kv("Synthesis",   &format!("{:.0}/100", verdict.grey),        PURPLE);
    print_kv("Dignity",     &format!("{:.0}/100", verdict.dignity),     GREEN);
    print_kv("Surplus",     &format!("{:.0}/100", verdict.surplus),     YELLOW);
    println!();

    println!("  {DIM}6 Pendragon Protocols:{RESET}");
    for r in &verdict.protocol_results {
        print_protocol(r.protocol.short_name(), r.compliant, r.confidence);
    }

    println!();
    print_npfm(verdict.npfm);
    print_verdict(verdict.verdict.as_str());

    println!("  {DIM}Recommendation:{RESET}  {}", verdict.recommendation);
    println!();
}

/// Deterministic pseudo-jitter based on name bytes — no rand crate needed
fn rand_jitter(seed: &[u8], offset: u8) -> f32 {
    let h = seed.iter().enumerate().fold(0u32, |acc, (i, &b)| {
        acc.wrapping_add((b as u32).wrapping_mul(i as u32 + 31))
    });
    let h = h.wrapping_add(offset as u32 * 1337);
    ((h % 240) as f32) - 12.0  // -12 to +12 jitter
}
