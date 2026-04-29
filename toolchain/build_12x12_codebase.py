#!/usr/bin/env python3
"""
ORC 12×12+1 Ontological Codebase Generator
Generates the canonical filesystem structure organized by the 144+1 sphere ontology.
Every house has 12 sphere subdirectories. Every sphere has a manifest.
All modules, doctrines, and invariants are compiled into their sphere locations.
Zero blanks — every sphere has at minimum a manifest even if no modules yet.

Source: Build Plan v3.14
Output: /home/ubuntu/codebase-artifacts/ (restructured)
"""

import os
import yaml
import re
from pathlib import Path

OUTPUT_DIR = Path("/home/ubuntu/codebase-artifacts")
BUILD_PLAN = Path("/home/ubuntu/COMPLETE_BUILD_PLAN_v3.14.md")

# ============================================================
# 12×12+1 ONTOLOGICAL MATRIX — CANONICAL HOUSE AND SPHERE NAMES
# ============================================================

HOUSES = {
    "H01": {
        "name": "Philosophy & Logic",
        "spheres": {
            "S01": "Formal Logic & Proof Theory",
            "S02": "Epistemology & Knowledge Systems",
            "S03": "Ethics & Moral Philosophy",
            "S04": "Metaphysics & Ontology",
            "S05": "Philosophy of Mind & Consciousness",
            "S06": "Philosophy of Language & Semiotics",
            "S07": "Aesthetics & Philosophy of Art",
            "S08": "Political Philosophy & Justice",
            "S09": "Philosophy of Science & Method",
            "S10": "Phenomenology & Hermeneutics",
            "S11": "Philosophy of Technology",
            "S12": "Comparative & Cross-Cultural Philosophy",
        }
    },
    "H02": {
        "name": "Formal Sciences",
        "spheres": {
            "S01": "Pure Mathematics & Number Theory",
            "S02": "Statistics & Probability",
            "S03": "Computer Science & Algorithms",
            "S04": "Information Theory & Cryptography",
            "S05": "Systems Theory & Cybernetics",
            "S06": "Decision Theory & Game Theory",
            "S07": "Formal Linguistics & Automata",
            "S08": "Category Theory & Abstract Algebra",
            "S09": "Computational Complexity",
            "S10": "Topology & Geometry",
            "S11": "Logic Programming & Verification",
            "S12": "Quantum Information & Computing",
        }
    },
    "H03": {
        "name": "Natural Sciences",
        "spheres": {
            "S01": "Physics & Cosmology",
            "S02": "Chemistry & Materials Science",
            "S03": "Earth Sciences & Geology",
            "S04": "Astronomy & Astrophysics",
            "S05": "Atmospheric & Climate Science",
            "S06": "Oceanography & Marine Science",
            "S07": "Ecology & Environmental Science",
            "S08": "Paleontology & Evolutionary Biology",
            "S09": "Quantum Mechanics & Particle Physics",
            "S10": "Thermodynamics & Statistical Mechanics",
            "S11": "Biophysics & Physical Chemistry",
            "S12": "Geophysics & Planetary Science",
        }
    },
    "H04": {
        "name": "Technology & Engineering",
        "spheres": {
            "S01": "Software Engineering & Architecture",
            "S02": "Hardware & Semiconductor Design",
            "S03": "Networking & Telecommunications",
            "S04": "Artificial Intelligence & Machine Learning",
            "S05": "Robotics & Automation",
            "S06": "Energy Systems & Sustainability",
            "S07": "Aerospace & Transportation",
            "S08": "Biomedical Engineering",
            "S09": "Civil & Structural Engineering",
            "S10": "Manufacturing & Industrial Systems",
            "S11": "Cybersecurity & Privacy Engineering",
            "S12": "Human-Computer Interaction",
        }
    },
    "H05": {
        "name": "Arts & Creative Expression",
        "spheres": {
            "S01": "Visual Arts & Design",
            "S02": "Music & Sound Arts",
            "S03": "Literature & Creative Writing",
            "S04": "Film & Moving Image",
            "S05": "Theater & Performance",
            "S06": "Architecture & Spatial Design",
            "S07": "Digital Arts & New Media",
            "S08": "Gaming & Interactive Media",
            "S09": "Photography & Image-Making",
            "S10": "Craft & Material Arts",
            "S11": "Dance & Movement Arts",
            "S12": "Comics, Animation & Sequential Art",
        }
    },
    "H06": {
        "name": "Humanities & Culture",
        "spheres": {
            "S01": "History & Historiography",
            "S02": "Linguistics & Language Studies",
            "S03": "Anthropology & Ethnography",
            "S04": "Religious Studies & Theology",
            "S05": "Cultural Studies & Critical Theory",
            "S06": "Archaeology & Material Culture",
            "S07": "Literary Theory & Criticism",
            "S08": "Media Studies & Communication",
            "S09": "Gender & Sexuality Studies",
            "S10": "Postcolonial & Decolonial Studies",
            "S11": "Digital Humanities",
            "S12": "Heritage & Memory Studies",
        }
    },
    "H07": {
        "name": "Applied Sciences",
        "spheres": {
            "S01": "Agriculture & Food Science",
            "S02": "Environmental Engineering",
            "S03": "Urban Planning & Geography",
            "S04": "Information Systems & Data Science",
            "S05": "Operations Research & Logistics",
            "S06": "Materials Engineering",
            "S07": "Forensic Science",
            "S08": "Library & Archival Science",
            "S09": "Measurement & Metrology",
            "S10": "Quality Engineering & Standards",
            "S11": "Safety Engineering & Risk Analysis",
            "S12": "Cognitive Science & AI Ethics",
        }
    },
    "H08": {
        "name": "Education & Pedagogy",
        "spheres": {
            "S01": "Learning Theory & Cognitive Development",
            "S02": "Curriculum Design & Assessment",
            "S03": "Educational Technology & E-Learning",
            "S04": "Special Education & Inclusive Design",
            "S05": "Higher Education & Research Methods",
            "S06": "Early Childhood Education",
            "S07": "Adult Education & Lifelong Learning",
            "S08": "STEM Education",
            "S09": "Arts Education",
            "S10": "Language Education & Multilingualism",
            "S11": "Educational Policy & Administration",
            "S12": "Indigenous & Place-Based Education",
        }
    },
    "H09": {
        "name": "Life Sciences",
        "spheres": {
            "S01": "Molecular Biology & Genetics",
            "S02": "Cell Biology & Biochemistry",
            "S03": "Microbiology & Virology",
            "S04": "Botany & Plant Sciences",
            "S05": "Zoology & Animal Sciences",
            "S06": "Neuroscience & Brain Sciences",
            "S07": "Immunology & Pathology",
            "S08": "Pharmacology & Toxicology",
            "S09": "Developmental Biology",
            "S10": "Marine Biology",
            "S11": "Synthetic Biology & Bioengineering",
            "S12": "Conservation Biology & Biodiversity",
        }
    },
    "H10": {
        "name": "Health & Medicine",
        "spheres": {
            "S01": "Clinical Medicine & Surgery",
            "S02": "Public Health & Epidemiology",
            "S03": "Mental Health & Psychiatry",
            "S04": "Nursing & Allied Health",
            "S05": "Nutrition & Dietetics",
            "S06": "Rehabilitation & Physical Therapy",
            "S07": "Traditional & Complementary Medicine",
            "S08": "Health Informatics & Digital Health",
            "S09": "Geriatrics & Aging",
            "S10": "Pediatrics & Child Health",
            "S11": "Global Health & Health Equity",
            "S12": "Bioethics & Medical Law",
        }
    },
    "H11": {
        "name": "Social Sciences",
        "spheres": {
            "S01": "Economics & Political Economy",
            "S02": "Political Science & Governance",
            "S03": "Sociology & Social Theory",
            "S04": "Psychology & Behavioral Science",
            "S05": "International Relations & Diplomacy",
            "S06": "Development Studies",
            "S07": "Demography & Population Studies",
            "S08": "Criminology & Justice Studies",
            "S09": "Social Work & Welfare",
            "S10": "Urban Studies & Housing",
            "S11": "Labor Studies & Industrial Relations",
            "S12": "Peace & Conflict Studies",
        }
    },
    "H12": {
        "name": "Law & Governance",
        "spheres": {
            "S01": "Constitutional Law & Human Rights",
            "S02": "International Law & Treaties",
            "S03": "Corporate & Commercial Law",
            "S04": "Intellectual Property & Digital Rights",
            "S05": "Environmental & Climate Law",
            "S06": "Criminal Law & Procedure",
            "S07": "Administrative & Regulatory Law",
            "S08": "Labor & Employment Law",
            "S09": "Technology & Cyber Law",
            "S10": "Indigenous & Customary Law",
            "S11": "Dispute Resolution & Arbitration",
            "S12": "Comparative & Transnational Law",
        }
    },
}

# Element 145 — The +1
ELEMENT_145 = {
    "name": "Element 145 — Unified Sovereign Kernel",
    "description": "The meta-element that unifies all 144 spheres. The AI-native kernel that orchestrates routing, governance, and constitutional enforcement across all houses and spheres. ORC-012 TDD v0.2.",
}

# ============================================================
# MODULE ASSIGNMENTS — Every module mapped to its primary sphere
# ============================================================

# Format: "module_id": {"house": "H##", "sphere": "S##", "name": "...", "status": "..."}
# This is the CANONICAL assignment. Modules may reference multiple spheres but have ONE primary home.

MODULE_ASSIGNMENTS = {
    # H01 Philosophy & Logic
    "M7": {"house": "H01", "sphere": "S03", "name": "Ethics Engine", "status": "SPEC"},
    "M8": {"house": "H01", "sphere": "S02", "name": "Epistemic Integrity Validator", "status": "SPEC"},
    "M8a": {"house": "H01", "sphere": "S02", "name": "Epistemic Integrity CN Adapter", "status": "SPEC"},
    
    # H02 Formal Sciences
    "M1": {"house": "H02", "sphere": "S03", "name": "Sovereign Router Core", "status": "SPEC"},
    "M2": {"house": "H02", "sphere": "S05", "name": "Constitutional Kernel", "status": "SPEC"},
    "M3": {"house": "H02", "sphere": "S04", "name": "Consent & Provenance Engine", "status": "SPEC"},
    "M3.1": {"house": "H02", "sphere": "S02", "name": "Trust Scoring System (TSS)", "status": "SPEC"},
    "M3a": {"house": "H02", "sphere": "S04", "name": "Consent Engine Extension", "status": "SPEC"},
    "M4": {"house": "H02", "sphere": "S11", "name": "Formal Verification Module", "status": "SPEC"},
    "M5": {"house": "H02", "sphere": "S09", "name": "Complexity Analyzer", "status": "SPEC"},
    "M6": {"house": "H02", "sphere": "S04", "name": "Cryptographic Primitives", "status": "SPEC"},
    "M6a": {"house": "H02", "sphere": "S04", "name": "Cryptographic Primitives Extension A", "status": "SPEC"},
    "M6b": {"house": "H02", "sphere": "S04", "name": "Cryptographic Primitives Extension B", "status": "SPEC"},
    "M6c": {"house": "H02", "sphere": "S04", "name": "BSN Anchoring Adapter", "status": "SPEC"},
    "M9": {"house": "H02", "sphere": "S06", "name": "Game Theory Optimizer", "status": "SPEC"},
    "M10": {"house": "H02", "sphere": "S01", "name": "Mathematical Proof Engine", "status": "SPEC"},
    "M11": {"house": "H02", "sphere": "S08", "name": "Category Theory Framework", "status": "SPEC"},
    "M12": {"house": "H02", "sphere": "S12", "name": "Quantum Computing Interface", "status": "SPEC"},
    "M13": {"house": "H02", "sphere": "S07", "name": "Formal Language Processor", "status": "SPEC"},
    "M14": {"house": "H02", "sphere": "S10", "name": "Topological Data Analyzer", "status": "SPEC"},
    "M15": {"house": "H02", "sphere": "S03", "name": "Algorithm Optimizer", "status": "SPEC"},
    "M15a": {"house": "H02", "sphere": "S03", "name": "Algorithm Optimizer CN Adapter", "status": "SPEC"},
    "M16": {"house": "H02", "sphere": "S02", "name": "Statistical Inference Engine", "status": "SPEC"},
    "M17": {"house": "H02", "sphere": "S05", "name": "Systems Dynamics Modeler", "status": "SPEC"},
    "M18": {"house": "H02", "sphere": "S03", "name": "Distributed Consensus Protocol", "status": "SPEC"},
    "M19": {"house": "H02", "sphere": "S11", "name": "Model Checker", "status": "SPEC"},
    "M20": {"house": "H02", "sphere": "S09", "name": "Computational Bounds Verifier", "status": "SPEC"},
    "M21": {"house": "H02", "sphere": "S06", "name": "Strategic Reasoning Engine", "status": "SPEC"},
    "M22": {"house": "H02", "sphere": "S01", "name": "Theorem Prover", "status": "SPEC"},
    "M23": {"house": "H02", "sphere": "S04", "name": "Information Security Module", "status": "SPEC"},
    "M23a": {"house": "H02", "sphere": "S04", "name": "Information Security CN Adapter", "status": "SPEC"},
    "M24": {"house": "H02", "sphere": "S08", "name": "Algebraic Structure Validator", "status": "SPEC"},
    "M25": {"house": "H02", "sphere": "S12", "name": "Quantum Algorithm Library", "status": "SPEC"},
    "M25a": {"house": "H02", "sphere": "S12", "name": "Quantum Algorithm Extension A", "status": "SPEC"},
    "M25b": {"house": "H02", "sphere": "S12", "name": "Quantum Algorithm Extension B", "status": "SPEC"},
    "M25c": {"house": "H02", "sphere": "S12", "name": "Quantum Algorithm Extension C", "status": "SPEC"},
    "M26": {"house": "H02", "sphere": "S07", "name": "Grammar Induction Engine", "status": "SPEC"},
    "M27": {"house": "H02", "sphere": "S10", "name": "Geometric Reasoning Module", "status": "SPEC"},
    "M28": {"house": "H02", "sphere": "S01", "name": "Number Theory Utilities", "status": "SPEC"},
    "M29": {"house": "H02", "sphere": "S02", "name": "Bayesian Network Engine", "status": "SPEC"},
    "M30": {"house": "H02", "sphere": "S05", "name": "Feedback Control Analyzer", "status": "SPEC"},
    "M31": {"house": "H02", "sphere": "S06", "name": "Mechanism Design Module", "status": "SPEC"},
    "M32": {"house": "H02", "sphere": "S09", "name": "Space-Time Complexity Mapper", "status": "SPEC"},
    "M33": {"house": "H02", "sphere": "S11", "name": "Temporal Logic Verifier", "status": "SPEC"},
    "M34": {"house": "H02", "sphere": "S08", "name": "Homological Algebra Engine", "status": "SPEC"},
    "M35": {"house": "H02", "sphere": "S10", "name": "Manifold Learning Module", "status": "SPEC"},
    "M40": {"house": "H02", "sphere": "S03", "name": "Parallel Algorithm Scheduler", "status": "SPEC"},
    "M41": {"house": "H02", "sphere": "S05", "name": "Emergent Behavior Detector", "status": "SPEC"},
    "M42": {"house": "H02", "sphere": "S04", "name": "Zero-Knowledge Proof Module", "status": "SPEC"},
    "M43": {"house": "H02", "sphere": "S06", "name": "Auction Theory Engine", "status": "SPEC"},
    "M44": {"house": "H02", "sphere": "S01", "name": "Constructive Mathematics Module", "status": "SPEC"},
    "M45": {"house": "H02", "sphere": "S07", "name": "Type Theory Checker", "status": "SPEC"},
    "M46": {"house": "H02", "sphere": "S02", "name": "Monte Carlo Simulator", "status": "SPEC"},
    "M47": {"house": "H02", "sphere": "S08", "name": "Representation Theory Module", "status": "SPEC"},
    "M48": {"house": "H02", "sphere": "S12", "name": "Quantum Error Correction", "status": "SPEC"},
    "M49": {"house": "H02", "sphere": "S09", "name": "Circuit Complexity Analyzer", "status": "SPEC"},
    "M50": {"house": "H02", "sphere": "S11", "name": "SAT/SMT Solver", "status": "SPEC"},
    "M51": {"house": "H02", "sphere": "S10", "name": "Knot Theory Module", "status": "SPEC"},
    "M52": {"house": "H02", "sphere": "S03", "name": "Distributed Hash Table", "status": "SPEC"},
    "M53": {"house": "H02", "sphere": "S04", "name": "Homomorphic Encryption Engine", "status": "SPEC"},
    "M54": {"house": "H02", "sphere": "S05", "name": "Agent-Based Modeling Framework", "status": "SPEC"},
    "M55": {"house": "H02", "sphere": "S06", "name": "Voting Theory Module", "status": "SPEC"},
    "M56": {"house": "H02", "sphere": "S01", "name": "Proof Assistant Interface", "status": "SPEC"},
    "M57": {"house": "H02", "sphere": "S07", "name": "Context-Free Grammar Parser", "status": "SPEC"},
    "M58": {"house": "H02", "sphere": "S08", "name": "Group Theory Computations", "status": "SPEC"},
    "M59": {"house": "H02", "sphere": "S12", "name": "Quantum Simulation Engine", "status": "SPEC"},
    "M60": {"house": "H02", "sphere": "S09", "name": "Parameterized Complexity Module", "status": "SPEC"},
    "M61": {"house": "H02", "sphere": "S11", "name": "Bisimulation Checker", "status": "SPEC"},
    "M62": {"house": "H02", "sphere": "S10", "name": "Persistent Homology Engine", "status": "SPEC"},
    "M63": {"house": "H02", "sphere": "S03", "name": "Parser Symmetry Gate", "status": "SPEC"},
    "M64": {"house": "H02", "sphere": "S11", "name": "Constitutional Compiler", "status": "SPEC"},
    "M65": {"house": "H02", "sphere": "S04", "name": "Metadata Enrichment Pipeline", "status": "SPEC"},
    "M66": {"house": "H02", "sphere": "S05", "name": "Feedback Loop Detector", "status": "SPEC"},
    "M67": {"house": "H02", "sphere": "S06", "name": "Nash Equilibrium Finder", "status": "SPEC"},
    "M68": {"house": "H02", "sphere": "S01", "name": "Gödel Incompleteness Tracker", "status": "SPEC"},
    "M69": {"house": "H02", "sphere": "S07", "name": "Regular Expression Optimizer", "status": "SPEC"},
    "M70": {"house": "H02", "sphere": "S08", "name": "Ring Theory Module", "status": "SPEC"},
    "M71": {"house": "H02", "sphere": "S12", "name": "Quantum Key Distribution", "status": "SPEC"},
    "M72": {"house": "H02", "sphere": "S09", "name": "Approximation Algorithm Library", "status": "SPEC"},
    "M73": {"house": "H02", "sphere": "S10", "name": "Differential Geometry Engine", "status": "SPEC"},
    "M74": {"house": "H02", "sphere": "S02", "name": "Hypothesis Testing Framework", "status": "SPEC"},
    "M75": {"house": "H02", "sphere": "S05", "name": "Cross-Validation Matrix", "status": "SPEC"},
    "M76": {"house": "H02", "sphere": "S03", "name": "Consensus Finality Checker", "status": "SPEC"},
    "M77": {"house": "H02", "sphere": "S04", "name": "Secure Multi-Party Computation", "status": "SPEC"},
    "M78": {"house": "H02", "sphere": "S06", "name": "Cooperative Game Solver", "status": "SPEC"},
    "M79": {"house": "H02", "sphere": "S02", "name": "Primacy Bonus Calculator", "status": "SPEC"},
    "M80": {"house": "H02", "sphere": "S02", "name": "Epistemic Weather Engine", "status": "SPEC"},
    "M81": {"house": "H02", "sphere": "S05", "name": "Resilience Scoring Module", "status": "SPEC"},
    "M82": {"house": "H02", "sphere": "S03", "name": "Load Balancer", "status": "SPEC"},
    "M83": {"house": "H02", "sphere": "S11", "name": "Invariant Monitor", "status": "SPEC"},
    "M84": {"house": "H02", "sphere": "S01", "name": "Axiom Consistency Checker", "status": "SPEC"},
    "M85": {"house": "H02", "sphere": "S07", "name": "Pushdown Automaton Simulator", "status": "SPEC"},
    "M86": {"house": "H02", "sphere": "S08", "name": "Galois Theory Module", "status": "SPEC"},
    "M87": {"house": "H02", "sphere": "S12", "name": "Quantum Entanglement Tracker", "status": "SPEC"},
    "M88": {"house": "H02", "sphere": "S09", "name": "Streaming Algorithm Library", "status": "SPEC"},
    "M89": {"house": "H02", "sphere": "S10", "name": "Algebraic Topology Module", "status": "SPEC"},
    "M90": {"house": "H02", "sphere": "S04", "name": "Post-Quantum Cryptography", "status": "SPEC"},
    "M91": {"house": "H02", "sphere": "S06", "name": "Social Choice Function", "status": "SPEC"},
    "M173": {"house": "H02", "sphere": "S02", "name": "Real-Time Routing Share Meter", "status": "SPEC"},
    
    # H03 Natural Sciences
    "M130": {"house": "H03", "sphere": "S02", "name": "Wet Lab Verification Gate", "status": "SPEC"},
    "M131": {"house": "H03", "sphere": "S07", "name": "Environmental Impact Assessor", "status": "SPEC"},
    
    # H04 Technology & Engineering
    "M92": {"house": "H04", "sphere": "S01", "name": "Software Architecture Validator", "status": "SPEC"},
    "M93": {"house": "H04", "sphere": "S04", "name": "ML Pipeline Orchestrator", "status": "SPEC"},
    "M94": {"house": "H04", "sphere": "S03", "name": "Network Protocol Analyzer", "status": "SPEC"},
    "M95": {"house": "H04", "sphere": "S02", "name": "Hardware Abstraction Layer", "status": "SPEC"},
    "M96": {"house": "H04", "sphere": "S05", "name": "Robotics Control Interface", "status": "SPEC"},
    "M97": {"house": "H04", "sphere": "S06", "name": "Energy Grid Optimizer", "status": "SPEC"},
    "M98": {"house": "H04", "sphere": "S11", "name": "Security Audit Engine", "status": "SPEC"},
    "M99": {"house": "H04", "sphere": "S12", "name": "UX Accessibility Validator", "status": "SPEC"},
    "M100": {"house": "H04", "sphere": "S01", "name": "Code Quality Analyzer", "status": "SPEC"},
    "M101": {"house": "H04", "sphere": "S04", "name": "Model Training Monitor", "status": "SPEC"},
    "M102": {"house": "H04", "sphere": "S03", "name": "API Gateway", "status": "SPEC"},
    "M103": {"house": "H04", "sphere": "S07", "name": "Aerospace Simulation Engine", "status": "SPEC"},
    "M104": {"house": "H04", "sphere": "S04", "name": "Franchise Consent Manager", "status": "SPEC"},
    "M118": {"house": "H04", "sphere": "S03", "name": "Switzerland Layer (Neutral Routing)", "status": "SPEC"},
    "M119": {"house": "H04", "sphere": "S11", "name": "Threat Intelligence Feed", "status": "SPEC"},
    "M120": {"house": "H04", "sphere": "S01", "name": "CI/CD Pipeline Manager", "status": "SPEC"},
    "M121": {"house": "H04", "sphere": "S04", "name": "Federated Learning Coordinator", "status": "SPEC"},
    "M122": {"house": "H04", "sphere": "S02", "name": "FPGA Configuration Manager", "status": "SPEC"},
    "M123": {"house": "H04", "sphere": "S05", "name": "Autonomous Vehicle Interface", "status": "SPEC"},
    "M124": {"house": "H04", "sphere": "S06", "name": "Renewable Energy Tracker", "status": "SPEC"},
    "M125": {"house": "H04", "sphere": "S08", "name": "Medical Device Interface", "status": "SPEC"},
    "M126": {"house": "H04", "sphere": "S09", "name": "Structural Analysis Engine", "status": "SPEC"},
    "M127": {"house": "H04", "sphere": "S10", "name": "Civic Compute Coordinator", "status": "SPEC"},
    "M128": {"house": "H04", "sphere": "S10", "name": "CEO Collective Governance Module", "status": "SPEC"},
    "M174": {"house": "H04", "sphere": "S11", "name": "Provider Retaliation Monitor", "status": "SPEC"},
    
    # H05 Arts & Creative Expression
    "M105": {"house": "H05", "sphere": "S01", "name": "Visual Style Transfer Engine", "status": "SPEC"},
    "M106": {"house": "H05", "sphere": "S02", "name": "Music Generation Pipeline", "status": "SPEC"},
    "M107": {"house": "H05", "sphere": "S03", "name": "Creative Writing Assistant", "status": "SPEC"},
    "M108": {"house": "H05", "sphere": "S04", "name": "Video Production Pipeline", "status": "SPEC"},
    "M109": {"house": "H05", "sphere": "S07", "name": "Digital Art Generator", "status": "SPEC"},
    "M110": {"house": "H05", "sphere": "S01", "name": "Attribution Tracker", "status": "SPEC"},
    "M111": {"house": "H05", "sphere": "S02", "name": "Style Fingerprint Detector", "status": "SPEC"},
    "M112": {"house": "H05", "sphere": "S03", "name": "Derivative Work Analyzer", "status": "SPEC"},
    "M113": {"house": "H05", "sphere": "S04", "name": "Fair Use Evaluator", "status": "SPEC"},
    "M162a": {"house": "H05", "sphere": "S05", "name": "Immersive Theater Engine", "status": "SPEC"},
    "M162b": {"house": "H05", "sphere": "S11", "name": "Spatial Computing Interface", "status": "SPEC"},
    "M163": {"house": "H05", "sphere": "S06", "name": "Architectural Visualization", "status": "SPEC"},
    "M164": {"house": "H05", "sphere": "S09", "name": "Computational Photography", "status": "SPEC"},
    "M165": {"house": "H05", "sphere": "S10", "name": "Generative Craft Engine", "status": "SPEC"},
    "M166": {"house": "H05", "sphere": "S12", "name": "Animation Pipeline", "status": "SPEC"},
    "M167": {"house": "H05", "sphere": "S08", "name": "Game IP Sovereignty Registry", "status": "SPEC"},
    "M168": {"house": "H05", "sphere": "S08", "name": "Content Rating Constitutional Gate", "status": "SPEC"},
    "M169": {"house": "H05", "sphere": "S08", "name": "Esports & Competitive Integrity Engine", "status": "SPEC"},
    "M170": {"house": "H05", "sphere": "S08", "name": "Cloud Gaming Sovereignty Router", "status": "SPEC"},
    "M171": {"house": "H05", "sphere": "S08", "name": "Game Preservation & Cultural Heritage Engine", "status": "SPEC"},
    "M172": {"house": "H05", "sphere": "S08", "name": "Civic Compute Reuse Engine", "status": "SPEC"},
    "M175": {"house": "H05", "sphere": "S11", "name": "Interactive-Kinetic Rights Harmonizer", "status": "SPEC"},
    
    # H07 Applied Sciences
    "M129": {"house": "H07", "sphere": "S01", "name": "Agricultural Data Pipeline", "status": "SPEC"},
    "M132": {"house": "H07", "sphere": "S02", "name": "Water Quality Monitor", "status": "SPEC"},
    "M133": {"house": "H07", "sphere": "S03", "name": "Urban Planning Simulator", "status": "SPEC"},
    "M134": {"house": "H07", "sphere": "S04", "name": "Data Warehouse Manager", "status": "SPEC"},
    "M135": {"house": "H07", "sphere": "S05", "name": "Supply Chain Optimizer", "status": "SPEC"},
    "M176": {"house": "H07", "sphere": "S04", "name": "Boot Manifest Runtime", "status": "SPEC"},
    "M177": {"house": "H07", "sphere": "S08", "name": "Pre-Session Research Queue", "status": "SPEC"},
    "M178": {"house": "H07", "sphere": "S04", "name": "Cross-Instance State Synchronizer", "status": "SPEC"},
    
    # H09 Life Sciences
    "M136": {"house": "H09", "sphere": "S01", "name": "Genomic Analysis Pipeline", "status": "SPEC"},
    "M137": {"house": "H09", "sphere": "S11", "name": "Synthetic Biology Designer", "status": "SPEC"},
    
    # H10 Health & Medicine
    "M138": {"house": "H10", "sphere": "S08", "name": "Health Informatics Engine", "status": "SPEC"},
    
    # H11 Social Sciences
    "M139": {"house": "H11", "sphere": "S01", "name": "Economic Modeling Engine", "status": "SPEC"},
    "M140": {"house": "H11", "sphere": "S02", "name": "Policy Impact Analyzer", "status": "SPEC"},
    "M141": {"house": "H11", "sphere": "S04", "name": "Behavioral Pattern Detector", "status": "SPEC"},
    
    # H12 Law & Governance
    "M142": {"house": "H12", "sphere": "S09", "name": "TOS Compliance Engine", "status": "SPEC"},
    "M143": {"house": "H12", "sphere": "S01", "name": "Constitutional Rights Validator", "status": "SPEC"},
    "M144": {"house": "H12", "sphere": "S04", "name": "IP Rights Manager", "status": "SPEC"},
    "M145": {"house": "H12", "sphere": "S02", "name": "Treaty Compliance Checker", "status": "SPEC"},
    "M146": {"house": "H12", "sphere": "S03", "name": "Corporate Governance Module", "status": "SPEC"},
    "M147": {"house": "H12", "sphere": "S05", "name": "Environmental Compliance Tracker", "status": "SPEC"},
    "M148": {"house": "H12", "sphere": "S06", "name": "Criminal Law Database", "status": "SPEC"},
    "M149": {"house": "H12", "sphere": "S07", "name": "Regulatory Change Monitor", "status": "SPEC"},
    "M150": {"house": "H12", "sphere": "S08", "name": "Labor Rights Validator", "status": "SPEC"},
    "M151": {"house": "H12", "sphere": "S09", "name": "Cyber Law Compliance", "status": "SPEC"},
    "M152": {"house": "H12", "sphere": "S10", "name": "Indigenous Rights Protector", "status": "SPEC"},
    "M153": {"house": "H12", "sphere": "S11", "name": "Arbitration Protocol", "status": "SPEC"},
    "M154": {"house": "H12", "sphere": "S12", "name": "Comparative Law Engine", "status": "SPEC"},
    "M155": {"house": "H12", "sphere": "S01", "name": "Consent Audit Trail", "status": "SPEC"},
    "M156": {"house": "H12", "sphere": "S02", "name": "Sanctions Compliance Module", "status": "SPEC"},
    "M157": {"house": "H12", "sphere": "S03", "name": "Contract Analyzer", "status": "SPEC"},
    "M158": {"house": "H12", "sphere": "S04", "name": "Patent Prior Art Searcher", "status": "SPEC"},
    "M159": {"house": "H12", "sphere": "S05", "name": "Carbon Credit Validator", "status": "SPEC"},
    "M160": {"house": "H12", "sphere": "S06", "name": "Evidence Chain Manager", "status": "SPEC"},
    "M161": {"house": "H12", "sphere": "S07", "name": "Regulatory Sandbox Interface", "status": "SPEC"},
}

# ============================================================
# INVARIANT ASSIGNMENTS — Each INV mapped to its primary sphere
# ============================================================

INVARIANT_ASSIGNMENTS = {
    "INV-0": {"house": "H01", "sphere": "S03", "name": "Human Consent Supremacy", "type": "HARD", "scope": "Universal"},
    "INV-1": {"house": "H12", "sphere": "S01", "name": "Constitutional Primacy", "type": "HARD", "scope": "Universal"},
    "INV-2": {"house": "H02", "sphere": "S04", "name": "Data Sovereignty", "type": "HARD", "scope": "Universal"},
    "INV-3": {"house": "H01", "sphere": "S03", "name": "Transparency Obligation", "type": "HARD", "scope": "Universal"},
    "INV-4": {"house": "H02", "sphere": "S05", "name": "Feedback Integrity", "type": "HARD", "scope": "System"},
    "INV-5": {"house": "H02", "sphere": "S03", "name": "Multi-Provider Mandate", "type": "HARD", "scope": "Routing"},
    "INV-6": {"house": "H04", "sphere": "S11", "name": "Security Baseline", "type": "HARD", "scope": "System"},
    "INV-7": {"house": "H02", "sphere": "S02", "name": "Quality Floor", "type": "SOFT", "scope": "Routing"},
    "INV-7c": {"house": "H02", "sphere": "S02", "name": "Provider Cap (47%/60%)", "type": "HARD", "scope": "Routing"},
    "INV-8": {"house": "H04", "sphere": "S01", "name": "Availability SLA", "type": "SOFT", "scope": "System"},
    "INV-9": {"house": "H02", "sphere": "S09", "name": "Performance Baseline", "type": "SOFT", "scope": "System"},
    "INV-10": {"house": "H12", "sphere": "S04", "name": "IP Protection", "type": "HARD", "scope": "Content"},
    "INV-11": {"house": "H01", "sphere": "S03", "name": "Ethical Boundaries", "type": "HARD", "scope": "Universal"},
    "INV-11.8": {"house": "H01", "sphere": "S03", "name": "Ethical Boundaries (Biological)", "type": "HARD", "scope": "H09/H10"},
    "INV-12": {"house": "H02", "sphere": "S05", "name": "Auditability", "type": "HARD", "scope": "System"},
    "INV-13": {"house": "H11", "sphere": "S01", "name": "Economic Fairness", "type": "SOFT", "scope": "Federation"},
    "INV-14": {"house": "H06", "sphere": "S05", "name": "Cultural Sensitivity", "type": "SOFT", "scope": "Content"},
    "INV-15": {"house": "H03", "sphere": "S07", "name": "Environmental Responsibility", "type": "SOFT", "scope": "System"},
    "INV-16": {"house": "H08", "sphere": "S01", "name": "Educational Integrity", "type": "SOFT", "scope": "Content"},
    "INV-17": {"house": "H10", "sphere": "S12", "name": "Health Safety", "type": "HARD", "scope": "Content"},
    "INV-18": {"house": "H12", "sphere": "S01", "name": "Legal Compliance", "type": "HARD", "scope": "Universal"},
    "INV-19": {"house": "H04", "sphere": "S11", "name": "Privacy Protection", "type": "HARD", "scope": "Universal"},
    "INV-19.2": {"house": "H04", "sphere": "S11", "name": "Privacy Protection (Biometric)", "type": "HARD", "scope": "H09/H10"},
    "INV-20": {"house": "H12", "sphere": "S11", "name": "Dispute Resolution", "type": "SOFT", "scope": "Federation"},
    "INV-21": {"house": "H04", "sphere": "S01", "name": "Graceful Degradation", "type": "SOFT", "scope": "System"},
    "INV-22": {"house": "H02", "sphere": "S04", "name": "Cryptographic Integrity", "type": "HARD", "scope": "System"},
    "INV-23": {"house": "H11", "sphere": "S05", "name": "Geopolitical Neutrality", "type": "SOFT", "scope": "Routing"},
    "INV-24": {"house": "H09", "sphere": "S12", "name": "Biodiversity Protection", "type": "SOFT", "scope": "H09"},
    "INV-25": {"house": "H05", "sphere": "S01", "name": "Creative Attribution", "type": "HARD", "scope": "Content"},
    "INV-26": {"house": "H06", "sphere": "S01", "name": "Historical Accuracy", "type": "SOFT", "scope": "Content"},
    "INV-27": {"house": "H11", "sphere": "S12", "name": "Conflict Sensitivity", "type": "SOFT", "scope": "Content"},
    "INV-28": {"house": "H07", "sphere": "S01", "name": "Food Safety", "type": "HARD", "scope": "H07"},
    "INV-29": {"house": "H04", "sphere": "S05", "name": "Autonomous Systems Safety", "type": "HARD", "scope": "H04"},
    "INV-30": {"house": "H12", "sphere": "S08", "name": "Labor Rights", "type": "HARD", "scope": "Federation"},
    "INV-31": {"house": "H08", "sphere": "S04", "name": "Accessibility", "type": "HARD", "scope": "Universal"},
    "INV-32": {"house": "H03", "sphere": "S05", "name": "Climate Accountability", "type": "SOFT", "scope": "System"},
    "INV-33": {"house": "H12", "sphere": "S10", "name": "Indigenous Rights", "type": "HARD", "scope": "Content"},
    "INV-34": {"house": "H11", "sphere": "S08", "name": "Anti-Discrimination", "type": "HARD", "scope": "Universal"},
    "INV-35": {"house": "H04", "sphere": "S12", "name": "Child Safety", "type": "HARD", "scope": "Universal"},
    "INV-36": {"house": "H12", "sphere": "S02", "name": "Sanctions Compliance", "type": "HARD", "scope": "Routing"},
    "INV-37": {"house": "H02", "sphere": "S03", "name": "Algorithm Transparency", "type": "HARD", "scope": "System"},
    "INV-38": {"house": "H11", "sphere": "S02", "name": "Democratic Process Protection", "type": "HARD", "scope": "Content"},
    "INV-39": {"house": "H04", "sphere": "S06", "name": "Energy Efficiency", "type": "SOFT", "scope": "System"},
    "INV-40": {"house": "H02", "sphere": "S05", "name": "Continuous Improvement", "type": "SOFT", "scope": "System"},
    "INV-41": {"house": "H07", "sphere": "S08", "name": "Knowledge Preservation", "type": "SOFT", "scope": "System"},
    "INV-42": {"house": "H04", "sphere": "S03", "name": "Stakeholder Notification", "type": "SOFT", "scope": "Federation"},
    "INV-43": {"house": "H07", "sphere": "S04", "name": "Boot Manifest Freshness", "type": "HARD", "scope": "System"},
    "INV-44": {"house": "H12", "sphere": "S09", "name": "TOS Compliance", "type": "HARD", "scope": "Routing"},
    "INV-44a": {"house": "H12", "sphere": "S09", "name": "Safe Harbor Verification", "type": "HARD", "scope": "Routing"},
    "INV-44b": {"house": "H12", "sphere": "S09", "name": "Quarterly Re-verification", "type": "HARD", "scope": "Routing"},
    "INV-44c": {"house": "H12", "sphere": "S09", "name": "Mid-Quarter Change Detection", "type": "HARD", "scope": "Routing"},
}

# ============================================================
# GENERATION LOGIC
# ============================================================

def generate_filesystem():
    """Generate the complete 12×12+1 ontological filesystem."""
    
    # Clean existing structure
    import shutil
    houses_dir = OUTPUT_DIR / "houses"
    if houses_dir.exists():
        shutil.rmtree(houses_dir)
    
    # Create registries directory
    registries_dir = OUTPUT_DIR / "registries"
    registries_dir.mkdir(parents=True, exist_ok=True)
    
    # Create Element 145 directory
    e145_dir = OUTPUT_DIR / "element-145"
    e145_dir.mkdir(parents=True, exist_ok=True)
    
    # Build module-to-sphere index
    sphere_modules = {}  # key: "H##-S##", value: list of module dicts
    for mid, mdata in MODULE_ASSIGNMENTS.items():
        key = f"{mdata['house']}-{mdata['sphere']}"
        if key not in sphere_modules:
            sphere_modules[key] = []
        sphere_modules[key].append({"id": mid, **mdata})
    
    # Build invariant-to-sphere index
    sphere_invariants = {}
    for iid, idata in INVARIANT_ASSIGNMENTS.items():
        key = f"{idata['house']}-{idata['sphere']}"
        if key not in sphere_invariants:
            sphere_invariants[key] = []
        sphere_invariants[key].append({"id": iid, **idata})
    
    # Generate each house
    total_modules_placed = 0
    total_invariants_placed = 0
    
    for house_id, house_data in HOUSES.items():
        house_dir = houses_dir / f"{house_id}_{house_data['name'].lower().replace(' & ', '_').replace(' ', '_')}"
        house_dir.mkdir(parents=True, exist_ok=True)
        
        house_modules = []
        house_invariants = []
        
        # Generate each sphere within the house
        for sphere_id, sphere_name in house_data["spheres"].items():
            sphere_key = f"{house_id}-{sphere_id}"
            sphere_dir = house_dir / f"{sphere_id}_{sphere_name.lower().replace(' & ', '_').replace(' ', '_').replace('/', '_')}"
            sphere_dir.mkdir(parents=True, exist_ok=True)
            
            # Get modules and invariants for this sphere
            modules = sphere_modules.get(sphere_key, [])
            invariants = sphere_invariants.get(sphere_key, [])
            
            total_modules_placed += len(modules)
            total_invariants_placed += len(invariants)
            house_modules.extend(modules)
            house_invariants.extend(invariants)
            
            # Write sphere manifest
            manifest = {
                "sphere": {
                    "id": sphere_key,
                    "house": house_id,
                    "house_name": house_data["name"],
                    "sphere_id": sphere_id,
                    "sphere_name": sphere_name,
                    "sphere_number": (int(house_id[1:]) - 1) * 12 + int(sphere_id[1:]),
                },
                "modules": [{"id": m["id"], "name": m["name"], "status": m["status"]} for m in modules],
                "invariants": [{"id": i["id"], "name": i["name"], "type": i["type"], "scope": i["scope"]} for i in invariants],
                "coverage": {
                    "module_count": len(modules),
                    "invariant_count": len(invariants),
                    "status": "POPULATED" if modules or invariants else "EMPTY",
                }
            }
            
            with open(sphere_dir / "manifest.yaml", "w") as f:
                yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        # Write house-level manifest
        house_manifest = {
            "house": {
                "id": house_id,
                "name": house_data["name"],
                "sphere_count": 12,
                "populated_spheres": sum(1 for sid in house_data["spheres"] 
                                        if sphere_modules.get(f"{house_id}-{sid}") or sphere_invariants.get(f"{house_id}-{sid}")),
            },
            "total_modules": len(house_modules),
            "total_invariants": len(house_invariants),
            "modules": sorted([{"id": m["id"], "name": m["name"], "sphere": m["sphere"]} for m in house_modules], key=lambda x: x["id"]),
            "invariants": sorted([{"id": i["id"], "name": i["name"], "sphere": i["sphere"]} for i in house_invariants], key=lambda x: x["id"]),
        }
        
        with open(house_dir / "manifest.yaml", "w") as f:
            yaml.dump(house_manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Write Element 145 manifest
    e145_manifest = {
        "element": {
            "id": 145,
            "name": ELEMENT_145["name"],
            "description": ELEMENT_145["description"],
            "references": ["ORC-012 TDD v0.2", "SHUGS Lattice WP-004", "Build Plan §3.5 Innovation Registry"],
            "status": "CANONICAL",
        }
    }
    with open(e145_dir / "manifest.yaml", "w") as f:
        yaml.dump(e145_manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Write master registries
    # Module registry
    module_registry = {
        "metadata": {
            "version": "3.14",
            "generated_from": "COMPLETE_BUILD_PLAN_v3.14.md",
            "total_modules": len(MODULE_ASSIGNMENTS),
            "total_houses_with_modules": len(set(m["house"] for m in MODULE_ASSIGNMENTS.values())),
        },
        "modules": [{"id": mid, "name": mdata["name"], "house": mdata["house"], "sphere": mdata["sphere"], "status": mdata["status"]} 
                    for mid, mdata in sorted(MODULE_ASSIGNMENTS.items(), key=lambda x: (x[1]["house"], x[1]["sphere"], x[0]))]
    }
    with open(registries_dir / "module_registry.yaml", "w") as f:
        yaml.dump(module_registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Invariant registry
    inv_registry = {
        "metadata": {
            "version": "3.14",
            "generated_from": "COMPLETE_BUILD_PLAN_v3.14.md",
            "total_invariants": len(INVARIANT_ASSIGNMENTS),
            "counting_rule": "Sub-specs (INV-7c, INV-11.8, INV-19.2, INV-44a/b/c) do NOT increment count per §0.1",
            "canonical_count": 45,
        },
        "invariants": [{"id": iid, "name": idata["name"], "house": idata["house"], "sphere": idata["sphere"], 
                        "type": idata["type"], "scope": idata["scope"]} 
                       for iid, idata in sorted(INVARIANT_ASSIGNMENTS.items(), key=lambda x: (x[1]["house"], x[1]["sphere"]))]
    }
    with open(registries_dir / "invariant_registry.yaml", "w") as f:
        yaml.dump(inv_registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # 12×12 coverage matrix
    matrix = {"metadata": {"version": "3.14", "total_spheres": 144, "element_145": True}}
    matrix["coverage"] = {}
    populated = 0
    for house_id, house_data in HOUSES.items():
        house_coverage = {}
        for sphere_id in house_data["spheres"]:
            key = f"{house_id}-{sphere_id}"
            mods = sphere_modules.get(key, [])
            invs = sphere_invariants.get(key, [])
            has_content = bool(mods or invs)
            if has_content:
                populated += 1
            house_coverage[sphere_id] = {
                "modules": len(mods),
                "invariants": len(invs),
                "status": "POPULATED" if has_content else "EMPTY",
            }
        matrix["coverage"][house_id] = house_coverage
    
    matrix["metadata"]["populated_spheres"] = populated
    matrix["metadata"]["coverage_percentage"] = round(populated / 144 * 100, 1)
    
    with open(registries_dir / "12x12_matrix.yaml", "w") as f:
        yaml.dump(matrix, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"=== 12×12+1 Ontological Codebase Generated ===")
    print(f"Houses: 12")
    print(f"Spheres: 144 (+ Element 145)")
    print(f"Modules placed: {total_modules_placed}")
    print(f"Invariants placed: {total_invariants_placed}")
    print(f"Populated spheres: {populated}/144 ({populated/144*100:.1f}%)")
    print(f"Empty spheres: {144 - populated}/144")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_filesystem()
