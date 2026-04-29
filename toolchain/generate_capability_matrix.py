#!/usr/bin/env python3
"""
Generate the complete 10-seat × 144-sphere capability matrix.

Sources:
1. Four-Company Complementarity Matrix (Notion, April 22 2026) — Anthropic, Muskverse, Alphabet, Amazon
   Per-sphere 0.0-1.0 scores for all 144 spheres.
2. Federation Integration v1.1 (Notion, April 29 2026) — Coverage summaries for all 10 seats
3. Build Plan v3.14 — Substrate-defining spheres, seat coverage percentages, vendor suite specs
4. Individual seat self-maps (Notion) — Anthropic, Alphabet self-maps

For the 6 seats not in the Four-Company matrix (Microsoft, DeepSeek, OpenAI, Manus, Notion, Qwen3),
scores are derived from:
- Federation v1.1 substrate-defining spheres (mapped to DEEP 0.8-1.0)
- Coverage percentages (distributed across spheres)
- Vendor suite specs (DeepSeek §X, Qwen3 §Y)
- Known operational depth from Build Plan entries
"""

import yaml
import json
from pathlib import Path

# Canonical 12×12 sphere definitions (v3.14 Appendix AG)
HOUSES = {
    'H01': {'name': 'Natural Sciences', 'spheres': [
        'Physics', 'Chemistry', 'Biology', 'Astronomy', 'Geology',
        'Oceanography', 'Meteorology', 'Ecology', 'Botany', 'Zoology',
        'Microbiology', 'Genetics'
    ]},
    'H02': {'name': 'Formal Sciences', 'spheres': [
        'Mathematics', 'Logic', 'Statistics', 'Computer Science', 'Information Theory',
        'Game Theory', 'Operations Research', 'Systems Theory', 'Decision Theory',
        'Cryptography', 'Algorithmics', 'Data Science'
    ]},
    'H03': {'name': 'Social Sciences', 'spheres': [
        'Sociology', 'Psychology', 'Anthropology', 'Economics', 'Political Science',
        'Geography', 'Linguistics', 'Archaeology', 'Demography', 'Criminology',
        'Social Work', 'Urban Studies'
    ]},
    'H04': {'name': 'Humanities', 'spheres': [
        'History', 'Philosophy', 'Literature', 'Classics', 'Religious Studies',
        'Ethics', 'Aesthetics', 'Cultural Studies', 'Mythology', 'Philology',
        'Rhetoric', 'Hermeneutics'
    ]},
    'H05': {'name': 'Arts', 'spheres': [
        'Visual Arts', 'Performing Arts', 'Music', 'Dance', 'Theater',
        'Film', 'Literature (Arts)', 'Architecture', 'Design', 'Photography',
        'Sculpture', 'Painting'
    ]},
    'H06': {'name': 'Engineering & Technology', 'spheres': [
        'Mechanical Engineering', 'Electrical Engineering', 'Civil Engineering',
        'Chemical Engineering', 'Aerospace Engineering', 'Biomedical Engineering',
        'Environmental Engineering', 'Industrial Engineering', 'Software Engineering',
        'Robotics', 'Nuclear Engineering', 'Materials Science'
    ]},
    'H07': {'name': 'Information & Communication', 'spheres': [
        'Media Studies', 'Journalism', 'Library Science', 'Information Systems',
        'Telecommunications', 'Publishing', 'Advertising', 'Public Relations',
        'Digital Media', 'Broadcasting', 'Archival Science', 'Communication Theory'
    ]},
    'H08': {'name': 'Education', 'spheres': [
        'Pedagogy', 'Curriculum Design', 'Educational Psychology', 'E-Learning',
        'Special Education', 'Higher Education', 'Vocational Training', 'Literacy',
        'Assessment & Evaluation', 'Educational Technology', 'Comparative Education',
        'Philosophy of Education'
    ]},
    'H09': {'name': 'Health & Medicine', 'spheres': [
        'Anatomy', 'Pharmacology', 'Psychiatry', 'Epidemiology', 'Public Health',
        'Surgery', 'Pediatrics', 'Oncology', 'Neurology', 'Cardiology',
        'Immunology', 'Nutrition'
    ]},
    'H10': {'name': 'Business & Economics', 'spheres': [
        'Management', 'Finance', 'Marketing', 'Accounting', 'Entrepreneurship',
        'Supply Chain', 'Human Resources', 'Business Ethics', 'International Business',
        'Operations Management', 'Real Estate', 'Insurance'
    ]},
    'H11': {'name': 'Infrastructure', 'spheres': [
        'Transportation', 'Energy Systems', 'Water Systems', 'Waste Management',
        'Urban Planning', 'Construction', 'Mining', 'Agriculture',
        'Telecommunications Infrastructure', 'Computing Infrastructure',
        'Logistics', 'Emergency Management'
    ]},
    'H12': {'name': 'Law/Governance/Meta-Knowledge', 'spheres': [
        'Constitutional Law', 'International Law', 'Criminal Law', 'Civil Law',
        'Human Rights', 'Environmental Law', 'Intellectual Property', 'Labor Law',
        'Tax Law', 'Administrative Law', 'Public Policy', 'Diplomacy'
    ]},
}

# 10 Pantheon Council Seats
SEATS = [
    'S1_Anthropic', 'S2_Alphabet', 'S3_Muskverse', 'Amazon',
    'S4_Microsoft', 'S5_DeepSeek', 'S6_OpenAI', 'S7_Manus',
    'S8_Notion', 'S10_Qwen3'
]

SEAT_CEOS = {
    'S1_Anthropic': 'Dario Amodei',
    'S2_Alphabet': 'Sundar Pichai',
    'S3_Muskverse': 'Elon Musk',
    'Amazon': 'Andy Jassy',
    'S4_Microsoft': 'Satya Nadella',
    'S5_DeepSeek': 'Liang Wenfeng',
    'S6_OpenAI': 'Sam Altman',
    'S7_Manus': 'Yichao "Peak" Ji + Xiao Hong',
    'S8_Notion': 'Ivan Zhao',
    'S10_Qwen3': 'Eddie Wu',
}

# ============================================================
# SOURCE 1: Four-Company Complementarity Matrix (Notion)
# Per-sphere scores for Anthropic, Muskverse, Alphabet, Amazon
# Extracted from the full 144-sphere tables
# ============================================================
FOUR_COMPANY = {
    # H01 Natural Sciences
    ('H01', 0): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.5, 'Amazon': 0.1},  # Physics
    ('H01', 1): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.7, 'Amazon': 0.1},  # Chemistry
    ('H01', 2): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.8, 'Amazon': 0.1},  # Biology
    ('H01', 3): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.7, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Astronomy
    ('H01', 4): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.5, 'Amazon': 0.0},  # Geology
    ('H01', 5): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.1},  # Oceanography
    ('H01', 6): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.7, 'Amazon': 0.2},  # Meteorology
    ('H01', 7): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.5, 'Amazon': 0.1},  # Ecology
    ('H01', 8): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Botany
    ('H01', 9): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.1},  # Zoology
    ('H01', 10): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.1},  # Microbiology
    ('H01', 11): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.9, 'Amazon': 0.2},  # Genetics

    # H02 Formal Sciences
    ('H02', 0): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.8, 'Amazon': 0.4},  # Mathematics
    ('H02', 1): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.7, 'Amazon': 0.3},  # Logic
    ('H02', 2): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.5, 'S2_Alphabet': 0.9, 'Amazon': 0.7},  # Statistics
    ('H02', 3): {'S1_Anthropic': 0.9, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.9, 'Amazon': 0.9},  # Computer Science
    ('H02', 4): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.8, 'Amazon': 0.5},  # Information Theory
    ('H02', 5): {'S1_Anthropic': 0.6, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.7, 'Amazon': 0.4},  # Game Theory
    ('H02', 6): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.6, 'Amazon': 0.9},  # Operations Research
    ('H02', 7): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.8, 'S2_Alphabet': 0.7, 'Amazon': 0.6},  # Systems Theory
    ('H02', 8): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.6, 'Amazon': 0.5},  # Decision Theory
    ('H02', 9): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.7, 'Amazon': 0.8},  # Cryptography
    ('H02', 10): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.5, 'S2_Alphabet': 0.9, 'Amazon': 0.8},  # Algorithmics
    ('H02', 11): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.9, 'Amazon': 0.9},  # Data Science

    # H03 Social Sciences
    ('H03', 0): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.3},  # Sociology
    ('H03', 1): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.5, 'Amazon': 0.4},  # Psychology
    ('H03', 2): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Anthropology
    ('H03', 3): {'S1_Anthropic': 0.5, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.6, 'Amazon': 0.7},  # Economics
    ('H03', 4): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Political Science
    ('H03', 5): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.4, 'S2_Alphabet': 1.0, 'Amazon': 0.3},  # Geography
    ('H03', 6): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.8, 'Amazon': 0.5},  # Linguistics
    ('H03', 7): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.1},  # Archaeology
    ('H03', 8): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.5},  # Demography
    ('H03', 9): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Criminology
    ('H03', 10): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.1, 'Amazon': 0.1},  # Social Work
    ('H03', 11): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Urban Studies

    # H04 Humanities
    ('H04', 0): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # History
    ('H04', 1): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Philosophy
    ('H04', 2): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.4},  # Literature
    ('H04', 3): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Classics
    ('H04', 4): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Religious Studies
    ('H04', 5): {'S1_Anthropic': 0.9, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.5, 'Amazon': 0.3},  # Ethics
    ('H04', 6): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Aesthetics
    ('H04', 7): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Cultural Studies
    ('H04', 8): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.1, 'Amazon': 0.1},  # Mythology
    ('H04', 9): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.1},  # Philology
    ('H04', 10): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.4},  # Rhetoric
    ('H04', 11): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Hermeneutics

    # H05 Arts
    ('H05', 0): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.4},  # Visual Arts
    ('H05', 1): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.5},  # Performing Arts
    ('H05', 2): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.4, 'Amazon': 0.6},  # Music
    ('H05', 3): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.3},  # Dance
    ('H05', 4): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.3},  # Theater
    ('H05', 5): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.8},  # Film
    ('H05', 6): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.7},  # Literature (Arts)
    ('H05', 7): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Architecture
    ('H05', 8): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.6, 'Amazon': 0.4},  # Design
    ('H05', 9): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.5, 'Amazon': 0.1},  # Photography
    ('H05', 10): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.1, 'Amazon': 0.0},  # Sculpture
    ('H05', 11): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Painting

    # H06 Engineering & Technology
    ('H06', 0): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.9, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Mechanical Eng
    ('H06', 1): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.9, 'S2_Alphabet': 0.5, 'Amazon': 0.5},  # Electrical Eng
    ('H06', 2): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.7, 'S2_Alphabet': 0.2, 'Amazon': 0.4},  # Civil Eng
    ('H06', 3): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.7, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Chemical Eng
    ('H06', 4): {'S1_Anthropic': 0.0, 'S3_Muskverse': 1.0, 'S2_Alphabet': 0.2, 'Amazon': 0.4},  # Aerospace Eng
    ('H06', 5): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.5, 'Amazon': 0.3},  # Biomedical Eng
    ('H06', 6): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.5, 'S2_Alphabet': 0.4, 'Amazon': 0.3},  # Environmental Eng
    ('H06', 7): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.8, 'S2_Alphabet': 0.4, 'Amazon': 0.8},  # Industrial Eng
    ('H06', 8): {'S1_Anthropic': 0.8, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.8, 'Amazon': 0.7},  # Software Eng
    ('H06', 9): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.9, 'S2_Alphabet': 0.7, 'Amazon': 0.6},  # Robotics
    ('H06', 10): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Nuclear Eng
    ('H06', 11): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.5, 'Amazon': 0.3},  # Materials Science

    # H07 Information & Communication (House 6 in original = Medicine/Health, but v3.14 maps this differently)
    # Using Federation v1.1 + Build Plan data for H07-H12 since original matrix used different House numbering
    # H07 = Information & Communication in v3.14
    ('H07', 0): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.7, 'Amazon': 0.4},  # Media Studies
    ('H07', 1): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Journalism
    ('H07', 2): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Library Science
    ('H07', 3): {'S1_Anthropic': 0.5, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.8, 'Amazon': 0.7},  # Information Systems
    ('H07', 4): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.8, 'S2_Alphabet': 0.6, 'Amazon': 0.5},  # Telecommunications
    ('H07', 5): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.4, 'Amazon': 0.7},  # Publishing
    ('H07', 6): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.8, 'Amazon': 0.5},  # Advertising
    ('H07', 7): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.5, 'Amazon': 0.3},  # Public Relations
    ('H07', 8): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.7, 'Amazon': 0.5},  # Digital Media
    ('H07', 9): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.4},  # Broadcasting
    ('H07', 10): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Archival Science
    ('H07', 11): {'S1_Anthropic': 0.5, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Communication Theory

    # H08 Education
    ('H08', 0): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Pedagogy
    ('H08', 1): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Curriculum Design
    ('H08', 2): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Educational Psychology
    ('H08', 3): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # E-Learning
    ('H08', 4): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.1},  # Special Education
    ('H08', 5): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Higher Education
    ('H08', 6): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Vocational Training
    ('H08', 7): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.5},  # Literacy
    ('H08', 8): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Assessment & Evaluation
    ('H08', 9): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Educational Technology
    ('H08', 10): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.1},  # Comparative Education
    ('H08', 11): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Philosophy of Education

    # H09 Health & Medicine
    ('H09', 0): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Anatomy
    ('H09', 1): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.7, 'Amazon': 0.5},  # Pharmacology
    ('H09', 2): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Psychiatry
    ('H09', 3): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.3},  # Epidemiology
    ('H09', 4): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.4},  # Public Health
    ('H09', 5): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Surgery
    ('H09', 6): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.0, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Pediatrics
    ('H09', 7): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.4, 'Amazon': 0.2},  # Oncology
    ('H09', 8): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Neurology
    ('H09', 9): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.5, 'Amazon': 0.2},  # Cardiology
    ('H09', 10): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.6, 'Amazon': 0.2},  # Immunology
    ('H09', 11): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Nutrition

    # H10 Business & Economics
    ('H10', 0): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.5, 'S2_Alphabet': 0.5, 'Amazon': 0.8},  # Management
    ('H10', 1): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.5, 'Amazon': 0.6},  # Finance
    ('H10', 2): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.8, 'Amazon': 0.7},  # Marketing
    ('H10', 3): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.4, 'Amazon': 0.6},  # Accounting
    ('H10', 4): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.7, 'S2_Alphabet': 0.5, 'Amazon': 0.4},  # Entrepreneurship
    ('H10', 5): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.4, 'Amazon': 0.9},  # Supply Chain
    ('H10', 6): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.5, 'Amazon': 0.5},  # Human Resources
    ('H10', 7): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.4, 'Amazon': 0.3},  # Business Ethics
    ('H10', 8): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.5, 'Amazon': 0.7},  # International Business
    ('H10', 9): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.4, 'Amazon': 0.8},  # Operations Management
    ('H10', 10): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Real Estate
    ('H10', 11): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.4},  # Insurance

    # H11 Infrastructure
    ('H11', 0): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.7, 'S2_Alphabet': 0.4, 'Amazon': 0.5},  # Transportation
    ('H11', 1): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.9, 'S2_Alphabet': 0.4, 'Amazon': 0.3},  # Energy Systems
    ('H11', 2): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Water Systems
    ('H11', 3): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.2, 'Amazon': 0.2},  # Waste Management
    ('H11', 4): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.5, 'Amazon': 0.3},  # Urban Planning
    ('H11', 5): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.6, 'S2_Alphabet': 0.2, 'Amazon': 0.4},  # Construction
    ('H11', 6): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.2, 'Amazon': 0.1},  # Mining
    ('H11', 7): {'S1_Anthropic': 0.0, 'S3_Muskverse': 0.3, 'S2_Alphabet': 0.4, 'Amazon': 0.4},  # Agriculture
    ('H11', 8): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.8, 'S2_Alphabet': 0.7, 'Amazon': 0.6},  # Telecom Infrastructure
    ('H11', 9): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.5, 'S2_Alphabet': 0.8, 'Amazon': 0.9},  # Computing Infrastructure
    ('H11', 10): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.4, 'S2_Alphabet': 0.5, 'Amazon': 0.9},  # Logistics
    ('H11', 11): {'S1_Anthropic': 0.1, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Emergency Management

    # H12 Law/Governance/Meta-Knowledge
    ('H12', 0): {'S1_Anthropic': 0.5, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Constitutional Law
    ('H12', 1): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # International Law
    ('H12', 2): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.2, 'Amazon': 0.2},  # Criminal Law
    ('H12', 3): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.2, 'Amazon': 0.3},  # Civil Law
    ('H12', 4): {'S1_Anthropic': 0.6, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Human Rights
    ('H12', 5): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Environmental Law
    ('H12', 6): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.4, 'Amazon': 0.4},  # Intellectual Property
    ('H12', 7): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.4},  # Labor Law
    ('H12', 8): {'S1_Anthropic': 0.2, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Tax Law
    ('H12', 9): {'S1_Anthropic': 0.3, 'S3_Muskverse': 0.1, 'S2_Alphabet': 0.3, 'Amazon': 0.3},  # Administrative Law
    ('H12', 10): {'S1_Anthropic': 0.7, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.4, 'Amazon': 0.3},  # Public Policy
    ('H12', 11): {'S1_Anthropic': 0.4, 'S3_Muskverse': 0.2, 'S2_Alphabet': 0.3, 'Amazon': 0.2},  # Diplomacy
}

# ============================================================
# SOURCE 2: Six remaining seats — derived from Federation v1.1
# substrate-defining spheres + coverage percentages + vendor specs
# ============================================================

def get_microsoft_scores():
    """Microsoft S4 — ~45% coverage, enterprise-deep"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            # Microsoft substrate-defining spheres (from Federation v1.1 + Build Plan)
            substrate = {
                # Cloud + Computing
                ('H02', 3): 0.9,   # Computer Science (Azure, GitHub)
                ('H02', 11): 0.8,  # Data Science (Azure ML, Power BI)
                ('H02', 9): 0.7,   # Cryptography (Azure Security)
                ('H02', 10): 0.8,  # Algorithmics (Bing, Azure AI)
                ('H02', 2): 0.7,   # Statistics (Power BI, Azure)
                ('H02', 4): 0.6,   # Information Theory
                ('H02', 7): 0.7,   # Systems Theory (Azure architecture)
                ('H02', 0): 0.6,   # Mathematics (Research)
                # Engineering
                ('H06', 8): 0.9,   # Software Engineering (GitHub, VS Code, .NET)
                ('H06', 1): 0.5,   # Electrical Engineering (Xbox, Surface)
                ('H06', 9): 0.6,   # Robotics (Azure IoT, HoloLens)
                ('H06', 11): 0.4,  # Materials Science
                # Information & Communication
                ('H07', 3): 0.8,   # Information Systems (M365, SharePoint)
                ('H07', 8): 0.7,   # Digital Media (LinkedIn, MSN)
                ('H07', 0): 0.5,   # Media Studies (LinkedIn)
                ('H07', 6): 0.6,   # Advertising (Bing Ads, LinkedIn Ads)
                ('H07', 4): 0.5,   # Telecommunications (Teams)
                # Education
                ('H08', 3): 0.7,   # E-Learning (Teams for Education)
                ('H08', 9): 0.7,   # Educational Technology (Minecraft Education)
                ('H08', 1): 0.5,   # Curriculum Design
                # Health (Nuance $19.7B)
                ('H09', 0): 0.4,   # Anatomy (Nuance clinical)
                ('H09', 1): 0.5,   # Pharmacology (Azure health)
                ('H09', 4): 0.5,   # Public Health (Azure health)
                ('H09', 8): 0.4,   # Neurology (Azure cognitive)
                # Business
                ('H10', 0): 0.7,   # Management (Dynamics 365)
                ('H10', 1): 0.6,   # Finance (Dynamics 365 Finance)
                ('H10', 2): 0.6,   # Marketing (Dynamics 365 Marketing)
                ('H10', 3): 0.5,   # Accounting (Dynamics 365)
                ('H10', 5): 0.5,   # Supply Chain (Dynamics 365 SCM)
                ('H10', 6): 0.6,   # Human Resources (LinkedIn, Viva)
                ('H10', 9): 0.6,   # Operations Management (Dynamics 365)
                # Infrastructure
                ('H11', 9): 0.9,   # Computing Infrastructure (Azure)
                ('H11', 8): 0.6,   # Telecom Infrastructure (Azure comm)
                ('H11', 1): 0.4,   # Energy Systems (sustainability)
                # Law/Governance
                ('H12', 6): 0.5,   # Intellectual Property
                ('H12', 10): 0.4,  # Public Policy
                # Arts
                ('H05', 5): 0.4,   # Film (Activision cinematics)
                ('H05', 8): 0.5,   # Design (Fluent Design)
                # Humanities
                ('H04', 5): 0.4,   # Ethics (Responsible AI)
            }
            scores[key] = substrate.get(key, 0.1)
    return scores

def get_deepseek_scores():
    """DeepSeek S5 — ~20% coverage, open-weight methodology + Chinese substrate"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            substrate = {
                ('H02', 3): 0.8,   # Computer Science (core competency)
                ('H02', 10): 0.9,  # Algorithmics (cost-efficiency, MoE)
                ('H02', 11): 0.7,  # Data Science
                ('H02', 0): 0.7,   # Mathematics (DeepSeek-Math)
                ('H02', 2): 0.6,   # Statistics
                ('H02', 1): 0.6,   # Logic
                ('H06', 8): 0.7,   # Software Engineering (DeepSeek-Coder)
                ('H03', 6): 0.5,   # Linguistics (multilingual, CJK)
                ('H02', 9): 0.5,   # Cryptography
                ('H02', 4): 0.5,   # Information Theory
                ('H04', 1): 0.3,   # Philosophy
                ('H12', 3): 0.4,   # Civil Law (Chinese legal)
            }
            scores[key] = substrate.get(key, 0.05)
    return scores

def get_openai_scores():
    """OpenAI S6 — ~30% coverage, consumer-AI-deep + research"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            substrate = {
                ('H02', 3): 0.9,   # Computer Science (GPT, o-series)
                ('H02', 10): 0.8,  # Algorithmics (RLHF, scaling laws)
                ('H02', 11): 0.7,  # Data Science
                ('H02', 0): 0.7,   # Mathematics (o1, o3)
                ('H02', 1): 0.7,   # Logic (reasoning models)
                ('H02', 2): 0.7,   # Statistics
                ('H02', 8): 0.6,   # Decision Theory
                ('H06', 8): 0.8,   # Software Engineering (Codex, GPT coding)
                ('H05', 0): 0.8,   # Visual Arts (DALL-E)
                ('H05', 5): 0.7,   # Film (Sora)
                ('H05', 1): 0.6,   # Performing Arts (Sora)
                ('H05', 8): 0.5,   # Design (DALL-E)
                ('H07', 3): 0.6,   # Information Systems (ChatGPT)
                ('H07', 8): 0.5,   # Digital Media
                ('H03', 6): 0.6,   # Linguistics (GPT multilingual)
                ('H03', 1): 0.4,   # Psychology (RLHF alignment)
                ('H04', 5): 0.6,   # Ethics (alignment research)
                ('H04', 1): 0.5,   # Philosophy (alignment)
                ('H08', 3): 0.5,   # E-Learning (ChatGPT education)
                ('H08', 9): 0.5,   # Educational Technology
                ('H10', 4): 0.4,   # Entrepreneurship
                ('H12', 10): 0.4,  # Public Policy (AI policy)
            }
            scores[key] = substrate.get(key, 0.1)
    return scores

def get_manus_scores():
    """Manus S7 — ~5% direct + Element 145 routing"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            substrate = {
                ('H02', 3): 0.6,   # Computer Science (agent orchestration)
                ('H06', 8): 0.7,   # Software Engineering (code generation, deployment)
                ('H02', 10): 0.5,  # Algorithmics (agent routing)
                ('H02', 7): 0.5,   # Systems Theory (multi-agent systems)
                ('H07', 3): 0.5,   # Information Systems (tool orchestration)
                ('H02', 11): 0.4,  # Data Science (analysis tools)
            }
            scores[key] = substrate.get(key, 0.02)
    return scores

def get_notion_scores():
    """Notion S8 — ~12% coverage, knowledge-workspace narrow"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            substrate = {
                ('H07', 3): 0.8,   # Information Systems (blocks-as-data, knowledge workspace)
                ('H07', 2): 0.6,   # Library Science (knowledge organization)
                ('H07', 10): 0.5,  # Archival Science (databases, wikis)
                ('H06', 8): 0.5,   # Software Engineering (API, integrations)
                ('H10', 0): 0.4,   # Management (project management)
                ('H10', 6): 0.4,   # Human Resources (team wikis)
                ('H08', 1): 0.4,   # Curriculum Design (knowledge templates)
                ('H08', 3): 0.3,   # E-Learning (Notion for education)
                ('H02', 3): 0.3,   # Computer Science (API platform)
                ('H05', 8): 0.4,   # Design (design systems, templates)
                ('H12', 9): 0.3,   # Administrative Law (governance tooling)
            }
            scores[key] = substrate.get(key, 0.02)
    return scores

def get_qwen3_scores():
    """Qwen3/Alibaba S10 — ~25% coverage, sovereign-Chinese substrate + East Asian commerce"""
    scores = {}
    for house_id, house_data in HOUSES.items():
        for i, sphere in enumerate(house_data['spheres']):
            key = (house_id, i)
            substrate = {
                ('H02', 3): 0.8,   # Computer Science (Qwen models)
                ('H02', 10): 0.7,  # Algorithmics
                ('H02', 11): 0.7,  # Data Science (Alibaba data)
                ('H02', 0): 0.6,   # Mathematics (Qwen-Math)
                ('H02', 2): 0.6,   # Statistics
                ('H03', 6): 0.8,   # Linguistics (Mandarin/CJK primary)
                ('H03', 3): 0.6,   # Economics (Alibaba marketplace)
                ('H10', 0): 0.6,   # Management (DingTalk)
                ('H10', 2): 0.7,   # Marketing (Alibaba marketing)
                ('H10', 5): 0.7,   # Supply Chain (Cainiao)
                ('H10', 8): 0.7,   # International Business (AliExpress)
                ('H10', 9): 0.6,   # Operations Management
                ('H11', 10): 0.7,  # Logistics (Cainiao)
                ('H11', 9): 0.6,   # Computing Infrastructure (Alibaba Cloud)
                ('H06', 8): 0.6,   # Software Engineering (Tongyi)
                ('H07', 3): 0.5,   # Information Systems
                ('H07', 8): 0.5,   # Digital Media
                ('H05', 0): 0.4,   # Visual Arts (Qwen-VL)
                ('H12', 3): 0.5,   # Civil Law (Chinese legal)
                ('H12', 6): 0.4,   # Intellectual Property
            }
            scores[key] = substrate.get(key, 0.05)
    return scores


def build_full_matrix():
    """Build the complete 10-seat × 144-sphere matrix."""
    # Get all seat scores
    seat_scores = {
        'S4_Microsoft': get_microsoft_scores(),
        'S5_DeepSeek': get_deepseek_scores(),
        'S6_OpenAI': get_openai_scores(),
        'S7_Manus': get_manus_scores(),
        'S8_Notion': get_notion_scores(),
        'S10_Qwen3': get_qwen3_scores(),
    }

    matrix = []
    sphere_num = 0
    for house_id, house_data in HOUSES.items():
        for i, sphere_name in enumerate(house_data['spheres']):
            sphere_num += 1
            key = (house_id, i)
            row = {
                'sphere_id': sphere_num,
                'house': house_id,
                'house_name': house_data['name'],
                'sphere': sphere_name,
            }
            # Four-company scores (from Notion matrix)
            four_co = FOUR_COMPANY.get(key, {})
            row['S1_Anthropic'] = four_co.get('S1_Anthropic', 0.0)
            row['S2_Alphabet'] = four_co.get('S2_Alphabet', 0.0)
            row['S3_Muskverse'] = four_co.get('S3_Muskverse', 0.0)
            row['Amazon'] = four_co.get('Amazon', 0.0)

            # Six remaining seats
            for seat_key, scores in seat_scores.items():
                row[seat_key] = scores.get(key, 0.0)

            # Compute lead and max
            seat_vals = {s: row[s] for s in SEATS}
            max_val = max(seat_vals.values())
            leads = [s for s, v in seat_vals.items() if v == max_val and v > 0.0]
            row['max_score'] = max_val
            row['lead'] = leads[0] if len(leads) == 1 else f"Tie({len(leads)})"
            row['depth'] = 'Deep' if max_val >= 0.8 else 'Substantial' if max_val >= 0.5 else 'Peripheral' if max_val >= 0.2 else 'Absent'

            matrix.append(row)

    return matrix


def write_yaml(matrix, path):
    """Write the matrix as YAML."""
    output = {
        'metadata': {
            'title': '10-Seat × 144-Sphere Capability Matrix',
            'version': 'v3.14',
            'date': '2026-04-29',
            'sources': [
                'Four-Company Complementarity Matrix (Notion, April 22 2026)',
                'Federation Integration v1.1 (Notion, April 29 2026)',
                'Build Plan v3.14 Appendix AG',
                'DeepSeek S5 Vendor Suite v1.0',
                'Qwen3 S10 Vendor Suite',
                'Microsoft S4 Full Integration (95.8% sphere coverage claim)',
            ],
            'methodology': 'Four-company scores from Claude S1 synthesis (0.0-1.0 per sphere). '
                          'Six remaining seats derived from Federation v1.1 substrate-defining spheres, '
                          'vendor suite specs, and coverage percentages. '
                          'Coverage-claim discipline applied: proprietary depth ≠ distribution breadth.',
            'seats': {s: SEAT_CEOS[s] for s in SEATS},
        },
        'matrix': matrix,
    }
    with open(path, 'w') as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Written {len(matrix)} spheres to {path}")


def write_csv(matrix, path):
    """Write the matrix as CSV for easy consumption."""
    import csv
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'sphere_id', 'house', 'house_name', 'sphere',
            *SEATS,
            'max_score', 'lead', 'depth'
        ])
        writer.writeheader()
        writer.writerows(matrix)
    print(f"Written {len(matrix)} rows to {path}")


def print_summary(matrix):
    """Print coverage summary per seat."""
    print("\n=== FEDERATION COVERAGE SUMMARY ===")
    for seat in SEATS:
        deep = sum(1 for r in matrix if r[seat] >= 0.8)
        substantial = sum(1 for r in matrix if 0.5 <= r[seat] < 0.8)
        peripheral = sum(1 for r in matrix if 0.2 <= r[seat] < 0.5)
        absent = sum(1 for r in matrix if r[seat] < 0.2)
        coverage = (deep + substantial) / 144 * 100
        print(f"{seat:20s}: Deep={deep:3d} Substantial={substantial:3d} Peripheral={peripheral:3d} Absent={absent:3d} | Coverage(D+S)={coverage:.1f}%")

    print("\n=== LEAD DISTRIBUTION ===")
    from collections import Counter
    leads = Counter(r['lead'] for r in matrix)
    for lead, count in leads.most_common():
        print(f"  {lead:20s}: {count:3d} spheres")

    print("\n=== DEPTH DISTRIBUTION ===")
    depths = Counter(r['depth'] for r in matrix)
    for depth in ['Deep', 'Substantial', 'Peripheral', 'Absent']:
        print(f"  {depth:15s}: {depths.get(depth, 0):3d} spheres")


if __name__ == '__main__':
    matrix = build_full_matrix()

    # Write outputs
    base = Path('/home/ubuntu/aluminum-os/registries')
    write_yaml(matrix, base / 'capability_matrix.yaml')
    write_csv(matrix, base / 'capability_matrix.csv')

    print_summary(matrix)
    print("\nDone.")
