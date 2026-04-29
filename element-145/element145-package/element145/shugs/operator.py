"""
HSUF Operator — Von Mangoldt-Sheldon Hilbert-Sheldon Unified Field
===================================================================
Builds the Hermitian operator for the Sheldonbrain lattice.

N=145 is the canonical default (12x12 + 1 Admin Sphere).
Architectural default per lattice design; empirical validation pending
canonical K=20 ensemble stability test with stochastic component.

Operator construction (WP-002 specification):
  Diagonal:  H_ii = Λ(i) + β·Σ_pp[Λ(pp)·exp(-|i-pp|/decay)] + γ·log(i+1)
  Off-diag:  H_ij = α·Σ_{k=1..20} cos(γ_k·log|i-j+1|)/γ_k · σ_Λ
  Boundary:  Hanning window (absorbing)
  Jitter:    Per-trial diagonal perturbation N(0, jitter_amp·σ_Λ) for ensemble variance

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.

Fix history:
  v0.1.0-CANDIDATE-2: Restored stochastic jitter component per Claude S1
    pre-vault assessment §2.1. Reference implementation: shugs_core.py
    (jitter_amplitude = 0.02 * sigma_lambda). Without jitter, K=20 ensemble
    produces K byte-identical matrices and degenerate p-values.
"""

from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

# Canonical lattice size — DO NOT change for production use.
# N=145 is the architectural default (12^2 + 1 Admin Sphere).
CANONICAL_N = 145

# Default jitter amplitude as fraction of σ_Λ
# Per shugs_core.py reference implementation (commit 414892c)
JITTER_AMP = 0.02

# First 20 non-trivial Riemann zeta zeros (imaginary parts)
RIEMANN_ZEROS: Tuple[float, ...] = (
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
)

# Smearing decay for prime-power diagonal enhancement
DEFAULT_DECAY = 18.9


@dataclass(frozen=True)
class HSUFParams:
    """Parameters for the HSUF operator construction."""
    alpha: float = 0.05       # Off-diagonal coupling strength
    beta: float = 0.30        # Prime-power smearing amplitude
    gamma: float = 0.15       # Logarithmic potential strength
    decay: float = 18.9       # Smearing decay length
    num_zeros: int = 20       # Number of Riemann zeros to use
    use_hanning: bool = True  # Apply Hanning window (absorbing boundary)
    jitter_amp: float = 0.02  # Ensemble jitter amplitude (fraction of σ_Λ)

    @classmethod
    def canonical(cls) -> "HSUFParams":
        """Canonical parameters (baseline)."""
        return cls(alpha=0.05, beta=0.30, gamma=0.15)

    @classmethod
    def optimized(cls) -> "HSUFParams":
        """Optimized parameters (from parameter sweep)."""
        return cls(alpha=0.12, beta=0.95, gamma=0.08)


# ═══════════════════════════════════════════════════════════════
# NUMBER THEORY UTILITIES
# ═══════════════════════════════════════════════════════════════

def von_mangoldt(n: int) -> float:
    """
    Compute the Von Mangoldt function Λ(n).

    Λ(n) = log(p)  if n = p^k for some prime p and integer k ≥ 1
    Λ(n) = 0       otherwise

    Parameters
    ----------
    n : int
        Positive integer.

    Returns
    -------
    float
        log(p) if n is a prime power, 0.0 otherwise.
    """
    if n < 2:
        return 0.0
    # Check if n is a prime power
    # Try each potential prime base
    for p in range(2, int(math.isqrt(n)) + 1):
        if n % p == 0:
            # p divides n — check if n is a power of p
            val = n
            while val % p == 0:
                val //= p
            if val == 1:
                return math.log(p)
            else:
                return 0.0  # n has multiple prime factors
    # n is prime (no factor found up to sqrt(n))
    return math.log(n)


def is_prime_power(n: int) -> bool:
    """Check if n is a prime power (p^k for k ≥ 1)."""
    return von_mangoldt(n) > 0


def get_prime_powers(N: int) -> List[int]:
    """Return all prime powers up to N."""
    return [i for i in range(2, N + 1) if is_prime_power(i)]


# ═══════════════════════════════════════════════════════════════
# HSUF OPERATOR BUILDER
# ═══════════════════════════════════════════════════════════════

def build_hsuf(
    N: int = CANONICAL_N,
    params: Optional[HSUFParams] = None,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Build the Von Mangoldt-Sheldon HSUF operator as an N×N Hermitian matrix.

    Construction per WP-002 specification:
      Diagonal:  H_ii = Λ(i+1) + β·Σ_pp[Λ(pp)·exp(-|i+1-pp|/decay)] + γ·log(i+2)
      Off-diag:  H_ij = α·Σ_{k=1..K} cos(γ_k·log|i-j+1|)/γ_k · σ_Λ
      Boundary:  Hanning window W; H_final = W · H_raw · W
      Jitter:    If seed is provided, add diagonal N(0, jitter_amp·σ_Λ) perturbation
                 for ensemble variance estimation.

    The stochastic jitter is essential for meaningful K-trial ensembles.
    Without it, all K trials produce byte-identical matrices and degenerate
    p-values (all 1.0). Reference: shugs_core.py, Claude S1 pre-vault
    assessment §2.1.

    Parameters
    ----------
    N : int
        Matrix dimension. Default 145 (canonical lattice size).
    params : HSUFParams, optional
        Operator parameters. Defaults to canonical.
    seed : int, optional
        Random seed. When provided, adds per-trial diagonal jitter
        for ensemble variance estimation. Each seed produces a unique
        operator realization.

    Returns
    -------
    np.ndarray
        N×N real symmetric matrix (Hermitian with real entries).
    """
    if params is None:
        params = HSUFParams.canonical()

    zeros = RIEMANN_ZEROS[:params.num_zeros]

    # Pre-compute Von Mangoldt values
    lambda_vals = np.array([von_mangoldt(i + 1) for i in range(N)])

    # Pre-compute prime powers up to N for smearing
    prime_powers = get_prime_powers(N)
    pp_lambda = np.array([von_mangoldt(pp) for pp in prime_powers])
    pp_positions = np.array(prime_powers, dtype=float)

    # Compute σ_Λ (standard deviation of non-zero Λ values)
    nonzero_lambda = lambda_vals[lambda_vals > 0]
    sigma_lambda = float(np.std(nonzero_lambda)) if len(nonzero_lambda) > 1 else 1.0

    # ─── Build diagonal ───
    H = np.zeros((N, N), dtype=np.float64)

    for i in range(N):
        # Base: Von Mangoldt function
        diag = lambda_vals[i]

        # Prime-power smearing
        if len(prime_powers) > 0:
            distances = np.abs((i + 1) - pp_positions)
            smeared = np.sum(pp_lambda * np.exp(-distances / params.decay))
            diag += params.beta * smeared

        # Logarithmic potential
        diag += params.gamma * math.log(i + 2)

        H[i, i] = diag

    # ─── Build off-diagonal (symmetric) ───
    for i in range(N):
        for j in range(i + 1, N):
            diff = abs(i - j)
            coupling = 0.0
            for gamma_k in zeros:
                coupling += math.cos(gamma_k * math.log(diff + 1)) / gamma_k
            coupling *= params.alpha * sigma_lambda
            H[i, j] = coupling
            H[j, i] = coupling

    # ─── Apply Hanning window (absorbing boundary) ───
    if params.use_hanning:
        window = np.hanning(N)
        # Outer product creates the 2D window
        W = np.sqrt(np.outer(window, window))
        H = W * H

    # ─── Ensemble jitter (CRITICAL for K-trial variance) ───
    # Per shugs_core.py reference: jitter_amplitude = 0.02 * sigma_lambda
    # Each seed produces a unique diagonal perturbation, giving the K-trial
    # ensemble actual variance and meaningful p-values.
    # Without this block, K=20 produces K byte-identical matrices.
    if seed is not None:
        rng = np.random.RandomState(seed)
        jitter = rng.normal(0, params.jitter_amp * sigma_lambda, N)
        H += np.diag(jitter)

    return H


def extract_house_couplings(H: np.ndarray, num_houses: int = 12) -> np.ndarray:
    """
    Extract the inter-House coupling matrix from the HSUF operator.

    Groups the N×N operator into num_houses blocks and computes
    the mean off-diagonal coupling for each House pair.

    Parameters
    ----------
    H : np.ndarray
        The HSUF operator matrix (N×N).
    num_houses : int
        Number of Houses (default 12).

    Returns
    -------
    np.ndarray
        num_houses × num_houses coupling matrix.
    """
    N = H.shape[0]
    spheres_per_house = N // num_houses
    remainder = N % num_houses  # Element 145 sits here

    couplings = np.zeros((num_houses, num_houses))

    for i in range(num_houses):
        for j in range(num_houses):
            if i == j:
                continue
            # Block boundaries
            i_start = i * spheres_per_house
            i_end = (i + 1) * spheres_per_house
            j_start = j * spheres_per_house
            j_end = (j + 1) * spheres_per_house
            block = H[i_start:i_end, j_start:j_end]
            couplings[i, j] = np.mean(np.abs(block))

    return couplings


def admin_sphere_coupling(H: np.ndarray, num_houses: int = 12) -> np.ndarray:
    """
    Extract Element 145's coupling strength to each House.

    For N=145, element 145 is index 144 (0-based). This function
    measures how strongly the Admin Sphere couples to each House block.

    Parameters
    ----------
    H : np.ndarray
        The HSUF operator matrix (N×N).
    num_houses : int
        Number of Houses (default 12).

    Returns
    -------
    np.ndarray
        Length-num_houses array of coupling strengths.
    """
    N = H.shape[0]
    spheres_per_house = N // num_houses
    admin_index = N - 1  # Last element = Element 145

    couplings = np.zeros(num_houses)
    for h in range(num_houses):
        h_start = h * spheres_per_house
        h_end = (h + 1) * spheres_per_house
        couplings[h] = np.mean(np.abs(H[admin_index, h_start:h_end]))

    return couplings


# ═══════════════════════════════════════════════════════════════
# DIAGNOSTIC UTILITIES
# ═══════════════════════════════════════════════════════════════

def operator_summary(H: np.ndarray) -> Dict:
    """Generate a diagnostic summary of the HSUF operator."""
    eigenvalues = np.linalg.eigvalsh(H)

    return {
        "N": H.shape[0],
        "trace": float(np.trace(H)),
        "frobenius_norm": float(np.linalg.norm(H, 'fro')),
        "spectral_range": [float(eigenvalues[0]), float(eigenvalues[-1])],
        "spectral_gap": float(eigenvalues[-1] - eigenvalues[-2]),
        "mean_diagonal": float(np.mean(np.diag(H))),
        "mean_off_diagonal": float(np.mean(np.abs(H - np.diag(np.diag(H))))),
        "symmetry_error": float(np.max(np.abs(H - H.T))),
        "num_eigenvalues": len(eigenvalues),
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    print("Building HSUF operator (N=145, canonical params, seed=42)...")
    H = build_hsuf(N=CANONICAL_N, params=HSUFParams.canonical(), seed=42)
    summary = operator_summary(H)
    print(json.dumps(summary, indent=2))

    # Verify stochastic component: two different seeds should produce different matrices
    H1 = build_hsuf(N=CANONICAL_N, params=HSUFParams.canonical(), seed=42)
    H2 = build_hsuf(N=CANONICAL_N, params=HSUFParams.canonical(), seed=43)
    diff = np.max(np.abs(H1 - H2))
    print(f"\nStochastic verification: max|H(seed=42) - H(seed=43)| = {diff:.6f}")
    if diff > 0:
        print("  ✓ Different seeds produce different operators (jitter working)")
    else:
        print("  ✗ DEGENERATE — seeds produce identical operators (jitter broken)")

    print("\nHouse coupling matrix:")
    couplings = extract_house_couplings(H)
    for i in range(12):
        row = " ".join(f"{couplings[i,j]:.4f}" for j in range(12))
        print(f"  H{i+1:2d}: {row}")

    print("\nElement 145 → House couplings:")
    admin = admin_sphere_coupling(H)
    for i in range(12):
        print(f"  H{i+1:2d}: {admin[i]:.6f}")
