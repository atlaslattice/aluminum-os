#!/usr/bin/env python3
"""
CANONICAL REBUILD — v3.14 Appendix AG Taxonomy
Restructures the aluminum-os monorepo from the old taxonomy to the canonical 12×12+1.

This script:
1. Creates the canonical house/sphere directory structure
2. Maps old house names to new canonical house names
3. Remaps all module code into correct canonical positions
4. Updates the module_registry.yaml to match
5. Preserves element-145 as e145/ (parallel to houses/)
"""

import os
import sys
import yaml
import shutil
from pathlib import Path

REPO_ROOT = Path("/home/ubuntu/aluminum-os")

# ============================================================
# CANONICAL 12×12+1 STRUCTURE (v3.14 Appendix AG)
# ============================================================

CANONICAL_HOUSES = {
    "h01_natural_sciences": {
        "id": "H01", "name": "Natural Sciences",
        "spheres": {
            "s01_physics": {"id": 1, "name": "Physics"},
            "s02_chemistry": {"id": 2, "name": "Chemistry"},
            "s03_biology": {"id": 3, "name": "Biology"},
            "s04_astronomy": {"id": 4, "name": "Astronomy"},
            "s05_geology": {"id": 5, "name": "Geology"},
            "s06_oceanography": {"id": 6, "name": "Oceanography"},
            "s07_meteorology": {"id": 7, "name": "Meteorology"},
            "s08_ecology": {"id": 8, "name": "Ecology"},
            "s09_botany": {"id": 9, "name": "Botany"},
            "s10_zoology": {"id": 10, "name": "Zoology"},
            "s11_microbiology": {"id": 11, "name": "Microbiology"},
            "s12_genetics": {"id": 12, "name": "Genetics"},
        }
    },
    "h02_formal_sciences": {
        "id": "H02", "name": "Formal Sciences",
        "spheres": {
            "s01_mathematics": {"id": 13, "name": "Mathematics"},
            "s02_logic": {"id": 14, "name": "Logic"},
            "s03_statistics": {"id": 15, "name": "Statistics"},
            "s04_computer_science": {"id": 16, "name": "Computer Science"},
            "s05_information_theory": {"id": 17, "name": "Information Theory"},
            "s06_game_theory": {"id": 18, "name": "Game Theory"},
            "s07_operations_research": {"id": 19, "name": "Operations Research"},
            "s08_systems_theory": {"id": 20, "name": "Systems Theory"},
            "s09_decision_theory": {"id": 21, "name": "Decision Theory"},
            "s10_cryptography": {"id": 22, "name": "Cryptography"},
            "s11_algorithmics": {"id": 23, "name": "Algorithmics"},
            "s12_data_science": {"id": 24, "name": "Data Science"},
        }
    },
    "h03_social_sciences": {
        "id": "H03", "name": "Social Sciences",
        "spheres": {
            "s01_sociology": {"id": 25, "name": "Sociology"},
            "s02_psychology": {"id": 26, "name": "Psychology"},
            "s03_anthropology": {"id": 27, "name": "Anthropology"},
            "s04_economics": {"id": 28, "name": "Economics"},
            "s05_political_science": {"id": 29, "name": "Political Science"},
            "s06_geography": {"id": 30, "name": "Geography"},
            "s07_linguistics": {"id": 31, "name": "Linguistics"},
            "s08_archaeology": {"id": 32, "name": "Archaeology"},
            "s09_demography": {"id": 33, "name": "Demography"},
            "s10_criminology": {"id": 34, "name": "Criminology"},
            "s11_social_work": {"id": 35, "name": "Social Work"},
            "s12_urban_studies": {"id": 36, "name": "Urban Studies"},
        }
    },
    "h04_humanities": {
        "id": "H04", "name": "Humanities",
        "spheres": {
            "s01_history": {"id": 37, "name": "History"},
            "s02_philosophy": {"id": 38, "name": "Philosophy"},
            "s03_literature": {"id": 39, "name": "Literature"},
            "s04_classics": {"id": 40, "name": "Classics"},
            "s05_religious_studies": {"id": 41, "name": "Religious Studies"},
            "s06_ethics": {"id": 42, "name": "Ethics"},
            "s07_aesthetics": {"id": 43, "name": "Aesthetics"},
            "s08_cultural_studies": {"id": 44, "name": "Cultural Studies"},
            "s09_mythology": {"id": 45, "name": "Mythology"},
            "s10_philology": {"id": 46, "name": "Philology"},
            "s11_rhetoric": {"id": 47, "name": "Rhetoric"},
            "s12_hermeneutics": {"id": 48, "name": "Hermeneutics"},
        }
    },
    "h05_arts": {
        "id": "H05", "name": "Arts",
        "spheres": {
            "s01_visual_arts": {"id": 49, "name": "Visual Arts"},
            "s02_performing_arts": {"id": 50, "name": "Performing Arts"},
            "s03_music": {"id": 51, "name": "Music"},
            "s04_dance": {"id": 52, "name": "Dance"},
            "s05_theater": {"id": 53, "name": "Theater"},
            "s06_film": {"id": 54, "name": "Film"},
            "s07_literature_creative": {"id": 55, "name": "Literature (creative)"},
            "s08_architecture": {"id": 56, "name": "Architecture"},
            "s09_design": {"id": 57, "name": "Design"},
            "s10_photography": {"id": 58, "name": "Photography"},
            "s11_sculpture": {"id": 59, "name": "Sculpture"},
            "s12_painting": {"id": 60, "name": "Painting"},
        }
    },
    "h06_engineering_technology": {
        "id": "H06", "name": "Engineering & Technology",
        "spheres": {
            "s01_mechanical_engineering": {"id": 61, "name": "Mechanical Engineering"},
            "s02_electrical_engineering": {"id": 62, "name": "Electrical Engineering"},
            "s03_civil_engineering": {"id": 63, "name": "Civil Engineering"},
            "s04_chemical_engineering": {"id": 64, "name": "Chemical Engineering"},
            "s05_aerospace_engineering": {"id": 65, "name": "Aerospace Engineering"},
            "s06_biomedical_engineering": {"id": 66, "name": "Biomedical Engineering"},
            "s07_environmental_engineering": {"id": 67, "name": "Environmental Engineering"},
            "s08_industrial_engineering": {"id": 68, "name": "Industrial Engineering"},
            "s09_software_engineering": {"id": 69, "name": "Software Engineering"},
            "s10_materials_engineering": {"id": 70, "name": "Materials Engineering"},
            "s11_nuclear_engineering": {"id": 71, "name": "Nuclear Engineering"},
            "s12_robotics": {"id": 72, "name": "Robotics"},
        }
    },
    "h07_information_communication": {
        "id": "H07", "name": "Information & Communication",
        "spheres": {
            "s01_media": {"id": 73, "name": "Media"},
            "s02_journalism": {"id": 74, "name": "Journalism"},
            "s03_telecommunications": {"id": 75, "name": "Telecommunications"},
            "s04_networks": {"id": 76, "name": "Networks"},
            "s05_information_systems": {"id": 77, "name": "Information Systems"},
            "s06_library_science": {"id": 78, "name": "Library Science"},
            "s07_archives": {"id": 79, "name": "Archives"},
            "s08_publishing": {"id": 80, "name": "Publishing"},
            "s09_broadcasting": {"id": 81, "name": "Broadcasting"},
            "s10_public_relations": {"id": 82, "name": "Public Relations"},
            "s11_information_policy": {"id": 83, "name": "Information Policy"},
            "s12_communication_theory": {"id": 84, "name": "Communication Theory"},
        }
    },
    "h08_education": {
        "id": "H08", "name": "Education",
        "spheres": {
            "s01_pedagogy": {"id": 85, "name": "Pedagogy"},
            "s02_curriculum_design": {"id": 86, "name": "Curriculum Design"},
            "s03_educational_psychology": {"id": 87, "name": "Educational Psychology"},
            "s04_special_education": {"id": 88, "name": "Special Education"},
            "s05_adult_education": {"id": 89, "name": "Adult Education"},
            "s06_e_learning": {"id": 90, "name": "E-Learning"},
            "s07_educational_technology": {"id": 91, "name": "Educational Technology"},
            "s08_assessment": {"id": 92, "name": "Assessment"},
            "s09_school_administration": {"id": 93, "name": "School Administration"},
            "s10_teacher_training": {"id": 94, "name": "Teacher Training"},
            "s11_literacy": {"id": 95, "name": "Literacy"},
            "s12_higher_education": {"id": 96, "name": "Higher Education"},
        }
    },
    "h09_health_medicine": {
        "id": "H09", "name": "Health & Medicine",
        "spheres": {
            "s01_anatomy": {"id": 97, "name": "Anatomy"},
            "s02_physiology": {"id": 98, "name": "Physiology"},
            "s03_pathology": {"id": 99, "name": "Pathology"},
            "s04_pharmacology": {"id": 100, "name": "Pharmacology"},
            "s05_surgery": {"id": 101, "name": "Surgery"},
            "s06_pediatrics": {"id": 102, "name": "Pediatrics"},
            "s07_psychiatry": {"id": 103, "name": "Psychiatry"},
            "s08_neurology": {"id": 104, "name": "Neurology"},
            "s09_oncology": {"id": 105, "name": "Oncology"},
            "s10_epidemiology": {"id": 106, "name": "Epidemiology"},
            "s11_nutrition": {"id": 107, "name": "Nutrition"},
            "s12_public_health": {"id": 108, "name": "Public Health"},
        }
    },
    "h10_business_economics": {
        "id": "H10", "name": "Business & Economics",
        "spheres": {
            "s01_management": {"id": 109, "name": "Management"},
            "s02_marketing": {"id": 110, "name": "Marketing"},
            "s03_finance": {"id": 111, "name": "Finance"},
            "s04_accounting": {"id": 112, "name": "Accounting"},
            "s05_entrepreneurship": {"id": 113, "name": "Entrepreneurship"},
            "s06_human_resources": {"id": 114, "name": "Human Resources"},
            "s07_operations_management": {"id": 115, "name": "Operations Management"},
            "s08_supply_chain": {"id": 116, "name": "Supply Chain"},
            "s09_international_business": {"id": 117, "name": "International Business"},
            "s10_business_ethics": {"id": 118, "name": "Business Ethics"},
            "s11_microeconomics": {"id": 119, "name": "Microeconomics"},
            "s12_macroeconomics": {"id": 120, "name": "Macroeconomics"},
        }
    },
    "h11_infrastructure": {
        "id": "H11", "name": "Infrastructure",
        "spheres": {
            "s01_transportation": {"id": 121, "name": "Transportation"},
            "s02_energy_systems": {"id": 122, "name": "Energy Systems"},
            "s03_water_systems": {"id": 123, "name": "Water Systems"},
            "s04_utilities": {"id": 124, "name": "Utilities"},
            "s05_physical_infrastructure": {"id": 125, "name": "Physical Infrastructure"},
            "s06_logistics": {"id": 126, "name": "Logistics"},
            "s07_construction": {"id": 127, "name": "Construction"},
            "s08_resource_management": {"id": 128, "name": "Resource Management"},
            "s09_waste_management": {"id": 129, "name": "Waste Management"},
            "s10_sanitation": {"id": 130, "name": "Sanitation"},
            "s11_telecom_infrastructure": {"id": 131, "name": "Telecom Infrastructure"},
            "s12_computing_infrastructure": {"id": 132, "name": "Computing Infrastructure"},
        }
    },
    "h12_law_governance": {
        "id": "H12", "name": "Law/Governance/Meta-Knowledge",
        "spheres": {
            "s01_constitutional_law": {"id": 133, "name": "Constitutional Law"},
            "s02_criminal_law": {"id": 134, "name": "Criminal Law"},
            "s03_civil_law": {"id": 135, "name": "Civil Law"},
            "s04_international_law": {"id": 136, "name": "International Law"},
            "s05_corporate_law": {"id": 137, "name": "Corporate Law"},
            "s06_environmental_law": {"id": 138, "name": "Environmental Law"},
            "s07_human_rights": {"id": 139, "name": "Human Rights"},
            "s08_political_theory": {"id": 140, "name": "Political Theory"},
            "s09_public_policy": {"id": 141, "name": "Public Policy"},
            "s10_international_relations": {"id": 142, "name": "International Relations"},
            "s11_comparative_politics": {"id": 143, "name": "Comparative Politics"},
            "s12_political_economy": {"id": 144, "name": "Political Economy"},
        }
    },
}

# ============================================================
# OLD → NEW HOUSE MAPPING
# Maps old house directory names to canonical house + best-fit sphere
# ============================================================

OLD_TO_NEW_HOUSE = {
    # Old H01 Philosophy & Logic → H04 Humanities (Philosophy S38, Logic → H02 S02)
    "H01_philosophy_logic": "h04_humanities",
    # Old H02 Formal Sciences → H02 Formal Sciences (direct match!)
    "H02_formal_sciences": "h02_formal_sciences",
    # Old H03 Natural Sciences → H01 Natural Sciences
    "H03_natural_sciences": "h01_natural_sciences",
    # Old H04 Technology & Engineering → split: Software Eng → H06, AI/ML → H06, Cloud → H11
    "H04_technology_engineering": "h06_engineering_technology",
    # Old H05 Arts & Creative Expression → H05 Arts
    "H05_arts_creative_expression": "h05_arts",
    # Old H06 Humanities & Culture → H04 Humanities
    "H06_humanities_culture": "h04_humanities",
    # Old H07 Applied Sciences → H06 Engineering & Technology
    "H07_applied_sciences": "h06_engineering_technology",
    # Old H08 Education & Pedagogy → H08 Education
    "H08_education_pedagogy": "h08_education",
    # Old H09 Life Sciences → H01 Natural Sciences (Biology, Genetics)
    "H09_life_sciences": "h01_natural_sciences",
    # Old H10 Health & Medicine → H09 Health & Medicine
    "H10_health_medicine": "h09_health_medicine",
    # Old H11 Social Sciences → H03 Social Sciences
    "H11_social_sciences": "h03_social_sciences",
    # Old H12 Law & Governance → H12 Law/Governance
    "H12_law_governance": "h12_law_governance",
}

# ============================================================
# MODULE-LEVEL REMAP TABLE
# For modules that need to go to a DIFFERENT house than their parent
# Key: old module directory name pattern → (new_house_dir, new_sphere_dir)
# ============================================================

MODULE_SPHERE_REMAP = {
    # Old H02 modules that are actually Computer Science → H02 S04
    "sovereign_router_core": ("h02_formal_sciences", "s04_computer_science"),
    "lattice_ontology_engine": ("h02_formal_sciences", "s04_computer_science"),
    "sphere_classifier": ("h02_formal_sciences", "s04_computer_science"),
    "bridge_v2_router": ("h02_formal_sciences", "s04_computer_science"),
    "model_router": ("h02_formal_sciences", "s04_computer_science"),
    "data_pipeline": ("h02_formal_sciences", "s12_data_science"),
    "synthesizer_e145": ("h02_formal_sciences", "s08_systems_theory"),
    # Cryptography modules
    "cryptographic_protocols": ("h02_formal_sciences", "s10_cryptography"),
    "encryption_engine": ("h02_formal_sciences", "s10_cryptography"),
    "hash_functions": ("h02_formal_sciences", "s10_cryptography"),
    # Logic modules
    "formal_logic_engine": ("h02_formal_sciences", "s02_logic"),
    "proof_assistant": ("h02_formal_sciences", "s02_logic"),
    "sat_smt_solver": ("h02_formal_sciences", "s02_logic"),
    "formal_verification": ("h02_formal_sciences", "s02_logic"),
    "model_checking": ("h02_formal_sciences", "s02_logic"),
    # Math modules
    "number_theory": ("h02_formal_sciences", "s01_mathematics"),
    "abstract_algebra": ("h02_formal_sciences", "s01_mathematics"),
    "topology": ("h02_formal_sciences", "s01_mathematics"),
    "numerical_analysis": ("h02_formal_sciences", "s01_mathematics"),
    "combinatorics": ("h02_formal_sciences", "s01_mathematics"),
    "differential_equations": ("h02_formal_sciences", "s01_mathematics"),
    "linear_algebra": ("h02_formal_sciences", "s01_mathematics"),
    "optimization": ("h02_formal_sciences", "s01_mathematics"),
    "category_theory": ("h02_formal_sciences", "s01_mathematics"),
    # Statistics
    "bayesian_inference": ("h02_formal_sciences", "s03_statistics"),
    "statistical_learning": ("h02_formal_sciences", "s03_statistics"),
    "time_series_analysis": ("h02_formal_sciences", "s03_statistics"),
    "hypothesis_testing": ("h02_formal_sciences", "s03_statistics"),
    "regression_analysis": ("h02_formal_sciences", "s03_statistics"),
    "probability_theory": ("h02_formal_sciences", "s03_statistics"),
    # Game Theory
    "game_theory": ("h02_formal_sciences", "s06_game_theory"),
    "mechanism_design": ("h02_formal_sciences", "s06_game_theory"),
    "auction_theory": ("h02_formal_sciences", "s06_game_theory"),
    # Info Theory
    "information_theory": ("h02_formal_sciences", "s05_information_theory"),
    "coding_theory": ("h02_formal_sciences", "s05_information_theory"),
    "signal_processing": ("h02_formal_sciences", "s05_information_theory"),
    # Algorithms
    "graph_algorithms": ("h02_formal_sciences", "s11_algorithmics"),
    "complexity_theory": ("h02_formal_sciences", "s11_algorithmics"),
    "streaming_algorithms": ("h02_formal_sciences", "s11_algorithmics"),
    "distributed_algorithms": ("h02_formal_sciences", "s11_algorithmics"),
    "approximation_algorithms": ("h02_formal_sciences", "s11_algorithmics"),
    # Decision Theory
    "decision_theory": ("h02_formal_sciences", "s09_decision_theory"),
    "multi_criteria_decision": ("h02_formal_sciences", "s09_decision_theory"),
    # Operations Research
    "operations_research": ("h02_formal_sciences", "s07_operations_research"),
    "scheduling_theory": ("h02_formal_sciences", "s07_operations_research"),
    "queueing_theory": ("h02_formal_sciences", "s07_operations_research"),
    # Systems Theory
    "systems_theory": ("h02_formal_sciences", "s08_systems_theory"),
    "control_theory": ("h02_formal_sciences", "s08_systems_theory"),
    "dynamical_systems": ("h02_formal_sciences", "s08_systems_theory"),
    # Data Science
    "machine_learning": ("h02_formal_sciences", "s12_data_science"),
    "deep_learning": ("h02_formal_sciences", "s12_data_science"),
    "neural_networks": ("h02_formal_sciences", "s12_data_science"),
    "natural_language_processing": ("h02_formal_sciences", "s12_data_science"),
    "computer_vision": ("h02_formal_sciences", "s12_data_science"),
    "reinforcement_learning": ("h02_formal_sciences", "s12_data_science"),
    # Old H04 tech modules → proper canonical homes
    "sovereign_oracle": ("h06_engineering_technology", "s09_software_engineering"),
    "saas_automation": ("h06_engineering_technology", "s09_software_engineering"),
    "cloud_computing": ("h11_infrastructure", "s12_computing_infrastructure"),
    "ai_ml_systems": ("h06_engineering_technology", "s09_software_engineering"),
    "quantum_computing": ("h02_formal_sciences", "s04_computer_science"),
    # Old H01 Philosophy → H04 Humanities
    "philosophical_reasoning": ("h04_humanities", "s02_philosophy"),
    "epistemology": ("h04_humanities", "s02_philosophy"),
    "ontological_analysis": ("h04_humanities", "s02_philosophy"),
    # Old H07 Applied Sciences → H06 Engineering
    "materials_science": ("h06_engineering_technology", "s10_materials_engineering"),
    "biomedical_engineering": ("h06_engineering_technology", "s06_biomedical_engineering"),
    "environmental_engineering": ("h06_engineering_technology", "s07_environmental_engineering"),
    "robotics_automation": ("h06_engineering_technology", "s12_robotics"),
    "aerospace_engineering": ("h06_engineering_technology", "s05_aerospace_engineering"),
    "chemical_engineering": ("h06_engineering_technology", "s04_chemical_engineering"),
    "civil_engineering": ("h06_engineering_technology", "s03_civil_engineering"),
    "electrical_engineering": ("h06_engineering_technology", "s02_electrical_engineering"),
    # Old H11 Social Sciences → H03
    "economic_modeling": ("h03_social_sciences", "s04_economics"),
    "political_analysis": ("h03_social_sciences", "s05_political_science"),
    "sociological_research": ("h03_social_sciences", "s01_sociology"),
    # Old H12 Law → H12 (stays)
    "constitutional_law": ("h12_law_governance", "s01_constitutional_law"),
    "international_law": ("h12_law_governance", "s04_international_law"),
    "corporate_governance": ("h12_law_governance", "s05_corporate_law"),
    "regulatory_compliance": ("h12_law_governance", "s09_public_policy"),
    "human_rights": ("h12_law_governance", "s07_human_rights"),
}


def create_canonical_structure():
    """Create the full canonical 12×12 directory structure."""
    houses_dir = REPO_ROOT / "houses"
    created = 0

    for house_dir_name, house_info in CANONICAL_HOUSES.items():
        house_path = houses_dir / house_dir_name
        for sphere_dir_name, sphere_info in house_info["spheres"].items():
            sphere_path = house_path / sphere_dir_name
            modules_path = sphere_path / "modules"
            modules_path.mkdir(parents=True, exist_ok=True)

            # Create sphere README
            readme = sphere_path / "README.md"
            if not readme.exists():
                readme.write_text(
                    f"# {house_info['name']} — {sphere_info['name']}\n\n"
                    f"**House:** {house_info['id']} ({house_info['name']})\n"
                    f"**Sphere:** S{sphere_info['id']:03d} ({sphere_info['name']})\n"
                    f"**Canonical ID:** {house_info['id']}.S{sphere_info['id']:02d}\n\n"
                    f"## Modules\n\nModules in this sphere are located in the `modules/` subdirectory.\n"
                )
                created += 1

    # Create e145 directory (parallel to houses)
    e145_dir = REPO_ROOT / "e145"
    e145_dir.mkdir(exist_ok=True)

    print(f"Created {created} new sphere READMEs")
    print(f"Canonical structure: 12 houses × 12 spheres = 144 sphere directories")
    return True


def migrate_modules():
    """Migrate all modules from old house structure to canonical positions."""
    old_houses_dir = REPO_ROOT / "houses"
    migrated = 0
    skipped = 0
    errors = []

    # Get all old house directories
    old_houses = sorted([d for d in old_houses_dir.iterdir()
                        if d.is_dir() and d.name.startswith("H")])

    for old_house in old_houses:
        old_house_name = old_house.name
        default_new_house = OLD_TO_NEW_HOUSE.get(old_house_name)

        if not default_new_house:
            errors.append(f"No mapping for old house: {old_house_name}")
            continue

        # Find all sphere directories in old house
        for old_sphere in sorted(old_house.iterdir()):
            if not old_sphere.is_dir():
                continue

            # Find all module directories in old sphere
            modules_dir = old_sphere / "modules"
            if not modules_dir.exists():
                # Maybe the sphere itself contains modules directly
                continue

            for old_module in sorted(modules_dir.iterdir()):
                if not old_module.is_dir():
                    continue

                module_name = old_module.name

                # Check if this module has a specific remap
                if module_name in MODULE_SPHERE_REMAP:
                    new_house, new_sphere = MODULE_SPHERE_REMAP[module_name]
                else:
                    # Use default house mapping, put in first sphere
                    new_house = default_new_house
                    # Try to infer sphere from old sphere name
                    new_sphere = infer_sphere(old_sphere.name, new_house)

                # Target path
                target = old_houses_dir / new_house / new_sphere / "modules" / module_name

                if target.exists():
                    skipped += 1
                    continue

                target.parent.mkdir(parents=True, exist_ok=True)

                # Copy module to new location
                try:
                    shutil.copytree(old_module, target)
                    migrated += 1
                except Exception as e:
                    errors.append(f"Error migrating {module_name}: {e}")

    print(f"Migrated: {migrated} modules")
    print(f"Skipped (already exists): {skipped}")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")

    return migrated


def infer_sphere(old_sphere_name, new_house):
    """Infer the best canonical sphere from old sphere name and new house."""
    # Normalize
    name = old_sphere_name.lower().replace("-", "_")

    # Try to find a matching sphere in the target house
    if new_house in CANONICAL_HOUSES:
        for sphere_dir, sphere_info in CANONICAL_HOUSES[new_house]["spheres"].items():
            sphere_name_lower = sphere_info["name"].lower().replace(" ", "_")
            if sphere_name_lower in name or name in sphere_name_lower:
                return sphere_dir

    # Default to first sphere in house
    if new_house in CANONICAL_HOUSES:
        first_sphere = list(CANONICAL_HOUSES[new_house]["spheres"].keys())[0]
        return first_sphere

    return "s01_general"


def migrate_element145():
    """Move element-145/ to e145/ (parallel to houses/)."""
    old_e145 = REPO_ROOT / "element-145"
    new_e145 = REPO_ROOT / "e145"

    if old_e145.exists() and not (new_e145 / "aluminum-os-core").exists():
        # Copy contents, don't overwrite
        for item in old_e145.iterdir():
            target = new_e145 / item.name
            if not target.exists():
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
        print(f"Migrated element-145/ → e145/ ({len(list(old_e145.iterdir()))} items)")
    else:
        print("e145/ already populated or element-145/ doesn't exist")


def generate_registry():
    """Generate a new canonical module_registry.yaml from the filesystem."""
    houses_dir = REPO_ROOT / "houses"
    modules = []
    module_id = 1

    for house_dir_name in sorted(CANONICAL_HOUSES.keys()):
        house_path = houses_dir / house_dir_name
        house_info = CANONICAL_HOUSES[house_dir_name]

        for sphere_dir_name in sorted(house_info["spheres"].keys()):
            sphere_path = house_path / sphere_dir_name / "modules"
            sphere_info = house_info["spheres"][sphere_dir_name]

            if not sphere_path.exists():
                continue

            for module_dir in sorted(sphere_path.iterdir()):
                if not module_dir.is_dir():
                    continue

                # Check if module has __init__.py
                init_file = module_dir / "__init__.py"
                has_code = init_file.exists()

                # Determine status
                if has_code:
                    content = init_file.read_text()
                    if "ABSORBED" in content or "def " in content or "class " in content:
                        status = "ACTIVE"
                    else:
                        status = "SPEC"
                else:
                    status = "SPEC"

                modules.append({
                    "module_id": f"M{module_id}",
                    "name": module_dir.name,
                    "house": house_info["id"],
                    "house_name": house_info["name"],
                    "sphere_id": sphere_info["id"],
                    "sphere_name": sphere_info["name"],
                    "house_dir": house_dir_name,
                    "sphere_dir": sphere_dir_name,
                    "status": status,
                    "path": str(module_dir.relative_to(REPO_ROOT)),
                })
                module_id += 1

    registry = {
        "version": "3.14",
        "canon": "COMPLETE_BUILD_PLAN_v3.14 Appendix AG",
        "houses": 12,
        "spheres_per_house": 12,
        "total_spheres": 144,
        "element_145": "e145/",
        "modules": modules,
    }

    registry_path = REPO_ROOT / "registries" / "module_registry.yaml"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Generated registry: {len(modules)} modules across {12} houses")

    # Stats
    active = sum(1 for m in modules if m["status"] == "ACTIVE")
    spec = sum(1 for m in modules if m["status"] == "SPEC")
    print(f"  ACTIVE: {active}")
    print(f"  SPEC: {spec}")

    return modules


def cleanup_old_structure():
    """Remove old house directories after migration."""
    houses_dir = REPO_ROOT / "houses"
    removed = 0
    for d in sorted(houses_dir.iterdir()):
        if d.is_dir() and d.name.startswith("H") and d.name[1].isupper():
            # This is an old-format directory (uppercase H followed by uppercase)
            shutil.rmtree(d)
            removed += 1
            print(f"  Removed old: {d.name}")

    # Remove old element-145 if e145 exists
    old_e145 = REPO_ROOT / "element-145"
    new_e145 = REPO_ROOT / "e145"
    if old_e145.exists() and new_e145.exists():
        shutil.rmtree(old_e145)
        print("  Removed old: element-145/")
        removed += 1

    print(f"Cleaned up {removed} old directories")


def main():
    print("=" * 60)
    print("CANONICAL REBUILD — v3.14 Appendix AG")
    print("=" * 60)

    print("\n--- Step 1: Create canonical 12×12 structure ---")
    create_canonical_structure()

    print("\n--- Step 2: Migrate Element 145 → e145/ ---")
    migrate_element145()

    print("\n--- Step 3: Migrate modules to canonical positions ---")
    migrate_modules()

    print("\n--- Step 4: Clean up old structure ---")
    cleanup_old_structure()

    print("\n--- Step 5: Generate canonical registry ---")
    generate_registry()

    print("\n" + "=" * 60)
    print("REBUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
