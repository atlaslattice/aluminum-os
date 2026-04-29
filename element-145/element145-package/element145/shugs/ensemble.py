"""
Ensemble Runner — K-Trial Statistical Testing for HSUF Operator
================================================================
Runs multiple independent trials of the HSUF operator at various N values
and computes ensemble statistics for GUE-KS distance.

Key functions:
  run_ensemble     — K trials at single N, returns statistics
  compare_n_values — Sweep across N range, rank by GUE-KS, compute p-values

Canonical results (Manus pipeline, commit 414892c):
  N=145: GUE-KS = 0.2677 (rank 1 of N=140-148)
  N=143: GUE-KS = 0.2896 (rank 2, p=0.0143 vs N=145)
  N=144: GUE-KS = 0.2939 (rank 4, p=0.0154 vs N=145)

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import time
import json
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Tuple
from element145.shugs.operator import build_hsuf, HSUFParams, CANONICAL_N
from element145.shugs.metrics import gue_ks_distance


@dataclass
class EnsembleResult:
    """Results from a K-trial ensemble at a single N value."""
    N: int
    K: int
    mean_ks: float
    std_ks: float
    median_ks: float
    min_ks: float
    max_ks: float
    ks_values: List[float]
    elapsed_seconds: float
    params: Dict

    def to_dict(self) -> Dict:
        return asdict(self)

    def summary(self) -> str:
        return (
            f"N={self.N}, K={self.K}: "
            f"GUE-KS = {self.mean_ks:.4f} ± {self.std_ks:.4f} "
            f"(median={self.median_ks:.4f}, range=[{self.min_ks:.4f}, {self.max_ks:.4f}]) "
            f"[{self.elapsed_seconds:.1f}s]"
        )


@dataclass
class ComparisonResult:
    """Results from comparing multiple N values."""
    results: List[EnsembleResult]
    rankings: List[Tuple[int, float]]  # (N, mean_ks) sorted ascending
    pairwise_pvalues: Dict[str, float]  # "N1_vs_N2" → p-value
    best_N: int
    total_elapsed: float

    def to_dict(self) -> Dict:
        return {
            "rankings": [{"N": n, "mean_ks": ks} for n, ks in self.rankings],
            "pairwise_pvalues": self.pairwise_pvalues,
            "best_N": self.best_N,
            "total_elapsed": self.total_elapsed,
            "individual_results": [r.to_dict() for r in self.results],
        }

    def summary(self) -> str:
        lines = ["═══ N-Value Comparison ═══", ""]
        lines.append("Rankings (lower GUE-KS = better):")
        for rank, (n, ks) in enumerate(self.rankings, 1):
            marker = " ◄ BEST" if n == self.best_N else ""
            lines.append(f"  {rank}. N={n}: GUE-KS = {ks:.4f}{marker}")

        if self.pairwise_pvalues:
            lines.append("")
            lines.append("Key p-values:")
            for key, pval in sorted(self.pairwise_pvalues.items()):
                sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else "ns"
                lines.append(f"  {key}: p={pval:.4f} {sig}")

        lines.append(f"\nTotal time: {self.total_elapsed:.1f}s")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# ENSEMBLE RUNNER
# ═══════════════════════════════════════════════════════════════

def run_ensemble(
    N: int = CANONICAL_N,
    K: int = 20,
    params: Optional[HSUFParams] = None,
    base_seed: int = 42,
    verbose: bool = False,
) -> EnsembleResult:
    """
    Run K independent trials of the HSUF operator at dimension N.

    Each trial uses a different random seed to get independent
    operator realizations, then computes GUE-KS distance.

    Parameters
    ----------
    N : int
        Matrix dimension. Default 145.
    K : int
        Number of independent trials. Default 20.
    params : HSUFParams, optional
        Operator parameters. Defaults to canonical.
    base_seed : int
        Base random seed. Trial k uses seed = base_seed + k.
    verbose : bool
        Print progress for each trial.

    Returns
    -------
    EnsembleResult
        Statistical summary of the K trials.
    """
    if params is None:
        params = HSUFParams.canonical()

    ks_values = []
    start = time.time()

    for k in range(K):
        seed = base_seed + k
        H = build_hsuf(N=N, params=params, seed=seed)
        ks = gue_ks_distance(matrix=H)
        ks_values.append(ks)

        if verbose:
            print(f"  Trial {k+1}/{K}: GUE-KS = {ks:.4f}")

    elapsed = time.time() - start
    ks_arr = np.array(ks_values)

    return EnsembleResult(
        N=N,
        K=K,
        mean_ks=float(np.mean(ks_arr)),
        std_ks=float(np.std(ks_arr)),
        median_ks=float(np.median(ks_arr)),
        min_ks=float(np.min(ks_arr)),
        max_ks=float(np.max(ks_arr)),
        ks_values=[float(v) for v in ks_values],
        elapsed_seconds=elapsed,
        params={
            "alpha": params.alpha,
            "beta": params.beta,
            "gamma": params.gamma,
            "decay": params.decay,
        },
    )


def compare_n_values(
    n_range: Optional[List[int]] = None,
    K: int = 20,
    params: Optional[HSUFParams] = None,
    base_seed: int = 42,
    reference_N: int = CANONICAL_N,
    verbose: bool = True,
) -> ComparisonResult:
    """
    Compare GUE-KS across a range of N values.

    Runs K-trial ensembles for each N, ranks them, and computes
    pairwise p-values (Welch's t-test) against the reference N.

    Parameters
    ----------
    n_range : list of int, optional
        N values to test. Default [140, 141, ..., 148].
    K : int
        Trials per N value.
    params : HSUFParams, optional
        Operator parameters.
    base_seed : int
        Base seed for reproducibility.
    reference_N : int
        Reference N for p-value computation. Default 145.
    verbose : bool
        Print progress.

    Returns
    -------
    ComparisonResult
        Rankings, p-values, and full ensemble results.
    """
    if n_range is None:
        n_range = list(range(140, 149))

    total_start = time.time()
    results = []

    for n in n_range:
        if verbose:
            print(f"Running N={n} (K={K})...")
        result = run_ensemble(N=n, K=K, params=params, base_seed=base_seed, verbose=False)
        results.append(result)
        if verbose:
            print(f"  → GUE-KS = {result.mean_ks:.4f} ± {result.std_ks:.4f}")

    # Rank by mean GUE-KS (ascending — lower is better)
    rankings = sorted([(r.N, r.mean_ks) for r in results], key=lambda x: x[1])
    best_N = rankings[0][0]

    # Compute pairwise p-values against reference_N
    ref_result = next((r for r in results if r.N == reference_N), None)
    pairwise = {}

    if ref_result is not None:
        ref_ks = np.array(ref_result.ks_values)

        for r in results:
            if r.N == reference_N:
                continue

            other_ks = np.array(r.ks_values)

            # Welch's t-test (unequal variance)
            n1, n2 = len(ref_ks), len(other_ks)
            m1, m2 = np.mean(ref_ks), np.mean(other_ks)
            v1, v2 = np.var(ref_ks, ddof=1), np.var(other_ks, ddof=1)

            se = np.sqrt(v1 / n1 + v2 / n2)
            if se < 1e-15:
                pval = 1.0
            else:
                t_stat = (m1 - m2) / se
                # Welch-Satterthwaite degrees of freedom
                df_num = (v1 / n1 + v2 / n2) ** 2
                df_den = (v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1)
                df = df_num / df_den if df_den > 0 else 1.0

                # Two-tailed p-value using t-distribution approximation
                # Using the complementary error function for large df
                from scipy import stats as scipy_stats
                pval = float(scipy_stats.t.sf(abs(t_stat), df) * 2)

            key = f"N{reference_N}_vs_N{r.N}"
            pairwise[key] = round(pval, 6)

    total_elapsed = time.time() - total_start

    comparison = ComparisonResult(
        results=results,
        rankings=rankings,
        pairwise_pvalues=pairwise,
        best_N=best_N,
        total_elapsed=total_elapsed,
    )

    if verbose:
        print()
        print(comparison.summary())

    return comparison


# ═══════════════════════════════════════════════════════════════
# PARAMETER SWEEP
# ═══════════════════════════════════════════════════════════════

def parameter_sweep(
    N: int = CANONICAL_N,
    K: int = 10,
    alpha_range: Optional[List[float]] = None,
    beta_range: Optional[List[float]] = None,
    gamma_range: Optional[List[float]] = None,
    base_seed: int = 42,
    verbose: bool = True,
) -> List[Dict]:
    """
    Sweep HSUF parameters to find optimal GUE-KS configuration.

    Parameters
    ----------
    N : int
        Fixed lattice size (default 145).
    K : int
        Trials per configuration.
    alpha_range, beta_range, gamma_range : list of float, optional
        Parameter values to sweep. Defaults to small grids.
    base_seed : int
        Base seed.
    verbose : bool
        Print progress.

    Returns
    -------
    list of dict
        Sorted results (best first) with params and mean_ks.
    """
    if alpha_range is None:
        alpha_range = [0.05, 0.08, 0.10, 0.12, 0.15]
    if beta_range is None:
        beta_range = [0.30, 0.50, 0.70, 0.95]
    if gamma_range is None:
        gamma_range = [0.05, 0.08, 0.10, 0.15]

    sweep_results = []
    total = len(alpha_range) * len(beta_range) * len(gamma_range)
    count = 0

    for alpha in alpha_range:
        for beta in beta_range:
            for gamma in gamma_range:
                count += 1
                params = HSUFParams(alpha=alpha, beta=beta, gamma=gamma)

                result = run_ensemble(N=N, K=K, params=params, base_seed=base_seed)
                entry = {
                    "alpha": alpha,
                    "beta": beta,
                    "gamma": gamma,
                    "mean_ks": result.mean_ks,
                    "std_ks": result.std_ks,
                }
                sweep_results.append(entry)

                if verbose and count % 10 == 0:
                    print(f"  [{count}/{total}] α={alpha}, β={beta}, γ={gamma} → KS={result.mean_ks:.4f}")

    # Sort by mean_ks ascending
    sweep_results.sort(key=lambda x: x["mean_ks"])

    if verbose:
        print(f"\nTop 5 configurations:")
        for i, r in enumerate(sweep_results[:5]):
            print(f"  {i+1}. α={r['alpha']}, β={r['beta']}, γ={r['gamma']} → KS={r['mean_ks']:.4f}")

    return sweep_results


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SHUGS Ensemble Runner")
    parser.add_argument("--mode", choices=["single", "compare", "sweep"], default="compare")
    parser.add_argument("--N", type=int, default=CANONICAL_N)
    parser.add_argument("--K", type=int, default=20)
    parser.add_argument("--n-min", type=int, default=140)
    parser.add_argument("--n-max", type=int, default=148)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    if args.mode == "single":
        print(f"Running K={args.K} ensemble at N={args.N}...")
        result = run_ensemble(N=args.N, K=args.K, base_seed=args.seed, verbose=True)
        print(f"\n{result.summary()}")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result.to_dict(), f, indent=2)

    elif args.mode == "compare":
        n_range = list(range(args.n_min, args.n_max + 1))
        comparison = compare_n_values(n_range=n_range, K=args.K, base_seed=args.seed)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(comparison.to_dict(), f, indent=2)

    elif args.mode == "sweep":
        sweep_results = parameter_sweep(N=args.N, K=min(args.K, 10), base_seed=args.seed)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(sweep_results, f, indent=2)
