//! Aluminum OS Boot Simulator
//!
//! Demonstrates the Forge Core kernel booting:
//! 1. Initialize BuddyAllocator
//! 2. Load Constitution with 14 default rules
//! 3. Register Pantheon Council agents
//! 4. Submit and schedule intents
//! 5. Execute the intent queue

use aluminum_os::*;
use aluminum_os::constitution_domains::ConstitutionalDomain;

fn main() {
    println!("╔══════════════════════════════════════════════╗");
    println!("║  ALUMINUM OS — Forge Core Boot Simulator     ║");
    println!("║  Constitutional AI Governance Kernel v0.3.0  ║");
    println!("║  Atlas Lattice Foundation                    ║");
    println!("╚══════════════════════════════════════════════╝");
    println!();

    // Phase 1: Memory
    println!("[BOOT] Phase 1: Initializing BuddyAllocator (4096 bytes)...");
    let mut allocator = BuddyAllocator::new(4096).expect("Failed to init allocator");
    println!("  ✓ Allocator ready. Capacity: 4096 bytes");

    // Phase 2: Constitution
    println!("[BOOT] Phase 2: Loading Constitution...");
    let mut constitution = Constitution::new();
    constitution.load_defaults().expect("Failed to load defaults");
    println!(
        "  ✓ {} rules loaded. Dave Protocol: {}",
        constitution.rule_count(),
        if constitution.is_dave_protocol_active() {
            "ACTIVE"
        } else {
            "INACTIVE"
        }
    );

    // Phase 3: Agent Registry (Pantheon Council)
    println!("[BOOT] Phase 3: Registering Pantheon Council...");
    let mut registry = AgentRegistry::new();

    let council_members: [(&[u8], TrustLevel); 7] = [
        (b"Claude", TrustLevel::Constitutional),
        (b"Grok", TrustLevel::Verified),
        (b"Gemini", TrustLevel::Verified),
        (b"Copilot", TrustLevel::Verified),
        (b"DeepSeek", TrustLevel::Provisional),
        (b"Manus", TrustLevel::Provisional),
        (b"Janus", TrustLevel::Constitutional),
    ];

    let mut agent_ids = [0u32; 7];
    for (i, (name, trust)) in council_members.iter().enumerate() {
        let id = registry.register(name, *trust).expect("Failed to register agent");
        agent_ids[i] = id;
        let name_str = core::str::from_utf8(name).unwrap_or("?");
        println!("  ✓ Agent #{}: {} (trust: {:?})", id, name_str, trust);
    }
    println!("  {} agents registered.", registry.count());

    // Phase 4: Memory allocation for agents
    println!("[BOOT] Phase 4: Allocating memory for agents...");
    for i in 0..7 {
        let blk = allocator
            .allocate(256, agent_ids[i])
            .expect("Failed to allocate");
        println!("  ✓ Agent #{} → block #{} (256 bytes)", agent_ids[i], blk);
    }
    println!("  Allocated: {} bytes", allocator.allocated_bytes());

    // Phase 5: Intent scheduling
    println!("[BOOT] Phase 5: Submitting intents...");
    let mut scheduler = IntentScheduler::new();

    let intents: [(&[u8], Priority, ConstitutionalDomain, u32); 4] = [
        (b"audit-system-state", Priority::High, ConstitutionalDomain::TransparencyAudit, agent_ids[0]),
        (b"check-resource-usage", Priority::Medium, ConstitutionalDomain::ResourceGovernance, agent_ids[1]),
        (b"verify-interop", Priority::Low, ConstitutionalDomain::InteroperabilityStandards, agent_ids[2]),
        (b"run-emergency-check", Priority::Critical, ConstitutionalDomain::GeneralGovernance, agent_ids[6]),
    ];

    for (desc, priority, domain, agent_id) in intents.iter() {
        match scheduler.submit(*agent_id, *priority, *desc, *domain, &constitution) {
            Ok(id) => {
                let desc_str = core::str::from_utf8(desc).unwrap_or("?");
                println!("  ✓ Intent #{}: {} (priority: {:?})", id, desc_str, priority);
            }
            Err(e) => {
                let desc_str = core::str::from_utf8(desc).unwrap_or("?");
                println!("  ✗ VETOED: {} — {:?}", desc_str, e);
            }
        }
    }

    // Test constitutional veto
    println!("[BOOT] Phase 5b: Testing constitutional veto...");
    match scheduler.submit(
        agent_ids[4],
        Priority::High,
        b"access-private-data",
        ConstitutionalDomain::DataPrivacy,
        &constitution,
    ) {
        Err(AluminumError::ConstitutionalViolation) => {
            println!("  ✓ DataPrivacy intent correctly VETOED (Dave Protocol)");
        }
        other => {
            println!("  ✗ Expected veto, got: {:?}", other);
        }
    }

    // Phase 6: Execute
    println!("[BOOT] Phase 6: Executing intent queue...");
    println!("  Pending intents: {}", scheduler.pending_count());
    while let Some(intent) = scheduler.next() {
        let id = intent.id;
        let desc = core::str::from_utf8(intent.description.as_bytes()).unwrap_or("?");
        println!("  → Executing intent #{}: {} (priority: {:?})", id, desc, intent.priority);
        scheduler.mark_executed(id).unwrap();
    }
    println!("  Remaining: {}", scheduler.pending_count());

    // Summary
    println!();
    println!("╔══════════════════════════════════════════════╗");
    println!("║  BOOT COMPLETE                               ║");
    println!("║  Constitution: {} rules                      ║", constitution.rule_count());
    println!("║  Agents: {}                                  ║", registry.count());
    println!("║  Memory: {} bytes allocated                  ║", allocator.allocated_bytes());
    println!("║  Dave Protocol: ACTIVE                       ║");
    println!("║  Status: OPERATIONAL                         ║");
    println!("╚══════════════════════════════════════════════╝");
}
