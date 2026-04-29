#!/usr/bin/env python3
"""
update_ontology_lock.py — Generate or verify SHA-256 lock file for ontology structure.
Implements D-89 Ontology Lock Protocol.

Usage:
  python toolchain/update_ontology_lock.py              # Generate lock file
  python toolchain/update_ontology_lock.py --verify-only  # Verify without updating
  python toolchain/update_ontology_lock.py --output FILE  # Write to specific file
"""

import hashlib
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK_FILE = os.path.join(ROOT, "toolchain", "ontology_lock.sha256")

# Files that constitute the "locked ontology" — any change requires protocol compliance
LOCKED_FILES = [
    "registries/lattice_ontology.yaml",
    "registries/module_registry.yaml",
    "registries/doctrine_registry.yaml",
    "registries/invariant_registry.yaml",
    "registries/12x12_matrix.yaml",
    "element-145/aluminum-os-core/lattice_ontology_v2.py",
]


def compute_hashes():
    """Compute SHA-256 for all locked files."""
    hashes = {}
    for rel_path in LOCKED_FILES:
        full_path = os.path.join(ROOT, rel_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                hashes[rel_path] = hashlib.sha256(f.read()).hexdigest()
        else:
            hashes[rel_path] = "FILE_MISSING"
    return hashes


def write_lock(hashes, output_path=None):
    """Write lock file."""
    path = output_path or LOCK_FILE
    with open(path, 'w') as f:
        for file_path, sha in sorted(hashes.items()):
            f.write(f"{sha}  {file_path}\n")
    print(f"✓ Ontology lock written to {path}")
    print(f"  {len(hashes)} files locked")


def verify_lock():
    """Verify current state matches lock file."""
    if not os.path.exists(LOCK_FILE):
        print("ERROR: Lock file missing. Run without --verify-only to generate.")
        sys.exit(1)

    # Read existing lock
    existing = {}
    with open(LOCK_FILE) as f:
        for line in f:
            parts = line.strip().split("  ", 1)
            if len(parts) == 2:
                existing[parts[1]] = parts[0]

    # Compute current
    current = compute_hashes()

    # Compare
    mismatches = []
    for path, sha in current.items():
        if path not in existing:
            mismatches.append(f"NEW: {path}")
        elif existing[path] != sha:
            mismatches.append(f"CHANGED: {path}")

    if mismatches:
        print("ERROR: Ontology lock verification FAILED")
        for m in mismatches:
            print(f"  {m}")
        sys.exit(1)
    else:
        print("✓ Ontology lock verification PASSED — D-89 compliant")


def main():
    args = sys.argv[1:]

    if "--verify-only" in args:
        verify_lock()
    elif "--output" in args:
        idx = args.index("--output")
        output_path = args[idx + 1] if idx + 1 < len(args) else "/tmp/current_lock.sha256"
        hashes = compute_hashes()
        write_lock(hashes, output_path)
    else:
        hashes = compute_hashes()
        write_lock(hashes)


if __name__ == "__main__":
    main()
