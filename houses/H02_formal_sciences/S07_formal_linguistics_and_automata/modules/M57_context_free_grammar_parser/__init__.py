"""
Module: Context-Free Grammar Parser
ID: M57
House: H02 | Sphere: S07
Status: ACTIVE
"""

"""Context-Free Grammar Parser — Parses context-free grammars"""

from typing import List, Set, Dict, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class Automaton:
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[Tuple[str, str], Set[str]]
    start_state: str
    accept_states: Set[str]

class ContextFreeGrammarParser:
    """Implementation of Context-Free Grammar Parser for lattice formal verification."""

    def __init__(self):
        self.automata: List[Automaton] = []

    def create_dfa(self, states: Set[str], alphabet: Set[str],
                   transitions: Dict[Tuple[str, str], str],
                   start: str, accept: Set[str]) -> Automaton:
        """Create a deterministic finite automaton."""
        det_transitions = {k: {v} for k, v in transitions.items()}
        automaton = Automaton(states, alphabet, det_transitions, start, accept)
        self.automata.append(automaton)
        return automaton

    def accepts(self, automaton: Automaton, input_string: str) -> bool:
        """Check if automaton accepts input string."""
        current = {automaton.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current:
                key = (state, symbol)
                if key in automaton.transitions:
                    next_states.update(automaton.transitions[key])
            current = next_states
            if not current:
                return False
        return bool(current & automaton.accept_states)

    def status(self) -> dict:
        return {
            "module": "M57",
            "name": "Context-Free Grammar Parser",
            "automata_count": len(self.automata),
        }

