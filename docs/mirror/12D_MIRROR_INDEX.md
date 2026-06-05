# 12D Mirror Index Control Ledger

Status: `ACTIVE_CONTROL_DOCUMENT`
Canon status: `CANDIDATE`
Authority: `HUMAN_ROOT_REQUIRED_FOR_CANON_OR_DEPLOYMENT`
Created: 2026-06-05
Repository anchor: `atlaslattice/aluminum-os`
Control issue: `#12`
Initial anchor commit: `128376e1ef2d23913226deac435a769e4bbc1f4d`

## Purpose

Ensure a complete, non-destructive, receipt-preserving mirror between:

- Notion
- Google Drive
- OneDrive
- GitHub

This file is the GitHub-side control ledger for the mirror/index effort. It does **not** claim completeness until every source surface has a manifest, hash/index receipt, parity report, and human-root review.

## Hard Invariants

1. **NOTHING DIES** — no source item is deleted, overwritten, or silently collapsed.
2. **Everything can connect to everything; nothing can promote itself.**
3. **Mirror does not mean merge.** Mirrored objects remain source-addressable.
4. **Receipt before authority.** Every import/export/sync requires a receipt.
5. **Canon requires human-root.** No connector, agent, script, or child seat can self-promote artifacts to canon.
6. **Quarantine beats deletion.** Unknown, duplicate, unsafe, malformed, or contradictory items are preserved under quarantine labels.

## 12D Index Schema

Every mirrored artifact should receive a 12D index packet:

| Dimension | Field | Description |
|---:|---|---|
| D01 | `source_surface` | Notion, Drive, OneDrive, GitHub, local export, chat export, etc. |
| D02 | `source_native_id` | Native document/file/page/repo/path ID where available. |
| D03 | `source_path_or_url` | Original path or URL, redacted where needed. |
| D04 | `artifact_type` | doc, markdown, pdf, image, spreadsheet, code, issue, thread, note, export bundle, etc. |
| D05 | `content_hash` | SHA-256 or stronger hash of exported content/bytes. |
| D06 | `export_timestamp` | Exact export/snapshot time in ISO 8601. |
| D07 | `lineage_parent` | Prior version, parent folder/page, repo path, or source thread. |
| D08 | `semantic_tags` | 12-house / 144-sphere tags plus freeform project tags. |
| D09 | `canon_status` | RAW, PARSED, CLAIM, CANDIDATE, REVIEWED, CONTRADICTED, SUPERSEDED, QUARANTINED, RATIFIED, CANON, DEPLOYED. |
| D10 | `mirror_targets` | Which surfaces should contain a mirrored copy/index pointer. |
| D11 | `parity_status` | missing, partial, mirrored, divergent, superseded, quarantined, verified. |
| D12 | `receipt_refs` | Commit SHAs, export manifests, logs, issue/PR references, audit notes. |

## Required Manifests

The mirror is incomplete until these manifests exist and are linked here:

| Surface | Required Manifest | Status | Notes |
|---|---|---|---|
| Notion | `notion_export_manifest.jsonl` | `MISSING_ACCESS` | Connector/export not available in this session. |
| Google Drive | `drive_export_manifest.jsonl` | `MISSING_ACCESS` | Connector/export not available in this session. |
| OneDrive | `onedrive_export_manifest.jsonl` | `MISSING_ACCESS` | Connector/export not available in this session. |
| GitHub | `github_manifest.jsonl` | `ANCHOR_STARTED` | GitHub repo anchor created here. |

## Mirror Packet Template

```json
{
  "d01_source_surface": "",
  "d02_source_native_id": "",
  "d03_source_path_or_url": "",
  "d04_artifact_type": "",
  "d05_content_hash": "",
  "d06_export_timestamp": "",
  "d07_lineage_parent": "",
  "d08_semantic_tags": [],
  "d09_canon_status": "RAW",
  "d10_mirror_targets": [],
  "d11_parity_status": "missing",
  "d12_receipt_refs": []
}
```

## Parity Rules

A mirrored artifact is considered `verified` only when:

1. It appears in the source manifest.
2. It has a content hash or stable source receipt.
3. It has a 12D packet.
4. Each target surface contains either the artifact copy or a source-addressable pointer.
5. Divergences are explicitly marked instead of silently overwritten.
6. Superseded versions remain reachable.

## Quarantine Rules

Use `QUARANTINED` when an artifact is:

- duplicate but not confidently identical
- malformed
- missing provenance
- sensitive/private beyond the target surface
- contradictory with a candidate/canon artifact
- machine-generated without sufficient evidence
- suspected of accidental promotion

Quarantine preserves the object and prevents promotion. It is not deletion.

## Current Access Reality

From this session, GitHub is connected and writable. Notion, Google Drive, and OneDrive are not directly available through the connected tool surface here. Therefore this commit establishes the GitHub anchor and the mirror/index contract, but does not claim cross-surface completion.

## Immediate Next Work Queue

1. Export or connect Notion and generate `notion_export_manifest.jsonl`.
2. Export or connect Google Drive and generate `drive_export_manifest.jsonl`.
3. Export or connect OneDrive and generate `onedrive_export_manifest.jsonl`.
4. Generate `github_manifest.jsonl` from the repository tree/issues/PRs.
5. Normalize all four manifests into the 12D packet schema.
6. Produce `12D_PARITY_REPORT.md` listing missing, partial, divergent, quarantined, superseded, and verified artifacts.
7. Only after parity review, mark selected artifacts as `RATIFIED` or `CANON` by human-root action.

## Status Block

```yaml
mirror_status: anchored_not_complete
repo_anchor: atlaslattice/aluminum-os
control_issue: 12
github_receipt: 128376e1ef2d23913226deac435a769e4bbc1f4d
notion_access: missing
drive_access: missing
onedrive_access: missing
canon_status: candidate
human_gate_required: true
```
