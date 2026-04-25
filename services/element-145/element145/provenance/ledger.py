"""Hardened provenance ledger with append-only semantics and stable API.

Design goals:
- append-only writes;
- stable constructor;
- property-based count;
- JSON-stable verification responses;
- full SHA-256 hashes stored;
- chain linkage for tamper detection.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from element145.provenance.models import ProvenanceRecord, ProvenanceQuery


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ProvenanceLedger:
    def __init__(
        self,
        backend: str = "sqlite",
        path: str | None = None,
        ledger_path: str | None = None,
        sqlite_path: str | None = None,
    ) -> None:
        self.backend = backend
        base = Path(ledger_path or path or "./data/ledger")
        base.mkdir(parents=True, exist_ok=True)
        self.sqlite_path = Path(sqlite_path or (base / "provenance.db"))
        self._conn = sqlite3.connect(self.sqlite_path)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._init_schema()
        self._record_count = self._count_rows()
        self._last_hash = self._load_last_hash()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                trace_id TEXT,
                ts REAL,
                classification TEXT,
                elapsed_ms REAL,
                input_hash TEXT,
                output_hash TEXT,
                chain_hash TEXT,
                prev_hash TEXT,
                payload TEXT
            );
            """
        )
        self._conn.commit()

    def _count_rows(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM records")
        return int(cur.fetchone()[0])

    def _load_last_hash(self) -> str:
        cur = self._conn.execute(
            "SELECT chain_hash FROM records ORDER BY ts DESC LIMIT 1"
        )
        row = cur.fetchone()
        return row[0] if row else ""

    @property
    def count(self) -> int:
        return self._record_count

    def append(self, record: ProvenanceRecord) -> dict[str, Any]:
        payload = record.to_ledger_entry()
        payload_json = json.dumps(payload, sort_keys=True).encode()

        input_hash = record.input_hash
        output_hash = record.output_hash
        prev_hash = self._last_hash or ""
        chain_hash = _sha256_hex(prev_hash.encode() + payload_json)

        self._conn.execute(
            "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record.record_id,
                record.trace_id,
                record.timestamp,
                record.classification,
                record.elapsed_ms,
                input_hash,
                output_hash,
                chain_hash,
                prev_hash,
                payload_json.decode(),
            ),
        )
        self._conn.commit()

        self._record_count += 1
        self._last_hash = chain_hash

        return {
            "record_id": record.record_id,
            "chain_hash": chain_hash,
            "prev_hash": prev_hash,
        }

    def query(self, q: ProvenanceQuery) -> list[dict[str, Any]]:
        clauses: list[str] = []
        args: list[Any] = []

        if q.trace_id:
            clauses.append("trace_id = ?")
            args.append(q.trace_id)
        if q.classification:
            clauses.append("classification = ?")
            args.append(q.classification)
        if q.start_time:
            clauses.append("ts >= ?")
            args.append(q.start_time)
        if q.end_time:
            clauses.append("ts <= ?")
            args.append(q.end_time)

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"SELECT payload FROM records{where} ORDER BY ts DESC LIMIT ?"
        args.append(q.limit)

        cur = self._conn.execute(sql, args)
        return [json.loads(row[0]) for row in cur.fetchall()]

    def verify_chain(self) -> dict[str, Any]:
        cur = self._conn.execute(
            "SELECT payload, chain_hash, prev_hash FROM records ORDER BY ts ASC"
        )
        prev = ""
        idx = 0
        for payload, chain_hash, prev_hash in cur.fetchall():
            payload_bytes = payload.encode()
            expected = _sha256_hex(prev.encode() + payload_bytes)
            if prev_hash != prev or chain_hash != expected:
                return {
                    "valid": False,
                    "error_index": idx,
                }
            prev = chain_hash
            idx += 1
        return {
            "valid": True,
            "chain_length": idx,
        }

    def export_json(self) -> list[dict[str, Any]]:
        cur = self._conn.execute("SELECT payload FROM records ORDER BY ts ASC")
        return [json.loads(row[0]) for row in cur.fetchall()]

    def close(self) -> None:
        self._conn.close()
