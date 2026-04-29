#!/usr/bin/env python3
"""
CSV Sphere Loader - Load 144-sphere framework from Dave's CSV
This allows Dave to edit the CSV and have changes reflected automatically
"""

import csv
import os
from typing import List, Dict, Tuple

def load_144_spheres_from_csv(csv_path: str = "../144 spheres chart - Sheet1.csv") -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Load the 144-sphere framework from Dave's authoritative CSV file

    Returns:
        Tuple of (SPHERES, ELEMENTS, GODS, CATEGORY_NAMES)
    """

    # Resolve path relative to this file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, csv_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"CSV not found: {full_path}")

    spheres = []
    elements = []
    gods = []
    categories = []

    with open(full_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Extract data
            sphere_name = row['Sub Sphere'].strip()
            element = row['Element (1-144)'].strip()
            god = row['God (Tailored to Sphere/Element Traits)'].strip()
            category = row['Main Category'].split('(')[0].strip()

            spheres.append(sphere_name)
            elements.append(element)
            gods.append(god)

            # Track unique categories in order
            if category not in categories:
                categories.append(category)

    # Validate we got 144 spheres
    assert len(spheres) == 144, f"Expected 144 spheres, got {len(spheres)}"
    assert len(elements) == 144, f"Expected 144 elements, got {len(elements)}"
    assert len(gods) == 144, f"Expected 144 gods, got {len(gods)}"
    assert len(categories) == 12, f"Expected 12 categories, got {len(categories)}"

    return spheres, elements, gods, categories


def verify_csv_matches_hardcoded():
    """
    Verification function to ensure CSV matches hardcoded implementation
    Run this to validate Dave's CSV against the current implementation
    """
    from grokbrain_v4 import SPHERES, ELEMENTS, GODS, CATEGORY_NAMES

    csv_spheres, csv_elements, csv_gods, csv_categories = load_144_spheres_from_csv()

    mismatches = []

    # Check spheres
    for i in range(144):
        if SPHERES[i] != csv_spheres[i]:
            mismatches.append(f"Sphere {i+1}: Code='{SPHERES[i]}' vs CSV='{csv_spheres[i]}'")

    # Check elements
    for i in range(144):
        if ELEMENTS[i] != csv_elements[i]:
            mismatches.append(f"Element {i+1}: Code='{ELEMENTS[i]}' vs CSV='{csv_elements[i]}'")

    # Check gods
    for i in range(144):
        if GODS[i] != csv_gods[i]:
            mismatches.append(f"God {i+1}: Code='{GODS[i]}' vs CSV='{csv_gods[i]}'")

    # Check categories
    for i in range(12):
        if CATEGORY_NAMES[i] != csv_categories[i]:
            mismatches.append(f"Category {i}: Code='{CATEGORY_NAMES[i]}' vs CSV='{csv_categories[i]}'")

    if mismatches:
        print("❌ MISMATCHES FOUND:")
        for m in mismatches:
            print(f"  {m}")
        return False
    else:
        print("✅ CSV matches hardcoded implementation 100%!")
        print(f"   - 144 spheres verified")
        print(f"   - 144 elements verified")
        print(f"   - 144 gods verified")
        print(f"   - 12 categories verified")
        return True


if __name__ == "__main__":
    print("=" * 70)
    print("CSV SPHERE LOADER - Verification")
    print("=" * 70)
    print()

    try:
        spheres, elements, gods, categories = load_144_spheres_from_csv()
        print(f"✅ Successfully loaded from CSV:")
        print(f"   - {len(spheres)} spheres")
        print(f"   - {len(elements)} elements")
        print(f"   - {len(gods)} gods")
        print(f"   - {len(categories)} categories")
        print()

        print("Sample data (first 3 spheres):")
        for i in range(3):
            print(f"  {i+1}. {spheres[i]} → {elements[i]} → {gods[i]}")
        print()

        print("Verifying against hardcoded implementation...")
        verify_csv_matches_hardcoded()

    except Exception as e:
        print(f"❌ Error: {e}")
