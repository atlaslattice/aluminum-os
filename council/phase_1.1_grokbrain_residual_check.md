# Grokbrain Residual Check — sheldonbrain-rag-api

## Summary

16 files still reference the old grokbrain_v4 ontology or use hardcoded S001-S144 codes.
They fall into three categories:

## Category A: Already Migrated (3 files)
These files were updated in the Phase 1.1 PR and now import from canonical/:

| File | Status |
|------|--------|
| `metadata_validator.py` | MIGRATED — uses canonical.lattice_ontology_v2 |
| `rag_api_gemini.py` | MIGRATED — uses canonical imports |
| `sphere_classifier.py` | PARTIALLY MIGRATED — imports from canonical but still uses CATEGORY_NAMES/ELEMENTS aliases |

**sphere_classifier.py fix needed:** Line 22 imports `ELEMENTS, CATEGORY_NAMES` which exist as aliases but the code still uses old-style `CATEGORY_NAMES[cat]` indexing (lines 75, 201, 252) and `S001-S144` format (lines 157, 199, 232). This file needs a deeper rewrite to use lattice addresses natively.

## Category B: grokbrain_parser/ Directory (8 files) — LEGACY, DO NOT MIGRATE
These are the original grokbrain v4.0 pipeline files. They should NOT be migrated in this PR:

| File | Purpose | Disposition |
|------|---------|-------------|
| `grokbrain_parser/app.py` | Streamlit GUI dashboard | LEGACY — superseded by lattice API |
| `grokbrain_parser/grokbrain_core.py` | Core processing functions | LEGACY — superseded by canonical/ |
| `grokbrain_parser/grokbrain_v4.py` | Ontology tables | LEGACY — superseded by lattice_ontology_v2.py |
| `grokbrain_parser/load_spheres_from_csv.py` | CSV sphere loader | LEGACY — superseded |
| `grokbrain_parser/main.py` | Pipeline orchestration | LEGACY — superseded |
| `grokbrain_parser/simple_test.py` | Standalone tests | LEGACY — superseded by tests/ |
| `grokbrain_parser/test_suite.py` | Comprehensive tests | LEGACY — superseded by tests/ |
| `grokbrain_parser/twelve_step_validation.py` | Roadmap validation | LEGACY — superseded |
| `grokbrain_parser/xai_integration.py` | xAI Collections API | LEGACY — needs separate migration |

**Recommendation:** Add a `grokbrain_parser/DEPRECATED.md` file marking the entire directory as legacy. Remove in Phase 2 after confirming no production dependencies.

## Category C: Other Files with Hardcoded S001-S144 (5 files) — PHASE 2 MIGRATION

| File | Old References | Priority |
|------|---------------|----------|
| `grok_rag.py` | `sphere="S016"` hardcoded | LOW — Grok-specific, not in production path |
| `pinecone_client.py` | `sphere_filter` param docs reference S069 | MEDIUM — production file |
| `rag_api.py` | S069, S016 in examples | LOW — superseded by rag_api_gemini.py |
| `rag_wrapper.py` | S069, S144 in docs | LOW — wrapper, not production |
| `unified_rag.py` | `sphere="S016"` hardcoded | MEDIUM — multi-LLM interface |
| `upload_to_notion.py` | 9 hardcoded S015/S042 references | LOW — one-time upload script |

## Action Items for This PR

1. Fix sphere_classifier.py to use lattice addresses natively (not just aliased imports)
2. Add grokbrain_parser/DEPRECATED.md
3. Leave Category C files for Phase 2 PR
