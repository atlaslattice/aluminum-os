#!/usr/bin/env python3
"""
perfect_square_validation.py — Perfect-Square Lattice Validation
================================================================
Per S4 Fixed-Lattice Reframe recommendation #2:
Canonical pipeline on N ∈ {100, 121, 144, 169, 196}.
If 144 is special among squares, the 12×12 grid structure has mathematical significance.

Uses OPTIMIZED parameters from operator_sweep_n145.py results.
"""

import numpy as np
from scipy import linalg, stats
import json
import time
import sys

sys.path.insert(0, '.')
from shugs_core import build_hsuf_operator, compute_gue_ks

# Perfect squares to test
PERFECT_SQUARES = [100, 121, 144, 169, 196]
SQUARE_ROOTS = {100: 10, 121: 11, 144: 12, 169: 13, 196: 14}

K = 20  # Ensemble size
BASE_SEED = 42


def run_perfect_square_test(N, K=20, base_seed=42):
    """Run K-ensemble GUE-KS test at a given N."""
    scores = []
    t0 = time.time()
    
    for k in range(K):
        jitter_seed = base_seed + k * 1000 + N
        H = build_hsuf_operator(N, jitter_seed=jitter_seed)
        eigenvalues = linalg.eigvalsh(H)
        ks = compute_gue_ks(eigenvalues)
        scores.append(ks)
    
    elapsed = time.time() - t0
    arr = np.array(scores)
    
    return {
        "N": N,
        "sqrt_N": SQUARE_ROOTS.get(N, int(np.sqrt(N))),
        "mean_gue_ks": float(np.mean(arr)),
        "std_gue_ks": float(np.std(arr)),
        "sem_gue_ks": float(np.std(arr) / np.sqrt(K)),
        "K": K,
        "elapsed": elapsed,
        "raw_scores": [float(x) for x in arr]
    }


def main():
    print("=== Perfect-Square Lattice Validation (Canonical Pipeline) ===")
    print(f"N ∈ {PERFECT_SQUARES}, K={K} ensemble each")
    print()
    
    results = []
    
    for N in PERFECT_SQUARES:
        r = run_perfect_square_test(N, K=K)
        results.append(r)
        print(f"  N={N:4d} (√N={r['sqrt_N']:2d}): GUE-KS = {r['mean_gue_ks']:.4f} ± {r['sem_gue_ks']:.4f}  [{r['elapsed']:.1f}s]")
    
    print()
    
    # Pairwise comparisons vs N=144
    ref = next(r for r in results if r["N"] == 144)
    ref_scores = ref["raw_scores"]
    
    print("--- Pairwise Comparisons vs N=144 ---")
    for r in results:
        if r["N"] == 144:
            print(f"  N={r['N']:4d}: (reference)")
            continue
        t_stat, p_val = stats.ttest_ind(ref_scores, r["raw_scores"])
        direction = "N=144 better" if ref["mean_gue_ks"] < r["mean_gue_ks"] else f"N={r['N']} better"
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        print(f"  N={r['N']:4d}: p={p_val:.4f} {sig} ({direction})")
        r["vs_144_p"] = float(p_val)
        r["vs_144_direction"] = direction
    
    print()
    
    # Check if 144 is locally special (better than 121 and 169)
    r121 = next(r for r in results if r["N"] == 121)
    r169 = next(r for r in results if r["N"] == 169)
    
    _, p_121 = stats.ttest_ind(ref_scores, r121["raw_scores"])
    _, p_169 = stats.ttest_ind(ref_scores, r169["raw_scores"])
    
    locally_special = (ref["mean_gue_ks"] < r121["mean_gue_ks"] and p_121 < 0.05 and
                       ref["mean_gue_ks"] < r169["mean_gue_ks"] and p_169 < 0.05)
    
    print(f"N=144 locally special (better than both neighbors 121, 169)? {'YES' if locally_special else 'NO'}")
    
    # Check global ranking
    sorted_results = sorted(results, key=lambda x: x["mean_gue_ks"])
    print(f"\nGlobal ranking among perfect squares:")
    for i, r in enumerate(sorted_results, 1):
        marker = " ← 12×12" if r["N"] == 144 else ""
        print(f"  {i}. N={r['N']} (√N={r['sqrt_N']}): GUE-KS = {r['mean_gue_ks']:.4f}{marker}")
    
    # Also test N=145 for comparison
    print(f"\n--- N=145 (architectural invariant) for comparison ---")
    r145 = run_perfect_square_test(145, K=K)
    r145["sqrt_N"] = "N/A"
    print(f"  N=145: GUE-KS = {r145['mean_gue_ks']:.4f} ± {r145['sem_gue_ks']:.4f}")
    _, p_145_vs_144 = stats.ttest_ind(r145["raw_scores"], ref_scores)
    print(f"  N=145 vs N=144: p={p_145_vs_144:.4f} ({'N=145 better' if r145['mean_gue_ks'] < ref['mean_gue_ks'] else 'N=144 better'})")
    
    results.append(r145)
    
    # Save
    output = {
        "test": "perfect_square_validation",
        "paradigm": "fixed-lattice",
        "perfect_squares_tested": PERFECT_SQUARES,
        "K": K,
        "results": results,
        "n144_locally_special": locally_special,
        "global_ranking": [r["N"] for r in sorted_results],
    }
    
    outpath = "perfect_square_validation_results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
