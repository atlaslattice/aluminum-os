#!/usr/bin/env python3
"""
validate_domain_repos.py — CI gate for domain_repos/domain_repo_index.yaml

Checks:
1. Each referenced repo URL resolves (optional — requires network)
2. Each has a declared house/sphere mapping
3. No duplicates
4. No unmapped entries
5. House/Sphere values are valid

Usage:
  python toolchain/validate_domain_repos.py              # Full validation (offline)
  python toolchain/validate_domain_repos.py --online     # Also verify GitHub URLs resolve
  python toolchain/validate_domain_repos.py --strict     # Require pinned refs
"""

import os
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "domain_repos", "domain_repo_index.yaml")

# Valid houses and spheres
VALID_HOUSES = {f"H{i:02d}" for i in range(1, 13)}
VALID_SPHERES = {f"S{i:02d}" for i in range(1, 13)}


def load_index():
    """Load and parse the domain repo index."""
    if not os.path.exists(INDEX_PATH):
        print(f"ERROR: Index file not found: {INDEX_PATH}")
        sys.exit(1)

    with open(INDEX_PATH) as f:
        data = yaml.safe_load(f)

    if not data or "repos" not in data:
        print("ERROR: Index file is empty or missing 'repos' key")
        sys.exit(1)

    return data


def validate_structure(data):
    """Validate the index structure and required fields."""
    errors = []
    warnings = []
    repos = data.get("repos", {})
    seen_repos = set()

    for repo_name, manifest in repos.items():
        # Check for duplicates
        if repo_name in seen_repos:
            errors.append(f"DUPLICATE: {repo_name} appears more than once")
        seen_repos.add(repo_name)

        # Check required fields
        if "lattice_position" not in manifest:
            errors.append(f"MISSING lattice_position: {repo_name}")
            continue

        pos = manifest["lattice_position"]

        # Check house
        house = pos.get("house")
        if not house:
            errors.append(f"MISSING house: {repo_name}")
        elif house not in VALID_HOUSES:
            errors.append(f"INVALID house '{house}': {repo_name} (valid: H01-H12)")

        # Check sphere
        sphere = pos.get("sphere")
        if not sphere:
            errors.append(f"MISSING sphere: {repo_name}")
        elif sphere not in VALID_SPHERES:
            errors.append(f"INVALID sphere '{sphere}': {repo_name} (valid: S01-S12)")

        # Check repo URL format
        repo_url = manifest.get("repo", "")
        if not repo_url:
            errors.append(f"MISSING repo URL: {repo_name}")
        elif not repo_url.startswith("atlaslattice/"):
            warnings.append(f"NON-STANDARD repo URL: {repo_name} → {repo_url}")

        # Check description
        if not manifest.get("description"):
            warnings.append(f"MISSING description: {repo_name}")

    return errors, warnings


def validate_online(data):
    """Verify that referenced repos actually exist on GitHub (requires network)."""
    import urllib.request
    import urllib.error

    repos = data.get("repos", {})
    errors = []
    checked = 0

    for repo_name, manifest in repos.items():
        repo_url = manifest.get("repo", "")
        if not repo_url:
            continue

        github_url = f"https://github.com/{repo_url}"
        try:
            req = urllib.request.Request(github_url, method="HEAD")
            urllib.request.urlopen(req, timeout=5)
            checked += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                errors.append(f"REPO NOT FOUND (404): {repo_url}")
            # 403 = private repo, that's OK
        except Exception as e:
            errors.append(f"UNREACHABLE: {repo_url} ({e})")

    print(f"  Online check: {checked}/{len(repos)} repos verified")
    return errors


def validate_strict(data):
    """Require pinned refs for reproducibility."""
    repos = data.get("repos", {})
    warnings = []

    for repo_name, manifest in repos.items():
        if "pinned_ref" not in manifest and "pinned_tag" not in manifest:
            warnings.append(f"NO PINNED REF: {repo_name} (not reproducible)")

    return warnings


def main():
    args = sys.argv[1:]
    online = "--online" in args
    strict = "--strict" in args

    print("=== Domain Repo Index Validation ===")
    print(f"  Index: {INDEX_PATH}")

    data = load_index()
    repos = data.get("repos", {})
    print(f"  Total repos: {len(repos)}")
    print()

    # Structure validation
    errors, warnings = validate_structure(data)

    # Online validation
    if online:
        print("  Running online validation...")
        online_errors = validate_online(data)
        errors.extend(online_errors)

    # Strict validation
    if strict:
        strict_warnings = validate_strict(data)
        warnings.extend(strict_warnings)

    # Report
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  {w}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        print(f"\nVALIDATION FAILED — {len(errors)} error(s)")
        sys.exit(1)
    else:
        # House distribution
        house_counts = {}
        for repo_name, manifest in repos.items():
            h = manifest.get("lattice_position", {}).get("house", "?")
            house_counts[h] = house_counts.get(h, 0) + 1

        print("\n  Distribution:")
        for h in sorted(house_counts.keys()):
            print(f"    {h}: {house_counts[h]} repos")

        print(f"\n✓ VALIDATION PASSED — {len(repos)} repos, 0 errors, {len(warnings)} warnings")


if __name__ == "__main__":
    main()
