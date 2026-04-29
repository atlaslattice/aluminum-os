"""
Module: Axiom Consistency Checker
ID: M84
House: H02 | Sphere: S01
Status: ACTIVE
"""

"""Axiom Consistency Checker — Verifies consistency of axiom sets."""

from typing import List, Set, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Axiom:
    id: str
    statement: str
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class ConsistencyChecker:
    """Checks axiom sets for obvious inconsistencies and circular dependencies."""

    def __init__(self):
        self.axioms: List[Axiom] = []

    def add_axiom(self, axiom: Axiom):
        self.axioms.append(axiom)

    def check_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependency chains."""
        cycles = []
        visited = set()
        path = []

        def dfs(axiom_id: str):
            if axiom_id in path:
                cycle_start = path.index(axiom_id)
                cycles.append(path[cycle_start:] + [axiom_id])
                return
            if axiom_id in visited:
                return
            visited.add(axiom_id)
            path.append(axiom_id)
            axiom = next((a for a in self.axioms if a.id == axiom_id), None)
            if axiom:
                for dep in axiom.dependencies:
                    dfs(dep)
            path.pop()

        for axiom in self.axioms:
            dfs(axiom.id)
        return cycles

    def check_contradictions(self) -> List[Tuple[str, str]]:
        """Simple contradiction detection (negation pairs)."""
        contradictions = []
        statements = {a.id: a.statement for a in self.axioms}
        for id1, s1 in statements.items():
            for id2, s2 in statements.items():
                if id1 >= id2: continue
                if s1 == f"¬({s2})" or s2 == f"¬({s1})":
                    contradictions.append((id1, id2))
        return contradictions

    def is_consistent(self) -> Tuple[bool, str]:
        """Run all consistency checks."""
        cycles = self.check_circular_dependencies()
        if cycles:
            return False, f"Circular dependencies detected: {cycles[0]}"
        contradictions = self.check_contradictions()
        if contradictions:
            return False, f"Contradictions found: {contradictions[0]}"
        return True, "No inconsistencies detected (limited check)"

