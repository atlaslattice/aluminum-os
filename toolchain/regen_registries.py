#!/usr/bin/env python3
"""
Regenerate all registries from the canonical lattice_ontology_v2.py.
This ensures lattice_ontology.yaml, 12x12_matrix.yaml, and module_registry.yaml
all match the v3.14 canon.
"""

import sys, os, yaml, json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "e145" / "aluminum-os-core"))

from lattice_ontology_v2 import (
    HOUSES, HOUSE_IDS, HOUSE_NAMES, HOUSE_DIRS,
    SPHERES, SPHERE_IDS, SPHERE_DIRS, KEYWORDS,
    ELEMENT_145, INTER_HOUSE_EDGES, compute_ontology_hash
)

# ============================================================
# 1. Regenerate lattice_ontology.yaml
# ============================================================

def regen_lattice_ontology():
    houses_list = []
    for i, hid in enumerate(HOUSE_IDS):
        h = HOUSES[hid]
        spheres = []
        for j in range(12):
            idx = i * 12 + j
            sid = f"S{j+1:02d}"
            kws = KEYWORDS.get(idx, [])
            spheres.append({
                "id": sid,
                "name": SPHERES[idx],
                "keywords": kws,
            })
        houses_list.append({
            "id": hid,
            "name": h["name"],
            "domain": f"Sphere of {h['name'].lower()}",
            "spheres": spheres,
        })

    ontology = {
        "version": "3.14",
        "lattice_size": 145,
        "invariant": True,
        "canon": "COMPLETE_BUILD_PLAN_v3.14 Appendix AG",
        "ontology_hash": compute_ontology_hash(),
        "houses": houses_list,
        "element_145": {
            "id": "E145",
            "name": ELEMENT_145["name"],
            "role": ELEMENT_145["description"],
            "components": ELEMENT_145["components"],
        },
        "inter_house_edges": INTER_HOUSE_EDGES,
    }

    out = ROOT / "registries" / "lattice_ontology.yaml"
    with open(out, "w") as f:
        f.write("# Lattice Ontology v3.14 — Canonical 12x12+1 Structure\n")
        f.write("# AUTO-GENERATED from lattice_ontology_v2.py — DO NOT EDIT MANUALLY\n")
        f.write(f"# Ontology hash: {compute_ontology_hash()}\n")
        yaml.dump(ontology, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  Written: {out}")


# ============================================================
# 2. Regenerate 12x12_matrix.yaml
# ============================================================

def regen_matrix():
    matrix = {
        "version": "3.14",
        "canon": "COMPLETE_BUILD_PLAN_v3.14 Appendix AG",
        "dimensions": {"houses": 12, "spheres_per_house": 12, "total": 144},
        "matrix": {},
    }

    for i, hid in enumerate(HOUSE_IDS):
        row = {}
        for j in range(12):
            idx = i * 12 + j
            sid = SPHERE_IDS[idx]
            row[sid] = {
                "name": SPHERES[idx],
                "dir": f"houses/{HOUSE_DIRS[i]}/{SPHERE_DIRS[idx]}",
                "index": idx,
            }
        matrix["matrix"][hid] = {
            "name": HOUSE_NAMES[i],
            "dir": HOUSE_DIRS[i],
            "spheres": row,
        }

    out = ROOT / "registries" / "12x12_matrix.yaml"
    with open(out, "w") as f:
        f.write("# 12x12 Ontological Matrix v3.14\n")
        f.write("# AUTO-GENERATED from lattice_ontology_v2.py — DO NOT EDIT MANUALLY\n")
        yaml.dump(matrix, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  Written: {out}")


# ============================================================
# 3. Regenerate module_registry.yaml from filesystem
# ============================================================

def regen_module_registry():
    modules = []
    mid = 0

    for i, hid in enumerate(HOUSE_IDS):
        hdir = HOUSE_DIRS[i]
        hname = HOUSE_NAMES[i]
        house_path = ROOT / "houses" / hdir

        for j in range(12):
            idx = i * 12 + j
            sdir = SPHERE_DIRS[idx]
            sname = SPHERES[idx]
            sphere_path = house_path / sdir / "modules"

            if not sphere_path.exists():
                continue

            for mod_dir in sorted(sphere_path.iterdir()):
                if mod_dir.is_dir() and (mod_dir / "__init__.py").exists():
                    mid += 1
                    init_path = mod_dir / "__init__.py"
                    init_text = init_path.read_text()

                    # Detect status from __init__.py content
                    status = "ACTIVE"
                    if "STATUS = 'SPEC'" in init_text or "Status: SPEC" in init_text:
                        status = "SPEC"

                    rel_path = str(mod_dir.relative_to(ROOT))
                    modules.append({
                        "module_id": f"M{mid}",
                        "name": mod_dir.name,
                        "house": hid,
                        "house_name": hname,
                        "sphere_name": sname,
                        "house_dir": hdir,
                        "sphere_dir": sdir,
                        "status": status,
                        "path": rel_path,
                    })

    registry = {
        "version": "3.14",
        "canon": "COMPLETE_BUILD_PLAN_v3.14 Appendix AG",
        "houses": 12,
        "spheres_per_house": 12,
        "total_spheres": 144,
        "element_145": "e145/",
        "total_modules": len(modules),
        "modules": modules,
    }

    out = ROOT / "registries" / "module_registry.yaml"
    with open(out, "w") as f:
        f.write("# Module Registry v3.14\n")
        f.write("# AUTO-GENERATED from filesystem — DO NOT EDIT MANUALLY\n")
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  Written: {out} ({len(modules)} modules)")

    # Stats
    active = sum(1 for m in modules if m["status"] == "ACTIVE")
    spec = sum(1 for m in modules if m["status"] == "SPEC")
    print(f"  ACTIVE: {active}, SPEC: {spec}")

    # Per-house breakdown
    from collections import Counter
    house_counts = Counter(m["house"] for m in modules)
    for hid in HOUSE_IDS:
        c = house_counts.get(hid, 0)
        print(f"    {hid} {HOUSE_NAMES[HOUSE_IDS.index(hid)]}: {c} modules")


# ============================================================
# 4. Update ontology lock file
# ============================================================

def update_lock():
    lock_dir = ROOT / "registries"
    lock_file = lock_dir / "ontology_lock.sha256"

    files_to_hash = [
        ROOT / "e145" / "aluminum-os-core" / "lattice_ontology_v2.py",
        ROOT / "registries" / "lattice_ontology.yaml",
        ROOT / "registries" / "12x12_matrix.yaml",
        ROOT / "registries" / "module_registry.yaml",
    ]

    hashes = {}
    for f in files_to_hash:
        if f.exists():
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            hashes[str(f.relative_to(ROOT))] = h

    with open(lock_file, "w") as f:
        f.write(f"# Ontology Lock — D-89 Enforcement\n")
        f.write(f"# Generated: {__import__('datetime').datetime.utcnow().isoformat()}Z\n")
        f.write(f"# Ontology hash: {compute_ontology_hash()}\n\n")
        for path, h in sorted(hashes.items()):
            f.write(f"{h}  {path}\n")

    print(f"  Written: {lock_file}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=== Regenerating registries from canonical v3.14 ===\n")

    print("1. lattice_ontology.yaml")
    regen_lattice_ontology()

    print("\n2. 12x12_matrix.yaml")
    regen_matrix()

    print("\n3. module_registry.yaml")
    regen_module_registry()

    print("\n4. ontology_lock.sha256")
    update_lock()

    print("\n=== DONE ===")
