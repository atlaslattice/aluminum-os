"""
Module: Number Theory Utilities
ID: M28
House: H02 | Sphere: S01
Status: ACTIVE
"""

"""Number Theory Utilities — Prime factorization, modular arithmetic, and number-theoretic functions."""

import math
from typing import List, Tuple

class NumberTheoryEngine:
    """Provides number-theoretic computations for lattice operations."""

    @staticmethod
    def is_prime(n: int) -> bool:
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    @staticmethod
    def prime_factorization(n: int) -> List[Tuple[int, int]]:
        """Return prime factorization as list of (prime, exponent) tuples."""
        factors = []
        d = 2
        while d * d <= n:
            exp = 0
            while n % d == 0:
                n //= d
                exp += 1
            if exp > 0:
                factors.append((d, exp))
            d += 1
        if n > 1:
            factors.append((n, 1))
        return factors

    @staticmethod
    def euler_totient(n: int) -> int:
        """Compute Euler totient function phi(n)."""
        result = n
        p = 2
        temp = n
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        if temp > 1:
            result -= result // temp
        return result

    @staticmethod
    def modular_exponentiation(base: int, exp: int, mod: int) -> int:
        """Fast modular exponentiation."""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    @staticmethod
    def gcd(a: int, b: int) -> int:
        while b: a, b = b, a % b
        return a

    @staticmethod
    def lcm(a: int, b: int) -> int:
        return abs(a * b) // NumberTheoryEngine.gcd(a, b)


def lattice_prime_signature(house: int, sphere: int) -> str:
    """Generate a unique prime signature for a lattice position."""
    n = house * 12 + sphere
    factors = NumberTheoryEngine.prime_factorization(n)
    return " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors)

