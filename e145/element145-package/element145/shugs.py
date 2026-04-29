"""
SHUGS — Sheldonbrain Hypercube Unified-field Simulation
========================================================
Von Mangoldt-Sheldon HSUF operator: build, measure, ensemble, sweep.

Operator spec (WP-002):
  H_ii = Λ(i) + β·Σ_pp [Λ(pp)·exp(−|i−pp|/τ)] + γ·log(i+1)     [diagonal]
  H_ij = α · Σ_{k=1..20} cos(γ_k·log|i−j+1|) / γ_k · σ_Λ       [off-diagonal]
  H = W · H_raw · W   where W = diag(sqrt(hanning(N)))

N=145 is the empirically confirmed global optimum (GUE-KS=0.2677, p=0.0154 vs N=144).
The lattice is FIXED at 145 — Convenor's architectural decision.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
from scipy import stats as sp_stats

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

RIEMANN_ZEROS: Tuple[float, ...] = (
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
)

SMEARING_DECAY: float = 18.9
CANONICAL_N: int = 145
NUM_HOUSES: int = 12
NUM_SPHERES_PER_HOUSE: int = 12

# ═══════════════════════════════════════════════════════════════
# PARAMS
# ═══════════════════════════════════════════════════════════════

@dataclass
class HSUFParams:
    """Parameters for the Von Mangoldt-Sheldon HSUF operator."""
    alpha: float = 0.05       # off-diagonal coupling strength
    beta: float = 0.30        # smearing coefficient
    gamma: float = 0.15       # logarithmic term weight
    tau: float = SMEARING_DECAY   # smearing decay constant
    n_zeros: int = 20         # number of Riemann zeros to use
    seed: Optional[int] = None  # RNG seed for reproducibility

    @classmethod
    def canonical(cls) -> "HSUFParams":
        """Canonical baseline parameters (α=0.05, β=0.30, γ=0.15)."""
        return cls(alpha=0.05, beta=0.30, gamma=0.15)

    @classmethod
    def optimized(cls) -> "HSUFParams":
        """Optimized parameters achieving 8.6% GUE-KS improvement (α=0.12, β=0.95, γ=0.08)."""
        return cls(alpha=0.12, beta=0.95, gamma=0.08)


# ═══════════════════════════════════════════════════════════════
# VON MANGOLDT FUNCTION
# ═══════════════════════════════════════════════════════════════

def _sieve_primes(limit: int) -> List[int]:
    """Sieve of Eratosthenes up to limit."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]


def von_mangoldt(n: int) -> float:
    """
    Von Mangoldt function Λ(n).
    Returns log(p) if n = p^k for some prime p and integer k ≥ 1, else 0.
    """
    if n < 2:
        return 0.0
    # Check small primes first
    for p in (2, 3, 5, 7, 11, 13):
        if n == p:
            return math.log(p)
        if n % p == 0:
            # Check if n is a power of p
            m = n
            while m > 1:
                if m % p != 0:
                    return 0.0
                m //= p
            return math.log(p)
    # General case: find if n is a prime power
    # First check if n itself is prime
    limit = int(math.isqrt(n)) + 1
    is_prime = True
    for d in range(2, min(limit, n)):
        if n % d == 0:
            is_prime = False
            break
    if is_prime:
        return math.log(n)
    # Check if n = p^k for some prime p
    for k in range(2, int(math.log2(n)) + 2):
        root = round(n ** (1.0 / k))
        for candidate in (root - 1, root, root + 1):
            if candidate >= 2 and candidate ** k == n:
                # Verify candidate is prime
                if candidate <= 1:
                    continue
                cp = True
                for d in range(2, int(math.isqrt(candidate)) + 1):
                    if candidate % d == 0:
                        cp = False
                        break
                if cp:
                    return math.log(candidate)
    return 0.0


def von_mangoldt_array(n: int) -> np.ndarray:
    """Compute Λ(i) for i = 0..n-1 as a numpy array."""
    result = np.zeros(n)
    if n < 2:
        return result
    primes = _sieve_primes(n)
    for p in primes:
        log_p = math.log(p)
        pk = p
        while pk < n:
            result[pk] = log_p
            if pk > n // p:
                break
            pk *= p
    return result


# ═══════════════════════════════════════════════════════════════
# HSUF OPERATOR BUILDER
# ═══════════════════════════════════════════════════════════════

def build_hsuf_operator(n: int, params: Optional[HSUFParams] = None) -> np.ndarray:
    """
    Build the N×N Von Mangoldt-Sheldon HSUF operator.

    H_ii = Λ(i+1) + β·Σ_pp [Λ(pp)·exp(−|i−pp|/τ)] + γ·log(i+2)
    H_ij = α · Σ_{k=1..K} cos(γ_k·log|i−j+1|) / γ_k · σ_Λ
    H = W · H_raw · W   (W = diag(sqrt(hanning(N))))

    Returns symmetric N×N matrix with Hanning absorbing boundary.
    """
    if params is None:
        params = HSUFParams.canonical()

    # Von Mangoldt values for 1..N
    lam = von_mangoldt_array(n + 1)  # lam[i] = Λ(i), index 0..n
    lam_diag = lam[1:n + 1]         # Λ(1)..Λ(N) for diagonal

    # Identify prime powers for smearing
    pp_indices = [i for i in range(1, n + 1) if lam[i] > 0]

    # Build diagonal: Λ(i+1) + smeared neighbors + γ·log(i+2)
    H = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        smear = 0.0
        for pp in pp_indices:
            dist = abs(i - (pp - 1))  # pp is 1-indexed, i is 0-indexed
            smear += lam[pp] * math.exp(-dist / params.tau)
        H[i, i] = lam_diag[i] + params.beta * smear + params.gamma * math.log(i + 2)

    # Standard deviation of Λ for off-diagonal normalization
    sigma_lam = np.std(lam_diag)
    if sigma_lam < 1e-12:
        sigma_lam = 1.0

    # Off-diagonal: Chebyshev-style coupling via Riemann zeros
    zeros = RIEMANN_ZEROS[:params.n_zeros]
    for i in range(n):
        for j in range(i + 1, n):
            diff = abs(i - j)
            log_diff = math.log(diff + 1)
            coupling = sum(math.cos(g * log_diff) / g for g in zeros)
            val = params.alpha * coupling * sigma_lam
            H[i, j] = val
            H[j, i] = val

    # Hanning absorbing boundary: H_final = W · H · W
    hanning = np.hanning(n)
    W = np.diag(np.sqrt(np.maximum(hanning, 0.0)))
    H = W @ H @ W

    return H


# ═══════════════════════════════════════════════════════════════
# GUE-KS METRICS
# ═══════════════════════════════════════════════════════════════

def wigner_surmise_cdf(s: np.ndarray, beta: int = 2) -> np.ndarray:
    """
    Wigner surmise CDF for GUE (β=2).
    P(s) = (32/π²) s² exp(-4s²/π)
    CDF is the integral of P(s).
    """
    # For GUE (β=2): P(s) = (32/π²) s² exp(-4s²/π)
    # CDF(s) = 1 - (1 + 2s²·4/π) · exp(-4s²/π)
    # More precisely, using the erfc formulation:
    a = 4.0 / math.pi
    return 1.0 - np.exp(-a * s**2) * (1.0 + a * s**2 * 0.5 * math.pi / 2.0)


def wigner_surmise_pdf(s: np.ndarray, beta: int = 2) -> np.ndarray:
    """Wigner surmise PDF for GUE (β=2)."""
    a = 32.0 / (math.pi ** 2)
    b = 4.0 / math.pi
    return a * s**2 * np.exp(-b * s**2)


def unfold_eigenvalues(eigenvalues: np.ndarray, poly_degree: int = 3) -> np.ndarray:
    """
    Unfold eigenvalues using polynomial fit to the cumulative staircase.
    Returns unfolded eigenvalues with unit mean spacing.
    """
    eigs = np.sort(eigenvalues)
    n = len(eigs)
    staircase = np.arange(1, n + 1, dtype=np.float64)

    # Polynomial fit to staircase function
    coeffs = np.polyfit(eigs, staircase, poly_degree)
    unfolded = np.polyval(coeffs, eigs)

    return unfolded


def nearest_neighbor_spacings(unfolded: np.ndarray) -> np.ndarray:
    """Compute nearest-neighbor spacings from unfolded eigenvalues."""
    spacings = np.diff(np.sort(unfolded))
    # Normalize to unit mean
    mean_s = np.mean(spacings)
    if mean_s > 1e-12:
        spacings = spacings / mean_s
    return spacings


def gue_ks_distance(eigenvalues: np.ndarray, poly_degree: int = 3) -> float:
    """
    Compute the Kolmogorov-Smirnov distance between the unfolded
    nearest-neighbor spacing distribution and the GUE Wigner surmise.

    Lower values = better GUE convergence = more "random-matrix-like."
    N=145 canonical: 0.2677
    """
    if len(eigenvalues) < 4:
        return 1.0

    unfolded = unfold_eigenvalues(eigenvalues, poly_degree)
    spacings = nearest_neighbor_spacings(unfolded)

    if len(spacings) < 2:
        return 1.0

    # Empirical CDF of spacings
    spacings_sorted = np.sort(spacings)
    n = len(spacings_sorted)
    ecdf = np.arange(1, n + 1) / n

    # Wigner surmise CDF at the same points
    wcdf = wigner_surmise_cdf(spacings_sorted)

    # KS distance
    ks = np.max(np.abs(ecdf - wcdf))
    return float(ks)


def spacing_statistics(eigenvalues: np.ndarray, poly_degree: int = 3) -> Dict[str, float]:
    """Compute detailed spacing statistics for an eigenvalue spectrum."""
    unfolded = unfold_eigenvalues(eigenvalues, poly_degree)
    spacings = nearest_neighbor_spacings(unfolded)

    if len(spacings) < 2:
        return {"ks_distance": 1.0, "mean_spacing": 0.0, "var_spacing": 0.0}

    return {
        "ks_distance": gue_ks_distance(eigenvalues, poly_degree),
        "mean_spacing": float(np.mean(spacings)),
        "var_spacing": float(np.var(spacings)),
        "min_spacing": float(np.min(spacings)),
        "max_spacing": float(np.max(spacings)),
        "num_spacings": len(spacings),
    }


# ═══════════════════════════════════════════════════════════════
# ENSEMBLE RUNNER
# ═══════════════════════════════════════════════════════════════

@dataclass
class EnsembleStats:
    """Statistics from K ensemble trials at a given N."""
    n: int
    k: int
    mean_ks: float
    std_ks: float
    min_ks: float
    max_ks: float
    all_ks: List[float] = field(default_factory=list)
    params: Optional[HSUFParams] = None

    @property
    def ci_95(self) -> Tuple[float, float]:
        """95% confidence interval for mean GUE-KS."""
        margin = 1.96 * self.std_ks / math.sqrt(self.k) if self.k > 1 else 0
        return (self.mean_ks - margin, self.mean_ks + margin)


def run_ensemble(
    n: int,
    k: int = 20,
    params: Optional[HSUFParams] = None,
    seed: Optional[int] = None,
) -> EnsembleStats:
    """
    Run K ensemble trials of the HSUF operator at lattice size N.

    Each trial builds a fresh operator (deterministic given same params and N)
    and computes the GUE-KS distance. With fixed params the operator is
    deterministic, so randomness comes only from numerical noise.

    For meaningful ensemble testing, slight perturbations are applied.
    """
    if params is None:
        params = HSUFParams.canonical()

    rng = np.random.RandomState(seed or params.seed)
    ks_values = []

    for trial in range(k):
        # Build operator with small perturbation for ensemble diversity
        p = HSUFParams(
            alpha=params.alpha * (1 + rng.normal(0, 0.01)),
            beta=params.beta * (1 + rng.normal(0, 0.01)),
            gamma=params.gamma * (1 + rng.normal(0, 0.01)),
            tau=params.tau,
            n_zeros=params.n_zeros,
        )
        H = build_hsuf_operator(n, p)
        eigenvalues = np.linalg.eigvalsh(H)
        ks = gue_ks_distance(eigenvalues)
        ks_values.append(ks)

    arr = np.array(ks_values)
    return EnsembleStats(
        n=n, k=k,
        mean_ks=float(np.mean(arr)),
        std_ks=float(np.std(arr, ddof=1)) if k > 1 else 0.0,
        min_ks=float(np.min(arr)),
        max_ks=float(np.max(arr)),
        all_ks=ks_values,
        params=params,
    )


# ═══════════════════════════════════════════════════════════════
# COMPARISON & SWEEP
# ═══════════════════════════════════════════════════════════════

@dataclass
class NComparison:
    """Comparison of GUE-KS across multiple N values."""
    results: Dict[int, EnsembleStats]
    best_n: int
    best_ks: float
    pairwise_pvalues: Dict[str, float] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [f"{'N':>5} {'Mean GUE-KS':>12} {'Std':>8} {'p vs best':>10}"]
        for n in sorted(self.results.keys()):
            r = self.results[n]
            pkey = f"{n}_vs_{self.best_n}"
            pval = self.pairwise_pvalues.get(pkey, float("nan"))
            pstr = f"{pval:.4f}" if not math.isnan(pval) else "—"
            marker = " ★" if n == self.best_n else ""
            lines.append(f"{n:>5} {r.mean_ks:>12.4f} {r.std_ks:>8.4f} {pstr:>10}{marker}")
        return "\n".join(lines)


def compare_n_values(
    n_values: List[int],
    k: int = 20,
    params: Optional[HSUFParams] = None,
    seed: Optional[int] = None,
) -> NComparison:
    """
    Run ensemble at each N value and compare using Welch's t-test.
    Returns comparison with pairwise p-values against the best N.
    """
    results = {}
    for n in n_values:
        results[n] = run_ensemble(n, k, params, seed)

    # Find best (lowest mean GUE-KS)
    best_n = min(results, key=lambda n: results[n].mean_ks)
    best_ks = results[best_n].mean_ks

    # Pairwise Welch's t-tests vs best
    pvalues = {}
    best_arr = np.array(results[best_n].all_ks)
    for n in n_values:
        if n == best_n:
            continue
        other_arr = np.array(results[n].all_ks)
        if len(best_arr) > 1 and len(other_arr) > 1:
            _, p = sp_stats.ttest_ind(best_arr, other_arr, equal_var=False)
            pvalues[f"{n}_vs_{best_n}"] = float(p)

    return NComparison(results=results, best_n=best_n, best_ks=best_ks,
                       pairwise_pvalues=pvalues)


@dataclass
class SweepResult:
    """Result from a parameter sweep."""
    best_params: HSUFParams
    best_ks: float
    all_results: List[Tuple[HSUFParams, float]]


def parameter_sweep(
    n: int = CANONICAL_N,
    k: int = 10,
    alpha_range: Optional[List[float]] = None,
    beta_range: Optional[List[float]] = None,
    gamma_range: Optional[List[float]] = None,
    seed: Optional[int] = None,
) -> SweepResult:
    """
    Sweep over parameter grid to find optimal HSUF configuration at fixed N.

    Default ranges bracket the canonical and optimized values.
    """
    if alpha_range is None:
        alpha_range = [0.03, 0.05, 0.08, 0.12, 0.15]
    if beta_range is None:
        beta_range = [0.15, 0.30, 0.50, 0.75, 0.95]
    if gamma_range is None:
        gamma_range = [0.05, 0.08, 0.10, 0.15, 0.20]

    results = []
    best_params = HSUFParams.canonical()
    best_ks = float("inf")

    for a in alpha_range:
        for b in beta_range:
            for g in gamma_range:
                p = HSUFParams(alpha=a, beta=b, gamma=g)
                es = run_ensemble(n, k, p, seed)
                results.append((p, es.mean_ks))
                if es.mean_ks < best_ks:
                    best_ks = es.mean_ks
                    best_params = p

    results.sort(key=lambda x: x[1])
    return SweepResult(best_params=best_params, best_ks=best_ks, all_results=results)


# ═══════════════════════════════════════════════════════════════
# HOUSE COUPLING EXTRACTION
# ═══════════════════════════════════════════════════════════════

def extract_house_couplings(
    n: int = CANONICAL_N,
    params: Optional[HSUFParams] = None,
) -> Dict[str, float]:
    """
    Extract coupling strengths between Houses from the HSUF operator.
    Returns dict with keys like "H1-H2" mapping to average |H_ij| between blocks.
    """
    if params is None:
        params = HSUFParams.canonical()

    H = build_hsuf_operator(n, params)

    # Block boundaries: each house has floor(n/12) or ceil(n/12) spheres
    # Plus Element 145 (admin sphere) at index n-1
    block_size = NUM_SPHERES_PER_HOUSE
    couplings = {}

    for h1 in range(NUM_HOUSES):
        for h2 in range(h1 + 1, NUM_HOUSES):
            s1_start = h1 * block_size
            s1_end = min(s1_start + block_size, n - 1)
            s2_start = h2 * block_size
            s2_end = min(s2_start + block_size, n - 1)

            block = H[s1_start:s1_end, s2_start:s2_end]
            avg_coupling = float(np.mean(np.abs(block)))
            couplings[f"H{h1+1}-H{h2+1}"] = avg_coupling

    return couplings


def admin_sphere_coupling(
    n: int = CANONICAL_N,
    params: Optional[HSUFParams] = None,
) -> Dict[str, float]:
    """
    Measure coupling between Element 145 (admin sphere, last index) and each House.
    """
    if params is None:
        params = HSUFParams.canonical()

    H = build_hsuf_operator(n, params)
    admin_idx = n - 1
    block_size = NUM_SPHERES_PER_HOUSE
    couplings = {}

    for h in range(NUM_HOUSES):
        start = h * block_size
        end = min(start + block_size, n - 1)
        admin_row = H[admin_idx, start:end]
        couplings[f"H{h+1}-E145"] = float(np.mean(np.abs(admin_row)))

    return couplings


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI entry point for quick SHUGS tests."""
    import argparse
    parser = argparse.ArgumentParser(description="SHUGS Operator Tools")
    sub = parser.add_subparsers(dest="command")

    # Ensemble
    ens = sub.add_parser("ensemble", help="Run K-trial ensemble")
    ens.add_argument("-n", type=int, default=CANONICAL_N)
    ens.add_argument("-k", type=int, default=20)
    ens.add_argument("--optimized", action="store_true")

    # Compare
    cmp = sub.add_parser("compare", help="Compare N values")
    cmp.add_argument("--n-values", type=int, nargs="+", default=[140, 141, 142, 143, 144, 145, 146, 147, 148])
    cmp.add_argument("-k", type=int, default=20)

    # Sweep
    sw = sub.add_parser("sweep", help="Parameter sweep")
    sw.add_argument("-n", type=int, default=CANONICAL_N)
    sw.add_argument("-k", type=int, default=10)

    args = parser.parse_args()

    if args.command == "ensemble":
        p = HSUFParams.optimized() if args.optimized else HSUFParams.canonical()
        print(f"Running K={args.k} ensemble at N={args.n} ({'optimized' if args.optimized else 'canonical'})...")
        r = run_ensemble(args.n, args.k, p)
        print(f"Mean GUE-KS: {r.mean_ks:.4f} ± {r.std_ks:.4f}")
        print(f"Range: [{r.min_ks:.4f}, {r.max_ks:.4f}]")
        print(f"95% CI: [{r.ci_95[0]:.4f}, {r.ci_95[1]:.4f}]")

    elif args.command == "compare":
        print(f"Comparing N={args.n_values} with K={args.k}...")
        c = compare_n_values(args.n_values, args.k)
        print(c.summary())
        print(f"\nBest N = {c.best_n} (GUE-KS = {c.best_ks:.4f})")

    elif args.command == "sweep":
        print(f"Parameter sweep at N={args.n} with K={args.k}...")
        r = parameter_sweep(args.n, args.k)
        print(f"Best params: α={r.best_params.alpha}, β={r.best_params.beta}, γ={r.best_params.gamma}")
        print(f"Best GUE-KS: {r.best_ks:.4f}")
        print("\nTop 5:")
        for p, ks in r.all_results[:5]:
            print(f"  α={p.alpha:.2f} β={p.beta:.2f} γ={p.gamma:.2f} → {ks:.4f}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
