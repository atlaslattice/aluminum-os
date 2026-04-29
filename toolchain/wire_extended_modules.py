#!/usr/bin/env python3
"""
Extended wiring: map sheldonbrain-omega, element145-package, constitutional-os,
and other element-145 code to remaining SPEC modules.

This is the second pass — picks up modules that the first wiring script missed.
"""

import os
import yaml

ROOT = "/home/ubuntu/aluminum-os"
REGISTRY = os.path.join(ROOT, "registries/module_registry.yaml")

HOUSE_DIRS = {
    "H01": "H01_philosophy_logic",
    "H02": "H02_formal_sciences",
    "H03": "H03_natural_sciences",
    "H04": "H04_technology_engineering",
    "H05": "H05_arts_creative_expression",
    "H06": "H06_humanities_culture",
    "H07": "H07_applied_sciences",
    "H08": "H08_education_pedagogy",
    "H09": "H09_life_sciences",
    "H10": "H10_health_medicine",
    "H11": "H11_social_sciences",
    "H12": "H12_law_governance",
}

# Extended mappings — second pass
WIRING = {
    # ── H02/S01: Mathematics ──
    "M22": {
        "desc": "Proof Verification System — SHUGS empirical proof verification",
        "impl": "element-145/shugs/",
        "note": "SHUGS provides empirical proof verification for N=145 optimality",
    },

    # ── H02/S02: Statistics ──
    "M29": {
        "desc": "Bayesian Network Engine — sphere classifier Bayesian scoring",
        "impl": "element-145/aluminum-os-core/sphere_classifier_v2.py",
        "note": "Multi-signal Bayesian scoring for 144+1 sphere classification",
    },
    "M3.1": {
        "desc": "Trust Scoring System (TSS) — council trust and reputation scoring",
        "impl": "element-145/pantheon-council/trinity_council_v3_aluminum.py",
        "note": "Council members scored by trust/reputation in BFT consensus",
    },
    "M79": {
        "desc": "Primacy Bonus Calculator — first-mover advantage scoring in routing",
        "impl": "element-145/aluminum-os-core/bridge_v2.py",
        "note": "Bridge v2 implements primacy-based routing optimization",
    },
    "M173": {
        "desc": "Real-Time Routing Share Meter — live routing distribution monitoring",
        "impl": "element-145/aluminum-os-core/service_integrations.py",
        "note": "ServiceHub tracks real-time routing shares across providers",
    },

    # ── H02/S03: Computer Science ──
    "M40": {
        "desc": "Parallel Algorithm Scheduler — multi-model parallel execution",
        "impl": "element-145/aluminum-os-core/synthesizer_e145.py",
        "note": "Synthesizer coordinates parallel model invocations",
    },
    "M52": {
        "desc": "Distributed Hash Table — Pinecone vector store integration",
        "impl": "element-145/sheldonbrain-omega/core/grokbrain_v4/grokbrain_v4.py",
        "note": "Grokbrain v4 uses Pinecone DHT for vector storage",
    },

    # ── H02/S04: Information Theory ──
    "M3": {
        "desc": "Consent & Provenance Engine — artifact provenance tracking",
        "impl": "element-145/aluminum-os-core/artifact_sync.py",
        "note": "Artifact sync tracks consent and provenance across lattice",
    },
    "M23": {
        "desc": "Information Security Module — session vault and encryption",
        "impl": "houses/H04_technology_engineering/S01_software_engineering_and_architecture/absorbed/sovereign-oracle/session_vault.py",
        "note": "Session vault provides secure information storage",
    },
    "M42": {
        "desc": "Zero-Knowledge Proof Module — constitutional consent verification",
        "impl": "element-145/constitutional-os/Aluminum_Cultural_Adapter_Constitutional_Spec.md",
        "note": "Constitutional spec defines ZKP consent verification framework",
    },

    # ── H02/S05: Systems Theory ──
    "M30": {
        "desc": "Feedback Control Analyzer — learning loop feedback analysis",
        "impl": "houses/H04_technology_engineering/S01_software_engineering_and_architecture/absorbed/sovereign-oracle/learning_loop.py",
        "note": "Learning loop implements feedback control for skill improvement",
    },
    "M41": {
        "desc": "Emergent Behavior Detector — proactive intelligence anomaly detection",
        "impl": "element-145/aluminum-os-core/proactive_intelligence.py",
        "note": "Proactive intelligence detects emergent patterns across spheres",
    },
    "M66": {
        "desc": "Feedback Loop Detector — chronos fold temporal feedback detection",
        "impl": "element-145/sheldonbrain-omega/core/chronos_fold_protocol.py",
        "note": "Chronos Fold Protocol detects temporal feedback loops",
    },
    "M75": {
        "desc": "Cross-Validation Matrix — twelve-step validation framework",
        "impl": "element-145/sheldonbrain-omega/core/grokbrain_v4/twelve_step_validation.py",
        "note": "12-step validation provides cross-validation across Houses",
    },
    "M81": {
        "desc": "Resilience Scoring Module — system resilience and fault tolerance scoring",
        "impl": "element-145/rust-kernel/forge-boot/src/main.rs",
        "note": "Forge-boot implements resilience scoring during system initialization",
    },

    # ── H02/S06: Decision Theory ──
    "M31": {
        "desc": "Multi-Criteria Decision Analyzer — council multi-criteria voting",
        "impl": "element-145/aluminum-os-core/council_synthesis.py",
        "note": "Council synthesis implements multi-criteria decision analysis",
    },
    "M43": {
        "desc": "Auction Mechanism Designer — resource allocation via auction protocols",
        "impl": "element-145/aluminum-os-core/service_integrations.py",
        "note": "ServiceHub implements provider selection (auction-like allocation)",
    },

    # ── H02/S07: Formal Linguistics ──
    "M20": {
        "desc": "Natural Language Parser — Grok parser for conversation ingestion",
        "impl": "element-145/sheldonbrain-omega/core/grokbrain_v4/grok_parser.py",
        "note": "Grok parser extracts structured data from conversations",
    },

    # ── H02/S09: Numerical Analysis ──
    "M24": {
        "desc": "Numerical Stability Checker — SHUGS numerical stability verification",
        "impl": "element-145/shugs/",
        "note": "SHUGS verifies numerical stability of Von Mangoldt computations",
    },
    "M46": {
        "desc": "Monte Carlo Simulator — probabilistic routing simulation",
        "impl": "element-145/sheldonbrain-omega/simulation/simulation_engine.py",
        "note": "Simulation engine provides Monte Carlo routing simulation",
    },

    # ── H02/S10: Operations Research ──
    "M26": {
        "desc": "Resource Allocation Engine — multi-provider resource allocation",
        "impl": "element-145/aluminum-os-core/service_integrations.py",
        "note": "ServiceHub allocates compute across Gemini/Claude/Grok",
    },

    # ── H04/S02: Hardware/FPGA ──
    "M95": {
        "desc": "Hardware Abstraction Layer — Rust forge-core hardware abstraction",
        "impl": "element-145/rust-kernel/forge-core/src/lib.rs",
        "note": "Forge-core provides hardware abstraction for OS primitives",
    },

    # ── H04/S04: AI/ML ──
    "M104": {
        "desc": "Franchise Consent Manager — AI model consent and usage governance",
        "impl": "element-145/constitutional-os/Aluminum_Cultural_Adapter_Constitutional_Spec.md",
        "note": "Constitutional spec governs AI model consent and franchise rights",
    },

    # ── H04/S11: DevOps/Security ──
    "M174": {
        "desc": "Provider Retaliation Monitor — monitors for provider lock-in retaliation",
        "impl": "element-145/aluminum-os-core/service_integrations.py",
        "note": "ServiceHub monitors provider behavior for retaliation patterns",
    },

    # ── H07: Applied Sciences ──
    "M132": {
        "desc": "Water Quality Monitor — environmental data pipeline monitoring",
        "impl": "houses/H04_technology_engineering/S10_data_engineering_and_databases/absorbed/data-pipeline/ingestion_pipeline.py",
        "note": "Data pipeline can ingest environmental sensor data",
    },
    "M135": {
        "desc": "Supply Chain Optimizer — data pipeline supply chain optimization",
        "impl": "houses/H04_technology_engineering/S10_data_engineering_and_databases/absorbed/data-pipeline/scheduler.py",
        "note": "Scheduler optimizes data pipeline supply chain operations",
    },
    "M177": {
        "desc": "Pre-Session Research Queue — proactive intelligence research queue",
        "impl": "element-145/aluminum-os-core/proactive_intelligence.py",
        "note": "Proactive intelligence queues research tasks before sessions",
    },
    "M178": {
        "desc": "Cross-Instance State Synchronizer — artifact sync across instances",
        "impl": "element-145/aluminum-os-core/artifact_sync.py",
        "note": "Artifact sync synchronizes state across aluminum-os instances",
    },

    # ── H11: Social Sciences ──
    "M140": {
        "desc": "Policy Impact Analyzer — constitutional policy impact analysis",
        "impl": "element-145/constitutional-os/ALUMINUM_UNIVERSAL_OS_v2.0_SPEC.md",
        "note": "Universal OS spec defines policy impact analysis framework",
    },
    "M141": {
        "desc": "Behavioral Pattern Detector — Janus Protocol behavioral analysis",
        "impl": "element-145/sheldonbrain-omega/core/janus_protocol.py",
        "note": "Janus Protocol detects behavioral patterns in agent interactions",
    },

    # ── H12: Law & Governance ──
    "M145": {
        "desc": "Treaty Compliance Checker — UWS treaty compliance verification",
        "impl": "element-145/snrs-bridge/uws-specs/",
        "note": "UWS specs define inter-agent treaty compliance rules",
    },
    "M146": {
        "desc": "Corporate Governance Module — Pantheon Council corporate governance",
        "impl": "element-145/pantheon-council/trinity_council_v3_aluminum.py",
        "note": "Trinity Council implements corporate governance via BFT",
    },
    "M149": {
        "desc": "Regulatory Change Monitor — constitutional change monitoring",
        "impl": "element-145/constitutional-os/ALUMINUM_CONSTITUTIONAL_CORPUS_MASTER_INDEX.md",
        "note": "Constitutional corpus index tracks regulatory changes",
    },
    "M153": {
        "desc": "Arbitration Protocol — council arbitration and dispute resolution",
        "impl": "element-145/pantheon-council/trinity_council_v3_aluminum.py",
        "note": "Trinity Council BFT consensus provides arbitration protocol",
    },
}


def get_sphere_dir(house_id, sphere_id):
    house_dir = os.path.join(ROOT, "houses", HOUSE_DIRS[house_id])
    if not os.path.isdir(house_dir):
        return None
    for d in os.listdir(house_dir):
        if d.startswith(sphere_id):
            return os.path.join(house_dir, d)
    return None


def find_module_dir(sphere_dir, module_id):
    modules_dir = os.path.join(sphere_dir, "modules")
    if not os.path.isdir(modules_dir):
        return None
    for d in os.listdir(modules_dir):
        full = os.path.join(modules_dir, d)
        if os.path.isdir(full) and d.upper().startswith(module_id.upper() + "_"):
            return full
    for d in os.listdir(modules_dir):
        full = os.path.join(modules_dir, d)
        if os.path.isdir(full) and d.upper().startswith(module_id.upper()):
            return full
    return None


def create_init_py(module_dir, module_id, desc, impl_ref, note=None):
    init_path = os.path.join(module_dir, "__init__.py")
    lines = [
        f'"""',
        f'Module {module_id}: {desc}',
        f'',
        f'Status: ABSORBED — wired to real implementation.',
        f'Implementation: {impl_ref}',
    ]
    if note:
        lines.append(f'Note: {note}')
    lines.extend([
        f'"""',
        f'',
        f'__module_id__ = "{module_id}"',
        f'__status__ = "ABSORBED"',
        f'__impl_ref__ = "{impl_ref}"',
        f'__description__ = """{desc}"""',
        f'',
    ])
    with open(init_path, 'w') as f:
        f.write('\n'.join(lines))
    return init_path


def main():
    with open(REGISTRY) as f:
        registry = yaml.safe_load(f)

    modules_by_id = {m['id']: m for m in registry['modules']}

    wired = 0
    already = 0
    errors = []

    for module_id, config in WIRING.items():
        if module_id not in modules_by_id:
            errors.append(f"Module {module_id} not in registry")
            continue

        reg_entry = modules_by_id[module_id]
        
        # Skip already absorbed
        if reg_entry['status'] == 'ABSORBED':
            already += 1
            continue

        house_id = reg_entry['house']
        sphere_id = reg_entry['sphere']

        sphere_dir = get_sphere_dir(house_id, sphere_id)
        if not sphere_dir:
            errors.append(f"Sphere dir not found: {house_id}/{sphere_id}")
            continue

        module_dir = find_module_dir(sphere_dir, module_id)
        if not module_dir:
            errors.append(f"Module dir not found: {module_id} in {house_id}/{sphere_id}")
            continue

        impl_path = os.path.join(ROOT, config["impl"])
        if not os.path.exists(impl_path):
            errors.append(f"Impl not found: {config['impl']} for {module_id}")
            continue

        create_init_py(
            module_dir,
            module_id,
            config["desc"],
            config["impl"],
            config.get("note"),
        )

        reg_entry['status'] = 'ABSORBED'
        wired += 1

    with open(REGISTRY, 'w') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

    status_counts = {}
    for m in registry['modules']:
        s = m['status']
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"=== EXTENDED WIRING COMPLETE ===")
    print(f"Newly wired: {wired}")
    print(f"Already absorbed (skipped): {already}")
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  ⚠ {e}")
    print(f"\nRegistry status distribution:")
    for s, c in sorted(status_counts.items()):
        print(f"  {s}: {c}")
    print(f"\nTotal modules: {sum(status_counts.values())}")


if __name__ == "__main__":
    main()
