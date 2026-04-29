#!/usr/bin/env python3
"""
Create __init__.py stubs for all SPEC modules that don't have one yet.
This makes every module importable and provides a consistent interface.
"""

import os
import yaml

ROOT = "/home/ubuntu/aluminum-os"
REGISTRY = os.path.join(ROOT, "registries/module_registry.yaml")

HOUSE_DIRS = {
    "H01": "H01_philosophy_logic",
    "H02": "H02_formal_sciences",
    "H03": "H03_natural_sciences",
    "H04": "H04_technology_engineering",
    "H05": "H05_arts_creative_expression",
    "H06": "H06_humanities_culture",
    "H07": "H07_applied_sciences",
    "H08": "H08_education_pedagogy",
    "H09": "H09_life_sciences",
    "H10": "H10_health_medicine",
    "H11": "H11_social_sciences",
    "H12": "H12_law_governance",
}


def get_sphere_dir(house_id, sphere_id):
    house_dir = os.path.join(ROOT, "houses", HOUSE_DIRS.get(house_id, ""))
    if not os.path.isdir(house_dir):
        return None
    for d in os.listdir(house_dir):
        if d.startswith(sphere_id):
            return os.path.join(house_dir, d)
    return None


def find_module_dir(sphere_dir, module_id):
    modules_dir = os.path.join(sphere_dir, "modules")
    if not os.path.isdir(modules_dir):
        return None
    for d in os.listdir(modules_dir):
        full = os.path.join(modules_dir, d)
        if os.path.isdir(full) and d.upper().startswith(module_id.upper() + "_"):
            return full
    for d in os.listdir(modules_dir):
        full = os.path.join(modules_dir, d)
        if os.path.isdir(full) and d.upper().startswith(module_id.upper()):
            return full
    return None


def main():
    with open(REGISTRY) as f:
        registry = yaml.safe_load(f)

    created = 0
    skipped = 0
    errors = []

    for m in registry["modules"]:
        if m["status"] != "SPEC":
            skipped += 1
            continue

        module_id = m["id"]
        house_id = m["house"]
        sphere_id = m["sphere"]
        name = m["name"]

        sphere_dir = get_sphere_dir(house_id, sphere_id)
        if not sphere_dir:
            errors.append(f"Sphere dir not found: {house_id}/{sphere_id} for {module_id}")
            continue

        module_dir = find_module_dir(sphere_dir, module_id)
        if not module_dir:
            errors.append(f"Module dir not found: {module_id} in {house_id}/{sphere_id}")
            continue

        init_path = os.path.join(module_dir, "__init__.py")
        if os.path.exists(init_path):
            skipped += 1
            continue

        content = f'''"""
Module {module_id}: {name}

Status: SPEC — interface defined, implementation pending.
House: {house_id} | Sphere: {sphere_id}

This module is registered in the Aluminum OS lattice but awaits
implementation. Contributions welcome — see manifest.yaml for the
module specification.
"""

__module_id__ = "{module_id}"
__status__ = "SPEC"
__name__ = "{name}"
__house__ = "{house_id}"
__sphere__ = "{sphere_id}"
'''
        with open(init_path, "w") as f:
            f.write(content)
        created += 1

    print(f"=== SPEC STUBS CREATED ===")
    print(f"Created: {created}")
    print(f"Skipped (already exists or ABSORBED): {skipped}")
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  ⚠ {e}")


if __name__ == "__main__":
    main()
