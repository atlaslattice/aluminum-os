"""
Module: Hypothesis Testing Framework
ID: M74
House: H02 | Sphere: S02
Status: ACTIVE
"""

"""Hypothesis Testing Framework — Statistical hypothesis testing for lattice decisions."""

import math
from typing import Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class TestType(Enum):
    ONE_SAMPLE_T = "one_sample_t"
    TWO_SAMPLE_T = "two_sample_t"
    CHI_SQUARE = "chi_square"
    Z_TEST = "z_test"

@dataclass
class TestResult:
    test_type: TestType
    statistic: float
    p_value: float
    reject_null: bool
    alpha: float
    conclusion: str

class HypothesisTestingFramework:
    """Statistical hypothesis testing for lattice routing decisions."""

    @staticmethod
    def z_test(sample_mean: float, pop_mean: float, pop_std: float, n: int, alpha: float = 0.05) -> TestResult:
        """One-sample Z-test."""
        z = (sample_mean - pop_mean) / (pop_std / math.sqrt(n))
        # Approximate p-value using normal CDF approximation
        p_value = 2 * (1 - HypothesisTestingFramework._normal_cdf(abs(z)))
        reject = p_value < alpha
        conclusion = f"{'Reject' if reject else 'Fail to reject'} H0 at α={alpha} (z={z:.4f}, p={p_value:.4f})"
        return TestResult(TestType.Z_TEST, z, p_value, reject, alpha, conclusion)

    @staticmethod
    def chi_square_goodness(observed: list, expected: list, alpha: float = 0.05) -> TestResult:
        """Chi-square goodness of fit test."""
        if len(observed) != len(expected):
            raise ValueError("Observed and expected must have same length")
        chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
        df = len(observed) - 1
        # Approximate p-value
        p_value = 1 - HypothesisTestingFramework._chi2_cdf(chi2, df)
        reject = p_value < alpha
        conclusion = f"{'Reject' if reject else 'Fail to reject'} H0 at α={alpha} (χ²={chi2:.4f}, df={df}, p≈{p_value:.4f})"
        return TestResult(TestType.CHI_SQUARE, chi2, p_value, reject, alpha, conclusion)

    @staticmethod
    def _normal_cdf(x: float) -> float:
        """Approximate standard normal CDF."""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    @staticmethod
    def _chi2_cdf(x: float, k: int) -> float:
        """Rough chi-square CDF approximation."""
        if x <= 0: return 0.0
        # Wilson-Hilferty approximation
        z = ((x / k) ** (1/3) - (1 - 2/(9*k))) / math.sqrt(2/(9*k))
        return HypothesisTestingFramework._normal_cdf(z)

