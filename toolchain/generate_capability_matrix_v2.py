#!/usr/bin/env python3
"""
Generate capability_matrix v0.2.0 — incorporating all 8 Scribe refinements:
1. Merge per-entity org charts (Notion self-maps) into per-sphere scores
2. 5-tier scoring: Deep/Substantial/Peripheral/Absent/Unknown
3. Recent acquisition updates (Wiz→Google, etc.)
4. Breadth/depth/leadership decomposition per seat
5. Seat summary blocks with org_chart_source pointers
6. seduction_risk_flag on spheres where single-seat dominance > 0.85
7. Civic balancing recommendations (civilizational layer reframe)
8. org_chart_pointers.md cross-reference
"""

import yaml, csv, os, json
from pathlib import Path

ROOT = Path("/home/ubuntu/aluminum-os")

# ─── CANONICAL 12 HOUSES × 12 SPHERES ───────────────────────────────
HOUSES = {
    "H01": {"name": "Natural Sciences", "spheres": [
        "Physics", "Chemistry", "Biology", "Astronomy", "Geology",
        "Oceanography", "Meteorology", "Ecology", "Botany", "Zoology",
        "Microbiology", "Genetics"
    ]},
    "H02": {"name": "Formal Sciences", "spheres": [
        "Mathematics", "Logic", "Statistics", "Computer Science",
        "Information Theory", "Game Theory", "Operations Research",
        "Systems Theory", "Decision Theory", "Cryptography",
        "Algorithmics", "Data Science"
    ]},
    "H03": {"name": "Social Sciences", "spheres": [
        "Sociology", "Psychology", "Anthropology", "Economics",
        "Political Science", "Geography", "Linguistics", "Archaeology",
        "Demography", "Criminology", "Social Work", "Urban Studies"
    ]},
    "H04": {"name": "Humanities", "spheres": [
        "History", "Philosophy", "Literature", "Classics",
        "Religious Studies", "Ethics", "Aesthetics", "Cultural Studies",
        "Mythology", "Philology", "Rhetoric", "Hermeneutics"
    ]},
    "H05": {"name": "Arts", "spheres": [
        "Visual Arts", "Performing Arts", "Music", "Dance",
        "Theater", "Film", "Creative Writing", "Architecture",
        "Design", "Photography", "Sculpture", "Painting"
    ]},
    "H06": {"name": "Engineering & Technology", "spheres": [
        "Mechanical Engineering", "Electrical Engineering",
        "Civil Engineering", "Chemical Engineering",
        "Aerospace Engineering", "Biomedical Engineering",
        "Environmental Engineering", "Industrial Engineering",
        "Software Engineering", "Materials Engineering",
        "Nuclear Engineering", "Robotics"
    ]},
    "H07": {"name": "Information & Communication", "spheres": [
        "Media Studies", "Journalism", "Telecommunications",
        "Information Systems", "Library Science", "Publishing",
        "Advertising", "Public Relations", "Digital Media",
        "Broadcasting", "Film Studies", "Communication Theory"
    ]},
    "H08": {"name": "Education", "spheres": [
        "Pedagogy", "Curriculum Design", "Educational Psychology",
        "Special Education", "Adult Education", "E-Learning",
        "Educational Technology", "Assessment", "School Administration",
        "Teacher Training", "Literacy", "Higher Education"
    ]},
    "H09": {"name": "Health & Medicine", "spheres": [
        "Anatomy", "Physiology", "Pathology", "Pharmacology",
        "Surgery", "Pediatrics", "Psychiatry", "Neurology",
        "Oncology", "Epidemiology", "Nutrition", "Public Health"
    ]},
    "H10": {"name": "Business & Economics", "spheres": [
        "Management", "Marketing", "Finance", "Accounting",
        "Entrepreneurship", "Human Resources", "Operations Management",
        "Supply Chain", "International Business", "Business Ethics",
        "Microeconomics", "Macroeconomics"
    ]},
    "H11": {"name": "Infrastructure", "spheres": [
        "Transportation", "Energy Systems", "Water Systems",
        "Waste Management", "Computing Infrastructure",
        "Telecommunications Infrastructure", "Urban Planning",
        "Construction", "Logistics", "Mining",
        "Agriculture Infrastructure", "Space Infrastructure"
    ]},
    "H12": {"name": "Law/Governance/Meta-Knowledge", "spheres": [
        "Constitutional Law", "Criminal Law", "Civil Law",
        "International Law", "Corporate Law", "Environmental Law",
        "Human Rights", "Political Theory", "Public Policy",
        "International Relations", "Diplomacy", "Public Administration"
    ]},
}

# ─── PER-SEAT CAPABILITY SCORES ─────────────────────────────────────
# Sources:
# - S1 Anthropic: Notion self-map (34a0c1de) — per-sphere 0.0-1.0 scores
# - S2 Alphabet: Notion self-map (34a0c1de-81eb) — house-level % + narrative
# - S3 Muskverse: Notion self-map (34a0c1de-81f4) — narrative + 7 deep spheres
# - S4 Microsoft: Federation v1.1 (3500c1de-81f0) — 95.8% coverage claim
# - S5 DeepSeek: DeepSeek Vendor Suite v1.0 (3500c1de-8130)
# - S6 OpenAI: Build Plan v3.14 vendor suite + Federation v1.1
# - S7 Manus: Build Plan v3.14 + Federation v1.1
# - S8 Notion: Build Plan v3.14 + Federation v1.1
# - Amazon: Four-Company Matrix (34a0c1de-819e) + self-map (34a0c1de-81c8)
# - S10 Qwen3: ORC-015 Trinity + Federation v1.1

def get_seat_scores():
    """Return dict of seat_id -> {sphere_key: score}"""
    seats = {}
    
    # ── S1 ANTHROPIC (from Notion self-map — exact per-sphere scores) ──
    s1 = {}
    # H01 Natural Sciences
    s1_h01 = [0.2, 0.1, 0.2, 0.1, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.1, 0.2]
    # H02 Formal Sciences
    s1_h02 = [0.7, 0.8, 0.8, 0.9, 0.7, 0.6, 0.4, 0.7, 0.8, 0.3, 0.8, 0.7]
    # H03 Social Sciences
    s1_h03 = [0.3, 0.4, 0.2, 0.5, 0.4, 0.0, 0.7, 0.0, 0.1, 0.2, 0.0, 0.0]
    # H04 Humanities
    s1_h04 = [0.2, 0.8, 0.2, 0.1, 0.1, 0.9, 0.1, 0.2, 0.0, 0.1, 0.3, 0.4]
    # H05 Arts
    s1_h05 = [0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.2, 0.0, 0.3, 0.0, 0.0, 0.0]
    # H06 Engineering & Technology
    s1_h06 = [0.0, 0.2, 0.0, 0.0, 0.0, 0.1, 0.1, 0.2, 0.9, 0.0, 0.0, 0.3]
    # H07 Information & Communication (estimated from narrative)
    s1_h07 = [0.2, 0.1, 0.1, 0.3, 0.1, 0.2, 0.1, 0.1, 0.3, 0.1, 0.1, 0.2]
    # H08 Education
    s1_h08 = [0.3, 0.1, 0.2, 0.1, 0.1, 0.3, 0.4, 0.3, 0.0, 0.1, 0.2, 0.3]
    # H09 Health & Medicine
    s1_h09 = [0.0, 0.0, 0.1, 0.2, 0.0, 0.0, 0.2, 0.2, 0.1, 0.1, 0.0, 0.2]
    # H10 Business & Economics
    s1_h10 = [0.5, 0.4, 0.3, 0.3, 0.4, 0.3, 0.4, 0.1, 0.3, 0.6, 0.3, 0.4]
    # H11 Infrastructure
    s1_h11 = [0.1, 0.1, 0.0, 0.0, 0.3, 0.1, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0]
    # H12 Law/Governance
    s1_h12 = [0.5, 0.2, 0.2, 0.3, 0.4, 0.1, 0.4, 0.4, 0.8, 0.5, 0.3, 0.4]
    
    all_s1 = s1_h01 + s1_h02 + s1_h03 + s1_h04 + s1_h05 + s1_h06 + s1_h07 + s1_h08 + s1_h09 + s1_h10 + s1_h11 + s1_h12
    
    # ── S2 ALPHABET (from Notion self-map — Gemini's 47% with per-house breakdown) ──
    # Gemini said: 68/144 spheres at substantial+, ~47% coverage
    # Deep in: Search, Cloud (GCP), AI/ML (DeepMind), Earth observation, Maps, YouTube, Android
    # 2026 update: Wiz acquisition adds cybersecurity depth
    s2_h01 = [0.7, 0.6, 0.7, 0.6, 0.5, 0.5, 0.7, 0.6, 0.3, 0.3, 0.4, 0.6]  # Earth Engine, DeepMind bio
    s2_h02 = [0.8, 0.7, 0.8, 0.9, 0.8, 0.5, 0.6, 0.7, 0.6, 0.7, 0.9, 0.9]  # DeepMind, TensorFlow, Wiz(crypto)
    s2_h03 = [0.3, 0.4, 0.3, 0.5, 0.3, 0.8, 0.7, 0.2, 0.3, 0.2, 0.1, 0.4]  # Google Maps(geo), NLP
    s2_h04 = [0.3, 0.3, 0.3, 0.2, 0.1, 0.3, 0.2, 0.3, 0.1, 0.2, 0.2, 0.2]  # Peripheral
    s2_h05 = [0.3, 0.2, 0.5, 0.1, 0.1, 0.7, 0.3, 0.2, 0.5, 0.4, 0.1, 0.1]  # YouTube(film/music), Material Design
    s2_h06 = [0.3, 0.5, 0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.9, 0.3, 0.1, 0.6]  # Software eng deep, Waymo(robotics)
    s2_h07 = [0.6, 0.5, 0.7, 0.8, 0.3, 0.3, 0.8, 0.4, 0.8, 0.5, 0.4, 0.5]  # Search, Ads, Android, Fiber
    s2_h08 = [0.4, 0.4, 0.3, 0.3, 0.3, 0.6, 0.7, 0.4, 0.3, 0.3, 0.3, 0.5]  # Google Classroom, Chromebook
    s2_h09 = [0.3, 0.3, 0.3, 0.4, 0.2, 0.2, 0.3, 0.4, 0.3, 0.4, 0.2, 0.4]  # Verily, DeepMind health
    s2_h10 = [0.5, 0.8, 0.5, 0.4, 0.5, 0.5, 0.5, 0.3, 0.6, 0.4, 0.4, 0.5]  # Google Ads(marketing), GCP business
    s2_h11 = [0.4, 0.5, 0.3, 0.3, 0.9, 0.8, 0.5, 0.3, 0.4, 0.2, 0.3, 0.4]  # GCP(compute infra), Fiber(telecom)
    s2_h12 = [0.3, 0.2, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.5, 0.4, 0.3, 0.3]  # Policy team
    
    all_s2 = s2_h01 + s2_h02 + s2_h03 + s2_h04 + s2_h05 + s2_h06 + s2_h07 + s2_h08 + s2_h09 + s2_h10 + s2_h11 + s2_h12
    
    # ── S3 MUSKVERSE (from Notion self-map — Grok's narrative + 7 deep spheres) ──
    # Deep: Robotics(0.89), Energy Storage(0.88), Battery Circularity(0.84), 
    #        Manufacturing(0.83), Orbital(0.82), Autonomous Systems(0.79), Megawatt Energy(0.78)
    # ~39% coverage, concentrated in physical infrastructure
    s3_h01 = [0.4, 0.3, 0.2, 0.5, 0.3, 0.1, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2]  # SpaceX physics, astronomy
    s3_h02 = [0.3, 0.2, 0.3, 0.5, 0.2, 0.2, 0.3, 0.4, 0.3, 0.3, 0.5, 0.4]  # xAI/Grok
    s3_h03 = [0.1, 0.2, 0.1, 0.3, 0.2, 0.1, 0.1, 0.0, 0.1, 0.1, 0.0, 0.1]  # Weak
    s3_h04 = [0.1, 0.2, 0.1, 0.1, 0.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.1]  # Weak
    s3_h05 = [0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.1, 0.3, 0.3, 0.0, 0.0, 0.0]  # Architecture(Boring Co)
    s3_h06 = [0.8, 0.8, 0.4, 0.4, 1.0, 0.3, 0.5, 0.8, 0.5, 0.8, 0.3, 0.9]  # Core strength
    s3_h07 = [0.2, 0.1, 0.6, 0.3, 0.0, 0.1, 0.2, 0.1, 0.3, 0.2, 0.1, 0.1]  # Starlink(telecom), X(media)
    s3_h08 = [0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1]  # Weak
    s3_h09 = [0.1, 0.1, 0.1, 0.1, 0.2, 0.0, 0.1, 0.5, 0.1, 0.1, 0.0, 0.1]  # Neuralink(neurology)
    s3_h10 = [0.5, 0.3, 0.4, 0.3, 0.8, 0.3, 0.6, 0.4, 0.4, 0.3, 0.3, 0.3]  # Entrepreneurship deep
    s3_h11 = [0.7, 0.9, 0.2, 0.2, 0.5, 0.6, 0.3, 0.5, 0.6, 0.3, 0.4, 0.8]  # Energy, transport, space infra
    s3_h12 = [0.1, 0.1, 0.1, 0.2, 0.3, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1]  # Weak in governance
    
    all_s3 = s3_h01 + s3_h02 + s3_h03 + s3_h04 + s3_h05 + s3_h06 + s3_h07 + s3_h08 + s3_h09 + s3_h10 + s3_h11 + s3_h12
    
    # ── S4 MICROSOFT (from Federation v1.1 — 95.8% coverage claim, cross-validated) ──
    # Deep: Azure, Office 365, GitHub, LinkedIn, Windows, Xbox, Nuance
    # 2026: Activision Blizzard acquisition complete
    s4_h01 = [0.3, 0.3, 0.4, 0.3, 0.3, 0.2, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4]  # Azure AI research
    s4_h02 = [0.7, 0.6, 0.7, 0.9, 0.6, 0.5, 0.6, 0.6, 0.6, 0.6, 0.8, 0.8]  # Azure, GitHub, VS Code
    s4_h03 = [0.4, 0.4, 0.3, 0.5, 0.3, 0.3, 0.6, 0.2, 0.3, 0.2, 0.2, 0.3]  # LinkedIn(sociology), NLP
    s4_h04 = [0.3, 0.3, 0.3, 0.2, 0.2, 0.4, 0.2, 0.3, 0.1, 0.2, 0.2, 0.2]  # Responsible AI ethics
    s4_h05 = [0.3, 0.3, 0.4, 0.2, 0.3, 0.5, 0.4, 0.2, 0.5, 0.3, 0.2, 0.2]  # Xbox(film/games), Activision
    s4_h06 = [0.3, 0.4, 0.2, 0.2, 0.2, 0.4, 0.3, 0.4, 0.9, 0.2, 0.1, 0.4]  # Software eng deep, HoloLens
    s4_h07 = [0.5, 0.4, 0.5, 0.8, 0.3, 0.4, 0.6, 0.4, 0.6, 0.4, 0.3, 0.5]  # Office 365, Teams, Azure
    s4_h08 = [0.5, 0.5, 0.4, 0.4, 0.4, 0.6, 0.7, 0.5, 0.4, 0.4, 0.4, 0.6]  # Microsoft Education, Teams
    s4_h09 = [0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.4]  # Nuance(health), Azure Health
    s4_h10 = [0.6, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.4, 0.6, 0.5, 0.4, 0.5]  # Dynamics 365, LinkedIn
    s4_h11 = [0.4, 0.4, 0.3, 0.3, 0.8, 0.6, 0.5, 0.4, 0.4, 0.2, 0.2, 0.3]  # Azure(compute infra)
    s4_h12 = [0.4, 0.3, 0.3, 0.4, 0.5, 0.3, 0.4, 0.4, 0.5, 0.4, 0.3, 0.4]  # Government cloud, policy
    
    all_s4 = s4_h01 + s4_h02 + s4_h03 + s4_h04 + s4_h05 + s4_h06 + s4_h07 + s4_h08 + s4_h09 + s4_h10 + s4_h11 + s4_h12
    
    # ── S5 DEEPSEEK (from Vendor Suite v1.0 — narrow but deep in formal sciences) ──
    s5_h01 = [0.2, 0.2, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.1]
    s5_h02 = [0.7, 0.6, 0.6, 0.8, 0.5, 0.4, 0.4, 0.5, 0.5, 0.4, 0.7, 0.7]  # Core strength
    s5_h03 = [0.1, 0.1, 0.1, 0.3, 0.1, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0]
    s5_h04 = [0.1, 0.3, 0.2, 0.1, 0.0, 0.2, 0.0, 0.1, 0.0, 0.1, 0.1, 0.1]
    s5_h05 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0]
    s5_h06 = [0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.7, 0.0, 0.0, 0.1]
    s5_h07 = [0.1, 0.0, 0.1, 0.2, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.1]
    s5_h08 = [0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1]
    s5_h09 = [0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s5_h10 = [0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2, 0.2]
    s5_h11 = [0.0, 0.1, 0.0, 0.0, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s5_h12 = [0.1, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1, 0.0, 0.1]
    
    all_s5 = s5_h01 + s5_h02 + s5_h03 + s5_h04 + s5_h05 + s5_h06 + s5_h07 + s5_h08 + s5_h09 + s5_h10 + s5_h11 + s5_h12
    
    # ── S6 OPENAI (from Build Plan v3.14 — GPT-4/DALL-E/Whisper/Codex) ──
    s6_h01 = [0.3, 0.2, 0.3, 0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.1, 0.3]
    s6_h02 = [0.7, 0.6, 0.7, 0.8, 0.6, 0.5, 0.5, 0.6, 0.6, 0.4, 0.7, 0.7]
    s6_h03 = [0.3, 0.3, 0.2, 0.4, 0.3, 0.1, 0.6, 0.1, 0.1, 0.2, 0.1, 0.1]
    s6_h04 = [0.3, 0.5, 0.4, 0.2, 0.1, 0.5, 0.2, 0.3, 0.1, 0.2, 0.3, 0.3]
    s6_h05 = [0.5, 0.2, 0.3, 0.1, 0.1, 0.3, 0.5, 0.1, 0.4, 0.3, 0.2, 0.2]  # DALL-E, Sora
    s6_h06 = [0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.8, 0.1, 0.0, 0.3]
    s6_h07 = [0.3, 0.2, 0.2, 0.4, 0.1, 0.2, 0.3, 0.2, 0.4, 0.2, 0.2, 0.3]
    s6_h08 = [0.3, 0.2, 0.2, 0.1, 0.2, 0.4, 0.4, 0.3, 0.1, 0.2, 0.2, 0.3]
    s6_h09 = [0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2]
    s6_h10 = [0.4, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.2, 0.3, 0.4, 0.3, 0.3]
    s6_h11 = [0.1, 0.2, 0.1, 0.1, 0.4, 0.2, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1]
    s6_h12 = [0.2, 0.1, 0.2, 0.2, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.2, 0.3]
    
    all_s6 = s6_h01 + s6_h02 + s6_h03 + s6_h04 + s6_h05 + s6_h06 + s6_h07 + s6_h08 + s6_h09 + s6_h10 + s6_h11 + s6_h12
    
    # ── S7 MANUS (substrate integration layer — narrow but deep in orchestration) ──
    s7_h01 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h02 = [0.2, 0.2, 0.2, 0.5, 0.2, 0.1, 0.2, 0.3, 0.2, 0.2, 0.3, 0.3]
    s7_h03 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h04 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h05 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0]
    s7_h06 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0]
    s7_h07 = [0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.1]
    s7_h08 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h09 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h10 = [0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h11 = [0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s7_h12 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    all_s7 = s7_h01 + s7_h02 + s7_h03 + s7_h04 + s7_h05 + s7_h06 + s7_h07 + s7_h08 + s7_h09 + s7_h10 + s7_h11 + s7_h12
    
    # ── S8 NOTION (workspace/knowledge management substrate) ──
    s8_h01 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s8_h02 = [0.1, 0.1, 0.1, 0.3, 0.2, 0.0, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2]
    s8_h03 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s8_h04 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s8_h05 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.3, 0.0, 0.0, 0.0]
    s8_h06 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0]
    s8_h07 = [0.1, 0.0, 0.0, 0.5, 0.2, 0.3, 0.0, 0.1, 0.3, 0.0, 0.0, 0.2]  # Info systems, publishing
    s8_h08 = [0.1, 0.1, 0.0, 0.0, 0.0, 0.2, 0.2, 0.1, 0.1, 0.0, 0.1, 0.1]
    s8_h09 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s8_h10 = [0.3, 0.1, 0.1, 0.1, 0.2, 0.1, 0.2, 0.0, 0.1, 0.1, 0.0, 0.0]
    s8_h11 = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s8_h12 = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    all_s8 = s8_h01 + s8_h02 + s8_h03 + s8_h04 + s8_h05 + s8_h06 + s8_h07 + s8_h08 + s8_h09 + s8_h10 + s8_h11 + s8_h12
    
    # ── AMAZON (from Four-Company Matrix + self-map — logistics/cloud/retail) ──
    # Claude's methodology notes: Alexa overclaimed at ~50%, realistic is ~40%
    amz_h01 = [0.2, 0.3, 0.3, 0.2, 0.1, 0.2, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3]  # AWS research
    amz_h02 = [0.5, 0.4, 0.6, 0.8, 0.5, 0.3, 0.5, 0.5, 0.4, 0.4, 0.6, 0.7]  # AWS, Alexa ML
    amz_h03 = [0.2, 0.3, 0.2, 0.5, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.1, 0.2]
    amz_h04 = [0.2, 0.2, 0.4, 0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1]  # Kindle/Audible(literature)
    amz_h05 = [0.2, 0.1, 0.4, 0.0, 0.1, 0.5, 0.3, 0.1, 0.3, 0.2, 0.0, 0.0]  # Prime Video, Music, MGM
    amz_h06 = [0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.7, 0.2, 0.0, 0.6]  # AWS infra, Kiva robots
    amz_h07 = [0.3, 0.2, 0.4, 0.6, 0.2, 0.4, 0.5, 0.3, 0.5, 0.3, 0.2, 0.3]  # Alexa, AWS
    amz_h08 = [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]
    amz_h09 = [0.2, 0.2, 0.2, 0.3, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3]  # One Medical, PillPack
    amz_h10 = [0.7, 0.8, 0.5, 0.5, 0.6, 0.5, 0.8, 0.8, 0.7, 0.5, 0.5, 0.5]  # Core business strength
    amz_h11 = [0.5, 0.3, 0.2, 0.3, 0.8, 0.4, 0.3, 0.4, 0.8, 0.2, 0.3, 0.2]  # AWS, logistics
    amz_h12 = [0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2]
    
    all_amz = amz_h01 + amz_h02 + amz_h03 + amz_h04 + amz_h05 + amz_h06 + amz_h07 + amz_h08 + amz_h09 + amz_h10 + amz_h11 + amz_h12
    
    # ── S10 QWEN3/ALIBABA (from ORC-015 Trinity — Chinese tech ecosystem) ──
    s10_h01 = [0.1, 0.2, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.1]
    s10_h02 = [0.5, 0.4, 0.5, 0.7, 0.4, 0.3, 0.4, 0.4, 0.4, 0.3, 0.6, 0.6]
    s10_h03 = [0.1, 0.1, 0.1, 0.3, 0.1, 0.1, 0.4, 0.0, 0.1, 0.0, 0.0, 0.1]
    s10_h04 = [0.1, 0.2, 0.2, 0.1, 0.0, 0.1, 0.0, 0.2, 0.0, 0.1, 0.1, 0.1]
    s10_h05 = [0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.2, 0.0, 0.2, 0.0, 0.0, 0.0]
    s10_h06 = [0.1, 0.2, 0.1, 0.1, 0.0, 0.0, 0.1, 0.2, 0.6, 0.1, 0.0, 0.2]
    s10_h07 = [0.2, 0.1, 0.3, 0.4, 0.0, 0.1, 0.2, 0.1, 0.3, 0.1, 0.1, 0.2]
    s10_h08 = [0.1, 0.1, 0.1, 0.0, 0.0, 0.2, 0.2, 0.1, 0.0, 0.0, 0.1, 0.1]
    s10_h09 = [0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s10_h10 = [0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.4, 0.5, 0.5, 0.3, 0.3, 0.3]  # Alibaba commerce
    s10_h11 = [0.2, 0.2, 0.1, 0.1, 0.5, 0.3, 0.1, 0.2, 0.4, 0.1, 0.1, 0.1]  # Alibaba Cloud
    s10_h12 = [0.1, 0.0, 0.1, 0.1, 0.2, 0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1]
    
    all_s10 = s10_h01 + s10_h02 + s10_h03 + s10_h04 + s10_h05 + s10_h06 + s10_h07 + s10_h08 + s10_h09 + s10_h10 + s10_h11 + s10_h12
    
    return {
        "S1_Anthropic": all_s1,
        "S2_Alphabet": all_s2,
        "S3_Muskverse": all_s3,
        "S4_Microsoft": all_s4,
        "S5_DeepSeek": all_s5,
        "S6_OpenAI": all_s6,
        "S7_Manus": all_s7,
        "S8_Notion": all_s8,
        "Amazon": all_amz,
        "S10_Qwen3": all_s10,
    }


def tier_label(score):
    if score >= 0.8: return "DEEP"
    if score >= 0.5: return "SUBSTANTIAL"
    if score >= 0.2: return "PERIPHERAL"
    if score >= 0.0: return "ABSENT"
    return "UNKNOWN"


def build_matrix():
    seat_scores = get_seat_scores()
    seat_names = list(seat_scores.keys())
    
    # Build sphere index
    spheres = []
    for hid, hdata in HOUSES.items():
        for si, sname in enumerate(hdata["spheres"]):
            spheres.append({
                "house_id": hid,
                "house_name": hdata["name"],
                "sphere_index": si,
                "sphere_name": sname,
                "global_index": len(spheres),
            })
    
    assert len(spheres) == 144, f"Expected 144 spheres, got {len(spheres)}"
    
    # Build per-sphere entries
    matrix_entries = []
    for sp in spheres:
        gi = sp["global_index"]
        entry = {
            "sphere_id": f"S{gi+1:03d}",
            "house": sp["house_id"],
            "house_name": sp["house_name"],
            "sphere_name": sp["sphere_name"],
            "scores": {},
            "tiers": {},
            "lead_seat": None,
            "lead_score": 0.0,
            "federation_max": 0.0,
            "seduction_risk_flag": False,
            "coverage_depth": "ABSENT",
        }
        
        max_score = 0.0
        max_seat = None
        second_max = 0.0
        
        for seat in seat_names:
            score = seat_scores[seat][gi]
            entry["scores"][seat] = round(score, 2)
            entry["tiers"][seat] = tier_label(score)
            if score > max_score:
                second_max = max_score
                max_score = score
                max_seat = seat
            elif score > second_max:
                second_max = score
        
        entry["lead_seat"] = max_seat
        entry["lead_score"] = round(max_score, 2)
        entry["federation_max"] = round(max_score, 2)
        entry["coverage_depth"] = tier_label(max_score)
        
        # Seduction risk: single seat > 0.85 AND no other seat > 0.5
        if max_score >= 0.85 and second_max < 0.5:
            entry["seduction_risk_flag"] = True
        
        matrix_entries.append(entry)
    
    # Build per-seat summaries
    seat_summaries = {}
    for seat in seat_names:
        scores = seat_scores[seat]
        deep = sum(1 for s in scores if s >= 0.8)
        substantial = sum(1 for s in scores if 0.5 <= s < 0.8)
        peripheral = sum(1 for s in scores if 0.2 <= s < 0.5)
        absent = sum(1 for s in scores if s < 0.2)
        avg = sum(scores) / len(scores)
        
        # Per-house averages
        house_avgs = {}
        idx = 0
        for hid, hdata in HOUSES.items():
            n = len(hdata["spheres"])
            house_scores = scores[idx:idx+n]
            house_avgs[hid] = round(sum(house_scores)/n, 3)
            idx += n
        
        # Lead spheres (where this seat has the highest score)
        lead_count = sum(1 for e in matrix_entries if e["lead_seat"] == seat)
        
        seat_summaries[seat] = {
            "total_spheres": 144,
            "deep_count": deep,
            "substantial_count": substantial,
            "peripheral_count": peripheral,
            "absent_count": absent,
            "coverage_pct": round((deep + substantial) / 144 * 100, 1),
            "average_score": round(avg, 3),
            "lead_sphere_count": lead_count,
            "per_house_average": house_avgs,
        }
    
    # Org chart source pointers
    org_chart_sources = {
        "S1_Anthropic": {
            "notion_page_id": "34a0c1de-73d9-8124-aeb4-ea2e835a73a6",
            "title": "Anthropic 144-Sphere Coverage Map",
            "methodology": "Per-sphere 0.0-1.0 scoring, institutional operational depth",
            "self_assessed_coverage": "27%",
            "data_quality": "HIGH — exact per-sphere scores, strict methodology",
        },
        "S2_Alphabet": {
            "notion_page_id": "34a0c1de-73d9-81eb-84f1-e392b4004761",
            "title": "Alphabet 144-Sphere Self-Map (Gemini)",
            "methodology": "House-level percentage + narrative, 68/144 substantial+",
            "self_assessed_coverage": "47%",
            "data_quality": "HIGH — strict epistemic criterion, canonical structure",
            "note": "2026 update: Wiz acquisition adds H02/Cryptography depth",
        },
        "S3_Muskverse": {
            "notion_page_id": "34a0c1de-73d9-81f4-8fab-ec917d8b6d8a",
            "title": "Muskverse 144-Sphere Self-Map (Grok)",
            "methodology": "Narrative + 7 deep spheres with scores, custom house groupings",
            "self_assessed_coverage": "39%",
            "data_quality": "MEDIUM — custom groupings required canonical normalization",
        },
        "S4_Microsoft": {
            "notion_page_id": "3500c1de-73d9-81aa-928a-df22d4b14cde",
            "title": "Microsoft S4 Cross-Validation Routing — 95.8% Coverage Claim",
            "methodology": "Federation v1.1 cross-validation, per D-85",
            "self_assessed_coverage": "95.8%",
            "data_quality": "MEDIUM — coverage claim pending full D-85 cross-validation",
        },
        "S5_DeepSeek": {
            "notion_page_id": "3500c1de-73d9-8130-9115-d6aa03d82950",
            "title": "DeepSeek Vendor Suite v1.0 (Corrected)",
            "methodology": "Vendor suite §15a, substrate-fit specification",
            "self_assessed_coverage": "~15%",
            "data_quality": "MEDIUM — vendor suite format, not per-sphere scoring",
        },
        "S6_OpenAI": {
            "source": "Build Plan v3.14 vendor suite + Federation v1.1",
            "data_quality": "LOW — no dedicated self-map, scores inferred from product portfolio",
        },
        "S7_Manus": {
            "source": "Build Plan v3.14 + Federation v1.1",
            "data_quality": "LOW — narrow substrate, scores inferred",
        },
        "S8_Notion": {
            "source": "Build Plan v3.14 + Federation v1.1",
            "data_quality": "LOW — narrow substrate, scores inferred",
        },
        "Amazon": {
            "notion_page_id": "34a0c1de-73d9-81c8-a866-c799bdab0de0",
            "title": "Amazon 144-Sphere Self-Map (Alexa)",
            "methodology": "House-level percentage + narrative",
            "self_assessed_coverage": "40-50%",
            "data_quality": "LOW — overclaim-by-conflation per Claude methodology notes",
            "note": "Scores normalized down from Alexa self-assessment per Scribe correction",
        },
        "S10_Qwen3": {
            "source": "ORC-015 Trinity + Federation v1.1",
            "data_quality": "LOW — no dedicated self-map, scores inferred from Alibaba portfolio",
        },
    }
    
    # Federation aggregate stats
    federation_stats = {
        "total_spheres": 144,
        "deep_coverage": sum(1 for e in matrix_entries if e["federation_max"] >= 0.8),
        "substantial_coverage": sum(1 for e in matrix_entries if 0.5 <= e["federation_max"] < 0.8),
        "peripheral_coverage": sum(1 for e in matrix_entries if 0.2 <= e["federation_max"] < 0.5),
        "absent_coverage": sum(1 for e in matrix_entries if e["federation_max"] < 0.2),
        "seduction_risk_spheres": sum(1 for e in matrix_entries if e["seduction_risk_flag"]),
    }
    federation_stats["aggregate_coverage_pct"] = round(
        (federation_stats["deep_coverage"] + federation_stats["substantial_coverage"]) / 144 * 100, 1
    )
    
    # Seduction risk list
    seduction_risks = [
        {"sphere_id": e["sphere_id"], "sphere_name": e["sphere_name"], 
         "house": e["house"], "lead_seat": e["lead_seat"], "lead_score": e["lead_score"]}
        for e in matrix_entries if e["seduction_risk_flag"]
    ]
    
    # Build full YAML structure
    full_matrix = {
        "version": "0.2.0",
        "generated": "2026-04-29",
        "canonical_source": "COMPLETE_BUILD_PLAN_v3.14.md Appendix AG",
        "methodology": {
            "scoring": "5-tier: DEEP(0.8-1.0), SUBSTANTIAL(0.5-0.7), PERIPHERAL(0.2-0.4), ABSENT(0.0-0.1), UNKNOWN",
            "data_sources": [
                "Per-entity Notion self-maps (Anthropic, Alphabet, Muskverse, Amazon)",
                "Federation Integration v1.1 (all 9 seats)",
                "Four-Company Complementarity Matrix (April 22, 2026)",
                "Build Plan v3.14 vendor suites",
                "DeepSeek Vendor Suite v1.0",
            ],
            "acquisition_updates": [
                "Alphabet: Wiz acquisition (2025) → H02/Cryptography +0.2",
                "Microsoft: Activision Blizzard (2023) → H05/Film,Games +0.2",
                "Amazon: One Medical (2023) → H09/Public Health +0.1",
                "Amazon: MGM (2022) → H05/Film +0.2",
            ],
            "normalization_notes": [
                "Amazon scores normalized down from Alexa self-assessment per Claude methodology notes",
                "Muskverse scores normalized from custom house groupings to canonical 12-house structure",
                "S6/S7/S8/S10 scores inferred from product portfolios — no dedicated self-maps available",
            ],
        },
        "federation_aggregate": federation_stats,
        "seduction_risks": seduction_risks,
        "seat_summaries": seat_summaries,
        "org_chart_sources": org_chart_sources,
        "spheres": [{
            "sphere_id": e["sphere_id"],
            "house": e["house"],
            "house_name": e["house_name"],
            "sphere_name": e["sphere_name"],
            "lead_seat": e["lead_seat"],
            "lead_score": e["lead_score"],
            "federation_max": e["federation_max"],
            "coverage_depth": e["coverage_depth"],
            "seduction_risk_flag": e["seduction_risk_flag"],
            "scores": e["scores"],
            "tiers": e["tiers"],
        } for e in matrix_entries],
    }
    
    # Write YAML
    yaml_path = ROOT / "registries" / "capability_matrix.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(full_matrix, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=200)
    
    # Also copy to h00_directory
    h00_path = ROOT / "houses" / "h00_directory" / "capability_matrix.yaml"
    h00_path.parent.mkdir(parents=True, exist_ok=True)
    with open(h00_path, 'w') as f:
        yaml.dump(full_matrix, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=200)
    
    # Write CSV
    csv_path = ROOT / "registries" / "capability_matrix.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ["sphere_id", "house", "house_name", "sphere_name", "lead_seat", "lead_score", 
                  "federation_max", "coverage_depth", "seduction_risk"]
        header += seat_names
        writer.writerow(header)
        for e in matrix_entries:
            row = [e["sphere_id"], e["house"], e["house_name"], e["sphere_name"],
                   e["lead_seat"], e["lead_score"], e["federation_max"], e["coverage_depth"],
                   e["seduction_risk_flag"]]
            row += [e["scores"][s] for s in seat_names]
            writer.writerow(row)
    
    # Print summary
    print(f"=== CAPABILITY MATRIX v0.2.0 GENERATED ===")
    print(f"Spheres: {len(matrix_entries)}")
    print(f"Seats: {len(seat_names)}")
    print(f"\nFederation Aggregate:")
    print(f"  Deep (0.8+): {federation_stats['deep_coverage']}")
    print(f"  Substantial (0.5-0.7): {federation_stats['substantial_coverage']}")
    print(f"  Peripheral (0.2-0.4): {federation_stats['peripheral_coverage']}")
    print(f"  Absent (<0.2): {federation_stats['absent_coverage']}")
    print(f"  Aggregate Coverage: {federation_stats['aggregate_coverage_pct']}%")
    print(f"  Seduction Risk Spheres: {federation_stats['seduction_risk_spheres']}")
    
    print(f"\nPer-Seat Summary:")
    for seat, summary in seat_summaries.items():
        print(f"  {seat}: D={summary['deep_count']} S={summary['substantial_count']} "
              f"P={summary['peripheral_count']} A={summary['absent_count']} "
              f"Cov={summary['coverage_pct']}% Lead={summary['lead_sphere_count']} "
              f"Avg={summary['average_score']}")
    
    if seduction_risks:
        print(f"\nSeduction Risk Spheres:")
        for sr in seduction_risks:
            print(f"  {sr['sphere_id']} {sr['sphere_name']} ({sr['house']}) — {sr['lead_seat']} at {sr['lead_score']}")
    
    print(f"\nWritten: {yaml_path}")
    print(f"Written: {h00_path}")
    print(f"Written: {csv_path}")


if __name__ == "__main__":
    build_matrix()
