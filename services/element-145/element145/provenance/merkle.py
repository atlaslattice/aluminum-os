"""Merkle tree helpers for provenance verification (display + integrity)."""
from __future__ import annotations

import hashlib
from typing import List


def _h(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


def merkle_root(leaves: List[bytes]) -> bytes:
    if not leaves:
        return b""
    level = [ _h(l) for l in leaves ]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            a = level[i]
            b = level[i+1] if i + 1 < len(level) else a
            nxt.append(_h(a + b))
        level = nxt
    return level[0]
