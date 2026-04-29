#!/usr/bin/env python3
"""
shugs_core.py — Canonical SHUGS Pipeline Implementation
=========================================================
Sheldon Harmonic Unification Gradient System
Von Mangoldt-Sheldon HSUF Operator Construction + GUE-KS Measurement

Implements the operator specified in WP-002:
  H_ii = Λ(i) + w_smear · Σ_pp [Λ(pp) · exp(-|i-pp|/decay)] + w_log · log(i+1)
  H_ij = w_offdiag · Σ_{k=1..M} cos(γ_k · log|i-j+1|) / γ_k · σ_Λ
  H = W · H_raw · W   (Hanning window, absorbing boundary)

GUE-KS: Kolmogorov-Smirnov distance from Wigner surmise CDF.

Attribution: Inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
Canonical pipeline: Manus S7 (Build Seat).
"""

import numpy as np
from scipy import linalg, stats
from sympy import isprime, factorint
import json
import sys
import time
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

# ============================================================
# §1 — CONSTANTS (Canonical Configuration)
# ============================================================

# First 50 imaginary parts of non-trivial Riemann zeta zeros
# Source: LMFDB / Odlyzko tables (verified to 6 decimal places)
RIEMANN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320220, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516684, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
]

# Operator weights — canonical configuration
W_SMEAR = 0.3          # Smearing weight for prime-power proximity
W_LOG = 0.15           # Logarithmic growth weight
W_OFFDIAG = 0.05       # Off-diagonal coupling weight
DECAY = 18.9           # Path B-Prime smearing constant
JITTER_AMP = 0.02      # Ensemble jitter amplitude (fraction of σ_Λ)
M_DEFAULT = 20         # Default number of Riemann zeros in off-diagonal kernel

# Lattice constants (per LATTICE_CONSTANTS.md)
LATTICE_SPHERES_ONLY = 144
LATTICE_FULL = 145
LATTICE_DEFAULT = 145


# ============================================================
# §2 — VON MANGOLDT FUNCTION
# ============================================================

def von_mangoldt(n: int) -> float:
    """
    Compute Λ(n) — the Von Mangoldt function.
    Λ(n) = log(p) if n = p^k for some prime p and integer k ≥ 1
    Λ(n) = 0 otherwise
    """
    if n < 2:
        return 0.0
    if isprime(n):
        return float(np.log(n))
    factors = factorint(n)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        return float(np.log(p))
    return 0.0


def precompute_von_mangoldt(N: int) -> np.ndarray:
    """Precompute Λ(i) for i = 1..N."""
    return np.array([von_mangoldt(i) for i in range(1, N + 1)])


# ============================================================
# §3 — HSUF OPERATOR CONSTRUCTION
# ============================================================

def build_hsuf_operator(
    N: int,
    M: int = M_DEFAULT,
    w_smear: float = W_SMEAR,
    w_log: float = W_LOG,
    w_offdiag: float = W_OFFDIAG,
    decay: float = DECAY,
    jitter_seed: Optional[int] = None,
    jitter_amp: float = JITTER_AMP,
) -> np.ndarray:
    """
    Build the N×N Hermitian HSUF operator matrix.

    Parameters
    ----------
    N : int
        Matrix dimension (lattice size).
    M : int
        Number of Riemann zeta zeros to use in off-diagonal kernel.
    w_smear, w_log, w_offdiag : float
        Operator weight parameters.
    decay : float
        Path B-Prime smearing constant.
    jitter_seed : int or None
        If not None, add small diagonal jitter for ensemble variance estimation.
    jitter_amp : float
        Jitter amplitude as fraction of σ_Λ.

    Returns
    -------
    H : np.ndarray
        N×N real symmetric matrix (Hermitian with real entries).
    """
    # Precompute Von Mangoldt values
    Lambda = precompute_von_mangoldt(N)

    # Find prime power positions (where Λ > 0)
    pp_indices = np.where(Lambda > 0)[0]
    pp_values = Lambda[pp_indices]

    # === DIAGONAL ===
    diag = np.zeros(N)
    for i in range(N):
        # Base: Λ(i+1)
        diag[i] = Lambda[i]

        # Smeared prime-power proximity
        smear = 0.0
        for pp_idx, pp_val in zip(pp_indices, pp_values):
            distance = abs(i - pp_idx)
            smear += pp_val * np.exp(-distance / decay)
        diag[i] += w_smear * smear

        # Logarithmic growth
        diag[i] += w_log * np.log(i + 2)  # log(i+1) with 1-indexed → log(i+2)

    # Compute σ_Λ (std of non-zero diagonal entries for scaling)
    nonzero_diag = diag[diag > 0]
    if len(nonzero_diag) > 1:
        sigma_lambda = np.std(nonzero_diag)
    else:
        sigma_lambda = 1.0

    # === OFF-DIAGONAL ===
    gamma = np.array(RIEMANN_ZEROS[:M])
    H = np.zeros((N, N))
    np.fill_diagonal(H, diag)

    for i in range(N):
        for j in range(i + 1, N):
            diff = abs(i - j)
            coupling = 0.0
            for k in range(M):
                coupling += np.cos(gamma[k] * np.log(diff + 1)) / gamma[k]
            H[i, j] = w_offdiag * coupling * sigma_lambda
            H[j, i] = H[i, j]

    # === HANNING WINDOW (absorbing boundary) ===
    window = np.hanning(N)
    # Normalize window so center ≈ 1
    window = window / window.max() if window.max() > 0 else window
    W = np.diag(window)
    H = W @ H @ W

    # === ENSEMBLE JITTER ===
    if jitter_seed is not None:
        rng = np.random.RandomState(jitter_seed)
        jitter = rng.normal(0, jitter_amp * sigma_lambda, N)
        H += np.diag(jitter)

    return H


# ============================================================
# §4 — GUE-KS MEASUREMENT
# ============================================================

def gue_wigner_surmise_cdf(s: np.ndarray) -> np.ndarray:
    """
    GUE Wigner surmise CDF: F(s) = erf(2s/√π) − (4s/π)·exp(−4s²/π)

    This is the CDF of the nearest-neighbor spacing distribution for
    the Gaussian Unitary Ensemble.
    """
    from scipy.special import erf
    term1 = erf(2 * s / np.sqrt(np.pi))
    term2 = (4 * s / np.pi) * np.exp(-4 * s**2 / np.pi)
    return term1 - term2


def compute_gue_ks(eigenvalues: np.ndarray, trim_fraction: float = 0.1) -> float:
    """
    Compute GUE-KS distance for a set of eigenvalues.

    Steps:
    1. Sort eigenvalues
    2. Unfold via degree-5 polynomial fit to staircase function
    3. Compute nearest-neighbor spacings
    4. Normalize spacings to mean = 1
    5. Trim boundary spacings
    6. KS-test against GUE Wigner surmise CDF

    Parameters
    ----------
    eigenvalues : np.ndarray
        Array of real eigenvalues.
    trim_fraction : float
        Fraction of spacings to trim from each boundary.

    Returns
    -------
    ks_distance : float
        KS statistic (lower = closer to GUE).
    """
    eigs = np.sort(np.real(eigenvalues))
    n = len(eigs)

    # Staircase function
    staircase_x = eigs
    staircase_y = np.arange(1, n + 1, dtype=float)

    # Unfolding: fit degree-5 polynomial to staircase
    try:
        coeffs = np.polyfit(staircase_x, staircase_y, 5)
        unfolded = np.polyval(coeffs, eigs)
    except (np.linalg.LinAlgError, ValueError):
        return 1.0  # Return worst-case on numerical failure

    # Nearest-neighbor spacings
    spacings = np.diff(unfolded)

    # Remove non-positive spacings (numerical artifacts)
    spacings = spacings[spacings > 0]
    if len(spacings) < 10:
        return 1.0

    # Normalize to mean = 1
    mean_spacing = np.mean(spacings)
    if mean_spacing > 0:
        spacings = spacings / mean_spacing

    # Trim boundary
    trim_n = int(trim_fraction * len(spacings))
    if trim_n > 0:
        spacings = spacings[trim_n:-trim_n]
    if len(spacings) < 10:
        return 1.0

    # KS test against GUE Wigner surmise
    ks_stat, _ = stats.kstest(spacings, gue_wigner_surmise_cdf)
    return float(ks_stat)


# ============================================================
# §5 — ENSEMBLE RUNNER
# ============================================================

@dataclass
class EnsembleResult:
    """Result of a single N-value ensemble run."""
    N: int
    K: int
    M: int
    mean_gue_ks: float
    std_gue_ks: float
    sem_gue_ks: float
    min_gue_ks: float
    max_gue_ks: float
    scores: List[float]
    elapsed_seconds: float


def run_ensemble(
    N: int,
    K: int = 20,
    M: int = M_DEFAULT,
    base_seed: int = 42,
    **operator_kwargs,
) -> EnsembleResult:
    """
    Run K-realization ensemble at lattice size N.

    Parameters
    ----------
    N : int
        Matrix dimension.
    K : int
        Number of ensemble realizations.
    M : int
        Number of Riemann zeros.
    base_seed : int
        Base seed for reproducibility. Jitter seed = base_seed + k*1000 + N.

    Returns
    -------
    EnsembleResult
        Aggregated statistics.
    """
    scores = []
    t0 = time.time()

    for k in range(K):
        jitter_seed = base_seed + k * 1000 + N
        H = build_hsuf_operator(N, M=M, jitter_seed=jitter_seed, **operator_kwargs)
        eigenvalues = linalg.eigvalsh(H)
        ks = compute_gue_ks(eigenvalues)
        scores.append(ks)

    elapsed = time.time() - t0
    scores_arr = np.array(scores)

    return EnsembleResult(
        N=N,
        K=K,
        M=M,
        mean_gue_ks=float(np.mean(scores_arr)),
        std_gue_ks=float(np.std(scores_arr)),
        sem_gue_ks=float(np.std(scores_arr) / np.sqrt(K)),
        min_gue_ks=float(np.min(scores_arr)),
        max_gue_ks=float(np.max(scores_arr)),
        scores=[float(s) for s in scores],
        elapsed_seconds=elapsed,
    )


# ============================================================
# §6 — PAIRWISE SIGNIFICANCE TEST
# ============================================================

def welch_t_test(scores_a: List[float], scores_b: List[float]) -> Tuple[float, float]:
    """
    Welch's t-test (unequal variance) on two score arrays.
    Returns (t_statistic, p_value).
    """
    result = stats.ttest_ind(scores_a, scores_b, equal_var=False)
    return float(result.statistic), float(result.pvalue)


# ============================================================
# §7 — CLI ENTRY POINTS
# ============================================================

def run_lattice_optimum_test(K: int = 20, N_range: Tuple[int, int] = (140, 148)):
    """
    Run the lattice optimum test: K-ensemble across N=N_range[0]..N_range[1].
    This is the canonical replication of Claude S1's inter-seat ask #1.
    """
    results = {}
    N_values = list(range(N_range[0], N_range[1] + 1))

    print(f"=== SHUGS Canonical Lattice Optimum Test ===")
    print(f"K={K} ensemble, N={N_range[0]}-{N_range[1]}")
    print(f"Pipeline: shugs_core.py (Manus S7 canonical)")
    print()

    for N in N_values:
        print(f"  Running N={N}...", end=" ", flush=True)
        result = run_ensemble(N, K=K)
        results[N] = result
        print(f"mean={result.mean_gue_ks:.4f} std={result.std_gue_ks:.4f} "
              f"SEM={result.sem_gue_ks:.4f} [{result.elapsed_seconds:.1f}s]")

    # Rank by mean GUE-KS (lower is better)
    ranked = sorted(results.items(), key=lambda x: x[1].mean_gue_ks)

    print()
    print("=== RANKING (lower GUE-KS = closer to GUE) ===")
    print(f"{'Rank':<6} {'N':<5} {'Mean GUE-KS':<14} {'Std':<10} {'SEM':<10}")
    for rank, (N, r) in enumerate(ranked, 1):
        marker = " ***" if N in (144, 145, 146) else ""
        print(f"{rank:<6} {N:<5} {r.mean_gue_ks:<14.4f} {r.std_gue_ks:<10.4f} "
              f"{r.sem_gue_ks:<10.4f}{marker}")

    # Pairwise tests for focal trio
    print()
    print("=== PAIRWISE SIGNIFICANCE (focal trio) ===")
    for a, b in [(143, 144), (143, 145), (144, 145), (145, 146)]:
        if a in results and b in results:
            t, p = welch_t_test(results[a].scores, results[b].scores)
            sig = "SIGNIFICANT" if p < 0.05 else "not significant"
            diff = results[a].mean_gue_ks - results[b].mean_gue_ks
            print(f"  N={a} vs N={b}: diff={diff:+.4f}, t={t:.3f}, p={p:.4f} → {sig}")

    return results


def run_n_scaling_test(K: int = 20, N_values: List[int] = None):
    """
    Run the N-scaling test: K-ensemble across multiple N values.
    This is the canonical replication of Claude S1's inter-seat ask #2.
    """
    if N_values is None:
        N_values = [144, 256, 512, 1024]

    results = {}

    print(f"=== SHUGS Canonical N-Scaling Test ===")
    print(f"K={K} ensemble, N={N_values}")
    print(f"Pipeline: shugs_core.py (Manus S7 canonical)")
    print()

    for N in N_values:
        # Reduce K for large N to keep runtime manageable
        effective_K = K if N <= 512 else max(5, K // 2)
        print(f"  Running N={N} (K={effective_K})...", end=" ", flush=True)
        result = run_ensemble(N, K=effective_K)
        results[N] = result
        print(f"mean={result.mean_gue_ks:.4f} std={result.std_gue_ks:.4f} "
              f"SEM={result.sem_gue_ks:.4f} [{result.elapsed_seconds:.1f}s]")

    # Check monotonicity
    means = [results[N].mean_gue_ks for N in N_values]
    is_monotonic_decreasing = all(means[i] >= means[i+1] for i in range(len(means)-1))

    print()
    print(f"=== MONOTONICITY CHECK ===")
    print(f"Means: {[f'{m:.4f}' for m in means]}")
    print(f"Monotonically decreasing: {'YES ✓' if is_monotonic_decreasing else 'NO ✗'}")

    if not is_monotonic_decreasing:
        print("WARNING: Non-monotonic behavior detected. GUE convergence claim constrained.")

    return results


def main():
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="SHUGS Canonical Pipeline")
    parser.add_argument("test", choices=["lattice-optimum", "n-scaling", "both"],
                        help="Which test to run")
    parser.add_argument("--K", type=int, default=20, help="Ensemble size (default: 20)")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file")
    args = parser.parse_args()

    all_results = {}

    if args.test in ("lattice-optimum", "both"):
        results = run_lattice_optimum_test(K=args.K)
        all_results["lattice_optimum"] = {
            N: asdict(r) for N, r in results.items()
        }

    if args.test in ("n-scaling", "both"):
        results = run_n_scaling_test(K=args.K)
        all_results["n_scaling"] = {
            N: asdict(r) for N, r in results.items()
        }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
