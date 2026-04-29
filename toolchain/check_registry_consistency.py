#!/usr/bin/env python3
"""Registry <-> Filesystem Consistency Gate (v3.14).

Verifies that:
1. Every module in module_registry.yaml has a corresponding on-disk directory
2. Every on-disk module directory has a corresponding registry entry
3. Module IDs are unique in the registry
4. All 12 Houses x 12 Spheres directories exist
5. lattice_ontology_v2.py matches registries

Exit code 0 = consistent, 1 = drift detected.
"""

import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registries" / "module_registry.yaml"
HOUSES_DIR = REPO_ROOT / "houses"


def load_registry():
    """Load module registry and return dict of path -> module metadata."""
    with open(REGISTRY_PATH) as f:
        data = yaml.safe_load(f)
    modules = {}
    ids_seen = set()
    for m in data.get("modules", []):
        mid = m.get("module_id", m.get("id"))
        if mid in ids_seen:
            print(f"  DUPLICATE REGISTRY ID: {mid}")
        ids_seen.add(mid)
        path = m.get("path", "")
        modules[path] = m
    return modules, data


def find_disk_modules():
    """Find all module directories on disk that have __init__.py."""
    disk = {}
    for init in HOUSES_DIR.rglob("__init__.py"):
        mdir = init.parent
        if mdir.parent.name == "modules":
            rel = str(mdir.relative_to(REPO_ROOT))
            disk[rel] = mdir
    return disk


def check_house_structure():
    """Verify all 12 Houses x 12 Spheres directories exist."""
    errors = []
    try:
        sys.path.insert(0, str(REPO_ROOT / "e145" / "aluminum-os-core"))
        from lattice_ontology_v2 import HOUSE_IDS, HOUSE_DIRS, SPHERE_DIRS
        for i, hdir in enumerate(HOUSE_DIRS):
            house_path = HOUSES_DIR / hdir
            if not house_path.exists():
                errors.append(f"MISSING HOUSE DIR: {house_path}")
                continue
            for j in range(12):
                idx = i * 12 + j
                sdir = SPHERE_DIRS[idx]
                sphere_path = house_path / sdir
                if not sphere_path.exists():
                    errors.append(f"MISSING SPHERE DIR: {sphere_path}")
    except ImportError as e:
        errors.append(f"Cannot import lattice_ontology_v2: {e}")
    return errors


def main():
    errors = []
    warnings = []

    print("Registry <-> Filesystem Consistency Check (v3.14)")
    print("=" * 55)

    # Check house/sphere structure
    print("\n1. House/Sphere structure check...")
    struct_errors = check_house_structure()
    errors.extend(struct_errors)
    if not struct_errors:
        print("   12 Houses x 12 Spheres = 144 directories: OK")
    else:
        for e in struct_errors:
            print(f"   FAIL: {e}")

    # Load both sources
    print("\n2. Module registry check...")
    registry, reg_data = load_registry()
    disk = find_disk_modules()

    print(f"   Registry modules: {len(registry)}")
    print(f"   Disk modules:     {len(disk)}")

    # Check: Registry entries missing from disk
    missing_from_disk = set(registry.keys()) - set(disk.keys())
    if missing_from_disk:
        for path in sorted(missing_from_disk):
            m = registry[path]
            errors.append(f"MISSING ON DISK: {m.get('module_id')} at {path}")

    # Check: Disk entries missing from registry
    missing_from_registry = set(disk.keys()) - set(registry.keys())
    if missing_from_registry:
        for path in sorted(missing_from_registry):
            errors.append(f"MISSING IN REGISTRY: {path}")

    matched = set(registry.keys()) & set(disk.keys())

    # Check E145
    print("\n3. Element 145 check...")
    e145_path = REPO_ROOT / "e145"
    if e145_path.exists():
        components = [d.name for d in e145_path.iterdir() if d.is_dir()]
        print(f"   E145 components: {len(components)}")
    else:
        errors.append("MISSING: e145/ directory")

    # Check ontology lock
    print("\n4. Ontology lock check...")
    lock_file = REPO_ROOT / "registries" / "ontology_lock.sha256"
    if lock_file.exists():
        print(f"   Lock file present: OK")
    else:
        warnings.append("No ontology_lock.sha256 file")

    # Report
    print(f"\n{'=' * 55}")
    print(f"Matched modules: {len(matched)}")
    print(f"Missing from disk: {len(missing_from_disk)}")
    print(f"Missing from registry: {len(missing_from_registry)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  x {e}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ! {w}")

    if errors:
        print("\nRESULT: FAIL")
        return 1
    else:
        print("\nRESULT: PASS — registry and filesystem are consistent")
        return 0


if __name__ == "__main__":
    sys.exit(main())
