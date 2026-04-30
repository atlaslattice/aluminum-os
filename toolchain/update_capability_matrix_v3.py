#!/usr/bin/env python3
"""
Update capability_matrix.yaml to v0.3.0:
- Add VIP element scores (E146, E147, E148, E149)
- Add market vertical coverage flags
- Update metadata
"""

import yaml
from datetime import date

MATRIX_PATH = "registries/capability_matrix.yaml"

def main():
    with open(MATRIX_PATH) as f:
        matrix = yaml.safe_load(f)
    
    # Update metadata
    matrix["version"] = "v0.3.0"
    matrix["generated"] = str(date.today())
    matrix["phase"] = "1.6"
    
    # Add VIP elements section
    matrix["vip_elements"] = {
        "E145": {
            "name": "Aluminum OS Core",
            "type": "Meta-Orchestrator",
            "status": "locked",
            "scores": {
                "S1_Anthropic": 0.6,
                "S2_Alphabet": 0.8,
                "S3_Muskverse": 0.5,
                "S4_Microsoft": 0.7,
                "Amazon": 0.5,
                "S5_DeepSeek": 0.4,
                "S6_OpenAI": 0.6,
                "S7_Manus": 0.9,  # Manus IS the orchestrator
                "S8_Notion": 0.3,
                "S10_Qwen3": 0.4,
            }
        },
        "E146": {
            "name": "Entertainment & Interactive Media",
            "type": "Domain VIP",
            "status": "provisional",
            "scores": {
                "S1_Anthropic": 0.2,
                "S2_Alphabet": 0.8,
                "S3_Muskverse": 0.3,
                "S4_Microsoft": 0.9,
                "Amazon": 0.6,
                "S5_DeepSeek": 0.1,
                "S6_OpenAI": 0.4,
                "S7_Manus": 0.1,
                "S8_Notion": 0.0,
                "S10_Qwen3": 0.2,
            }
        },
        "E147": {
            "name": "Cybersecurity & Adversarial Systems",
            "type": "Domain VIP",
            "status": "provisional",
            "scores": {
                "S1_Anthropic": 0.7,
                "S2_Alphabet": 0.8,
                "S3_Muskverse": 0.4,
                "S4_Microsoft": 0.9,
                "Amazon": 0.7,
                "S5_DeepSeek": 0.2,
                "S6_OpenAI": 0.5,
                "S7_Manus": 0.3,
                "S8_Notion": 0.1,
                "S10_Qwen3": 0.3,
            }
        },
        "E148": {
            "name": "AI Systems & Autonomous Intelligence",
            "type": "Domain VIP",
            "status": "provisional",
            "scores": {
                "S1_Anthropic": 0.9,
                "S2_Alphabet": 0.95,
                "S3_Muskverse": 0.7,
                "S4_Microsoft": 0.85,
                "Amazon": 0.6,
                "S5_DeepSeek": 0.8,
                "S6_OpenAI": 0.95,
                "S7_Manus": 0.6,
                "S8_Notion": 0.2,
                "S10_Qwen3": 0.75,
            }
        },
        "E149": {
            "name": "Climate Metabolism & Earth Systems",
            "type": "Domain VIP",
            "status": "provisional",
            "scores": {
                "S1_Anthropic": 0.4,
                "S2_Alphabet": 0.7,
                "S3_Muskverse": 0.8,
                "S4_Microsoft": 0.6,
                "Amazon": 0.5,
                "S5_DeepSeek": 0.1,
                "S6_OpenAI": 0.3,
                "S7_Manus": 0.2,
                "S8_Notion": 0.0,
                "S10_Qwen3": 0.2,
            }
        },
    }
    
    # Add market vertical coverage
    matrix["market_verticals"] = {
        "gaming": {
            "covered_by": "E146",
            "primary_spheres": ["S057.08", "S016.07", "S055.06"],
            "lead_seats": ["S4_Microsoft", "S2_Alphabet"],
        },
        "film_production": {
            "covered_by": "E146",
            "primary_spheres": ["S054.01", "S054.02", "S054.06"],
            "lead_seats": ["S2_Alphabet", "Amazon"],
        },
        "cybersecurity": {
            "covered_by": "E147",
            "primary_spheres": ["S020.13", "S020.14", "S016.19"],
            "lead_seats": ["S4_Microsoft", "S2_Alphabet"],
        },
        "ai_ml": {
            "covered_by": "E148",
            "primary_spheres": ["S016.06", "S016.13", "S016.21"],
            "lead_seats": ["S6_OpenAI", "S2_Alphabet", "S1_Anthropic"],
        },
        "climate_tech": {
            "covered_by": "E149",
            "primary_spheres": ["S005.13", "S067.14", "S122.13"],
            "lead_seats": ["S3_Muskverse", "S2_Alphabet"],
        },
        "biotech": {
            "covered_by": None,
            "primary_spheres": ["S003.13", "S003.14", "S003.18"],
            "lead_seats": ["S2_Alphabet"],
            "note": "No dedicated VIP yet — candidate for E150"
        },
        "fintech": {
            "covered_by": None,
            "primary_spheres": ["S111.13", "S111.14", "S111.17"],
            "lead_seats": ["Amazon", "S4_Microsoft"],
            "note": "No dedicated VIP yet — candidate for E151"
        },
        "robotics": {
            "covered_by": None,
            "primary_spheres": ["S072.01", "S072.13", "S072.14"],
            "lead_seats": ["S3_Muskverse", "S2_Alphabet"],
            "note": "Covered by tier-2 sub-spheres, no VIP needed yet"
        },
        "autonomous_vehicles": {
            "covered_by": "E148",
            "primary_spheres": ["S072.13", "S065.01"],
            "lead_seats": ["S3_Muskverse", "S2_Alphabet"],
        },
        "xr_vr": {
            "covered_by": "E146",
            "primary_spheres": ["S081.08", "S081.09"],
            "lead_seats": ["S4_Microsoft", "S2_Alphabet"],
        },
        "animation_vfx": {
            "covered_by": "E146",
            "primary_spheres": ["S054.06", "S054.07"],
            "lead_seats": ["S2_Alphabet", "S4_Microsoft"],
        },
        "music_production": {
            "covered_by": "E146",
            "primary_spheres": ["S051.03", "S051.04"],
            "lead_seats": ["S2_Alphabet", "Amazon"],
        },
    }
    
    with open(MATRIX_PATH, "w") as f:
        yaml.dump(matrix, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Capability matrix updated to v0.3.0")
    print(f"  VIP elements: 5 (E145-E149)")
    print(f"  Market verticals: {len(matrix['market_verticals'])}")
    print(f"  Written to: {MATRIX_PATH}")


if __name__ == "__main__":
    main()
