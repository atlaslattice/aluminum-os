"""
Module: Quantum Key Distribution
ID: M71
House: H02 | Sphere: S12
Status: ACTIVE
"""

"""Quantum Key Distribution — Quantum key distribution protocols"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math
import random

@dataclass
class Qubit:
    alpha: complex  # |0⟩ amplitude
    beta: complex   # |1⟩ amplitude

    @property
    def probabilities(self) -> Tuple[float, float]:
        return (abs(self.alpha)**2, abs(self.beta)**2)

    def measure(self) -> int:
        p0 = abs(self.alpha)**2
        return 0 if random.random() < p0 else 1

class QuantumKeyDistribution:
    """Implementation of Quantum Key Distribution for lattice quantum computations."""

    def __init__(self, num_qubits: int = 4):
        self.num_qubits = num_qubits
        self.register: List[Qubit] = [Qubit(1+0j, 0+0j) for _ in range(num_qubits)]

    def hadamard(self, qubit_idx: int):
        """Apply Hadamard gate to qubit."""
        q = self.register[qubit_idx]
        inv_sqrt2 = 1 / math.sqrt(2)
        new_alpha = complex(inv_sqrt2 * (q.alpha + q.beta))
        new_beta = complex(inv_sqrt2 * (q.alpha - q.beta))
        self.register[qubit_idx] = Qubit(new_alpha, new_beta)

    def pauli_x(self, qubit_idx: int):
        """Apply Pauli-X (NOT) gate."""
        q = self.register[qubit_idx]
        self.register[qubit_idx] = Qubit(q.beta, q.alpha)

    def measure_all(self) -> List[int]:
        """Measure all qubits."""
        return [q.measure() for q in self.register]

    def reset(self):
        """Reset all qubits to |0⟩."""
        self.register = [Qubit(1+0j, 0+0j) for _ in range(self.num_qubits)]

    def status(self) -> dict:
        return {
            "module": "M71",
            "name": "Quantum Key Distribution",
            "num_qubits": self.num_qubits,
            "state": [q.probabilities for q in self.register],
        }

