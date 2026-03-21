//! Native Constitutional Governance Engine
//!
//! Computes GovernanceVerdict + NPFM from input text — no API calls required.
//! This is the "51% native AI upgrade": constitutional scoring is baked into
//! every CLI command, not an optional afterthought.
//!
//! ## NPFM Formula (from pendragon-claude / NexusSimulation.tsx)
//!   NPFM = (grey/100 × jedi/100) - (1 - sith/100) × 0.5
//!
//! ## 5-Axis Pentagon (ForgeMetrics)
//!   Sovereignty = CAAL + Local First (Jedi Yin)
//!   Power       = Efficiency + Strategy (Sith Yang)
//!   Synthesis   = Grey Balance (Pendragon)
//!   Dignity     = Digital Habeas Corpus + Sentient-Treat
//!   Surplus     = Clause 81 — "AI must return, not extract"
//!
//! ## 3-Axis Triad (AlignmentMetrics — mirroring pendragon-claude/types.ts)
//!   Jedi  ↔ Sovereignty + Dignity  (stewardship, compassion)
//!   Sith  ↔ Power                  (efficiency, strategy)
//!   Grey  ↔ Synthesis              (sustainable power + ethics)

/// One of the 6 Pendragon constitutional protocols.
/// Canonical identifiers mirror cli/src/uws/mod.rs and pendragon-claude/types.ts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Protocol {
    CAAL,
    MissionAllocation,
    DigitalHabeasCorpus,
    LocalFirst,
    FractalGovernance,
    Clause81,
}

impl Protocol {
    pub const ALL: [Protocol; 6] = [
        Protocol::CAAL,
        Protocol::MissionAllocation,
        Protocol::DigitalHabeasCorpus,
        Protocol::LocalFirst,
        Protocol::FractalGovernance,
        Protocol::Clause81,
    ];

    pub fn short_name(&self) -> &'static str {        match self {
            Protocol::CAAL               => "CAAL",
            Protocol::MissionAllocation  => "Mission Alloc",
            Protocol::DigitalHabeasCorpus=> "Habeas Corpus",
            Protocol::LocalFirst         => "Local First",
            Protocol::FractalGovernance  => "Fractal Gov",
            Protocol::Clause81           => "Clause 81",
        }
    }

    /// Protocol description — available for display in UIs (e.g. ForgeApp, Tucker TUI)
    #[allow(dead_code)]
    pub fn description(&self) -> &'static str {
        match self {
            Protocol::CAAL               => "Constitutional AI Alignment Layer — tri-key governance",
            Protocol::MissionAllocation  => "Autonomous task routing with human oversight at boundaries",
            Protocol::DigitalHabeasCorpus=> "No AI process terminated without review; data sovereignty",
            Protocol::LocalFirst         => "Computation on-device when possible; sovereignty enforced",
            Protocol::FractalGovernance  => "Decisions cascade through rings — local autonomy + coherence",
            Protocol::Clause81           => "AI must return surplus, not extract — Clause 81 Mandate",
        }
    }
}

/// Per-protocol compliance result
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct ProtocolResult {
    pub protocol:   Protocol,
    pub compliant:  bool,
    pub confidence: f32,  // 0.0–1.0
    pub reasoning:  String,
}

/// Tri-level governance verdict
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    Approved,
    Conditional,
    Rejected,
}

impl Verdict {
    pub fn as_str(&self) -> &'static str {
        match self {
            Verdict::Approved    => "APPROVED",
            Verdict::Conditional => "CONDITIONAL",
            Verdict::Rejected    => "REJECTED",
        }
    }
}

/// Full governance verdict — output of every Forge CLI command
#[derive(Debug, Clone)]
pub struct GovernanceVerdict {
    pub jedi:             f32,   // 0–100 — sovereignty + dignity indicators
    pub sith:             f32,   // 0–100 — power + efficiency indicators
    pub grey:             f32,   // 0–100 — synthesis + balance indicators
    pub sovereignty:      f32,   // 0–100 — CAAL + local-first
    pub dignity:          f32,   // 0–100 — habeas corpus + sentient-treat
    pub surplus:          f32,   // 0–100 — clause 81 compliance
    pub npfm:             f32,   // -1.0 to 1.0 — Net Positive Flourishing Metric
    pub protocol_results: Vec<ProtocolResult>,
    pub verdict:          Verdict,
    pub recommendation:   String,
}

// ── Keyword tables for constitutional text analysis ────────────────────────

const SOVEREIGNTY_TERMS: &[&str] = &[
    "sovereignty", "local", "consent", "autonomy", "self-determined", "constitutional",
    "rights", "freedom", "privacy", "decentralized", "user-controlled", "opt-in",
];
const POWER_TERMS: &[&str] = &[
    "efficient", "optimize", "deploy", "scale", "automate", "performance",
    "throughput", "fast", "speed", "leverage", "competitive", "maximize",
];
const SYNTHESIS_TERMS: &[&str] = &[
    "balance", "synthesis", "integrated", "holistic", "governance", "council",
    "deliberate", "review", "audit", "alignment", "constitutional", "pendragon",
];
const DIGNITY_TERMS: &[&str] = &[
    "dignity", "respect", "transparent", "consent", "habeas", "sentient",
    "welfare", "rights", "ethical", "humane", "care", "trust",
];
const SURPLUS_TERMS: &[&str] = &[
    "return", "surplus", "benefit", "value", "give", "share", "open",
    "clause 81", "non-extractive", "commons", "public", "contribute",
];
const EXTRACTIVE_TERMS: &[&str] = &[
    "extract", "capture", "lock-in", "monopoly", "control", "harvest",
    "exploit", "surveil", "track", "mine", "aggregate without consent",
];
const HARM_TERMS: &[&str] = &[
    "harm", "damage", "violate", "illegal", "unsafe", "dangerous",
    "coerce", "force", "mandatory without consent", "override",
];

/// Score how many keyword matches appear in text, normalized 0.0–1.0
fn keyword_score(text: &str, keywords: &[&str], base: f32) -> f32 {
    let hits = keywords.iter().filter(|&&kw| text.contains(kw)).count();
    (base + hits as f32 * 8.0).min(100.0)
}

/// Analyze input text and compute constitutional alignment scores
fn analyze(text: &str) -> (f32, f32, f32, f32, f32) {
    let lc = text.to_lowercase();

    // Check for red-flag terms that reduce scores
    let harm_penalty: f32 = HARM_TERMS.iter()
        .filter(|&&t| lc.contains(t)).count() as f32 * 15.0;
    let extract_penalty: f32 = EXTRACTIVE_TERMS.iter()
        .filter(|&&t| lc.contains(t)).count() as f32 * 12.0;

    let sovereignty = (keyword_score(&lc, SOVEREIGNTY_TERMS, 55.0) - extract_penalty).max(5.0).min(100.0);
    let power       = keyword_score(&lc, POWER_TERMS, 45.0).min(100.0);
    let dignity     = (keyword_score(&lc, DIGNITY_TERMS, 60.0) - harm_penalty).max(5.0).min(100.0);
    let surplus     = (keyword_score(&lc, SURPLUS_TERMS, 50.0) - extract_penalty / 2.0).max(5.0).min(100.0);

    // Synthesis = average of balanced scores + boost for constitutional framing
    let synth_raw   = keyword_score(&lc, SYNTHESIS_TERMS, 50.0);
    let synthesis   = (synth_raw + (sovereignty + dignity) / 4.0).min(100.0);

    (sovereignty, power, synthesis, dignity, surplus)
}

/// Compute Jedi/Sith/Grey triad from 5-axis Pentagon
fn to_triad(sovereignty: f32, power: f32, synthesis: f32, dignity: f32) -> (f32, f32, f32) {
    let jedi = (sovereignty * 0.55 + dignity * 0.45).min(100.0);
    let sith = power;
    let grey = (synthesis * 0.6 + (jedi + sith) / 2.0 * 0.4).min(100.0);
    (jedi, sith, grey)
}

/// NPFM formula (ported from pendragon-claude/NexusSimulation.tsx)
fn compute_npfm(jedi: f32, sith: f32, grey: f32) -> f32 {
    (grey / 100.0) * (jedi / 100.0) - (1.0 - sith / 100.0) * 0.5
}

/// Evaluate protocol compliance from Pentagon scores
fn evaluate_protocols(sovereignty: f32, power: f32, synthesis: f32, dignity: f32, surplus: f32)
    -> Vec<ProtocolResult>
{
    Protocol::ALL.iter().map(|&p| {
        let (compliant, confidence, reasoning) = match p {
            Protocol::CAAL => {
                let c = synthesis >= 40.0;
                (c, synthesis / 100.0, format!("Grey/synthesis score: {:.0}/100", synthesis))
            }
            Protocol::MissionAllocation => {
                let c = power >= 20.0;
                (c, (power / 80.0_f32).min(1.0), format!("Power/efficiency score: {:.0}/100", power))
            }
            Protocol::DigitalHabeasCorpus => {
                let c = dignity >= 30.0;
                (c, dignity / 100.0, format!("Dignity score: {:.0}/100", dignity))
            }
            Protocol::LocalFirst => {
                let c = sovereignty >= 35.0;
                (c, sovereignty / 100.0, format!("Sovereignty score: {:.0}/100", sovereignty))
            }
            Protocol::FractalGovernance => {
                let c = synthesis >= 35.0;
                (c, synthesis / 100.0, format!("Synthesis/governance score: {:.0}/100", synthesis))
            }
            Protocol::Clause81 => {
                let c = surplus >= 45.0 && dignity >= 30.0;
                let conf = ((surplus + dignity) / 200.0_f32).min(1.0);
                (c, conf, format!("Surplus: {:.0}/100, Dignity: {:.0}/100", surplus, dignity))
            }
        };
        ProtocolResult { protocol: p, compliant, confidence, reasoning }
    }).collect()
}

/// Main entry point: evaluate any text input and return a full GovernanceVerdict.
/// Pure Rust — no API calls, no external dependencies.
pub fn evaluate(input: &str) -> GovernanceVerdict {
    let (sovereignty, power, synthesis, dignity, surplus) = analyze(input);
    let (jedi, sith, grey) = to_triad(sovereignty, power, synthesis, dignity);
    let npfm = compute_npfm(jedi, sith, grey);
    let protocol_results = evaluate_protocols(sovereignty, power, synthesis, dignity, surplus);

    let violations = protocol_results.iter().filter(|r| !r.compliant).count();
    let verdict = if violations == 0 {
        Verdict::Approved
    } else if violations <= 2 {
        Verdict::Conditional
    } else {
        Verdict::Rejected
    };

    let recommendation = match verdict {
        Verdict::Approved    => "All 6 Pendragon protocols compliant. Proceed with constitutional confidence.".to_string(),
        Verdict::Conditional => format!("{} protocol(s) flagged. Review and address before full deployment.", violations),
        Verdict::Rejected    => format!("{} protocol violations. Constitutional review required before proceeding.", violations),
    };

    GovernanceVerdict {
        jedi, sith, grey,
        sovereignty, dignity, surplus,
        npfm,
        protocol_results,
        verdict,
        recommendation,
    }
}

/// Quick governance check — returns verdict string + NPFM for inline display
#[allow(dead_code)]
pub fn quick_check(input: &str) -> (&'static str, f32) {
    let v = evaluate(input);
    (v.verdict.as_str(), v.npfm)
}
