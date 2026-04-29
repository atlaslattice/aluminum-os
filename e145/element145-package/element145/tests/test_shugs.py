"""
Test Suite: SHUGS — Von Mangoldt-Sheldon HSUF Operator
=======================================================
35+ tests covering Von Mangoldt function, HSUF operator construction,
symmetry, Hanning window, reproducibility, GUE-KS metrics, ensemble,
house couplings, and parameter presets.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
import math
import pytest
import numpy as np

from element145.shugs import (
    von_mangoldt,
    von_mangoldt_array,
    build_hsuf_operator,
    gue_ks_distance,
    spacing_statistics,
    unfold_eigenvalues,
    nearest_neighbor_spacings,
    wigner_surmise_cdf,
    wigner_surmise_pdf,
    run_ensemble,
    compare_n_values,
    parameter_sweep,
    extract_house_couplings,
    admin_sphere_coupling,
    HSUFParams,
    EnsembleStats,
    RIEMANN_ZEROS,
    CANONICAL_N,
    SMEARING_DECAY,
)


# ═══════════════════════════════════════════════════════════════
# VON MANGOLDT FUNCTION
# ═══════════════════════════════════════════════════════════════

class TestVonMangoldt:
    """Verify Λ(n) correctness."""

    def test_lambda_of_0(self):
        assert von_mangoldt(0) == 0.0

    def test_lambda_of_1(self):
        assert von_mangoldt(1) == 0.0

    def test_lambda_of_prime_2(self):
        assert abs(von_mangoldt(2) - math.log(2)) < 1e-10

    def test_lambda_of_prime_3(self):
        assert abs(von_mangoldt(3) - math.log(3)) < 1e-10

    def test_lambda_of_prime_5(self):
        assert abs(von_mangoldt(5) - math.log(5)) < 1e-10

    def test_lambda_of_prime_7(self):
        assert abs(von_mangoldt(7) - math.log(7)) < 1e-10

    def test_lambda_of_prime_11(self):
        assert abs(von_mangoldt(11) - math.log(11)) < 1e-10

    def test_lambda_of_prime_13(self):
        assert abs(von_mangoldt(13) - math.log(13)) < 1e-10

    def test_lambda_of_prime_large(self):
        assert abs(von_mangoldt(97) - math.log(97)) < 1e-10

    def test_lambda_of_prime_power_4(self):
        # 4 = 2^2
        assert abs(von_mangoldt(4) - math.log(2)) < 1e-10

    def test_lambda_of_prime_power_8(self):
        # 8 = 2^3
        assert abs(von_mangoldt(8) - math.log(2)) < 1e-10

    def test_lambda_of_prime_power_9(self):
        # 9 = 3^2
        assert abs(von_mangoldt(9) - math.log(3)) < 1e-10

    def test_lambda_of_prime_power_27(self):
        # 27 = 3^3
        assert abs(von_mangoldt(27) - math.log(3)) < 1e-10

    def test_lambda_of_prime_power_16(self):
        # 16 = 2^4
        assert abs(von_mangoldt(16) - math.log(2)) < 1e-10

    def test_lambda_of_composite_6(self):
        # 6 = 2 × 3 — not a prime power
        assert von_mangoldt(6) == 0.0

    def test_lambda_of_composite_10(self):
        assert von_mangoldt(10) == 0.0

    def test_lambda_of_composite_12(self):
        assert von_mangoldt(12) == 0.0

    def test_lambda_of_composite_15(self):
        assert von_mangoldt(15) == 0.0

    def test_von_mangoldt_array_length(self):
        arr = von_mangoldt_array(20)
        assert len(arr) == 20

    def test_von_mangoldt_array_zero_at_0_and_1(self):
        arr = von_mangoldt_array(5)
        assert arr[0] == 0.0
        assert arr[1] == 0.0

    def test_von_mangoldt_array_prime_values(self):
        arr = von_mangoldt_array(10)
        assert abs(arr[2] - math.log(2)) < 1e-10
        assert abs(arr[3] - math.log(3)) < 1e-10
        assert abs(arr[5] - math.log(5)) < 1e-10
        assert abs(arr[7] - math.log(7)) < 1e-10

    def test_von_mangoldt_array_composite_zero(self):
        arr = von_mangoldt_array(10)
        assert arr[6] == 0.0  # 6 = 2×3


# ═══════════════════════════════════════════════════════════════
# HSUF OPERATOR CONSTRUCTION
# ═══════════════════════════════════════════════════════════════

class TestHSUFOperator:
    """Verify HSUF operator properties."""

    def test_operator_is_square(self):
        H = build_hsuf_operator(20)
        assert H.shape == (20, 20)

    def test_operator_is_symmetric(self):
        H = build_hsuf_operator(30)
        assert np.allclose(H, H.T, atol=1e-12)

    def test_operator_n145_shape(self):
        H = build_hsuf_operator(145)
        assert H.shape == (145, 145)

    def test_operator_n145_symmetric(self):
        H = build_hsuf_operator(145)
        assert np.allclose(H, H.T, atol=1e-12)

    def test_operator_real_eigenvalues(self):
        H = build_hsuf_operator(50)
        eigenvalues = np.linalg.eigvalsh(H)
        assert np.all(np.isreal(eigenvalues))

    def test_hanning_boundary_zeros_edges(self):
        """Hanning window should suppress matrix edges."""
        H = build_hsuf_operator(50)
        # First and last rows/cols should be near zero due to Hanning
        assert abs(H[0, 0]) < abs(H[25, 25])  # Center > edge

    def test_operator_deterministic(self):
        """Same params → same operator."""
        p = HSUFParams.canonical()
        H1 = build_hsuf_operator(30, p)
        H2 = build_hsuf_operator(30, p)
        assert np.allclose(H1, H2, atol=1e-14)

    def test_canonical_vs_optimized_differ(self):
        """Different params should produce different operators."""
        H_can = build_hsuf_operator(50, HSUFParams.canonical())
        H_opt = build_hsuf_operator(50, HSUFParams.optimized())
        assert not np.allclose(H_can, H_opt)

    def test_operator_not_diagonal(self):
        """Off-diagonal elements should be non-zero."""
        H = build_hsuf_operator(30)
        off_diag = H - np.diag(np.diag(H))
        assert np.max(np.abs(off_diag)) > 0


# ═══════════════════════════════════════════════════════════════
# GUE-KS METRICS
# ═══════════════════════════════════════════════════════════════

class TestGUEKSMetrics:
    """Verify GUE-KS distance computation."""

    def test_gue_ks_returns_float(self):
        H = build_hsuf_operator(50)
        eigs = np.linalg.eigvalsh(H)
        ks = gue_ks_distance(eigs)
        assert isinstance(ks, float)

    def test_gue_ks_bounded(self):
        """KS distance should be between 0 and 1."""
        H = build_hsuf_operator(50)
        eigs = np.linalg.eigvalsh(H)
        ks = gue_ks_distance(eigs)
        assert 0.0 <= ks <= 1.0

    def test_gue_ks_small_input(self):
        """Very small eigenvalue set should return 1.0."""
        ks = gue_ks_distance(np.array([1.0, 2.0]))
        assert ks == 1.0

    def test_unfold_preserves_order(self):
        eigs = np.sort(np.random.randn(50))
        unfolded = unfold_eigenvalues(eigs)
        assert np.all(np.diff(unfolded) >= -1e-10)

    def test_nearest_neighbor_spacings_positive(self):
        unfolded = np.linspace(0, 50, 51)
        spacings = nearest_neighbor_spacings(unfolded)
        assert np.all(spacings >= 0)

    def test_spacing_statistics_keys(self):
        H = build_hsuf_operator(50)
        eigs = np.linalg.eigvalsh(H)
        stats = spacing_statistics(eigs)
        assert "ks_distance" in stats
        assert "mean_spacing" in stats
        assert "var_spacing" in stats

    def test_wigner_cdf_monotonic(self):
        s = np.linspace(0, 4, 100)
        cdf = wigner_surmise_cdf(s)
        assert np.all(np.diff(cdf) >= -1e-10)

    def test_wigner_cdf_boundary(self):
        assert abs(wigner_surmise_cdf(np.array([0.0]))[0]) < 0.01
        assert wigner_surmise_cdf(np.array([10.0]))[0] > 0.99

    def test_wigner_pdf_nonnegative(self):
        s = np.linspace(0, 4, 100)
        pdf = wigner_surmise_pdf(s)
        assert np.all(pdf >= -1e-10)


# ═══════════════════════════════════════════════════════════════
# ENSEMBLE RUNNER
# ═══════════════════════════════════════════════════════════════

class TestEnsemble:
    """Verify ensemble runner."""

    def test_ensemble_returns_stats(self):
        r = run_ensemble(30, k=3, seed=42)
        assert isinstance(r, EnsembleStats)
        assert r.n == 30
        assert r.k == 3
        assert len(r.all_ks) == 3

    def test_ensemble_mean_in_range(self):
        r = run_ensemble(30, k=3, seed=42)
        assert 0.0 < r.mean_ks < 1.0

    def test_ensemble_ci_contains_mean(self):
        r = run_ensemble(30, k=5, seed=42)
        lo, hi = r.ci_95
        assert lo <= r.mean_ks <= hi

    def test_ensemble_std_nonnegative(self):
        r = run_ensemble(30, k=3, seed=42)
        assert r.std_ks >= 0


# ═══════════════════════════════════════════════════════════════
# COMPARISON & SWEEP
# ═══════════════════════════════════════════════════════════════

class TestComparison:
    """Verify N-value comparison."""

    def test_compare_returns_result(self):
        c = compare_n_values([28, 29, 30], k=3, seed=42)
        assert len(c.results) == 3
        assert c.best_n in (28, 29, 30)

    def test_compare_summary_string(self):
        c = compare_n_values([28, 29, 30], k=3, seed=42)
        s = c.summary()
        assert "28" in s
        assert "29" in s
        assert "30" in s

    def test_compare_pvalues_computed(self):
        c = compare_n_values([28, 29, 30], k=5, seed=42)
        # Should have p-values for non-best N values
        assert len(c.pairwise_pvalues) >= 1


# ═══════════════════════════════════════════════════════════════
# HOUSE COUPLINGS
# ═══════════════════════════════════════════════════════════════

class TestHouseCouplings:
    """Verify house coupling extraction."""

    def test_extract_house_couplings_keys(self):
        couplings = extract_house_couplings(145)
        # Should have C(12,2) = 66 pairs
        assert len(couplings) == 66
        assert "H1-H2" in couplings

    def test_couplings_positive(self):
        couplings = extract_house_couplings(145)
        assert all(v >= 0 for v in couplings.values())

    def test_admin_sphere_coupling_keys(self):
        couplings = admin_sphere_coupling(145)
        assert len(couplings) == 12
        assert "H1-E145" in couplings
        assert "H12-E145" in couplings

    def test_admin_couplings_positive(self):
        couplings = admin_sphere_coupling(145)
        assert all(v >= 0 for v in couplings.values())


# ═══════════════════════════════════════════════════════════════
# CONSTANTS & PARAMS
# ═══════════════════════════════════════════════════════════════

class TestConstants:
    """Verify constants and parameter presets."""

    def test_canonical_n_is_145(self):
        assert CANONICAL_N == 145

    def test_20_riemann_zeros(self):
        assert len(RIEMANN_ZEROS) == 20

    def test_first_riemann_zero(self):
        assert abs(RIEMANN_ZEROS[0] - 14.134725) < 0.001

    def test_smearing_decay(self):
        assert SMEARING_DECAY == 18.9

    def test_canonical_params(self):
        p = HSUFParams.canonical()
        assert p.alpha == 0.05
        assert p.beta == 0.30
        assert p.gamma == 0.15

    def test_optimized_params(self):
        p = HSUFParams.optimized()
        assert p.alpha == 0.12
        assert p.beta == 0.95
        assert p.gamma == 0.08

    def test_riemann_zeros_ascending(self):
        for i in range(len(RIEMANN_ZEROS) - 1):
            assert RIEMANN_ZEROS[i] < RIEMANN_ZEROS[i + 1]
