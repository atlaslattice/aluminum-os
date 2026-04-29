#!/usr/bin/env python3
"""
Grokbrain v4.0 - Complete Implementation
Full 144-sphere knowledge organization with xAI Collections, Qdrant, Dual AI Consensus
"""

import os
import json
import time
import functools
import re
import requests
import datetime
import shutil
import argparse
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant as LangchainQdrant
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from openai import OpenAI

import structlog

# Load environment
load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ALLOWED_IP = os.getenv('ALLOWED_IP', 'your_ip_here')
DEV_BYPASS = os.getenv('DEV_BYPASS', '0') == '1'
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
GROK_MODEL = os.getenv('GROK_MODEL', 'grok-beta')
XAI_BASE_URL = os.getenv('XAI_BASE_URL', 'https://api.x.ai/v1')

# Configure structured logging
structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

# ============================================================================
# SECURITY & UTILITIES
# ============================================================================

def get_public_ip():
    """Get public IP for whitelisting"""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return '127.0.0.1'

def ip_whitelist(func):
    """Decorator to enforce IP whitelisting"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if DEV_BYPASS:
            logger.info("ip_check_bypassed", mode="DEV")
            return func(*args, **kwargs)

        current_ip = get_public_ip()
        if current_ip != ALLOWED_IP:
            logger.error("ip_denied", current=current_ip, allowed=ALLOWED_IP)
            raise PermissionError(f"Access denied: IP {current_ip} not whitelisted. Flagged and nuked.")

        logger.info("ip_allowed", ip=current_ip)
        return func(*args, **kwargs)
    return wrapper

def mitigate_loops(max_depth=100, timeout_sec=30):
    """Decorator to prevent infinite loops and timeouts"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, _depth=0, _start_time=None, **kwargs):
            if _depth > max_depth:
                raise RecursionError("Looping failure mitigated: Max depth exceeded.")

            if _start_time is None:
                _start_time = time.time()

            if time.time() - _start_time > timeout_sec:
                raise TimeoutError("Looping failure mitigated: Timeout exceeded.")

            try:
                # Call the actual function WITHOUT passing depth/start_time
                return func(*args, **kwargs)
            except Exception as e:
                logger.error("function_error", func=func.__name__, error=str(e), depth=_depth)
                time.sleep(1)  # Backoff
                if _depth < 3:  # Retry limit
                    return wrapper(*args, _depth=_depth+1, _start_time=_start_time, **kwargs)
                raise e
        return wrapper
    return decorator

# ============================================================================
# 144-SPHERE ONTOLOGY
# ============================================================================

# Full 144 Spheres (12 categories × 12 subsets)
SPHERES = [
    # Main 1: Natural Sciences (0-11)
    'Physics', 'Chemistry', 'Biology', 'Astronomy', 'Geology', 'Oceanography',
    'Meteorology', 'Ecology', 'Botany', 'Zoology', 'Microbiology', 'Genetics',

    # Main 2: Formal Sciences (12-23)
    'Mathematics', 'Logic', 'Statistics', 'Computer Science', 'Information Theory',
    'Game Theory', 'Operations Research', 'Systems Theory', 'Decision Theory',
    'Cryptography', 'Algorithmics', 'Data Science',

    # Main 3: Social Sciences (24-35)
    'Sociology', 'Psychology', 'Anthropology', 'Economics', 'Political Science',
    'Geography', 'Linguistics', 'Archaeology', 'Demography', 'Criminology',
    'Social Work', 'Urban Studies',

    # Main 4: Humanities (36-47)
    'History', 'Philosophy', 'Literature', 'Classics', 'Religious Studies',
    'Ethics', 'Aesthetics', 'Cultural Studies', 'Mythology', 'Philology',
    'Rhetoric', 'Hermeneutics',

    # Main 5: Arts (48-59)
    'Visual Arts', 'Performing Arts', 'Music', 'Dance', 'Theater', 'Film',
    'Literature', 'Architecture', 'Design', 'Photography', 'Sculpture', 'Painting',

    # Main 6: Engineering and Technology (60-71)
    'Mechanical Engineering', 'Electrical Engineering', 'Civil Engineering',
    'Chemical Engineering', 'Aerospace Engineering', 'Biomedical Engineering',
    'Environmental Engineering', 'Industrial Engineering', 'Software Engineering',
    'Materials Engineering', 'Nuclear Engineering', 'Robotics',

    # Main 7: Medicine and Health (72-83)
    'Anatomy', 'Physiology', 'Pathology', 'Pharmacology', 'Surgery', 'Pediatrics',
    'Psychiatry', 'Neurology', 'Oncology', 'Epidemiology', 'Nutrition', 'Public Health',

    # Main 8: Education (84-95)
    'Pedagogy', 'Curriculum Design', 'Educational Psychology', 'Special Education',
    'Adult Education', 'E-Learning', 'Educational Technology', 'Assessment',
    'School Administration', 'Teacher Training', 'Literacy', 'Higher Education',

    # Main 9: Business and Economics (96-107)
    'Management', 'Marketing', 'Finance', 'Accounting', 'Entrepreneurship',
    'Human Resources', 'Operations Management', 'Supply Chain', 'International Business',
    'Business Ethics', 'Microeconomics', 'Macroeconomics',

    # Main 10: Law and Politics (108-119)
    'Constitutional Law', 'Criminal Law', 'Civil Law', 'International Law',
    'Corporate Law', 'Environmental Law', 'Human Rights', 'Political Theory',
    'Public Policy', 'International Relations', 'Comparative Politics', 'Political Economy',

    # Main 11: Religion and Philosophy (120-131)
    'Theology', 'Comparative Religion', 'Philosophy of Religion', 'Metaphysics',
    'Epistemology', 'Logic', 'Ethics', 'Existentialism', 'Eastern Philosophy',
    'Western Philosophy', 'Mysticism', 'Spiritual Studies',

    # Main 12: Interdisciplinary Studies (132-143)
    'Environmental Studies', 'Cognitive Science', 'Neuroscience', 'Bioinformatics',
    'Gender Studies', 'Media Studies', 'Cultural Anthropology',
    'Science and Technology Studies', 'Bioethics', 'Global Studies',
    'Sustainability', 'Complex Systems'
]

# Full 144 Elements (1-144)
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
    'Moscovium (115)', 'Livermorium (116)', 'Tennessine (117)', 'Oganesson (118)',
    'Ununennium (119, hyp)', 'Unbinilium (120, hyp)', 'Unbiunium (121, hyp)', 'Unbibium (122, hyp)',
    'Unbitrium (123, hyp)', 'Unbiquadium (124, hyp)', 'Unbipentium (125, hyp)', 'Unbihexium (126, hyp)',
    'Unbiseptium (127, hyp)', 'Unbioctium (128, hyp)', 'Unbiennium (129, hyp)', 'Untrinilium (130, hyp)',
    'Untriunium (131, hyp)', 'Untribium (132, hyp)', 'Untritrium (133, hyp)', 'Untriquadium (134, hyp)',
    'Untripentium (135, hyp)', 'Untrihexium (136, hyp)', 'Untriseptium (137, hyp)', 'Untrioctium (138, hyp)',
    'Untriennium (139, hyp)', 'Unquadnilium (140, hyp)', 'Unquadunium (141, hyp)', 'Unquadbium (142, hyp)',
    'Unquadtrium (143, hyp)', 'Unquadquadium (144, hyp)'
]

# 144 Gods (tailored to spheres/elements)
GODS_MAIN1 = ['Zeus (thunder/energy-H)', 'Athena (wisdom/crafts-He)', 'Gaia (life-Li)', 'Uranus (sky-Be)',
              'Hephaestus (forge-earth-B)', 'Poseidon (sea-C)', 'Aeolus (winds-N)', 'Artemis (nature-O)',
              'Demeter (plants-F)', 'Pan (animals-Ne)', 'Asclepius (healing/micro-Na)', 'Athena (inheritance-Mg)']

GODS_MAIN2 = ['Hermes (calculation-Al)', 'Apollo (reason-Si)', 'Fortuna (chance-P)', 'Vulcan (tech-S)',
              'Mnemosyne (memory-Cl)', 'Tyche (luck/games-Ar)', 'Ares (strategy-K)', 'Chronos (time/Ca)',
              'Themis (justice-Sc)', 'Titans (hidden-Ti)', 'Hecate (magic/paths-V)', 'Thoth (knowledge-Cr)']

GODS_MAIN3 = ['Hestia (society-Mn)', 'Psyche (mind-Fe)', 'Odin (cultures-Co)', 'Plutus (wealth-Ni)',
              'Jupiter (politics-Cu)', 'Geb (lands-Zn)', 'Thoth (language-Ga)', 'Clio (history-Ge)',
              'Ananke (pop-As)', 'Selene (crimes-Se)', 'Eirene (aid-Br)', 'Janus (cities-Kr)']

GODS_MAIN4 = ['Clio (history-Rb)', 'Socrates (philo-Sr)', 'Muses (lit-Y)', 'Minerva (classics-Zr)',
              'Niobe (religion-Nb)', 'Dike (ethics-Mo)', 'Aphrodite (beauty-Tc)', 'Eris (cultures-Ru)',
              'Rhea (myths-Rh)', 'Pallas (philo-Pd)', 'Peitho (rhetoric-Ag)', 'Hermes (interpretation-Cd)']

GODS_MAIN5 = ['Apollo (visual-In)', 'Dionysus (performing-Sn)', 'Orpheus (music-Sb)', 'Terpsichore (dance-Te)',
              'Melpomene (theater-I)', 'Calliope (film-Xe)', 'Erato (lit-Cs)', 'Hestia (arch-Ba)',
              'Harmonia (design-La)', 'Ceres (photo-Ce)', 'Pygmalion (sculpt-Pr)', 'Euphrosyne (painting-Nd)']

GODS_MAIN6 = ['Prometheus (mech-Pm)', 'Thor (elect-Sm)', 'Europa (civil-Eu)', 'Hermes (chem-Gd)',
              'Icarus (aero-Tb)', 'Hygieia (bio-Dy)', 'Gaea (env-Ho)', 'Ergane (ind-Er)',
              'Loki (soft-Tm)', 'Ymir (mat-Yb)', 'Hades (nuc-Lu)', 'Talos (robot-Hf)']

GODS_MAIN7 = ['Tantalus (anat-Ta)', 'Asclepius (phys-W)', 'Nosos (path-Re)', 'Circe (pharm-Os)',
              'Iris (surg-Ir)', 'Leto (ped-Pt)', 'Morpheus (psych-Au)', 'Mercury (neuro-Hg)',
              'Thanatos (onc-Tl)', 'Pestilentia (epi-Pb)', 'Annona (nut-Bi)', 'Salus (public-Po)']

GODS_MAIN8 = ['Chiron (ped-At)', 'Muse (curr-Rn)', 'Metis (ed psych-Fr)', 'Eunomia (special-Ra)',
              'Nestor (adult-Ac)', 'Thor (e-learn-Th)', 'Techne (ed tech-Pa)', 'Uranus (assess-U)',
              'Neptune (admin-Np)', 'Pluto (train-Pu)', 'Seshat (literacy-Am)', 'Sophia (higher-Cm)']

GODS_MAIN9 = ['Hermes (mgmt-Bk)', 'Persuasion (market-Cf)', 'Hades (fin-Es)', 'Arithmos (acct-Fm)',
              'Atalanta (entre-Md)', 'Eileithyia (HR-No)', 'Ergon (ops-Lr)', 'Hecate (supply-Rf)',
              'Zeus (intl-Db)', 'Eunomia (ethics-Sg)', 'Oikos (micro-Bh)', 'Cosmos (macro-Hs)']

GODS_MAIN10 = ['Themis (const-Mt)', 'Nemesis (crim-Ds)', 'Dike (civil-Rg)', 'Pax (intl-Cn)',
               'Athena (corp-Nh)', 'Gaia (env-Fl)', 'Eleutheria (rights-Ms)', 'Plato (theory-Lv)',
               'Politeia (policy-Ts)', 'Iris (intl rel-Og)', 'Anubis (comp-Uue)', 'Hermes (econ-Ubn)']

GODS_MAIN11 = ['Ra (theo-Ubi)', 'Ahura Mazda (comp rel-Ubb)', 'Ananke (phil rel-Ubt)', 'Nyx (meta-Ubq)',
               'Athena (epist-Ubp)', 'Loki (logic-Ubh)', "Ma'at (ethics-Ubs)", 'Sisyphus (exist-Ubo)',
               'Buddha (east-Ubn)', 'Aristotle (west-Utr)', 'Odin (myst-Utu)', 'Isis (spirit-Utb)']

GODS_MAIN12 = ['Pan (env-Utt)', 'Psyche (cog-Utq)', 'Morpheus (neuro-Utp)', 'Thoth (bioinfo-Uth)',
               'Hera (gender-Uts)', 'Fame (media-Uto)', 'Freyja (cult anth-Utn)', 'Vulcan (STS-Uqn)',
               'Asclepius (bioeth-Uqu)', 'Atlas (global-Uqb)', 'Persephone (sustain-Uqt)', 'Chaos (complex-Uqq)']

GODS = GODS_MAIN1 + GODS_MAIN2 + GODS_MAIN3 + GODS_MAIN4 + GODS_MAIN5 + GODS_MAIN6 + \
       GODS_MAIN7 + GODS_MAIN8 + GODS_MAIN9 + GODS_MAIN10 + GODS_MAIN11 + GODS_MAIN12

# Mythical overlays
MYTHICAL_OVERLAYS = ['Fire', 'Water', 'Earth', 'Air', 'Aether', 'Sulfur', 'Mercury', 'Salt',
                      'Gold', 'Silver', 'Azoth', 'Ambrosia'] * 12

# Numerology overlays
NUMEROLOGY_OVERLAYS = {
    'tibetan': ['9' if i % 9 == 0 else str((i % 9) + 1) for i in range(144)],
    'kabbalah': [str((i % 9) + 1) for i in range(144)],
    'iching': [str(8 if i % 8 == 0 else (i % 8)) for i in range(144)],
    'christian': ['3' if 'Theology' in SPHERES[i] else '7' if 'Philosophy' in SPHERES[i] else '12' for i in range(144)],
    'sikh': ['13' if i % 13 == 0 else '1' for i in range(144)],
    'native': ['4' if i % 7 < 4 else '7' for i in range(144)]
}

# Project keywords (expandable to 127+ IPs)
PROJECT_KEYWORDS = {
    'x-wing': ['x-wing', 'helicarrier', 'squad deployments'],
    'juggernaut': ['juggernaut'],
    'mars_terraforming': ['mars', 'terraforming', 'H_SG', 'Sheldonium', 'viability curves', 'ecosuits'],
    'animated_screenplay': ['animated screenplay', 'Iron Man', 'Trashium squad'],
    'quantum_sim': ['quantum', 'entanglement', 'simulation'],
    'neural_dreams': ['neural', 'dreams', 'mapping', 'consciousness'],
    'chemistry_binding': ['binding', 'molecular', 'chemistry', 'affinity']
}

# Category names
CATEGORY_NAMES = [
    'Natural Sciences',
    'Formal Sciences',
    'Social Sciences',
    'Humanities',
    'Arts',
    'Engineering and Technology',
    'Medicine and Health',
    'Education',
    'Business and Economics',
    'Law and Politics',
    'Religion and Philosophy',
    'Interdisciplinary Studies'
]

# ============================================================================
# GRID GENERATION
# ============================================================================

def generate_grid_descriptions() -> List[Document]:
    """Generate 144 grid reference documents"""
    docs = []
    for idx in range(144):
        sphere = SPHERES[idx]
        element = ELEMENTS[idx]
        god = GODS[idx]
        mythical = MYTHICAL_OVERLAYS[idx]
        num_overlays = {trad: NUMEROLOGY_OVERLAYS[trad][idx] for trad in NUMEROLOGY_OVERLAYS}

        desc = f"{sphere} sphere, with {element} element, {god} god, {mythical} mythical overlay, " \
               f"and numerology: {num_overlays} from traditions."

        cat_idx = idx // 12
        sub_idx = idx % 12
        category = CATEGORY_NAMES[cat_idx]

        docs.append(Document(
            page_content=desc,
            metadata={
                'cat': cat_idx,
                'sub': sub_idx,
                'sphere': sphere,
                'element': element,
                'god': god,
                'category': category,
                'flat_idx': idx
            }
        ))

    logger.info("grid_descriptions_generated", count=len(docs))
    return docs

# ============================================================================
# ENRICHMENT
# ============================================================================

@mitigate_loops(timeout_sec=15)
def enrich_with_grokipedia(sphere_name: str, tradition: str = '') -> str:
    """Enrich sphere with Wikipedia summary"""
    query = f"{sphere_name} {tradition} numerology" if tradition else sphere_name
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={query.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        data = response.json()
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]

        if 'extract' in pages[page_id]:
            summary = pages[page_id]['extract'][:500]
            logger.info("grokipedia_enriched", sphere=sphere_name, tradition=tradition)
            return summary

        return "No summary found."
    except Exception as e:
        logger.error("grokipedia_error", sphere=sphere_name, error=str(e))
        return "Error fetching summary."

@mitigate_loops(timeout_sec=20)
def enrich_with_grok(sphere_name: str, element: str, god: str) -> str:
    """Enrich sphere using Grok AI"""
    if not XAI_API_KEY:
        return "Grok enrichment skipped (no API key)"

    try:
        client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)
        prompt = f"Provide a concise 2-sentence summary of how {sphere_name} relates to {element} and {god} in knowledge organization."

        response = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        enrichment = response.choices[0].message.content.strip()
        logger.info("grok_enriched", sphere=sphere_name)
        return enrichment
    except Exception as e:
        logger.error("grok_enrichment_error", sphere=sphere_name, error=str(e))
        return f"Grok enrichment error: {str(e)}"

# ============================================================================
# VALIDATION & QUARANTINE
# ============================================================================

@ip_whitelist
@mitigate_loops()
def validate_export(file_path: str) -> Optional[Dict]:
    """Validate export file for corruption/loops"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        seen = set()
        def check_loops(obj):
            obj_id = id(obj)
            if obj_id in seen:
                raise ValueError("Looping structure detected.")
            seen.add(obj_id)

            if isinstance(obj, dict):
                for v in obj.values():
                    check_loops(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_loops(item)

        check_loops(data)
        logger.info("export_validated", file=file_path)
        return data
    except Exception as e:
        logger.error("validation_error", file=file_path, error=str(e))
        return None

@ip_whitelist
@mitigate_loops()
def quarantine_filter(export_dir='./exports/') -> str:
    """Filter chaos/irrelevant content to quarantine"""
    quarantine_dir = './quarantine/'
    os.makedirs(quarantine_dir, exist_ok=True)
    clean_dir = './clean_exports/'
    os.makedirs(clean_dir, exist_ok=True)

    # Chaos patterns
    chaos_patterns = [
        r'\b(rant|raving|personal diary|irrelevant|distraction|random thought)\b',
        r'^.{1,20}$',  # Very short
        r'\b(test|testing|hello|hi there)\b',
        r'(lol|lmao|wtf){2,}',  # Excessive slang
    ]
    chaos_regex = re.compile('|'.join(chaos_patterns), re.I)

    quarantined = 0
    cleaned = 0

    for file in os.listdir(export_dir):
        if not file.endswith(('.json', '.csv', '.txt')):
            continue

        path = os.path.join(export_dir, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if chaos_regex.search(content):
                shutil.move(path, os.path.join(quarantine_dir, file))
                quarantined += 1
                logger.info("file_quarantined", file=file)
            else:
                shutil.move(path, os.path.join(clean_dir, file))
                cleaned += 1
                logger.info("file_cleaned", file=file)
        except Exception as e:
            logger.error("filter_error", file=file, error=str(e))

    logger.info("quarantine_complete", quarantined=quarantined, cleaned=cleaned)
    return clean_dir

# ============================================================================
# ARTIFACT CREATION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def artifact_creation(clean_dir='./clean_exports/') -> List[Dict]:
    """Create input>output artifacts from clean exports"""
    from grok_parser import parse_grok_export, detect_export_format

    artifacts = []

    for file in os.listdir(clean_dir):
        path = os.path.join(clean_dir, file)

        try:
            if file.endswith('.json'):
                # Detect format and use appropriate parser
                format_type = detect_export_format(path)

                if format_type == 'grok':
                    # Use Grok-specific parser for nested conversation format
                    grok_artifacts = parse_grok_export(path)
                    artifacts.extend(grok_artifacts)
                    logger.info("grok_format_parsed", file=file, count=len(grok_artifacts))
                else:
                    # Standard chat format (OpenAI, Gemini, DeepSeek)
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if 'messages' in data:
                        messages = data['messages']
                        for i in range(len(messages) - 1):
                            if messages[i].get('role') == 'user' and messages[i+1].get('role') == 'assistant':
                                artifacts.append({
                                    'input': messages[i].get('content', ''),
                                    'output': messages[i+1].get('content', ''),
                                    'timestamp': datetime.datetime.now().isoformat(),
                                    'source_file': file
                                })
                    else:
                        # Try to parse as raw text
                        content = json.dumps(data)
                        pairs = re.split(r'(Human:|Assistant:|User:|AI:)', content)
                        for i in range(1, len(pairs), 4):
                            if i+1 < len(pairs):
                                artifacts.append({
                                    'input': pairs[i].strip(),
                                    'output': pairs[i+1].strip(),
                                    'timestamp': datetime.datetime.now().isoformat(),
                                    'source_file': file
                                })

            elif file.endswith('.txt'):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse dialogue patterns
                pairs = re.split(r'(Human:|Assistant:|User:|AI:)', content, flags=re.I)
                for i in range(1, len(pairs), 4):
                    if i+1 < len(pairs):
                        artifacts.append({
                            'input': pairs[i+1].strip() if i+1 < len(pairs) else '',
                            'output': pairs[i+3].strip() if i+3 < len(pairs) else '',
                            'timestamp': datetime.datetime.now().isoformat(),
                            'source_file': file
                        })

        except Exception as e:
            logger.error("artifact_creation_error", file=file, error=str(e))

    # Save artifacts
    os.makedirs('./parsed', exist_ok=True)
    with open('./artifacts.json', 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, indent=2)

    logger.info("artifacts_created", count=len(artifacts))
    return artifacts

# Continue in next file due to length...
