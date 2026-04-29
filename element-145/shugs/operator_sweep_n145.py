#!/usr/bin/env python3
"""
operator_sweep_n145.py — Operator Parameter Sweep at Fixed N=145
================================================================
Per S4 Fixed-Lattice Reframe recommendation #1:
Vary smearing decay, off-diagonal weight, Riemann zero count, and window function.
K=20 ensemble for each configuration. Find the parameter set that minimizes GUE-KS at N=145.

This is a tractable optimization problem over a 4D parameter space.
"""

import numpy as np
from scipy import linalg, stats
from sympy import isprime, factorint
import json
import time
import itertools
from dataclasses import dataclass, asdict
from typing import List, Optional

# Import core functions from shugs_core
import sys
sys.path.insert(0, '.')
from shugs_core import (
    precompute_von_mangoldt, RIEMANN_ZEROS, compute_gue_ks,
    JITTER_AMP, W_LOG
)

N_FIXED = 145  # ARCHITECTURAL INVARIANT

# ============================================================
# §1 — SWEEP PARAMETER RANGES (per S4 recommendation)
# ============================================================

DECAY_VALUES = [10, 14, 18.9, 24, 30]           # Smearing decay
W_OFFDIAG_VALUES = [0.01, 0.03, 0.05, 0.10, 0.15]  # Off-diagonal weight
M_VALUES = [10, 20, 30, 50]                       # Riemann zero count
WINDOW_FUNCTIONS = ['hanning', 'blackman', 'kaiser']  # Window type
W_SMEAR_VALUES = [0.1, 0.2, 0.3, 0.4, 0.5]     # Smearing weight

# For the initial sweep, we fix w_smear and sweep the other 4 dimensions
# Then do a focused sweep around the best configuration


# ============================================================
# §2 — OPERATOR WITH CONFIGURABLE WINDOW
# ============================================================

def build_operator_configurable(
    N: int,
    w_smear: float,
    w_offdiag: float,
    decay: float,
    M: int,
    window_type: str,
    jitter_seed: Optional[int] = None,
    jitter_amp: float = JITTER_AMP,
    w_log: float = W_LOG,
) -> np.ndarray:
    """Build HSUF operator with configurable window function."""
    Lambda = precompute_von_mangoldt(N)
    pp_indices = np.where(Lambda > 0)[0]
    pp_values = Lambda[pp_indices]

    # Diagonal
    diag = np.zeros(N)
    for i in range(N):
        diag[i] = Lambda[i]
        smear = 0.0
        for pp_idx, pp_val in zip(pp_indices, pp_values):
            smear += pp_val * np.exp(-abs(i - pp_idx) / decay)
        diag[i] += w_smear * smear
        diag[i] += w_log * np.log(i + 2)

    nonzero_diag = diag[diag > 0]
    sigma_lambda = np.std(nonzero_diag) if len(nonzero_diag) > 1 else 1.0

    # Off-diagonal
    gamma = np.array(RIEMANN_ZEROS[:M])
    H = np.zeros((N, N))
    np.fill_diagonal(H, diag)

    for i in range(N):
        for j in range(i + 1, N):
            diff = abs(i - j)
            coupling = sum(np.cos(gamma[k] * np.log(diff + 1)) / gamma[k] for k in range(M))
            H[i, j] = w_offdiag * coupling * sigma_lambda
            H[j, i] = H[i, j]

    # Window function
    if window_type == 'hanning':
        window = np.hanning(N)
    elif window_type == 'blackman':
        window = np.blackman(N)
    elif window_type == 'kaiser':
        window = np.kaiser(N, beta=14)
    else:
        window = np.hanning(N)

    window = window / window.max() if window.max() > 0 else window
    W = np.diag(window)
    H = W @ H @ W

    # Jitter
    if jitter_seed is not None:
        rng = np.random.RandomState(jitter_seed)
        H += np.diag(rng.normal(0, jitter_amp * sigma_lambda, N))

    return H


# ============================================================
# §3 — SWEEP RUNNER
# ============================================================

@dataclass
class SweepResult:
    decay: float
    w_smear: float
    w_offdiag: float
    M: int
    window: str
    mean_gue_ks: float
    std_gue_ks: float
    sem_gue_ks: float
    K: int
    elapsed: float


def run_sweep_point(decay, w_smear, w_offdiag, M, window, K=20, base_seed=42):
    """Run a single sweep configuration."""
    scores = []
    t0 = time.time()

    for k in range(K):
        jitter_seed = base_seed + k * 1000 + N_FIXED
        H = build_operator_configurable(
            N_FIXED, w_smear=w_smear, w_offdiag=w_offdiag,
            decay=decay, M=M, window_type=window, jitter_seed=jitter_seed
        )
        eigenvalues = linalg.eigvalsh(H)
        ks = compute_gue_ks(eigenvalues)
        scores.append(ks)

    elapsed = time.time() - t0
    arr = np.array(scores)

    return SweepResult(
        decay=decay, w_smear=w_smear, w_offdiag=w_offdiag,
        M=M, window=window,
        mean_gue_ks=float(np.mean(arr)),
        std_gue_ks=float(np.std(arr)),
        sem_gue_ks=float(np.std(arr) / np.sqrt(K)),
        K=K, elapsed=elapsed
    )


def main():
    """Run the operator parameter sweep at fixed N=145."""
    print(f"=== SHUGS Operator Parameter Sweep at Fixed N={N_FIXED} ===")
    print(f"Fixed-Lattice Paradigm — per S4 Recommendation #1")
    print()

    # Phase 1: Coarse sweep over key dimensions
    # Fix w_smear=0.3 (canonical), sweep decay x w_offdiag x M x window
    # That's 5 x 5 x 4 x 3 = 300 configs at K=20 each — too many
    # Instead: sweep each dimension independently first, then combine best

    results = []

    # === Sweep 1: Decay (fix others at canonical) ===
    print("--- Sweep 1: Smearing Decay ---")
    for decay in DECAY_VALUES:
        r = run_sweep_point(decay, 0.3, 0.05, 20, 'hanning', K=20)
        results.append(r)
        print(f"  decay={decay:5.1f}: GUE-KS={r.mean_gue_ks:.4f} ± {r.sem_gue_ks:.4f} [{r.elapsed:.1f}s]")

    best_decay = min(results, key=lambda x: x.mean_gue_ks).decay
    print(f"  → Best decay: {best_decay}")
    print()

    # === Sweep 2: Off-diagonal weight (fix others, use best decay) ===
    print("--- Sweep 2: Off-Diagonal Weight ---")
    sweep2 = []
    for w_od in W_OFFDIAG_VALUES:
        r = run_sweep_point(best_decay, 0.3, w_od, 20, 'hanning', K=20)
        sweep2.append(r)
        results.append(r)
        print(f"  w_offdiag={w_od:.2f}: GUE-KS={r.mean_gue_ks:.4f} ± {r.sem_gue_ks:.4f} [{r.elapsed:.1f}s]")

    best_w_offdiag = min(sweep2, key=lambda x: x.mean_gue_ks).w_offdiag
    print(f"  → Best w_offdiag: {best_w_offdiag}")
    print()

    # === Sweep 3: Riemann zero count (fix others, use best decay + w_offdiag) ===
    print("--- Sweep 3: Riemann Zero Count ---")
    sweep3 = []
    for M in M_VALUES:
        r = run_sweep_point(best_decay, 0.3, best_w_offdiag, M, 'hanning', K=20)
        sweep3.append(r)
        results.append(r)
        print(f"  M={M:3d}: GUE-KS={r.mean_gue_ks:.4f} ± {r.sem_gue_ks:.4f} [{r.elapsed:.1f}s]")

    best_M = min(sweep3, key=lambda x: x.mean_gue_ks).M
    print(f"  → Best M: {best_M}")
    print()

    # === Sweep 4: Window function ===
    print("--- Sweep 4: Window Function ---")
    sweep4 = []
    for win in WINDOW_FUNCTIONS:
        r = run_sweep_point(best_decay, 0.3, best_w_offdiag, best_M, win, K=20)
        sweep4.append(r)
        results.append(r)
        print(f"  window={win:10s}: GUE-KS={r.mean_gue_ks:.4f} ± {r.sem_gue_ks:.4f} [{r.elapsed:.1f}s]")

    best_window = min(sweep4, key=lambda x: x.mean_gue_ks).window
    print(f"  → Best window: {best_window}")
    print()

    # === Sweep 5: Smearing weight (with all best params) ===
    print("--- Sweep 5: Smearing Weight ---")
    sweep5 = []
    for w_sm in W_SMEAR_VALUES:
        r = run_sweep_point(best_decay, w_sm, best_w_offdiag, best_M, best_window, K=20)
        sweep5.append(r)
        results.append(r)
        print(f"  w_smear={w_sm:.1f}: GUE-KS={r.mean_gue_ks:.4f} ± {r.sem_gue_ks:.4f} [{r.elapsed:.1f}s]")

    best_w_smear = min(sweep5, key=lambda x: x.mean_gue_ks).w_smear
    print(f"  → Best w_smear: {best_w_smear}")
    print()

    # === Final: Best configuration ===
    print("=== FINAL: Best Configuration at N=145 ===")
    final = run_sweep_point(best_decay, best_w_smear, best_w_offdiag, best_M, best_window, K=20)
    results.append(final)

    print(f"  decay     = {best_decay}")
    print(f"  w_smear   = {best_w_smear}")
    print(f"  w_offdiag = {best_w_offdiag}")
    print(f"  M         = {best_M}")
    print(f"  window    = {best_window}")
    print(f"  GUE-KS    = {final.mean_gue_ks:.4f} ± {final.sem_gue_ks:.4f}")
    print()

    # Compare to canonical baseline
    canonical = run_sweep_point(18.9, 0.3, 0.05, 20, 'hanning', K=20)
    improvement = (canonical.mean_gue_ks - final.mean_gue_ks) / canonical.mean_gue_ks * 100
    print(f"  Canonical baseline: GUE-KS = {canonical.mean_gue_ks:.4f}")
    print(f"  Best found:         GUE-KS = {final.mean_gue_ks:.4f}")
    print(f"  Improvement:        {improvement:+.1f}%")

    # Save results
    output = {
        "N": N_FIXED,
        "paradigm": "fixed-lattice",
        "sweep_results": [asdict(r) for r in results],
        "best_config": {
            "decay": best_decay,
            "w_smear": best_w_smear,
            "w_offdiag": best_w_offdiag,
            "M": best_M,
            "window": best_window,
            "mean_gue_ks": final.mean_gue_ks,
            "std_gue_ks": final.std_gue_ks,
            "sem_gue_ks": final.sem_gue_ks,
        },
        "canonical_baseline": {
            "mean_gue_ks": canonical.mean_gue_ks,
            "improvement_pct": improvement,
        }
    }

    outpath = "operator_sweep_n145_results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
