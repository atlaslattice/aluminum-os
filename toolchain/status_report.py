#!/usr/bin/env python3
"""Show per-house ABSORBED vs SPEC breakdown."""
import yaml

with open("/home/ubuntu/aluminum-os/registries/module_registry.yaml") as f:
    data = yaml.safe_load(f)

houses = {}
for m in data["modules"]:
    h = m["house"]
    s = m["status"]
    if h not in houses:
        houses[h] = {"ABSORBED": 0, "SPEC": 0, "total": 0}
    houses[h][s] = houses[h].get(s, 0) + 1
    houses[h]["total"] += 1

header = f"{'House':6s} {'ABSORBED':>8s} {'SPEC':>6s} {'Total':>6s} {'%':>5s}"
print(header)
print("-" * len(header))
total_a, total_s = 0, 0
for h in sorted(houses.keys()):
    a = houses[h].get("ABSORBED", 0)
    s = houses[h].get("SPEC", 0)
    t = houses[h]["total"]
    pct = f"{a/t*100:.0f}%" if t > 0 else "0%"
    print(f"{h:6s} {a:8d} {s:6d} {t:6d} {pct:>5s}")
    total_a += a
    total_s += s
print("-" * len(header))
print(f"{'TOTAL':6s} {total_a:8d} {total_s:6d} {total_a+total_s:6d} {total_a/(total_a+total_s)*100:.0f}%")
