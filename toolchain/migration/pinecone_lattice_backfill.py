#!/usr/bin/env python3
"""
Pinecone Lattice Backfill — Safe Migration Tool

Reads existing Pinecone vectors, classifies them into the 12×12+1 lattice
ontology, and updates their metadata with lattice addresses. Designed for
production safety:

  - DRY RUN by default (--dry-run flag, no writes unless --commit)
  - Batch processing with configurable page size
  - Full audit log written to disk
  - Rollback manifest: every changed vector's old metadata is saved
  - Idempotent: vectors already tagged with lattice addresses are skipped

Usage:
  # Dry run (default) — see what would change
  python pinecone_lattice_backfill.py --dry-run

  # Commit changes (requires explicit flag)
  python pinecone_lattice_backfill.py --commit

  # Limit to N vectors (for testing)
  python pinecone_lattice_backfill.py --dry-run --limit 100

  # Rollback from manifest
  python pinecone_lattice_backfill.py --rollback rollback_manifest_20260429.json

Environment:
  PINECONE_API_KEY  — Pinecone API key
  PINECONE_INDEX    — Index name (default: sheldonbrain-rag)

Phase: 2 (follow-up to Phase 1.1 ontology migration PR)
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add parent directory for canonical imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from canonical.lattice_ontology_v2 import (
    classify_text, HOUSE_NAMES, HOUSE_IDS, SPHERES,
    address_for_index,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_INDEX = "sheldonbrain-rag"
BATCH_SIZE = 100
MAX_RETRIES = 3
RETRY_DELAY = 2.0

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(log_dir: str = "backfill_logs") -> logging.Logger:
    """Configure logging to both file and console."""
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"backfill_{timestamp}.log")

    logger = logging.getLogger("pinecone_backfill")
    logger.setLevel(logging.DEBUG)

    # File handler — verbose
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    logger.addHandler(fh)

    # Console handler — info only
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(ch)

    logger.info(f"Log file: {log_file}")
    return logger


# ---------------------------------------------------------------------------
# Legacy-to-Lattice Mapping
# ---------------------------------------------------------------------------

def legacy_to_lattice(sphere_code: str) -> Optional[str]:
    """
    Convert legacy S001-S144 code to lattice address.

    Args:
        sphere_code: Legacy sphere code (e.g., "S016")

    Returns:
        Lattice address (e.g., "H02.S04") or None if invalid
    """
    if not sphere_code or not isinstance(sphere_code, str):
        return None

    if "." in sphere_code:
        # Already a lattice address
        return sphere_code

    if sphere_code.startswith("S") and len(sphere_code) == 4:
        try:
            idx = int(sphere_code[1:]) - 1
            if 0 <= idx < 144:
                return address_for_index(idx)
        except ValueError:
            pass

    return None


def classify_vector_metadata(metadata: Dict) -> Dict:
    """
    Classify a vector's metadata into the lattice ontology.

    Uses text content from metadata fields to determine the best
    lattice address. Falls back to legacy sphere code if present.

    Args:
        metadata: Pinecone vector metadata dict

    Returns:
        Dict with lattice fields to merge into metadata
    """
    # Build classification text from available metadata
    parts = []
    for key in ["text", "content", "title", "description", "filename", "source"]:
        val = metadata.get(key, "")
        if val and isinstance(val, str):
            parts.append(val[:500])  # Cap each field

    classify_input = " ".join(parts)

    # Try text classification first
    if classify_input.strip():
        results = classify_text(classify_input, top_k=1)
        if results:
            best = results[0]
            return {
                "lattice_address": best["address"],
                "lattice_house": best["house"],
                "lattice_house_id": best["house_id"],
                "lattice_sphere": best["sphere"],
                "lattice_confidence": round(best["score"], 4),
                "lattice_method": "text_classification",
            }

    # Fall back to legacy sphere code
    legacy_sphere = metadata.get("sphere", "")
    lattice_addr = legacy_to_lattice(legacy_sphere)
    if lattice_addr:
        house_idx = int(lattice_addr.split(".")[0][1:]) - 1
        return {
            "lattice_address": lattice_addr,
            "lattice_house": HOUSE_NAMES[house_idx] if 0 <= house_idx < 12 else "Unknown",
            "lattice_house_id": HOUSE_IDS[house_idx] if 0 <= house_idx < 12 else "Unknown",
            "lattice_sphere": SPHERES[house_idx * 12 + int(lattice_addr.split(".")[1][1:]) - 1]
                if 0 <= house_idx < 12 else "Unknown",
            "lattice_confidence": 1.0,
            "lattice_method": "legacy_code_mapping",
        }

    # No classification possible
    return {
        "lattice_address": "E145",
        "lattice_house": "Admin Sphere",
        "lattice_house_id": "E145",
        "lattice_sphere": "Unclassified",
        "lattice_confidence": 0.0,
        "lattice_method": "fallback_e145",
    }


# ---------------------------------------------------------------------------
# Pinecone Operations
# ---------------------------------------------------------------------------

def get_pinecone_index(index_name: str):
    """Initialize Pinecone and return the index."""
    try:
        from pinecone import Pinecone
    except ImportError:
        print("ERROR: pinecone-client not installed. Run: pip install pinecone-client")
        sys.exit(1)

    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        print("ERROR: PINECONE_API_KEY environment variable not set")
        sys.exit(1)

    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)


def fetch_all_vectors(index, limit: Optional[int] = None,
                      logger: Optional[logging.Logger] = None) -> List[Dict]:
    """
    Fetch all vectors from the index using list + fetch pattern.

    Args:
        index: Pinecone index
        limit: Max vectors to fetch (None = all)
        logger: Logger instance

    Returns:
        List of {id, metadata} dicts
    """
    vectors = []
    pagination_token = None
    total_fetched = 0

    while True:
        # List vector IDs
        list_kwargs = {"limit": min(BATCH_SIZE, limit - total_fetched) if limit else BATCH_SIZE}
        if pagination_token:
            list_kwargs["pagination_token"] = pagination_token

        list_result = index.list_paginated(**list_kwargs)
        ids = [v.id for v in list_result.vectors]

        if not ids:
            break

        # Fetch full vectors with metadata
        fetch_result = index.fetch(ids=ids)
        for vid, vdata in fetch_result.vectors.items():
            vectors.append({
                "id": vid,
                "metadata": dict(vdata.metadata) if vdata.metadata else {},
            })

        total_fetched += len(ids)
        if logger:
            logger.info(f"  Fetched {total_fetched} vectors...")

        if limit and total_fetched >= limit:
            break

        pagination_token = list_result.pagination.next if list_result.pagination else None
        if not pagination_token:
            break

    return vectors


def update_vectors_batch(index, updates: List[Dict],
                         logger: Optional[logging.Logger] = None) -> int:
    """
    Update vector metadata in batches with retry logic.

    Args:
        index: Pinecone index
        updates: List of {id, metadata} dicts
        logger: Logger instance

    Returns:
        Number of successfully updated vectors
    """
    success_count = 0

    for i in range(0, len(updates), BATCH_SIZE):
        batch = updates[i:i + BATCH_SIZE]

        for attempt in range(MAX_RETRIES):
            try:
                for item in batch:
                    index.update(
                        id=item["id"],
                        set_metadata=item["new_metadata"],
                    )
                success_count += len(batch)
                if logger:
                    logger.debug(f"  Updated batch {i//BATCH_SIZE + 1} "
                                 f"({len(batch)} vectors)")
                break
            except Exception as e:
                if logger:
                    logger.warning(f"  Retry {attempt + 1}/{MAX_RETRIES} "
                                   f"for batch {i//BATCH_SIZE + 1}: {e}")
                time.sleep(RETRY_DELAY * (attempt + 1))
        else:
            if logger:
                logger.error(f"  FAILED batch {i//BATCH_SIZE + 1} after "
                             f"{MAX_RETRIES} retries")

    return success_count


# ---------------------------------------------------------------------------
# Rollback
# ---------------------------------------------------------------------------

def rollback_from_manifest(index, manifest_path: str,
                           logger: logging.Logger) -> int:
    """
    Rollback vector metadata from a saved manifest.

    Args:
        index: Pinecone index
        manifest_path: Path to rollback manifest JSON
        logger: Logger instance

    Returns:
        Number of rolled-back vectors
    """
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    logger.info(f"Rolling back {len(manifest)} vectors from {manifest_path}")

    rollback_updates = []
    for entry in manifest:
        rollback_updates.append({
            "id": entry["id"],
            "new_metadata": entry["old_metadata"],
        })

    return update_vectors_batch(index, rollback_updates, logger)


# ---------------------------------------------------------------------------
# Main Backfill Logic
# ---------------------------------------------------------------------------

def run_backfill(index_name: str, dry_run: bool = True,
                 limit: Optional[int] = None,
                 logger: Optional[logging.Logger] = None) -> Dict:
    """
    Run the lattice backfill on a Pinecone index.

    Args:
        index_name: Pinecone index name
        dry_run: If True, don't write changes
        limit: Max vectors to process
        logger: Logger instance

    Returns:
        Summary statistics dict
    """
    if not logger:
        logger = setup_logging()

    mode = "DRY RUN" if dry_run else "COMMIT"
    logger.info(f"=== Pinecone Lattice Backfill ({mode}) ===")
    logger.info(f"Index: {index_name}")
    if limit:
        logger.info(f"Limit: {limit} vectors")

    # Connect to Pinecone
    index = get_pinecone_index(index_name)
    stats = index.describe_index_stats()
    total_vectors = stats.total_vector_count
    logger.info(f"Total vectors in index: {total_vectors}")

    # Fetch vectors
    logger.info("Fetching vectors...")
    vectors = fetch_all_vectors(index, limit=limit, logger=logger)
    logger.info(f"Fetched {len(vectors)} vectors")

    # Classify and prepare updates
    updates = []
    skipped = 0
    already_tagged = 0
    classified_by_method = {"text_classification": 0, "legacy_code_mapping": 0,
                            "fallback_e145": 0}
    rollback_manifest = []

    for vec in vectors:
        vid = vec["id"]
        meta = vec["metadata"]

        # Skip if already has lattice address
        if meta.get("lattice_address") and meta["lattice_address"] != "E145":
            already_tagged += 1
            logger.debug(f"  SKIP {vid}: already tagged {meta['lattice_address']}")
            continue

        # Classify
        lattice_fields = classify_vector_metadata(meta)
        method = lattice_fields.get("lattice_method", "unknown")
        classified_by_method[method] = classified_by_method.get(method, 0) + 1

        # Save rollback info
        rollback_manifest.append({
            "id": vid,
            "old_metadata": {k: v for k, v in meta.items()},
            "new_fields": lattice_fields,
        })

        # Prepare update (merge new fields into existing metadata)
        new_metadata = {**lattice_fields}
        updates.append({
            "id": vid,
            "new_metadata": new_metadata,
        })

        logger.debug(f"  CLASSIFY {vid}: {lattice_fields['lattice_address']} "
                      f"({method}, conf={lattice_fields['lattice_confidence']})")

    # Save rollback manifest
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = f"rollback_manifest_{timestamp}.json"
    with open(manifest_path, "w") as f:
        json.dump(rollback_manifest, f, indent=2)
    logger.info(f"Rollback manifest saved: {manifest_path}")

    # Apply updates (or report dry run)
    if dry_run:
        logger.info(f"\n=== DRY RUN SUMMARY ===")
        logger.info(f"Would update: {len(updates)} vectors")
        logger.info(f"Already tagged: {already_tagged}")
        logger.info(f"Classification methods:")
        for method, count in classified_by_method.items():
            logger.info(f"  {method}: {count}")
    else:
        logger.info(f"\nCommitting {len(updates)} updates...")
        success = update_vectors_batch(index, updates, logger)
        logger.info(f"Successfully updated: {success}/{len(updates)}")

    summary = {
        "mode": mode,
        "index": index_name,
        "total_in_index": total_vectors,
        "fetched": len(vectors),
        "already_tagged": already_tagged,
        "to_update": len(updates),
        "classification_methods": classified_by_method,
        "rollback_manifest": manifest_path,
    }

    if not dry_run:
        summary["committed"] = True

    # Save summary
    summary_path = f"backfill_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Summary saved: {summary_path}")

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pinecone Lattice Backfill — migrate vector metadata to 12x12+1"
    )
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview changes without writing (default)")
    parser.add_argument("--commit", action="store_true",
                        help="Actually write changes to Pinecone")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max vectors to process")
    parser.add_argument("--index", default=DEFAULT_INDEX,
                        help=f"Pinecone index name (default: {DEFAULT_INDEX})")
    parser.add_argument("--rollback", type=str, default=None,
                        help="Rollback from manifest JSON file")

    args = parser.parse_args()
    logger = setup_logging()

    if args.rollback:
        index = get_pinecone_index(args.index)
        count = rollback_from_manifest(index, args.rollback, logger)
        logger.info(f"Rolled back {count} vectors")
        return

    dry_run = not args.commit
    summary = run_backfill(
        index_name=args.index,
        dry_run=dry_run,
        limit=args.limit,
        logger=logger,
    )

    print(f"\n{'='*60}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
