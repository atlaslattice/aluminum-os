#!/usr/bin/env python3
"""
Fill Claude's Gap Analysis — Phase 1.6 Sub-Sphere Expansion
Adds missing sub-spheres across 6 gap domains:
1. Cybersecurity & Adversarial Systems
2. AI/ML Native Disciplines
3. Climate / Earth Systems / Sustainability
4. Bioinformatics / Synthetic Biology
5. FinTech / Crypto-Economics / Digital Markets
6. Human-Computer Interaction (HCI)

Also fills incomplete H03, H04, H09, H12 sub-spheres per Claude's audit.
"""

import yaml
import os
from datetime import date

REGISTRY_PATH = "houses/h00_directory/sub_sphere_registry.yaml"

# ============================================================
# GAP DOMAIN 1: Cybersecurity & Adversarial Systems
# Expands S016 (Computer Science) and S019 sub-spheres
# ============================================================
CYBERSECURITY_ADDITIONS = {
    # S016 already has S016.12 Computer Security — expand it
    "S016": [
        ("S016.19", "Cybersecurity Engineering"),
        ("S016.20", "Adversarial Machine Learning"),
        ("S016.21", "Penetration Testing"),
        ("S016.22", "Malware Analysis"),
        ("S016.23", "Threat Intelligence"),
        ("S016.24", "Identity & Access Management"),
    ],
}

# ============================================================
# GAP DOMAIN 2: AI/ML Native Disciplines
# Expands S016 (Computer Science) with AI ecosystem sub-spheres
# ============================================================
AI_ML_ADDITIONS = {
    "S016": [
        # Note: S016 already at 18, these push to 24 (max wiggle room)
        # Some of these overlap with existing — only truly new ones
        # S016.06 = AI, S016.13 = ML, S016.14 = NLP, S016.15 = CV
        # Adding the missing ecosystem:
    ],
    # Better to add under a new approach: expand existing sub-spheres
    # S016.06 AI already exists — add AI-native as siblings
    "S016_ai_native": [
        ("S016.25", "AI Alignment & Safety"),
        ("S016.26", "Interpretability & Explainability"),
        ("S016.27", "Distributed Training Systems"),
        ("S016.28", "Synthetic Data Generation"),
        ("S016.29", "Reinforcement Learning"),
        ("S016.30", "Multi-Agent Systems"),
        ("S016.31", "Autonomous Systems"),
        ("S016.32", "AI Safety Engineering"),
    ],
}

# Wait — S016 would go to 32 sub-spheres which exceeds 24 max.
# Claude is right that these need to be here, but we need to respect
# the wiggle room policy. Solution: split into S016 additions (up to 24)
# and flag the rest as Phase 2 candidates.

# Revised: S016 gets to exactly 24 (currently 18, add 6)
CYBERSECURITY_AND_AI_FOR_S016 = [
    ("S016.19", "Cybersecurity Engineering"),
    ("S016.20", "Adversarial Machine Learning"),
    ("S016.21", "AI Alignment & Safety"),
    ("S016.22", "Interpretability & Explainability"),
    ("S016.23", "Reinforcement Learning"),
    ("S016.24", "Multi-Agent Systems"),
]

# Remaining AI/ML and Cybersecurity go to related spheres
AI_OVERFLOW_TO_OTHER_SPHERES = {
    # S069 Software Engineering (currently 15) — add safety engineering
    "S069": [
        ("S069.16", "AI Safety Engineering"),
        ("S069.17", "Distributed Training Infrastructure"),
        ("S069.18", "MLOps & Model Deployment"),
    ],
    # S072 Robotics (currently 12) — add autonomous systems
    "S072": [
        ("S072.13", "Autonomous Systems"),
        ("S072.14", "Swarm Intelligence"),
    ],
    # S024 Data Science (currently 12) — add synthetic data
    "S024": [
        ("S024.13", "Synthetic Data Generation"),
        ("S024.14", "Data Governance"),
    ],
    # S020 Cryptography (currently 12) — add cybersecurity specifics
    "S020": [
        ("S020.13", "Penetration Testing"),
        ("S020.14", "Malware Analysis"),
        ("S020.15", "Threat Intelligence"),
        ("S020.16", "Identity & Access Management"),
        ("S020.17", "Security Operations (SOC)"),
        ("S020.18", "Incident Response"),
    ],
}

# ============================================================
# GAP DOMAIN 3: Climate / Earth Systems / Sustainability
# ============================================================
CLIMATE_ADDITIONS = {
    # S005 Ecology (currently 12) — add sustainability
    "S005": [
        ("S005.13", "Carbon Accounting"),
        ("S005.14", "Circular Economy"),
        ("S005.15", "Planetary Boundaries"),
        ("S005.16", "Resilience Engineering"),
    ],
    # S006 Meteorology (currently 12) — add climate systems
    "S006": [
        ("S006.13", "Climate Modeling"),
        ("S006.14", "Climate Adaptation"),
        ("S006.15", "Disaster Response"),
    ],
    # S067 Environmental Engineering (currently 11, 1 blank) — fill blank + add
    "S067": [
        ("S067.12", "Resource Metabolism"),  # fills BLANK
        ("S067.13", "Green Infrastructure"),
        ("S067.14", "Decarbonization Engineering"),
    ],
    # S122 Energy Systems (currently 12) — add clean energy
    "S122": [
        ("S122.13", "Carbon Capture & Storage"),
        ("S122.14", "Hydrogen Economy"),
        ("S122.15", "Grid Modernization"),
    ],
}

# ============================================================
# GAP DOMAIN 4: Bioinformatics / Synthetic Biology
# ============================================================
BIOTECH_ADDITIONS = {
    # S003 Biology (currently 12) — add modern biotech
    "S003": [
        ("S003.13", "Proteomics"),
        ("S003.14", "CRISPR & Gene Editing"),
        ("S003.15", "Metabolic Engineering"),
        ("S003.16", "Biomanufacturing"),
        ("S003.17", "Computational Genomics"),
        ("S003.18", "Drug Discovery Pipelines"),
    ],
    # S097 Anatomy (currently 11, 1 blank) — fill blank
    "S097": [
        ("S097.12", "Regenerative Medicine"),  # fills BLANK
    ],
}

# ============================================================
# GAP DOMAIN 5: FinTech / Crypto-Economics / Digital Markets
# ============================================================
FINTECH_ADDITIONS = {
    # S111 Finance (currently 12) — add fintech specifics
    "S111": [
        ("S111.13", "Blockchain Engineering"),
        ("S111.14", "Smart Contracts"),
        ("S111.15", "Token Economics"),
        ("S111.16", "Digital Asset Markets"),
        ("S111.17", "Fraud Detection"),
        ("S111.18", "Compliance Technology (RegTech)"),
    ],
    # S112 Accounting (currently 11, 1 blank) — fill blank + add
    "S112": [
        ("S112.12", "Crypto Accounting"),  # fills BLANK
    ],
}

# ============================================================
# GAP DOMAIN 6: Human-Computer Interaction (HCI)
# ============================================================
HCI_ADDITIONS = {
    # S057 Design (currently 13) — add HCI specifics
    "S057": [
        ("S057.14", "Embodied Interaction Design"),
        ("S057.15", "Social Computing"),
    ],
    # S081 Digital Media (currently 12) — add interaction
    "S081": [
        ("S081.13", "Interface Architecture"),
        ("S081.14", "Conversational UI"),
    ],
}

# ============================================================
# INCOMPLETE HOUSES — H03, H04, H09, H12 per Claude's audit
# ============================================================
H03_SOCIAL_SCIENCES = {
    # S025 Sociology (currently 12) — add missing
    "S025": [
        ("S025.13", "Digital Sociology"),
        ("S025.14", "Computational Social Science"),
    ],
    # S027 Anthropology (currently 11, 1 blank)
    "S027": [
        ("S027.12", "Digital Anthropology"),  # fills BLANK
    ],
    # S029 Political Science (currently 12) — add
    "S029": [
        ("S029.13", "Computational Politics"),
        ("S029.14", "Digital Governance"),
    ],
    # S031 Criminology (currently 12) — add
    "S031": [
        ("S031.13", "Cybercrime"),
        ("S031.14", "Digital Forensics"),
    ],
    # S035 Gender Studies (currently 11, 1 blank)
    "S035": [
        ("S035.12", "Digital Gender Studies"),  # fills BLANK
    ],
    # S036 Urban Studies (currently 12) — add
    "S036": [
        ("S036.13", "Smart Cities"),
        ("S036.14", "Urban Informatics"),
    ],
}

H04_HUMANITIES = {
    # S046 Folklore (currently 11, 1 blank)
    "S046": [
        ("S046.12", "Digital Folklore"),  # fills BLANK
    ],
    # S047 Philology (currently 11, 1 blank)
    "S047": [
        ("S047.12", "Computational Philology"),  # fills BLANK
    ],
    # S048 Museology (currently 11, 1 blank)
    "S048": [
        ("S048.12", "Digital Museology"),  # fills BLANK
    ],
    # S045 Cultural Studies (currently 12) — already complete
}

H09_HEALTH = {
    # S098 Pharmacology (currently 12) — add
    "S098": [
        ("S098.13", "Computational Pharmacology"),
        ("S098.14", "Drug Repurposing"),
    ],
    # S099 Psychiatry (currently 12) — add
    "S099": [
        ("S099.13", "Digital Therapeutics"),
    ],
    # S100 Epidemiology (currently 12) — add
    "S100": [
        ("S100.13", "Pandemic Modeling"),
        ("S100.14", "Genomic Epidemiology"),
    ],
    # S101 Public Health (currently 12) — add
    "S101": [
        ("S101.13", "Digital Public Health"),
        ("S101.14", "Health Informatics"),
    ],
    # S102 Nursing (currently 12) — add
    "S102": [
        ("S102.13", "Telehealth Nursing"),
    ],
    # S103 Surgery (currently 12) — add
    "S103": [
        ("S103.13", "Robotic Surgery"),
        ("S103.14", "AI-Assisted Diagnostics"),
    ],
    # S104 Dentistry (currently 11, 1 blank) — fill
    "S104": [
        ("S104.12", "Digital Dentistry"),  # fills BLANK
    ],
    # S105 Veterinary Medicine (currently 11, 1 blank) — fill
    "S105": [
        ("S105.12", "Veterinary Telemedicine"),  # fills BLANK
    ],
    # S106 Rehabilitation (currently 12) — add
    "S106": [
        ("S106.13", "VR Rehabilitation"),
    ],
    # S108 Pathology (currently 11, 1 blank) — fill
    "S108": [
        ("S108.12", "Digital Pathology"),  # fills BLANK
    ],
}

H12_LAW_GOVERNANCE = {
    # S133 Constitutional Law (currently 11, 1 blank)
    "S133": [
        ("S133.12", "Digital Constitutional Rights"),  # fills BLANK
    ],
    # S137 IP Law (currently 12) — add
    "S137": [
        ("S137.13", "AI-Generated IP"),
        ("S137.14", "Open Source Licensing"),
    ],
    # S140 Tax Law (currently 11, 1 blank)
    "S140": [
        ("S140.12", "Digital Tax Policy"),  # fills BLANK
    ],
    # S143 Diplomacy (currently 11, 1 blank)
    "S143": [
        ("S143.12", "Digital Diplomacy"),  # fills BLANK
    ],
    # S144 International Relations (currently 12) — add
    "S144": [
        ("S144.13", "Cyber Governance"),
        ("S144.14", "AI Treaty Frameworks"),
    ],
}


def apply_additions(registry, additions_dict, domain_name):
    """Apply a set of additions to the registry."""
    added = 0
    for sphere_id_raw, new_subs in additions_dict.items():
        # Handle special keys like "S016_ai_native"
        sphere_id = sphere_id_raw.split("_")[0] if "_" in sphere_id_raw else sphere_id_raw
        
        if sphere_id not in registry["spheres"]:
            print(f"  WARNING: {sphere_id} not found in registry, skipping")
            continue
        
        sphere = registry["spheres"][sphere_id]
        existing_ids = {ss["id"] for ss in sphere["sub_spheres"]}
        
        for sub_id, sub_name in new_subs:
            if sub_id in existing_ids:
                # Check if it's a BLANK being filled
                for ss in sphere["sub_spheres"]:
                    if ss["id"] == sub_id and ss["status"] == "BLANK":
                        ss["name"] = sub_name
                        ss["status"] = "populated"
                        added += 1
                        print(f"  FILLED BLANK: {sub_id} → {sub_name}")
                        break
                continue
            
            # Check wiggle room
            current_count = len(sphere["sub_spheres"])
            if current_count >= 24:
                print(f"  SKIP (max 24): {sub_id} {sub_name} for {sphere_id} ({current_count} already)")
                continue
            
            sphere["sub_spheres"].append({
                "id": sub_id,
                "name": sub_name,
                "status": "populated"
            })
            added += 1
        
        # Recalculate counts
        sphere["populated_count"] = sum(1 for ss in sphere["sub_spheres"] if ss["status"] == "populated")
        sphere["blank_count"] = sum(1 for ss in sphere["sub_spheres"] if ss["status"] == "BLANK")
        if sphere["blank_count"] == 0:
            sphere["population_priority"] = "complete"
    
    print(f"  [{domain_name}] Added {added} sub-spheres")
    return added


def main():
    with open(REGISTRY_PATH) as f:
        registry = yaml.safe_load(f)
    
    total_added = 0
    
    print("=== Phase 1.6: Claude Gap Analysis Integration ===\n")
    
    # Domain 1: Cybersecurity (S016 capped at 24, overflow to S020)
    total_added += apply_additions(registry, {"S016": CYBERSECURITY_AND_AI_FOR_S016}, "Cybersecurity+AI→S016")
    total_added += apply_additions(registry, AI_OVERFLOW_TO_OTHER_SPHERES, "AI/Cyber overflow")
    
    # Domain 3: Climate
    total_added += apply_additions(registry, CLIMATE_ADDITIONS, "Climate/Earth Systems")
    
    # Domain 4: Biotech
    total_added += apply_additions(registry, BIOTECH_ADDITIONS, "Biotech/SynBio")
    
    # Domain 5: FinTech
    total_added += apply_additions(registry, FINTECH_ADDITIONS, "FinTech/Crypto")
    
    # Domain 6: HCI
    total_added += apply_additions(registry, HCI_ADDITIONS, "HCI")
    
    # Incomplete Houses
    total_added += apply_additions(registry, H03_SOCIAL_SCIENCES, "H03 Social Sciences")
    total_added += apply_additions(registry, H04_HUMANITIES, "H04 Humanities")
    total_added += apply_additions(registry, H09_HEALTH, "H09 Health & Medicine")
    total_added += apply_additions(registry, H12_LAW_GOVERNANCE, "H12 Law/Governance")
    
    # Recalculate totals
    total_populated = 0
    total_blanks = 0
    for sid, sphere in registry["spheres"].items():
        total_populated += sphere["populated_count"]
        total_blanks += sphere["blank_count"]
    
    registry["total_sub_spheres_populated"] = total_populated
    registry["total_blanks"] = total_blanks
    registry["version"] = "v3.6.0"
    registry["generated"] = str(date.today())
    registry["phase"] = "1.6"
    
    # Write updated registry
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total sub-spheres added: {total_added}")
    print(f"Total populated: {total_populated}")
    print(f"Total BLANKs remaining: {total_blanks}")
    print(f"Registry version: v3.6.0")
    print(f"Written to: {REGISTRY_PATH}")
    
    # Report spheres that hit or approach the 24 limit
    print(f"\n=== SPHERES NEAR LIMIT (>18) ===")
    for sid, sphere in sorted(registry["spheres"].items()):
        count = len(sphere["sub_spheres"])
        if count > 18:
            print(f"  {sid} {sphere['name']}: {count} sub-spheres")


if __name__ == "__main__":
    main()
