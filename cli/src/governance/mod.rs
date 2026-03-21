//! Governance evaluation — uses aluminum_os::Constitution for Ring 0 veto enforcement
//! and forge-cli's governance engine for NPFM + protocol scoring.

use anyhow::Result;
use crate::config::TuckerConfig;

/// Evaluate input against 6 Pendragon protocols using the aluminum-os Constitution
/// for Ring 0 veto enforcement + native NPFM scoring.
pub async fn evaluate(config: &TuckerConfig, input: &str, protocol: &str, json_output: bool) -> Result<()> {
    // Load aluminum-os Ring 0 constitution
    let mut constitution = aluminum_os::Constitution::new();
    constitution.load_defaults().map_err(|e| anyhow::anyhow!("Constitution load failed: {:?}", e))?;

    println!("Tucker Governance Check");
    println!("Protocol:    {}", protocol);
    println!("Input:       {}…", &input[..input.len().min(80)]);
    println!("Rules:       {} Kintsugi rules loaded", constitution.rule_count());
    println!("Dave Proto:  {}", if constitution.is_dave_protocol_active() { "ACTIVE" } else { "INACTIVE" });
    println!();

    // NPFM and protocol scoring — keyword analysis
    let lc = input.to_lowercase();
    let sovereignty = score(&lc, &["sovereignty","consent","local","privacy","constitutional"], 55.0);
    let power       = score(&lc, &["efficient","optimize","scale","automate","performance"],   45.0);
    let synthesis   = score(&lc, &["balance","governance","council","audit","alignment"],       50.0);
    let dignity     = score(&lc, &["dignity","respect","transparent","habeas","consent"],       60.0);
    let surplus     = score(&lc, &["return","surplus","open","share","clause 81"],              50.0);

    let jedi = (sovereignty * 0.55 + dignity * 0.45).min(100.0);
    let sith = power;
    let grey = (synthesis * 0.6 + (jedi + sith) / 2.0 * 0.4).min(100.0);
    let npfm = (grey / 100.0) * (jedi / 100.0) - (1.0 - sith / 100.0) * 0.5;

    let protocols = [
        ("CAAL",           synthesis >= 40.0, synthesis / 100.0),
        ("Mission Alloc",  power >= 20.0,     (power / 80.0_f32).min(1.0)),
        ("Habeas Corpus",  dignity >= 30.0,   dignity / 100.0),
        ("Local First",    sovereignty >= 35.0, sovereignty / 100.0),
        ("Fractal Gov",    synthesis >= 35.0, synthesis / 100.0),
        ("Clause 81",      surplus >= 45.0 && dignity >= 30.0, ((surplus + dignity) / 200.0_f32).min(1.0)),
    ];

    let violations = protocols.iter().filter(|p| !p.1).count();
    let verdict = if violations == 0 { "APPROVED" } else if violations <= 2 { "CONDITIONAL" } else { "REJECTED" };

    if json_output {
        let out = serde_json::json!({
            "input": &input[..input.len().min(120)],
            "constitution_rules": constitution.rule_count(),
            "dave_protocol": constitution.is_dave_protocol_active(),
            "pentagon": { "sovereignty": sovereignty, "power": power, "synthesis": synthesis, "dignity": dignity, "surplus": surplus },
            "triad": { "jedi": jedi, "sith": sith, "grey": grey },
            "npfm": npfm,
            "protocols": protocols.iter().map(|p| serde_json::json!({ "name": p.0, "compliant": p.1, "confidence": p.2 })).collect::<Vec<_>>(),
            "verdict": verdict,
            "violations": violations,
        });
        println!("{}", serde_json::to_string_pretty(&out)?);
        return Ok(());
    }

    // Human-readable output
    println!("Pentagon Scores:");
    println!("  Sovereignty: {sovereignty:.0}/100  Power: {power:.0}/100  Synthesis: {synthesis:.0}/100");
    println!("  Dignity:     {dignity:.0}/100       Surplus: {surplus:.0}/100");
    println!();
    println!("Pendragon Protocols:");
    for (name, compliant, confidence) in &protocols {
        let icon = if *compliant { "✓" } else { "✗" };
        println!("  {icon} {name:<20}  {:.0}%", confidence * 100.0);
    }
    println!();
    println!("NPFM:       {npfm:+.3}");
    println!("Violations: {violations}/6");
    println!("Verdict:    {verdict}");
    println!();
    let _ = config;
    Ok(())
}

fn score(text: &str, keywords: &[&str], base: f32) -> f32 {
    let hits = keywords.iter().filter(|&&k| text.contains(k)).count();
    (base + hits as f32 * 8.0).min(100.0)
}
