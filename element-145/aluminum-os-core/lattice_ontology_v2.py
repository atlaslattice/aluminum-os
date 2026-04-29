#!/usr/bin/env python3
"""
Lattice Ontology v2.0 — Canonical 12×12+1 Sphere Constants

This module replaces grokbrain_v4.py's SPHERES, CATEGORY_NAMES, and ELEMENTS
with the canonical 12-House × 12-Sphere + Element 145 ontology.

Migration: grokbrain_v4 used 12 academic discipline categories.
This module uses 12 operational Houses that map to real governance/operational
domains. The 144 Spheres are domain-specific subdivisions within each House.

Usage:
    from lattice_ontology_v2 import (
        HOUSES, SPHERES, HOUSE_NAMES, SPHERE_NAMES,
        KEYWORDS, INTER_HOUSE_EDGES, ELEMENT_145,
        sphere_index, house_for_sphere, address_for_index,
        classify_text
    )

Compatibility:
    - SPHERES[0:143] → flat list of sphere names (same interface as grokbrain_v4)
    - HOUSE_NAMES[0:11] → replaces CATEGORY_NAMES
    - sphere_index("H04.S03") → integer index (0-143)
    - classify_text("quantum computing") → best matching sphere address
"""

from typing import List, Dict, Tuple, Optional
import re

# ============================================================================
# 12 HOUSES (replaces CATEGORY_NAMES)
# ============================================================================

HOUSE_NAMES = [
    "Consciousness & Cognition",       # H01 (index 0)
    "Technology & Engineering",         # H02 (index 1)
    "Economics & Finance",              # H03 (index 2)
    "Governance & Law",                 # H04 (index 3)
    "Culture & Society",                # H05 (index 4)
    "Health & Biology",                 # H06 (index 5)
    "Earth & Environment",             # H07 (index 6)
    "Mathematics & Logic",             # H08 (index 7)
    "Physics & Chemistry",             # H09 (index 8)
    "History & Philosophy",            # H10 (index 9)
    "Communication & Information",     # H11 (index 10)
    "Security & Defense",              # H12 (index 11)
]

# House IDs for structured addressing
HOUSE_IDS = [f"H{i+1:02d}" for i in range(12)]

# ============================================================================
# 144 SPHERES (replaces SPHERES from grokbrain_v4)
# Organized as 12 Houses × 12 Spheres = 144 total
# Index = house_index * 12 + sphere_index_within_house
# ============================================================================

SPHERES = [
    # H01: Consciousness & Cognition (0-11)
    "Perception", "Attention", "Memory", "Reasoning",
    "Emotion", "Language", "Learning", "Creativity",
    "Metacognition", "Social Cognition", "Altered States", "Development",

    # H02: Technology & Engineering (12-23)
    "Computing", "Networking", "Energy Systems", "Materials",
    "Manufacturing", "Robotics", "Biotech", "Aerospace",
    "Civil Engineering", "Environmental Tech", "Quantum Tech", "AI/ML",

    # H03: Economics & Finance (24-35)
    "Microeconomics", "Macroeconomics", "Monetary Policy", "Trade",
    "Labor Markets", "Financial Markets", "Development Economics", "Behavioral Economics",
    "Public Finance", "Inequality", "Innovation Economics", "Environmental Economics",

    # H04: Governance & Law (36-47)
    "Constitutional Law", "International Law", "Regulatory Frameworks", "Human Rights",
    "Criminal Justice", "Administrative Law", "Electoral Systems", "Federalism",
    "Treaty Law", "Maritime Law", "Cyber Law", "Indigenous Rights",

    # H05: Culture & Society (48-59)
    "Anthropology", "Sociology", "Media Studies", "Education",
    "Religion", "Arts", "Linguistics", "Migration",
    "Gender Studies", "Urban Studies", "Sports & Recreation", "Food Culture",

    # H06: Health & Biology (60-71)
    "Anatomy", "Genetics", "Immunology", "Neuroscience",
    "Pharmacology", "Epidemiology", "Ecology", "Evolution",
    "Microbiology", "Nutrition", "Mental Health", "Public Health",

    # H07: Earth & Environment (72-83)
    "Geology", "Meteorology", "Oceanography", "Ecology",
    "Climate Science", "Hydrology", "Soil Science", "Atmospheric Chemistry",
    "Natural Hazards", "Conservation", "Resource Management", "Planetary Science",

    # H08: Mathematics & Logic (84-95)
    "Algebra", "Geometry", "Analysis", "Probability",
    "Statistics", "Number Theory", "Topology", "Combinatorics",
    "Logic", "Computation Theory", "Optimization", "Applied Mathematics",

    # H09: Physics & Chemistry (96-107)
    "Classical Mechanics", "Quantum Mechanics", "Thermodynamics", "Electromagnetism",
    "Relativity", "Nuclear Physics", "Organic Chemistry", "Inorganic Chemistry",
    "Physical Chemistry", "Materials Science", "Optics", "Particle Physics",

    # H10: History & Philosophy (108-119)
    "Ancient History", "Medieval History", "Modern History", "Philosophy of Mind",
    "Ethics", "Epistemology", "Political Philosophy", "Aesthetics",
    "Philosophy of Science", "Historiography", "Comparative Religion", "Existentialism",

    # H11: Communication & Information (120-131)
    "Journalism", "Rhetoric", "Information Theory", "Library Science",
    "Data Science", "Cryptography", "Semiotics", "Public Relations",
    "Advertising", "Telecommunications", "Archival Science", "Knowledge Management",

    # H12: Security & Defense (132-143)
    "Military Strategy", "Intelligence Analysis", "Cybersecurity", "Counterterrorism",
    "Nuclear Deterrence", "Maritime Security", "Space Security", "Biosecurity",
    "Critical Infrastructure", "Conflict Resolution", "Peacekeeping", "Arms Control",
]

# Full sphere names with House prefix for display
SPHERE_FULL_NAMES = [
    f"{HOUSE_NAMES[i // 12]} → {SPHERES[i]}" for i in range(144)
]

# ============================================================================
# KEYWORDS — semantic matching for each sphere
# ============================================================================

KEYWORDS = {
    # H01: Consciousness & Cognition
    0: ["sensory processing", "visual perception", "auditory processing", "proprioception", "pattern recognition"],
    1: ["selective attention", "divided attention", "sustained attention", "attentional control", "salience"],
    2: ["working memory", "long-term memory", "episodic memory", "semantic memory", "memory consolidation"],
    3: ["deductive reasoning", "inductive reasoning", "abductive reasoning", "causal reasoning", "analogical reasoning"],
    4: ["affect", "emotional regulation", "valence", "arousal", "emotional intelligence"],
    5: ["natural language processing", "syntax", "semantics", "pragmatics", "discourse"],
    6: ["reinforcement learning", "supervised learning", "transfer learning", "curriculum learning", "meta-learning"],
    7: ["divergent thinking", "ideation", "generative processes", "novelty", "combinatorial creativity"],
    8: ["self-monitoring", "reflection", "confidence calibration", "cognitive control", "introspection"],
    9: ["theory of mind", "empathy", "social inference", "perspective taking", "joint attention"],
    10: ["consciousness states", "meditation", "flow states", "dreaming", "psychedelic states"],
    11: ["cognitive development", "neural plasticity", "maturation", "critical periods", "lifespan development"],

    # H02: Technology & Engineering
    12: ["hardware", "processors", "operating systems", "distributed systems", "cloud computing"],
    13: ["protocols", "routing", "bandwidth", "latency", "network topology", "mesh networks"],
    14: ["power generation", "grid management", "renewable energy", "storage", "transmission"],
    15: ["composites", "semiconductors", "polymers", "nanomaterials", "metamaterials"],
    16: ["CNC", "additive manufacturing", "supply chain", "quality control", "automation"],
    17: ["actuators", "sensors", "control systems", "autonomous navigation", "human-robot interaction"],
    18: ["genetic engineering", "CRISPR", "synthetic biology", "bioinformatics", "tissue engineering"],
    19: ["propulsion", "orbital mechanics", "avionics", "spacecraft design", "atmospheric reentry"],
    20: ["structural engineering", "geotechnical", "transportation", "water resources", "construction"],
    21: ["carbon capture", "water treatment", "waste management", "remediation", "monitoring"],
    22: ["quantum computing", "quantum communication", "quantum sensing", "error correction", "qubits"],
    23: ["neural networks", "transformers", "reinforcement learning", "computer vision", "NLP", "foundation models"],

    # H03: Economics & Finance
    24: ["supply demand", "price theory", "market structure", "consumer behavior", "firm theory"],
    25: ["GDP", "inflation", "unemployment", "business cycles", "fiscal policy"],
    26: ["central banking", "interest rates", "money supply", "quantitative easing", "currency"],
    27: ["international trade", "tariffs", "trade agreements", "comparative advantage", "supply chains"],
    28: ["employment", "wages", "unions", "gig economy", "workforce development"],
    29: ["equities", "bonds", "derivatives", "risk management", "market microstructure"],
    30: ["poverty", "aid", "microfinance", "institutional development", "growth theory"],
    31: ["cognitive biases", "nudge theory", "prospect theory", "bounded rationality"],
    32: ["taxation", "government spending", "debt", "fiscal sustainability", "public goods"],
    33: ["wealth distribution", "Gini coefficient", "social mobility", "economic justice"],
    34: ["R&D", "patents", "technology transfer", "startup ecosystems", "creative destruction"],
    35: ["carbon pricing", "externalities", "resource economics", "circular economy"],

    # H04: Governance & Law
    36: ["constitutions", "separation of powers", "judicial review", "fundamental rights"],
    37: ["treaties", "UN charter", "sovereignty", "international courts", "diplomatic law"],
    38: ["regulation", "compliance", "standards bodies", "licensing", "enforcement"],
    39: ["civil liberties", "UDHR", "refugee law", "discrimination", "dignity"],
    40: ["criminal law", "prosecution", "sentencing", "rehabilitation", "forensics"],
    41: ["bureaucracy", "administrative procedure", "government agencies", "public administration"],
    42: ["voting systems", "representation", "gerrymandering", "campaign finance", "democracy"],
    43: ["federal systems", "devolution", "subsidiarity", "intergovernmental relations"],
    44: ["treaty negotiation", "ratification", "compliance", "withdrawal", "Vienna Convention"],
    45: ["UNCLOS", "admiralty", "shipping", "territorial waters", "piracy"],
    46: ["data protection", "GDPR", "cybercrime", "digital rights", "platform regulation"],
    47: ["land rights", "self-determination", "cultural preservation", "UNDRIP"],

    # H05: Culture & Society
    48: ["ethnography", "cultural anthropology", "kinship", "ritual", "material culture"],
    49: ["social stratification", "institutions", "social movements", "deviance", "socialization"],
    50: ["journalism", "propaganda", "social media", "media literacy", "public discourse"],
    51: ["pedagogy", "curriculum", "assessment", "educational technology", "lifelong learning"],
    52: ["theology", "comparative religion", "secularism", "religious institutions", "spirituality"],
    53: ["visual arts", "performing arts", "literature", "music", "architecture", "design"],
    54: ["phonology", "morphology", "syntax", "semantics", "sociolinguistics", "language families"],
    55: ["immigration", "diaspora", "refugees", "integration", "transnationalism"],
    56: ["gender identity", "feminism", "masculinity", "intersectionality", "LGBTQ+"],
    57: ["urbanization", "city planning", "housing", "transportation", "smart cities"],
    58: ["athletics", "esports", "leisure", "physical fitness", "sports governance"],
    59: ["cuisine", "food security", "agriculture", "nutrition culture", "food systems"],

    # H06: Health & Biology
    60: ["organ systems", "physiology", "biomechanics", "histology", "pathology"],
    61: ["genomics", "heredity", "gene expression", "epigenetics", "genetic disorders"],
    62: ["immune response", "vaccines", "autoimmunity", "immunotherapy", "inflammation"],
    63: ["brain structure", "neural circuits", "neuroplasticity", "neurotransmitters"],
    64: ["drug design", "pharmacokinetics", "clinical trials", "drug interactions"],
    65: ["disease surveillance", "outbreak investigation", "risk factors", "cohort studies"],
    66: ["ecosystems", "biodiversity", "food webs", "population dynamics", "conservation biology"],
    67: ["natural selection", "speciation", "phylogenetics", "adaptation", "coevolution"],
    68: ["bacteria", "viruses", "fungi", "microbiome", "antimicrobial resistance"],
    69: ["macronutrients", "micronutrients", "dietary guidelines", "metabolism", "malnutrition"],
    70: ["psychiatry", "therapy", "depression", "anxiety", "trauma", "resilience"],
    71: ["health policy", "sanitation", "health equity", "pandemic preparedness"],

    # H07: Earth & Environment
    72: ["plate tectonics", "mineralogy", "stratigraphy", "volcanology", "seismology"],
    73: ["weather systems", "forecasting", "atmospheric dynamics", "severe weather"],
    74: ["ocean currents", "marine biology", "deep sea", "coral reefs", "ocean chemistry"],
    75: ["biomes", "ecosystem services", "habitat", "keystone species", "restoration"],
    76: ["climate models", "greenhouse gases", "paleoclimate", "tipping points"],
    77: ["water cycle", "groundwater", "watersheds", "flooding", "water management"],
    78: ["pedology", "soil chemistry", "erosion", "soil health", "land degradation"],
    79: ["ozone", "aerosols", "air quality", "atmospheric composition"],
    80: ["earthquakes", "tsunamis", "hurricanes", "wildfires", "volcanic eruptions"],
    81: ["protected areas", "endangered species", "rewilding", "sustainability"],
    82: ["mining", "forestry", "fisheries", "water rights", "resource depletion"],
    83: ["astrobiology", "planetary geology", "exoplanets", "space weather"],

    # H08: Mathematics & Logic
    84: ["group theory", "ring theory", "linear algebra", "abstract algebra"],
    85: ["Euclidean", "non-Euclidean", "differential geometry", "algebraic geometry"],
    86: ["real analysis", "complex analysis", "functional analysis", "measure theory"],
    87: ["probability theory", "stochastic processes", "Bayesian inference", "random variables"],
    88: ["hypothesis testing", "regression", "experimental design", "statistical inference"],
    89: ["primes", "modular arithmetic", "Diophantine equations", "analytic number theory"],
    90: ["point-set topology", "algebraic topology", "manifolds", "homology"],
    91: ["graph theory", "enumeration", "Ramsey theory", "extremal combinatorics"],
    92: ["propositional logic", "predicate logic", "model theory", "proof theory"],
    93: ["Turing machines", "complexity classes", "computability", "lambda calculus"],
    94: ["linear programming", "convex optimization", "metaheuristics", "constraint satisfaction"],
    95: ["differential equations", "numerical methods", "mathematical modeling"],

    # H09: Physics & Chemistry
    96: ["Newtonian mechanics", "Lagrangian", "Hamiltonian", "fluid dynamics"],
    97: ["wave function", "Schrodinger equation", "entanglement", "superposition"],
    98: ["entropy", "heat transfer", "phase transitions", "statistical mechanics"],
    99: ["Maxwell equations", "electromagnetic waves", "circuits", "photonics"],
    100: ["special relativity", "general relativity", "spacetime", "gravitational waves"],
    101: ["fission", "fusion", "radioactivity", "nuclear structure", "isotopes"],
    102: ["carbon compounds", "synthesis", "polymers", "biochemistry"],
    103: ["coordination chemistry", "solid state", "catalysis", "bioinorganic"],
    104: ["chemical kinetics", "spectroscopy", "surface chemistry", "electrochemistry"],
    105: ["crystallography", "metallurgy", "ceramics", "thin films", "biomaterials"],
    106: ["fiber optics", "lasers", "holography", "nonlinear optics", "imaging"],
    107: ["Standard Model", "quarks", "leptons", "Higgs boson", "collider physics"],

    # H10: History & Philosophy
    108: ["Mesopotamia", "Egypt", "Greece", "Rome", "Bronze Age", "classical antiquity"],
    109: ["feudalism", "Crusades", "Byzantine", "Islamic Golden Age", "monasticism"],
    110: ["Enlightenment", "Industrial Revolution", "World Wars", "Cold War", "decolonization"],
    111: ["consciousness", "qualia", "intentionality", "mental causation", "AI consciousness"],
    112: ["deontology", "consequentialism", "virtue ethics", "applied ethics", "moral philosophy"],
    113: ["knowledge", "justification", "skepticism", "truth", "epistemic virtue"],
    114: ["justice", "liberty", "authority", "social contract", "democracy theory"],
    115: ["beauty", "art criticism", "taste", "sublime", "aesthetic experience"],
    116: ["falsifiability", "paradigm shifts", "scientific realism", "demarcation"],
    117: ["historical method", "primary sources", "narrative", "periodization"],
    118: ["world religions", "interfaith dialogue", "religious studies", "mythology"],
    119: ["existence", "authenticity", "absurdity", "freedom", "phenomenology"],

    # H11: Communication & Information
    120: ["investigative reporting", "press freedom", "editorial", "fact-checking"],
    121: ["persuasion", "argumentation", "public speaking", "discourse analysis"],
    122: ["Shannon entropy", "coding theory", "channel capacity", "compression"],
    123: ["cataloging", "classification", "information retrieval", "digital libraries"],
    124: ["data mining", "visualization", "big data", "feature engineering", "ETL"],
    125: ["encryption", "public key", "hash functions", "zero knowledge", "post-quantum"],
    126: ["signs", "symbols", "meaning-making", "visual semiotics", "cultural codes"],
    127: ["reputation management", "crisis communication", "stakeholder engagement"],
    128: ["branding", "marketing strategy", "consumer psychology", "media buying"],
    129: ["5G", "satellite", "fiber optics", "spectrum management", "IoT"],
    130: ["preservation", "provenance", "digital archives", "records management"],
    131: ["organizational knowledge", "tacit knowledge", "knowledge graphs", "ontologies"],

    # H12: Security & Defense
    132: ["doctrine", "force structure", "logistics", "combined arms", "asymmetric warfare"],
    133: ["SIGINT", "HUMINT", "OSINT", "threat assessment", "counterintelligence"],
    134: ["threat detection", "incident response", "vulnerability", "zero-day", "SOC"],
    135: ["radicalization", "deradicalization", "threat finance", "border security"],
    136: ["MAD", "arms control", "nonproliferation", "nuclear posture"],
    137: ["naval operations", "piracy", "sea lanes", "coast guard", "UNCLOS enforcement"],
    138: ["space debris", "ASAT weapons", "space situational awareness", "Outer Space Treaty"],
    139: ["bioweapons", "pandemic preparedness", "dual-use research", "BWC"],
    140: ["SCADA", "grid security", "water systems", "transportation security"],
    141: ["mediation", "negotiation", "peace processes", "transitional justice"],
    142: ["UN peacekeeping", "stabilization", "DDR", "civilian protection"],
    143: ["treaties", "verification", "disarmament", "export controls", "MTCR"],
}

# ============================================================================
# ELEMENT 145 — Admin Sphere (Aluminum OS Core)
# ============================================================================

ELEMENT_145 = {
    "id": "E145",
    "name": "Admin Sphere (Aluminum OS Core)",
    "role": "meta-coordination",
    "functions": [
        "cross_domain_routing",
        "emergent_risk_detection",
        "unified_synthesis",
        "blind_spot_identification",
        "constitutional_enforcement",
    ],
    "components": [
        "aluminum-os-core",
        "boot-manifest",
        "pantheon-council",
        "shugs",
        "snrs-bridge",
        "constitutional-os",
    ],
}

# ============================================================================
# INTER-HOUSE CONNECTION MATRIX
# ============================================================================

INTER_HOUSE_EDGES = [
    # H01 Consciousness ↔ others
    {"source": "H01", "target": "H02", "type": "human-computer-interaction", "strength": 0.8},
    {"source": "H01", "target": "H05", "type": "cultural-cognition", "strength": 0.7},
    {"source": "H01", "target": "H06", "type": "neuroscience-bridge", "strength": 0.9},
    {"source": "H01", "target": "H08", "type": "formal-reasoning", "strength": 0.6},
    {"source": "H01", "target": "H10", "type": "philosophy-of-mind", "strength": 0.8},
    {"source": "H01", "target": "H12", "type": "cognitive-security", "strength": 0.5},

    # H02 Technology ↔ others
    {"source": "H02", "target": "H03", "type": "tech-economics", "strength": 0.8},
    {"source": "H02", "target": "H04", "type": "tech-regulation", "strength": 0.7},
    {"source": "H02", "target": "H07", "type": "environmental-tech", "strength": 0.7},
    {"source": "H02", "target": "H08", "type": "computational-math", "strength": 0.9},
    {"source": "H02", "target": "H09", "type": "applied-physics", "strength": 0.9},
    {"source": "H02", "target": "H11", "type": "information-infrastructure", "strength": 0.8},
    {"source": "H02", "target": "H12", "type": "defense-tech", "strength": 0.8},

    # H03 Economics ↔ others
    {"source": "H03", "target": "H04", "type": "regulatory-economic", "strength": 0.9},
    {"source": "H03", "target": "H05", "type": "socioeconomic", "strength": 0.7},
    {"source": "H03", "target": "H07", "type": "environmental-economics", "strength": 0.7},
    {"source": "H03", "target": "H11", "type": "information-economics", "strength": 0.6},
    {"source": "H03", "target": "H12", "type": "defense-economics", "strength": 0.7},

    # H04 Governance ↔ others
    {"source": "H04", "target": "H05", "type": "social-governance", "strength": 0.8},
    {"source": "H04", "target": "H06", "type": "health-policy", "strength": 0.7},
    {"source": "H04", "target": "H07", "type": "environmental-regulation", "strength": 0.8},
    {"source": "H04", "target": "H10", "type": "political-philosophy", "strength": 0.8},
    {"source": "H04", "target": "H12", "type": "security-governance", "strength": 0.9},

    # H05 Culture ↔ others
    {"source": "H05", "target": "H06", "type": "health-culture", "strength": 0.5},
    {"source": "H05", "target": "H10", "type": "cultural-history", "strength": 0.8},
    {"source": "H05", "target": "H11", "type": "media-culture", "strength": 0.8},

    # H06 Health ↔ others
    {"source": "H06", "target": "H07", "type": "environmental-health", "strength": 0.7},
    {"source": "H06", "target": "H09", "type": "biochemistry", "strength": 0.8},
    {"source": "H06", "target": "H12", "type": "biosecurity", "strength": 0.6},

    # H07 Earth ↔ others
    {"source": "H07", "target": "H09", "type": "geophysics-geochemistry", "strength": 0.8},

    # H08 Mathematics ↔ others
    {"source": "H08", "target": "H09", "type": "mathematical-physics", "strength": 0.9},
    {"source": "H08", "target": "H11", "type": "information-theory", "strength": 0.7},

    # H09 Physics ↔ others
    {"source": "H09", "target": "H12", "type": "weapons-physics", "strength": 0.6},

    # H10 History ↔ others
    {"source": "H10", "target": "H11", "type": "intellectual-history", "strength": 0.6},
    {"source": "H10", "target": "H12", "type": "military-history", "strength": 0.7},

    # H11 Communication ↔ others
    {"source": "H11", "target": "H12", "type": "information-warfare", "strength": 0.8},
]

# ============================================================================
# MIGRATION MAPPING — Old grokbrain_v4 → New 12×12+1
# ============================================================================

MIGRATION_MAP = {
    # Old Category → New House(s)
    "Natural Sciences": ["H06", "H07", "H09"],      # Split: Health, Earth, Physics
    "Formal Sciences": ["H08"],                       # Mathematics & Logic
    "Social Sciences": ["H01", "H03", "H05"],        # Split: Cognition, Economics, Culture
    "Humanities": ["H10"],                             # History & Philosophy
    "Arts": ["H05"],                                   # Culture & Society (sphere-level)
    "Engineering and Technology": ["H02"],             # Technology & Engineering
    "Medicine and Health": ["H06"],                    # Health & Biology
    "Education": ["H05"],                              # Culture & Society (sphere-level)
    "Business and Economics": ["H03"],                 # Economics & Finance
    "Law and Politics": ["H04"],                       # Governance & Law
    "Religion and Philosophy": ["H10", "H05"],        # Split: Philosophy, Religion
    "Interdisciplinary Studies": ["E145"],             # Element 145
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def sphere_index(address: str) -> int:
    """Convert a lattice address (e.g., 'H04.S03') to a flat index (0-143).

    Args:
        address: Lattice address in format 'H{nn}.S{nn}' (1-indexed)

    Returns:
        Flat index (0-indexed, 0-143)

    Raises:
        ValueError: If address format is invalid or out of range
    """
    match = re.match(r"H(\d{1,2})\.S(\d{1,2})", address)
    if not match:
        raise ValueError(f"Invalid lattice address: {address}. Expected format: H01.S01")
    house = int(match.group(1))
    sphere = int(match.group(2))
    if not (1 <= house <= 12 and 1 <= sphere <= 12):
        raise ValueError(f"Address out of range: {address}. Houses: 1-12, Spheres: 1-12")
    return (house - 1) * 12 + (sphere - 1)


def address_for_index(index: int) -> str:
    """Convert a flat index (0-143) to a lattice address (e.g., 'H04.S03').

    Args:
        index: Flat index (0-indexed, 0-143)

    Returns:
        Lattice address string
    """
    if not (0 <= index <= 143):
        raise ValueError(f"Index out of range: {index}. Must be 0-143.")
    house = (index // 12) + 1
    sphere = (index % 12) + 1
    return f"H{house:02d}.S{sphere:02d}"


def house_for_sphere(index: int) -> Tuple[int, str]:
    """Get the House index and name for a given sphere index.

    Args:
        index: Flat sphere index (0-143)

    Returns:
        Tuple of (house_index, house_name)
    """
    house_idx = index // 12
    return house_idx, HOUSE_NAMES[house_idx]


def classify_text(text: str, top_k: int = 3) -> List[Dict]:
    """Classify text against the 144 spheres using keyword matching.

    This is a lightweight classifier for use when vector embeddings are
    not available. For production use, prefer the SphereClassifier with
    HuggingFace embeddings.

    Args:
        text: Input text to classify
        top_k: Number of top matches to return

    Returns:
        List of dicts with 'address', 'sphere', 'house', 'score' keys
    """
    text_lower = text.lower()
    scores = []

    for idx in range(144):
        keywords = KEYWORDS.get(idx, [])
        score = 0.0
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1.0
            # Partial word matching
            for word in kw.lower().split():
                if word in text_lower and len(word) > 3:
                    score += 0.3

        if score > 0:
            house_idx, house_name = house_for_sphere(idx)
            scores.append({
                "address": address_for_index(idx),
                "sphere": SPHERES[idx],
                "house": house_name,
                "house_id": HOUSE_IDS[house_idx],
                "score": round(score, 2),
            })

    scores.sort(key=lambda x: -x["score"])
    return scores[:top_k]


def get_connected_houses(house_id: str) -> List[Dict]:
    """Get all Houses connected to the given House via inter-House edges.

    Args:
        house_id: House ID (e.g., 'H04')

    Returns:
        List of connected houses with edge type and strength
    """
    connections = []
    for edge in INTER_HOUSE_EDGES:
        if edge["source"] == house_id:
            connections.append({
                "house": edge["target"],
                "type": edge["type"],
                "strength": edge["strength"],
                "direction": "outbound",
            })
        elif edge["target"] == house_id:
            connections.append({
                "house": edge["source"],
                "type": edge["type"],
                "strength": edge["strength"],
                "direction": "inbound",
            })
    connections.sort(key=lambda x: -x["strength"])
    return connections


def get_activated_context(text: str, depth: int = 1) -> Dict:
    """Full LCP INGEST + ACTIVATE pipeline.

    Classifies text, identifies primary spheres, then activates
    connected Houses via inter-House edges.

    Args:
        text: Input text to process
        depth: How many edge hops to follow (1 = direct connections only)

    Returns:
        Dict with 'primary_spheres', 'activated_houses', 'edges'
    """
    primary = classify_text(text, top_k=5)
    if not primary:
        return {"primary_spheres": [], "activated_houses": [], "edges": []}

    # Collect unique primary houses
    primary_houses = list(set(s["house_id"] for s in primary))

    # Follow edges
    activated = set(primary_houses)
    all_edges = []
    for house_id in primary_houses:
        connections = get_connected_houses(house_id)
        for conn in connections:
            if conn["strength"] >= 0.6:  # Only follow strong connections
                activated.add(conn["house"])
                all_edges.append({
                    "from": house_id,
                    "to": conn["house"],
                    "type": conn["type"],
                    "strength": conn["strength"],
                })

    return {
        "primary_spheres": primary,
        "activated_houses": sorted(list(activated)),
        "edges": all_edges,
    }


# ============================================================================
# BACKWARD COMPATIBILITY — grokbrain_v4 interface
# ============================================================================

# CATEGORY_NAMES is the old name for HOUSE_NAMES
CATEGORY_NAMES = HOUSE_NAMES

# ELEMENTS — map spheres to periodic table elements (preserving grokbrain_v4 convention)
ELEMENTS = [
    'Hydrogen (1)', 'Helium (2)', 'Lithium (3)', 'Beryllium (4)', 'Boron (5)', 'Carbon (6)',
    'Nitrogen (7)', 'Oxygen (8)', 'Fluorine (9)', 'Neon (10)', 'Sodium (11)', 'Magnesium (12)',
    'Aluminum (13)', 'Silicon (14)', 'Phosphorus (15)', 'Sulfur (16)', 'Chlorine (17)', 'Argon (18)',
    'Potassium (19)', 'Calcium (20)', 'Scandium (21)', 'Titanium (22)', 'Vanadium (23)', 'Chromium (24)',
    'Manganese (25)', 'Iron (26)', 'Cobalt (27)', 'Nickel (28)', 'Copper (29)', 'Zinc (30)',
    'Gallium (31)', 'Germanium (32)', 'Arsenic (33)', 'Selenium (34)', 'Bromine (35)', 'Krypton (36)',
    'Rubidium (37)', 'Strontium (38)', 'Yttrium (39)', 'Zirconium (40)', 'Niobium (41)', 'Molybdenum (42)',
    'Technetium (43)', 'Ruthenium (44)', 'Rhodium (45)', 'Palladium (46)', 'Silver (47)', 'Cadmium (48)',
    'Indium (49)', 'Tin (50)', 'Antimony (51)', 'Tellurium (52)', 'Iodine (53)', 'Xenon (54)',
    'Cesium (55)', 'Barium (56)', 'Lanthanum (57)', 'Cerium (58)', 'Praseodymium (59)', 'Neodymium (60)',
    'Promethium (61)', 'Samarium (62)', 'Europium (63)', 'Gadolinium (64)', 'Terbium (65)', 'Dysprosium (66)',
    'Holmium (67)', 'Erbium (68)', 'Thulium (69)', 'Ytterbium (70)', 'Lutetium (71)', 'Hafnium (72)',
    'Tantalum (73)', 'Tungsten (74)', 'Rhenium (75)', 'Osmium (76)', 'Iridium (77)', 'Platinum (78)',
    'Gold (79)', 'Mercury (80)', 'Thallium (81)', 'Lead (82)', 'Bismuth (83)', 'Polonium (84)',
    'Astatine (85)', 'Radon (86)', 'Francium (87)', 'Radium (88)', 'Actinium (89)', 'Thorium (90)',
    'Protactinium (91)', 'Uranium (92)', 'Neptunium (93)', 'Plutonium (94)', 'Americium (95)', 'Curium (96)',
    'Berkelium (97)', 'Californium (98)', 'Einsteinium (99)', 'Fermium (100)', 'Mendelevium (101)', 'Nobelium (102)',
    'Lawrencium (103)', 'Rutherfordium (104)', 'Dubnium (105)', 'Seaborgium (106)', 'Bohrium (107)', 'Hassium (108)',
    'Meitnerium (109)', 'Darmstadtium (110)', 'Roentgenium (111)', 'Copernicium (112)', 'Nihonium (113)', 'Flerovium (114)',
    'Moscovium (115)', 'Livermorium (116)', 'Tennessine (117)', 'Oganesson (118)', 'Ununennium (119)', 'Unbinilium (120)',
    'Unbiunium (121)', 'Unbibium (122)', 'Unbitrium (123)', 'Unbiquadium (124)', 'Unbipentium (125)', 'Unbihexium (126)',
    'Unbiseptium (127)', 'Unbioctium (128)', 'Unbiennium (129)', 'Untrinilium (130)', 'Untriunium (131)', 'Untribium (132)',
    'Untritrium (133)', 'Untriquadium (134)', 'Untripentium (135)', 'Untrihexium (136)', 'Untriseptium (137)', 'Untrioctium (138)',
    'Untriennium (139)', 'Unquadnilium (140)', 'Unquadunium (141)', 'Unquadbium (142)', 'Unquadtrium (143)', 'Unquadquadium (144)',
]


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== Lattice Ontology v2.0 Self-Test ===\n")

    # Basic counts
    print(f"Houses: {len(HOUSE_NAMES)}")
    print(f"Spheres: {len(SPHERES)}")
    print(f"Keywords entries: {len(KEYWORDS)}")
    print(f"Inter-House edges: {len(INTER_HOUSE_EDGES)}")
    print(f"Element 145: {ELEMENT_145['name']}")
    print()

    # Address conversion
    addr = "H04.S03"
    idx = sphere_index(addr)
    print(f"sphere_index('{addr}') = {idx} → {SPHERES[idx]}")
    print(f"address_for_index({idx}) = {address_for_index(idx)}")
    print()

    # Classification test
    test_texts = [
        "quantum computing and error correction",
        "climate change policy and carbon pricing",
        "CRISPR gene editing for disease treatment",
        "cybersecurity threat detection and incident response",
        "Kantian ethics and moral philosophy",
    ]

    for text in test_texts:
        results = classify_text(text, top_k=3)
        print(f"classify_text('{text[:50]}...')")
        for r in results:
            print(f"  → {r['address']} {r['sphere']} ({r['house']}) score={r['score']}")
        print()

    # Activated context test
    print("=== Full INGEST + ACTIVATE ===")
    ctx = get_activated_context("quantum computing threatens encryption standards")
    print(f"Primary spheres: {[s['address'] for s in ctx['primary_spheres']]}")
    print(f"Activated houses: {ctx['activated_houses']}")
    print(f"Edges followed: {len(ctx['edges'])}")
    for edge in ctx['edges']:
        print(f"  {edge['from']} → {edge['to']} ({edge['type']}, {edge['strength']})")
