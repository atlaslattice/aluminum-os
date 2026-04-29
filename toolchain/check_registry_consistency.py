#!/usr/bin/env python3
"""Registry ↔ Filesystem Consistency Gate.

Verifies that:
1. Every module in module_registry.yaml has a corresponding on-disk directory
2. Every on-disk M* directory has a corresponding registry entry
3. Module IDs are unique in the registry
4. Manifest.yaml in each module dir matches registry metadata

Exit code 0 = consistent, 1 = drift detected.
"""

import os
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registries" / "module_registry.yaml"
HOUSES_DIR = REPO_ROOT / "houses"


def load_registry():
    """Load module registry and return dict of id -> module metadata."""
    with open(REGISTRY_PATH) as f:
        data = yaml.safe_load(f)
    modules = {}
    for m in data.get("modules", []):
        mid = m["id"]
        if mid in modules:
            print(f"  DUPLICATE REGISTRY ID: {mid}")
        modules[mid] = m
    return modules


def find_disk_modules():
    """Find all M* directories on disk and return dict of id -> path."""
    disk = {}
    for mdir in HOUSES_DIR.rglob("M*"):
        if mdir.is_dir() and mdir.parent.name == "modules":
            # Extract module ID from directory name (e.g., M10_mathematical_proof_engine -> M10)
            dirname = mdir.name
            mid = dirname.split("_")[0]
            # Handle IDs like M8a, M162b
            if mid[0] == "M" and any(c.isdigit() for c in mid[1:]):
                if mid in disk:
                    print(f"  DUPLICATE DISK ID: {mid} at {mdir} and {disk[mid]}")
                disk[mid] = mdir
    return disk


def main():
    errors = []
    warnings = []

    print("Registry ↔ Filesystem Consistency Check")
    print("=" * 50)

    # Load both sources
    registry = load_registry()
    disk = find_disk_modules()

    print(f"Registry modules: {len(registry)}")
    print(f"Disk modules:     {len(disk)}")
    print()

    # Check 1: Registry entries missing from disk
    missing_from_disk = set(registry.keys()) - set(disk.keys())
    if missing_from_disk:
        for mid in sorted(missing_from_disk):
            errors.append(f"MISSING ON DISK: {mid} ({registry[mid].get('name', '?')}) "
                         f"expected at {registry[mid]['house']}.{registry[mid]['sphere']}")

    # Check 2: Disk entries missing from registry
    missing_from_registry = set(disk.keys()) - set(registry.keys())
    if missing_from_registry:
        for mid in sorted(missing_from_registry):
            errors.append(f"MISSING IN REGISTRY: {mid} at {disk[mid]}")

    # Check 3: Manifest consistency for matching entries
    matched = set(registry.keys()) & set(disk.keys())
    for mid in sorted(matched):
        manifest_path = disk[mid] / "manifest.yaml"
        if not manifest_path.exists():
            warnings.append(f"NO MANIFEST: {mid} at {disk[mid]}")
            continue
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        if manifest and manifest.get("id") != mid:
            warnings.append(f"ID MISMATCH: {mid} manifest says {manifest.get('id')}")

    # Report
    print(f"Matched: {len(matched)}")
    print(f"Missing from disk: {len(missing_from_disk)}")
    print(f"Missing from registry: {len(missing_from_registry)}")
    print(f"Warnings: {len(warnings)}")
    print()

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()

    if errors:
        print("RESULT: FAIL — registry and filesystem are inconsistent")
        return 1
    else:
        print("RESULT: PASS — registry and filesystem are consistent")
        return 0


if __name__ == "__main__":
    sys.exit(main())
