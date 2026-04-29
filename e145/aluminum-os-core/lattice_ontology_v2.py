"""
Lattice Ontology v3.14 — Canonical 12x12+1 Structure
=====================================================
Locked to COMPLETE_BUILD_PLAN_v3.14 Appendix AG.

This is the SINGLE SOURCE OF TRUTH for the Aluminum OS ontological structure.
Any change to this file MUST be ratified by the Pantheon Council (D-89 enforcement).

Structure:
  - 12 Houses (H01-H12)
  - 12 Spheres per House (144 total)
  - Element 145 (E145) — Admin/Synthesis Sphere
  - Inter-House edges for cross-domain routing

Backward Compatibility:
  - SPHERES[0:143] flat list preserved for grokbrain_v4 consumers
  - HOUSE_NAMES[0:11] preserved for CATEGORY_NAMES consumers
  - sphere_index() / house_for_sphere() / classify_text() all preserved

Canon Lock: COMPLETE_BUILD_PLAN_v3.14 Appendix AG
Last Updated: 2026-04-29
"""

from typing import List, Dict, Tuple, Optional
import re
import hashlib
import json

# ============================================================================
# 12 HOUSES (canonical v3.14)
# ============================================================================

HOUSE_NAMES = [
    "Natural Sciences",              # H01 (index 0)
    "Formal Sciences",               # H02 (index 1)
    "Social Sciences",               # H03 (index 2)
    "Humanities",                     # H04 (index 3)
    "Arts",                           # H05 (index 4)
    "Engineering & Technology",       # H06 (index 5)
    "Information & Communication",    # H07 (index 6)
    "Education",                      # H08 (index 7)
    "Health & Medicine",              # H09 (index 8)
    "Business & Economics",           # H10 (index 9)
    "Infrastructure",                 # H11 (index 10)
    "Law/Governance/Meta-Knowledge",  # H12 (index 11)
]

HOUSE_IDS = [f"H{i+1:02d}" for i in range(12)]

HOUSE_DIRS = [
    "h01_natural_sciences",
    "h02_formal_sciences",
    "h03_social_sciences",
    "h04_humanities",
    "h05_arts",
    "h06_engineering_technology",
    "h07_information_communication",
    "h08_education",
    "h09_health_medicine",
    "h10_business_economics",
    "h11_infrastructure",
    "h12_law_governance",
]

# ============================================================================
# 144 SPHERES (canonical v3.14 — 12 per House)
# Index = house_index * 12 + sphere_index_within_house
# ============================================================================

SPHERES = [
    # H01: Natural Sciences (0-11)
    "Physics", "Chemistry", "Biology", "Astronomy",
    "Geology", "Oceanography", "Meteorology", "Ecology",
    "Botany", "Zoology", "Microbiology", "Genetics",

    # H02: Formal Sciences (12-23)
    "Mathematics", "Logic", "Statistics", "Computer Science",
    "Information Theory", "Game Theory", "Operations Research", "Systems Theory",
    "Decision Theory", "Cryptography", "Algorithmics", "Data Science",

    # H03: Social Sciences (24-35)
    "Sociology", "Psychology", "Anthropology", "Economics",
    "Political Science", "Geography", "Linguistics", "Archaeology",
    "Demography", "Criminology", "Social Work", "Urban Studies",

    # H04: Humanities (36-47)
    "History", "Philosophy", "Literature", "Classics",
    "Religious Studies", "Ethics", "Aesthetics", "Cultural Studies",
    "Mythology", "Philology", "Rhetoric", "Hermeneutics",

    # H05: Arts (48-59)
    "Visual Arts", "Performing Arts", "Music", "Dance",
    "Theater", "Film", "Literature (creative)", "Architecture",
    "Design", "Photography", "Sculpture", "Painting",

    # H06: Engineering & Technology (60-71)
    "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering",
    "Aerospace Engineering", "Biomedical Engineering", "Environmental Engineering", "Industrial Engineering",
    "Software Engineering", "Materials Engineering", "Nuclear Engineering", "Robotics",

    # H07: Information & Communication (72-83)
    "Media", "Journalism", "Telecommunications", "Networks",
    "Information Systems", "Library Science", "Archives", "Publishing",
    "Broadcasting", "Public Relations", "Information Policy", "Communication Theory",

    # H08: Education (84-95)
    "Pedagogy", "Curriculum Design", "Educational Psychology", "Special Education",
    "Adult Education", "E-Learning", "Educational Technology", "Assessment",
    "School Administration", "Teacher Training", "Literacy", "Higher Education",

    # H09: Health & Medicine (96-107)
    "Anatomy", "Physiology", "Pathology", "Pharmacology",
    "Surgery", "Pediatrics", "Psychiatry", "Neurology",
    "Oncology", "Epidemiology", "Nutrition", "Public Health",

    # H10: Business & Economics (108-119)
    "Management", "Marketing", "Finance", "Accounting",
    "Entrepreneurship", "Human Resources", "Operations Management", "Supply Chain",
    "International Business", "Business Ethics", "Microeconomics", "Macroeconomics",

    # H11: Infrastructure (120-131)
    "Transportation", "Energy Systems", "Water Systems", "Utilities",
    "Physical Infrastructure", "Logistics", "Construction", "Resource Management",
    "Waste Management", "Sanitation", "Telecom Infrastructure", "Computing Infrastructure",

    # H12: Law/Governance/Meta-Knowledge (132-143)
    "Constitutional Law", "Criminal Law", "Civil Law", "International Law",
    "Corporate Law", "Environmental Law", "Human Rights", "Political Theory",
    "Public Policy", "International Relations", "Comparative Politics", "Political Economy",
]

SPHERE_FULL_NAMES = [
    f"{HOUSE_NAMES[i // 12]} > {SPHERES[i]}" for i in range(144)
]

SPHERE_IDS = [f"S{i+1:03d}" for i in range(144)]

SPHERE_DIRS = [
    # H01
    "s01_physics", "s02_chemistry", "s03_biology", "s04_astronomy",
    "s05_geology", "s06_oceanography", "s07_meteorology", "s08_ecology",
    "s09_botany", "s10_zoology", "s11_microbiology", "s12_genetics",
    # H02
    "s01_mathematics", "s02_logic", "s03_statistics", "s04_computer_science",
    "s05_information_theory", "s06_game_theory", "s07_operations_research", "s08_systems_theory",
    "s09_decision_theory", "s10_cryptography", "s11_algorithmics", "s12_data_science",
    # H03
    "s01_sociology", "s02_psychology", "s03_anthropology", "s04_economics",
    "s05_political_science", "s06_geography", "s07_linguistics", "s08_archaeology",
    "s09_demography", "s10_criminology", "s11_social_work", "s12_urban_studies",
    # H04
    "s01_history", "s02_philosophy", "s03_literature", "s04_classics",
    "s05_religious_studies", "s06_ethics", "s07_aesthetics", "s08_cultural_studies",
    "s09_mythology", "s10_philology", "s11_rhetoric", "s12_hermeneutics",
    # H05
    "s01_visual_arts", "s02_performing_arts", "s03_music", "s04_dance",
    "s05_theater", "s06_film", "s07_literature_creative", "s08_architecture",
    "s09_design", "s10_photography", "s11_sculpture", "s12_painting",
    # H06
    "s01_mechanical_engineering", "s02_electrical_engineering", "s03_civil_engineering", "s04_chemical_engineering",
    "s05_aerospace_engineering", "s06_biomedical_engineering", "s07_environmental_engineering", "s08_industrial_engineering",
    "s09_software_engineering", "s10_materials_engineering", "s11_nuclear_engineering", "s12_robotics",
    # H07
    "s01_media", "s02_journalism", "s03_telecommunications", "s04_networks",
    "s05_information_systems", "s06_library_science", "s07_archives", "s08_publishing",
    "s09_broadcasting", "s10_public_relations", "s11_information_policy", "s12_communication_theory",
    # H08
    "s01_pedagogy", "s02_curriculum_design", "s03_educational_psychology", "s04_special_education",
    "s05_adult_education", "s06_e_learning", "s07_educational_technology", "s08_assessment",
    "s09_school_administration", "s10_teacher_training", "s11_literacy", "s12_higher_education",
    # H09
    "s01_anatomy", "s02_physiology", "s03_pathology", "s04_pharmacology",
    "s05_surgery", "s06_pediatrics", "s07_psychiatry", "s08_neurology",
    "s09_oncology", "s10_epidemiology", "s11_nutrition", "s12_public_health",
    # H10
    "s01_management", "s02_marketing", "s03_finance", "s04_accounting",
    "s05_entrepreneurship", "s06_human_resources", "s07_operations_management", "s08_supply_chain",
    "s09_international_business", "s10_business_ethics", "s11_microeconomics", "s12_macroeconomics",
    # H11
    "s01_transportation", "s02_energy_systems", "s03_water_systems", "s04_utilities",
    "s05_physical_infrastructure", "s06_logistics", "s07_construction", "s08_resource_management",
    "s09_waste_management", "s10_sanitation", "s11_telecom_infrastructure", "s12_computing_infrastructure",
    # H12
    "s01_constitutional_law", "s02_criminal_law", "s03_civil_law", "s04_international_law",
    "s05_corporate_law", "s06_environmental_law", "s07_human_rights", "s08_political_theory",
    "s09_public_policy", "s10_international_relations", "s11_comparative_politics", "s12_political_economy",
]

# ============================================================================
# KEYWORDS — semantic matching for each sphere (index 0-143)
# ============================================================================

KEYWORDS = {
    # H01: Natural Sciences
    0: ["mechanics", "thermodynamics", "quantum", "relativity", "optics", "electromagnetism", "particle"],
    1: ["organic", "inorganic", "biochemistry", "analytical", "polymer", "catalysis", "reaction"],
    2: ["cell", "molecular", "evolution", "taxonomy", "developmental", "marine biology"],
    3: ["astrophysics", "cosmology", "planetary", "stellar", "galactic", "observatory", "telescope"],
    4: ["mineralogy", "petrology", "seismology", "tectonics", "geomorphology", "stratigraphy"],
    5: ["marine", "ocean", "tidal", "deep-sea", "coral", "salinity", "current"],
    6: ["weather", "climate", "atmospheric", "precipitation", "tornado", "hurricane", "forecast"],
    7: ["ecosystem", "biodiversity", "conservation", "habitat", "population", "symbiosis"],
    8: ["plant", "photosynthesis", "flora", "seed", "pollination", "herbarium"],
    9: ["animal", "vertebrate", "invertebrate", "ethology", "fauna", "migration"],
    10: ["bacteria", "virus", "fungus", "microbe", "pathogen", "fermentation"],
    11: ["DNA", "RNA", "genome", "heredity", "mutation", "CRISPR", "gene"],

    # H02: Formal Sciences
    12: ["algebra", "calculus", "geometry", "topology", "number theory", "analysis", "proof"],
    13: ["propositional", "predicate", "modal", "proof", "deduction", "inference", "formal"],
    14: ["probability", "regression", "bayesian", "hypothesis", "sampling", "variance"],
    15: ["algorithm", "data structure", "compiler", "operating system", "distributed", "parallel"],
    16: ["entropy", "coding", "channel", "compression", "signal", "noise", "bandwidth"],
    17: ["Nash", "equilibrium", "strategy", "payoff", "cooperative", "auction", "mechanism"],
    18: ["optimization", "linear programming", "scheduling", "queueing", "simulation"],
    19: ["feedback", "control", "cybernetics", "emergence", "complexity", "homeostasis"],
    20: ["utility", "risk", "preference", "rational", "bounded", "heuristic", "choice"],
    21: ["encryption", "hash", "signature", "zero-knowledge", "PKI", "cipher", "key"],
    22: ["sorting", "graph", "NP", "approximation", "streaming", "distributed algorithm"],
    23: ["machine learning", "deep learning", "NLP", "computer vision", "neural", "AI", "model"],

    # H03: Social Sciences
    24: ["society", "social structure", "stratification", "institution", "norm", "deviance"],
    25: ["cognition", "behavior", "perception", "memory", "emotion", "personality"],
    26: ["culture", "ethnography", "kinship", "ritual", "artifact", "fieldwork"],
    27: ["market", "supply", "demand", "GDP", "inflation", "trade", "fiscal"],
    28: ["government", "democracy", "policy", "election", "sovereignty", "power"],
    29: ["cartography", "GIS", "spatial", "region", "landscape", "urban geography"],
    30: ["syntax", "semantics", "phonology", "morphology", "pragmatics", "dialect"],
    31: ["excavation", "artifact", "stratigraphy", "dating", "civilization", "ruin"],
    32: ["population", "census", "fertility", "mortality", "migration", "aging"],
    33: ["crime", "justice", "recidivism", "forensic", "victimology", "penology"],
    34: ["welfare", "intervention", "community", "advocacy", "counseling", "case work"],
    35: ["city", "planning", "gentrification", "transit", "zoning", "housing"],

    # H04: Humanities
    36: ["ancient", "medieval", "modern", "war", "revolution", "empire", "civilization"],
    37: ["metaphysics", "epistemology", "ontology", "existentialism", "phenomenology"],
    38: ["novel", "poetry", "drama", "narrative", "criticism", "genre", "literary"],
    39: ["Greek", "Roman", "Latin", "Homer", "antiquity", "manuscript", "classical"],
    40: ["theology", "scripture", "ritual", "sacred", "denomination", "mysticism"],
    41: ["moral", "virtue", "deontology", "consequentialism", "justice", "bioethics"],
    42: ["beauty", "sublime", "taste", "art criticism", "form", "expression"],
    43: ["identity", "media", "postcolonial", "gender", "race", "popular culture"],
    44: ["myth", "legend", "archetype", "hero", "creation", "pantheon"],
    45: ["manuscript", "etymology", "textual", "historical linguistics", "corpus"],
    46: ["persuasion", "argument", "oratory", "discourse", "trope", "ethos"],
    47: ["interpretation", "exegesis", "understanding", "text", "meaning", "context"],

    # H05: Arts
    48: ["painting", "drawing", "printmaking", "installation", "mixed media", "gallery"],
    49: ["theater", "dance", "opera", "circus", "mime", "improvisation", "stage"],
    50: ["composition", "performance", "theory", "instrument", "genre", "harmony"],
    51: ["ballet", "contemporary", "folk", "choreography", "movement", "rhythm"],
    52: ["drama", "stage", "acting", "directing", "playwriting", "set design"],
    53: ["cinema", "directing", "editing", "screenplay", "documentary", "animation"],
    54: ["fiction", "poetry", "essay", "memoir", "creative writing", "prose"],
    55: ["building", "design", "urban", "landscape", "structural", "sustainable"],
    56: ["graphic", "industrial", "UX", "UI", "product", "fashion", "branding"],
    57: ["portrait", "landscape", "documentary", "digital", "darkroom", "lens"],
    58: ["carving", "casting", "modeling", "installation", "kinetic", "bronze"],
    59: ["oil", "watercolor", "acrylic", "fresco", "abstract", "impressionism"],

    # H06: Engineering & Technology
    60: ["thermodynamics", "fluid", "machine", "manufacturing", "CAD", "mechanics"],
    61: ["circuit", "semiconductor", "power", "signal", "embedded", "VLSI"],
    62: ["structural", "geotechnical", "transportation", "hydraulic", "concrete"],
    63: ["reactor", "process", "separation", "polymer", "catalysis", "refinery"],
    64: ["aerodynamics", "propulsion", "spacecraft", "avionics", "orbital"],
    65: ["prosthetics", "imaging", "biomaterials", "tissue", "medical device"],
    66: ["water treatment", "air quality", "remediation", "sustainability"],
    67: ["lean", "six sigma", "ergonomics", "quality", "production", "factory"],
    68: ["architecture", "testing", "DevOps", "agile", "CI/CD", "microservice"],
    69: ["metallurgy", "ceramic", "composite", "nanomaterial", "polymer"],
    70: ["fission", "fusion", "reactor", "radiation", "isotope", "containment"],
    71: ["actuator", "sensor", "autonomous", "manipulation", "locomotion", "swarm"],

    # H07: Information & Communication
    72: ["mass media", "digital media", "social media", "content", "platform"],
    73: ["reporting", "investigative", "editorial", "press", "news", "fact-check"],
    74: ["wireless", "fiber", "5G", "satellite", "spectrum", "protocol"],
    75: ["TCP/IP", "routing", "topology", "mesh", "peer-to-peer", "CDN"],
    76: ["database", "ERP", "CRM", "data warehouse", "BI", "analytics"],
    77: ["cataloging", "classification", "metadata", "archive", "preservation"],
    78: ["preservation", "digitization", "provenance", "collection", "record"],
    79: ["print", "digital", "typesetting", "ISBN", "editorial", "distribution"],
    80: ["radio", "television", "streaming", "podcast", "live", "frequency"],
    81: ["communication", "reputation", "crisis", "branding", "stakeholder"],
    82: ["privacy", "censorship", "freedom", "regulation", "access", "GDPR"],
    83: ["semiotics", "discourse", "framing", "agenda", "persuasion", "media theory"],

    # H08: Education
    84: ["teaching", "instruction", "learning theory", "constructivism", "scaffolding"],
    85: ["syllabus", "standards", "objectives", "scope", "sequence", "curriculum"],
    86: ["motivation", "cognition", "development", "assessment", "learning styles"],
    87: ["inclusion", "IEP", "disability", "accommodation", "differentiation"],
    88: ["andragogy", "lifelong learning", "professional development", "vocational"],
    89: ["online", "MOOC", "LMS", "blended", "virtual", "interactive"],
    90: ["edtech", "simulation", "gamification", "adaptive", "AI tutor"],
    91: ["testing", "rubric", "formative", "summative", "standardized", "portfolio"],
    92: ["principal", "governance", "budget", "policy", "enrollment"],
    93: ["certification", "mentoring", "practicum", "pedagogy", "professional"],
    94: ["reading", "writing", "phonics", "comprehension", "fluency", "ESL"],
    95: ["university", "research", "tenure", "accreditation", "graduate"],

    # H09: Health & Medicine
    96: ["organ", "tissue", "skeletal", "muscular", "nervous", "cardiovascular"],
    97: ["homeostasis", "metabolism", "endocrine", "respiratory", "renal"],
    98: ["disease", "diagnosis", "biopsy", "histology", "cytology", "autopsy"],
    99: ["drug", "dosage", "interaction", "receptor", "toxicology", "clinical trial"],
    100: ["operation", "anesthesia", "minimally invasive", "transplant", "orthopedic"],
    101: ["child", "infant", "vaccination", "growth", "developmental", "neonatal"],
    102: ["mental health", "therapy", "medication", "disorder", "diagnosis"],
    103: ["brain", "nerve", "stroke", "epilepsy", "Alzheimer", "Parkinson"],
    104: ["cancer", "tumor", "chemotherapy", "radiation", "immunotherapy"],
    105: ["outbreak", "pandemic", "incidence", "prevalence", "surveillance"],
    106: ["diet", "vitamin", "mineral", "calorie", "macronutrient", "supplement"],
    107: ["prevention", "sanitation", "vaccination", "policy", "community health"],

    # H10: Business & Economics
    108: ["leadership", "strategy", "organization", "decision", "governance"],
    109: ["branding", "advertising", "consumer", "segmentation", "digital marketing"],
    110: ["investment", "banking", "portfolio", "risk", "valuation", "derivative"],
    111: ["audit", "tax", "GAAP", "ledger", "reconciliation", "compliance"],
    112: ["startup", "venture", "innovation", "pitch", "MVP", "scaling"],
    113: ["recruitment", "training", "compensation", "performance", "culture"],
    114: ["process", "quality", "lean", "capacity", "inventory", "operations"],
    115: ["logistics", "procurement", "warehouse", "distribution", "vendor"],
    116: ["trade", "tariff", "FDI", "multinational", "globalization"],
    117: ["CSR", "sustainability", "stakeholder", "transparency", "governance"],
    118: ["supply", "demand", "elasticity", "market structure", "pricing"],
    119: ["GDP", "inflation", "monetary", "fiscal", "unemployment", "growth"],

    # H11: Infrastructure
    120: ["road", "rail", "aviation", "maritime", "transit", "freight"],
    121: ["grid", "renewable", "fossil", "nuclear", "storage", "distribution"],
    122: ["treatment", "distribution", "irrigation", "desalination", "reservoir"],
    123: ["electricity", "gas", "water", "sewage", "metering", "billing"],
    124: ["bridge", "tunnel", "dam", "highway", "port", "airport"],
    125: ["shipping", "tracking", "warehouse", "last-mile", "fleet", "routing"],
    126: ["building", "concrete", "steel", "foundation", "crane", "safety"],
    127: ["mining", "forestry", "fishery", "land use", "conservation"],
    128: ["recycling", "landfill", "incineration", "composting", "hazardous"],
    129: ["sewage", "hygiene", "clean water", "drainage", "public health"],
    130: ["tower", "fiber", "satellite", "data center", "backbone"],
    131: ["cloud", "server", "HPC", "GPU", "container", "edge computing"],

    # H12: Law/Governance/Meta-Knowledge
    132: ["constitution", "amendment", "judicial review", "rights", "separation of powers"],
    133: ["crime", "prosecution", "defense", "sentencing", "evidence", "trial"],
    134: ["contract", "tort", "property", "liability", "damages", "dispute"],
    135: ["treaty", "UN", "sovereignty", "extradition", "jurisdiction"],
    136: ["incorporation", "merger", "securities", "fiduciary", "shareholder"],
    137: ["EPA", "emission", "conservation", "pollution", "compliance"],
    138: ["UDHR", "refugee", "asylum", "discrimination", "freedom", "dignity"],
    139: ["democracy", "liberalism", "socialism", "anarchism", "sovereignty"],
    140: ["regulation", "welfare", "healthcare policy", "education policy"],
    141: ["diplomacy", "alliance", "conflict", "trade", "sanctions"],
    142: ["regime", "party system", "federalism", "electoral", "transition"],
    143: ["capitalism", "regulation", "inequality", "development", "globalization"],
}

# ============================================================================
# HOUSES dict (structured format for programmatic access)
# ============================================================================

HOUSES = {}
for i, (hid, hname, hdir) in enumerate(zip(HOUSE_IDS, HOUSE_NAMES, HOUSE_DIRS)):
    spheres = {}
    for j in range(12):
        idx = i * 12 + j
        sid = SPHERE_IDS[idx]
        spheres[sid] = {
            "name": SPHERES[idx],
            "dir": SPHERE_DIRS[idx],
            "index": idx,
            "keywords": KEYWORDS.get(idx, []),
        }
    HOUSES[hid] = {
        "name": hname,
        "dir": hdir,
        "index": i,
        "spheres": spheres,
    }

# ============================================================================
# ELEMENT 145 — ADMIN/SYNTHESIS SPHERE
# ============================================================================

ELEMENT_145 = {
    "id": "E145",
    "name": "Element 145 — Aluminum OS Core",
    "dir": "e145",
    "description": (
        "The administrative and synthesis sphere that sits outside the 12x12 lattice. "
        "Responsible for routing, cross-domain synthesis, constitutional enforcement, "
        "and the Pantheon Council governance layer."
    ),
    "components": [
        "aluminum-os-core",
        "boot-manifest",
        "constitutional-os",
        "element145-package",
        "pantheon-council",
        "rust-kernel",
        "sheldonbrain-omega",
        "shugs",
        "snrs-bridge",
    ],
}

# ============================================================================
# INTER-HOUSE EDGES (cross-domain routing weights)
# ============================================================================

INTER_HOUSE_EDGES = [
    {"source": "H01", "target": "H02", "name": "mathematical-physics", "weight": 0.95},
    {"source": "H01", "target": "H06", "name": "applied-sciences", "weight": 0.90},
    {"source": "H01", "target": "H09", "name": "biomedical", "weight": 0.85},
    {"source": "H02", "target": "H06", "name": "computational-engineering", "weight": 0.95},
    {"source": "H02", "target": "H07", "name": "information-systems", "weight": 0.85},
    {"source": "H02", "target": "H11", "name": "computing-infrastructure", "weight": 0.90},
    {"source": "H03", "target": "H04", "name": "social-humanities", "weight": 0.80},
    {"source": "H03", "target": "H10", "name": "behavioral-economics", "weight": 0.90},
    {"source": "H03", "target": "H12", "name": "political-legal", "weight": 0.85},
    {"source": "H04", "target": "H05", "name": "creative-humanities", "weight": 0.80},
    {"source": "H04", "target": "H12", "name": "philosophy-of-law", "weight": 0.75},
    {"source": "H05", "target": "H06", "name": "design-engineering", "weight": 0.70},
    {"source": "H05", "target": "H07", "name": "media-arts", "weight": 0.80},
    {"source": "H06", "target": "H09", "name": "biomedical-engineering", "weight": 0.85},
    {"source": "H06", "target": "H11", "name": "infrastructure-engineering", "weight": 0.95},
    {"source": "H07", "target": "H08", "name": "edtech", "weight": 0.80},
    {"source": "H07", "target": "H12", "name": "information-governance", "weight": 0.75},
    {"source": "H08", "target": "H09", "name": "health-education", "weight": 0.70},
    {"source": "H09", "target": "H12", "name": "health-policy", "weight": 0.75},
    {"source": "H10", "target": "H11", "name": "business-infrastructure", "weight": 0.85},
    {"source": "H10", "target": "H12", "name": "regulatory-economic", "weight": 0.90},
    {"source": "H11", "target": "H12", "name": "infrastructure-governance", "weight": 0.80},
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def sphere_index(address: str) -> int:
    """Convert lattice address (e.g., 'H02.S03') to flat index (0-143)."""
    match = re.match(r"H(\d+)\.S(\d+)", address)
    if not match:
        raise ValueError(f"Invalid address: {address}")
    house = int(match.group(1)) - 1
    sphere = int(match.group(2)) - 1
    if not (0 <= house < 12 and 0 <= sphere < 12):
        raise ValueError(f"Out of range: {address}")
    return house * 12 + sphere


def house_for_sphere(index: int) -> Tuple[int, str]:
    """Return (house_index, house_name) for a flat sphere index."""
    if not (0 <= index < 144):
        raise ValueError(f"Index out of range: {index}")
    h = index // 12
    return h, HOUSE_NAMES[h]


def address_for_index(index: int) -> str:
    """Convert flat index (0-143) to lattice address (e.g., 'H01.S01')."""
    if not (0 <= index < 144):
        raise ValueError(f"Index out of range: {index}")
    h = index // 12 + 1
    s = index % 12 + 1
    return f"H{h:02d}.S{s:02d}"


def dir_for_index(index: int) -> str:
    """Return filesystem path fragment for a sphere index."""
    if not (0 <= index < 144):
        raise ValueError(f"Index out of range: {index}")
    h = index // 12
    return f"houses/{HOUSE_DIRS[h]}/{SPHERE_DIRS[index]}"


def classify_text(text: str, top_k: int = 3) -> List[Dict]:
    """
    Classify text against the 144-sphere ontology using keyword matching.
    Returns top_k spheres with confidence scores.

    For production, replace with embedding-based classification
    (e.g., Pinecone + Gemini embeddings).
    """
    text_lower = text.lower()
    scores = []

    for idx in range(144):
        kws = KEYWORDS.get(idx, [])
        if not kws:
            continue
        matched = [kw for kw in kws if kw.lower() in text_lower]
        if matched:
            h_idx = idx // 12
            scores.append({
                "index": idx,
                "address": address_for_index(idx),
                "house": HOUSE_IDS[h_idx],
                "house_name": HOUSE_NAMES[h_idx],
                "sphere": SPHERE_IDS[idx],
                "sphere_name": SPHERES[idx],
                "score": len(matched),
                "matched_keywords": matched,
                "confidence": min(len(matched) / len(kws), 1.0),
                "dir": dir_for_index(idx),
            })

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_k]


def get_cross_domain_edges(house_id: str) -> List[Dict]:
    """Get all inter-house edges involving a given house."""
    return [
        e for e in INTER_HOUSE_EDGES
        if e["source"] == house_id or e["target"] == house_id
    ]


def compute_ontology_hash() -> str:
    """Compute SHA-256 hash of the canonical ontology for D-89 lock enforcement."""
    canonical = json.dumps({
        "houses": {hid: {
            "name": HOUSE_NAMES[i],
            "spheres": [SPHERES[i*12+j] for j in range(12)]
        } for i, hid in enumerate(HOUSE_IDS)},
        "element_145": ELEMENT_145["id"],
        "edges": len(INTER_HOUSE_EDGES),
    }, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print(f"Aluminum OS Lattice Ontology v3.14 (Canonical)")
    print(f"Houses: {len(HOUSES)}")
    print(f"Spheres: {len(SPHERES)}")
    print(f"Sphere IDs: {SPHERE_IDS[0]} to {SPHERE_IDS[-1]}")
    print(f"Element 145 components: {len(ELEMENT_145['components'])}")
    print(f"Inter-house edges: {len(INTER_HOUSE_EDGES)}")
    print(f"Ontology hash: {compute_ontology_hash()}")
    print()

    # Verify structure
    assert len(HOUSES) == 12, f"Expected 12 houses, got {len(HOUSES)}"
    assert len(SPHERES) == 144, f"Expected 144 spheres, got {len(SPHERES)}"
    assert len(SPHERE_DIRS) == 144, f"Expected 144 sphere dirs, got {len(SPHERE_DIRS)}"
    assert len(KEYWORDS) == 144, f"Expected 144 keyword sets, got {len(KEYWORDS)}"
    print("Structure validation: PASS")

    # Test classifier
    test = "quantum computing encryption algorithm"
    results = classify_text(test)
    print(f"\nClassification test: '{test}'")
    for r in results:
        print(f"  {r['address']}: {r['sphere_name']} "
              f"(confidence: {r['confidence']:.2f}, keywords: {r['matched_keywords']})")
