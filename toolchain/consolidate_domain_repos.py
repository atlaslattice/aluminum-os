#!/usr/bin/env python3
"""
Domain Repo Consolidation — Phase 4

The atlaslattice org has ~135 non-fork repos. Of these:
- 17 are core project repos (aluminum-os, element-145, etc.) — ALREADY ABSORBED
- 79 are domain/swarm repos (ai-ethics, banking-revolution, etc.) — NEED MANIFESTS
- 39 are "other" repos (algorithmic-*, tech-*, etc.) — NEED MANIFESTS

Strategy:
1. Generate a lattice.yaml manifest for each domain repo that maps it to a House/Sphere
2. Create a domain_repos/ directory in the monorepo with these manifests
3. The manifests tell the lattice which module each repo belongs to

This script generates the mapping based on repo name → House/Sphere classification.
"""

import os
import yaml

ROOT = "/home/ubuntu/aluminum-os"
MANIFEST_DIR = os.path.join(ROOT, "domain_repos")
os.makedirs(MANIFEST_DIR, exist_ok=True)

# ─── Classification Rules ─────────────────────────────────────────────────────

HOUSE_MAPPING = {
    # H01 Philosophy & Logic
    "ai-consent-framework": ("H01", "S03", "Ethics of AI consent"),
    "ethical-ai-guidelines": ("H01", "S03", "Ethical guidelines for AI systems"),
    "ai-chatbot-ethics": ("H01", "S03", "Ethical frameworks for chatbot interactions"),

    # H02 Formal Sciences
    "algorithmic-accountability": ("H02", "S03", "Accountability in algorithmic systems"),
    "algorithmic-discrimination": ("H02", "S03", "Detection of algorithmic discrimination"),
    "algorithmic-justice": ("H02", "S03", "Justice-oriented algorithm design"),
    "algorithmic-radicalization": ("H02", "S04", "Information theory of radicalization"),
    "algorithmic-transparency-tools": ("H02", "S03", "Transparency tools for algorithms"),
    "ai-fairness-metrics": ("H02", "S02", "Statistical fairness metrics for AI"),
    "ai-bias-detection": ("H02", "S02", "Statistical bias detection in ML models"),
    "machine-learning-bias": ("H02", "S02", "ML model bias analysis"),
    "ai-audit-framework": ("H02", "S03", "Audit frameworks for AI systems"),
    "deepfake-detection": ("H02", "S04", "Deepfake detection via information theory"),
    "ai-generated-content-detection": ("H02", "S04", "AI content detection algorithms"),

    # H03 Natural Sciences
    "climate-ai-solutions": ("H03", "S07", "AI solutions for climate change"),

    # H04 Technology & Engineering
    "ai-accountability-tools": ("H04", "S01", "Software tools for AI accountability"),
    "automated-content-filtering": ("H04", "S04", "ML-based content filtering"),
    "automated-decision-systems": ("H04", "S04", "Automated decision-making systems"),
    "smart-home-security": ("H04", "S11", "IoT security for smart homes"),
    "ai-content-moderation": ("H04", "S04", "AI content moderation systems"),
    "responsible-ai-toolkit": ("H04", "S04", "Responsible AI development toolkit"),
    "ai-transparency-toolkit": ("H04", "S01", "AI transparency engineering tools"),
    "predictive-policing-critique": ("H04", "S04", "Analysis of predictive policing ML"),
    "social-media-algorithms": ("H04", "S04", "Social media recommendation algorithms"),
    "tech-monopoly-analysis": ("H04", "S03", "Analysis of tech monopoly infrastructure"),
    "tech-platform-accountability": ("H04", "S01", "Platform accountability engineering"),
    "digital-platform-regulation": ("H04", "S01", "Digital platform regulation tech"),
    "tech-accountability-framework": ("H04", "S01", "Tech accountability framework"),

    # H05 Arts & Creative Expression
    "ai-art-copyright": ("H05", "S01", "Copyright issues in AI-generated art"),
    "ai-copyright-issues": ("H05", "S01", "AI copyright analysis"),
    "creative-ai-rights": ("H05", "S01", "Rights framework for creative AI"),
    "synthetic-media-ethics": ("H05", "S04", "Ethics of synthetic media"),
    "streaming-economics": ("H05", "S02", "Economics of music/video streaming"),
    "gaming-labor": ("H05", "S08", "Labor practices in gaming industry"),

    # H07 Applied Sciences
    "agricultural-ai": ("H07", "S01", "AI for agriculture and food systems"),
    "waste-management-ai": ("H07", "S02", "AI for waste management"),
    "water-management-ai": ("H07", "S02", "AI for water resource management"),
    "energy-grid-ai": ("H07", "S03", "AI for energy grid optimization"),
    "transportation-ai": ("H07", "S04", "AI for transportation systems"),
    "supply-chain-transparency": ("H07", "S05", "Supply chain transparency tools"),

    # H08 Education
    "educational-ai": ("H08", "S01", "AI in education systems"),
    "ai-education-ethics": ("H08", "S01", "Ethics of AI in education"),
    "academic-publishing": ("H08", "S01", "Academic publishing reform"),

    # H09 Life Sciences
    "pharmaceutical-ai": ("H09", "S01", "AI in pharmaceutical research"),

    # H10 Health & Medicine
    "healthcare-ai": ("H10", "S08", "AI in healthcare systems"),
    "ai-healthcare-ethics": ("H10", "S08", "Ethics of AI in healthcare"),
    "mental-health-ai": ("H10", "S08", "AI for mental health applications"),
    "elder-care-tech": ("H10", "S08", "Technology for elder care"),
    "disability-tech-access": ("H10", "S08", "Accessibility technology"),

    # H11 Social Sciences
    "ai-employment-impact": ("H11", "S01", "Economic impact of AI on employment"),
    "ai-labor-exploitation": ("H11", "S01", "Labor exploitation in AI industry"),
    "tech-worker-exploitation": ("H11", "S01", "Tech worker exploitation analysis"),
    "tech-worker-organizing": ("H11", "S01", "Tech worker organizing resources"),
    "gig-economy-exploitation": ("H11", "S01", "Gig economy exploitation analysis"),
    "gig-economy-analysis": ("H11", "S01", "Gig economy structural analysis"),
    "platform-worker-rights": ("H11", "S01", "Platform worker rights framework"),
    "food-delivery-exploitation": ("H11", "S01", "Food delivery labor exploitation"),
    "ai-labor-practices": ("H11", "S01", "AI industry labor practices"),
    "surveillance-capitalism": ("H11", "S02", "Surveillance capitalism analysis"),
    "social-media-harm": ("H11", "S04", "Social media psychological harm"),
    "ai-impact-assessment": ("H11", "S02", "AI societal impact assessment"),
    "housing-crisis-ai": ("H11", "S01", "AI and housing crisis analysis"),
    "journalism-ai": ("H11", "S04", "AI in journalism and media"),
    "call-center-automation": ("H11", "S01", "Call center automation impact"),
    "logistics-exploitation": ("H11", "S01", "Logistics industry exploitation"),
    "construction-safety-ai": ("H11", "S01", "AI for construction safety"),
    "retail-automation": ("H11", "S01", "Retail automation impact"),

    # H12 Law & Governance
    "ai-governance-framework": ("H12", "S01", "AI governance legal framework"),
    "ai-risk-assessment": ("H12", "S01", "AI risk assessment legal tools"),
    "ai-safety-research": ("H12", "S01", "AI safety research and regulation"),
    "ai-safety-hypocrisy": ("H12", "S01", "Analysis of AI safety rhetoric"),
    "content-moderation-ethics": ("H12", "S06", "Legal ethics of content moderation"),
    "content-moderation-trauma": ("H12", "S08", "Content moderator labor rights"),
    "voice-assistant-privacy": ("H12", "S09", "Privacy law for voice assistants"),
    "child-safety-ai": ("H12", "S08", "Child safety AI regulation"),
    "police-surveillance": ("H12", "S06", "Police surveillance legal analysis"),
    "military-ai-ethics": ("H12", "S02", "Military AI international law"),
    "prison-tech-ethics": ("H12", "S06", "Prison technology ethics"),
    "immigration-tech": ("H12", "S02", "Immigration technology legal analysis"),
    "credit-scoring-injustice": ("H12", "S04", "Credit scoring legal injustice"),
    "recruitment-ai-bias": ("H12", "S08", "Recruitment AI bias legal issues"),
    "insurance-ai-bias": ("H12", "S04", "Insurance AI bias legal analysis"),
    "legal-ai-ethics": ("H12", "S01", "Legal AI ethics framework"),
    "tech-ethics-resources": ("H12", "S01", "Tech ethics legal resources"),
    "fintech-disruption": ("H12", "S07", "Fintech regulation and disruption"),
    "banking-revolution": ("H12", "S07", "Banking revolution regulation"),

    # Financial/DeFi repos → H12 (regulatory)
    "bank-killer-financial-freedom": ("H12", "S07", "Financial freedom tools"),
    "zero-fee-defi-protocol": ("H12", "S07", "Zero-fee DeFi protocol"),
    "usdt-brics-payment-rails": ("H12", "S02", "BRICS payment rails"),
    "mint-alternative-open-source": ("H12", "S07", "Open source finance tools"),
    "defi-swap-zero-fees": ("H12", "S07", "DeFi swap protocol"),
}

# ─── Generate Manifests ───────────────────────────────────────────────────────

def generate_manifest(repo_name, house, sphere, description):
    """Generate a lattice.yaml manifest for a domain repo."""
    return {
        "repo": f"atlaslattice/{repo_name}",
        "lattice_position": {
            "house": house,
            "sphere": sphere,
        },
        "description": description,
        "type": "domain_application",
        "status": "INDEXED",
        "has_app": True,  # Most have full React apps
        "consolidation_action": "REFERENCE",  # Don't absorb, just reference
    }


def main():
    manifests = {}
    unmapped = []

    for repo_name, mapping in sorted(HOUSE_MAPPING.items()):
        house, sphere, desc = mapping
        manifest = generate_manifest(repo_name, house, sphere, desc)
        manifests[repo_name] = manifest

    # Write consolidated index
    index_path = os.path.join(MANIFEST_DIR, "domain_repo_index.yaml")
    with open(index_path, 'w') as f:
        yaml.dump({
            "version": "1.0",
            "generated": "2026-04-29",
            "total_repos": len(manifests),
            "consolidation_strategy": "REFERENCE (repos remain standalone, manifests link to lattice)",
            "repos": manifests,
        }, f, default_flow_style=False, sort_keys=False)

    # Stats
    house_counts = {}
    for repo, manifest in manifests.items():
        h = manifest["lattice_position"]["house"]
        house_counts[h] = house_counts.get(h, 0) + 1

    print(f"=== DOMAIN REPO CONSOLIDATION ===")
    print(f"Total manifests generated: {len(manifests)}")
    print(f"Output: {index_path}")
    print()
    print("Distribution by House:")
    for h in sorted(house_counts.keys()):
        print(f"  {h}: {house_counts[h]} repos")
    print()
    print(f"Unmapped repos: {len(unmapped)}")
    for r in unmapped:
        print(f"  {r}")


if __name__ == "__main__":
    main()
