from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

OUTBOX_DIR = Path(".element145/notion_outbox")


def _ensure_dir():
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)


def queue_failed_write(kind: str, payload: Any, error: str) -> str:
    _ensure_dir()
    ts = int(time.time() * 1000)
    path = OUTBOX_DIR / f"{ts}_{kind}.json"
    with open(path, "w") as f:
        json.dump({"kind": kind, "payload": payload, "error": error}, f)
    return str(path)


def flush_outbox(process_fn):
    _ensure_dir()
    results = []
    for file in sorted(OUTBOX_DIR.glob("*.json")):
        try:
            data = json.loads(file.read_text())
            process_fn(data["kind"], data["payload"])
            file.unlink()
            results.append((str(file), True))
        except Exception as e:
            results.append((str(file), False, str(e)))
    return results
