PR Summary
PR: https://github.com/atlaslattice/sheldonbrain-rag-api/pull/2
Title: Phase 1.1: Ontology Migration to Canonical 12x12+1 Lattice
Base → Head: master ← feature/phase-1.1-ontology-migration
Commits: 1
Files changed: 9
Diffstat: +1940 / -332
Mergeable: ✅ clean (GitHub reports mergeable)
Risk: Medium (production service behavior changes: metadata schema + new endpoints; but backward-compat is intentionally kept)

High-level: this PR vendors a canonical ontology snapshot under canonical/, rewires classification/metadata to use it, adds two introspection/classification endpoints, and adds a dedicated migration test suite.

Core changes (what matters most)
1) Vendored canonical ontology (canonical/)
You added:

canonical/lattice_ontology_v2.py
canonical/sphere_classifier_v2.py
canonical/lattice_ontology.yaml
canonical/VENDORED_FROM.md
canonical/__init__.py
Review note: this satisfies your “hermetic deploy” requirement, and VENDORED_FROM.md documents provenance + upgrade path.

2) metadata_validator.py migration logic
VALID_SPHERES now accepts both:
lattice addresses: Hxx.Syy plus E145
legacy codes: S001…S144
Adds LEGACY_TO_LATTICE mapping (index-based).
auto_assign_sphere() now uses classify_text() from vendored ontology.
Enriches metadata with house, house_name, sphere_name when given/derived a lattice sphere.
This is the correct “bridge layer” to avoid breaking existing content while you backfill.

3) rag_api_gemini.py now auto-tags lattice metadata
On /store, if metadata lacks house or sphere, it calls pinecone_metadata() (vendored) to fill:
house, sphere, house_name, sphere_name, timestamp
/query supports Pinecone filters (as passthrough) and now returns house/sphere fields explicitly.
Adds:
POST /classify
GET /lattice
Other changes worth reviewing (with diffs)
sphere_classifier.py: import path migration
This PR changes it to import ontology from canonical/ rather than grokbrain_parser/grokbrain_v4.py.

Key thing to verify: nothing else in this file still assumes the old category semantics (beyond just array lengths).

Merge readiness & blockers
No hard blockers found from the diff listing alone; GitHub shows clean mergeability, and you added a focused test suite.

That said, I recommend fixing/confirming these two production-readiness items before merge (or immediately after):

canonical/sphere_classifier_v2.py has Pinecone migration code that is likely not correct as-is

It uses a dummy index.query(vector=[0.0] * 768, top_k=10000, ...) as a stand-in for “listing” vectors.
In Pinecone, query is not a general “scan/list all vectors” primitive, and embedding dimension may not be 768.
Suggestion: keep the file as vendored reference, but ensure no production code calls migrate_pinecone_vectors() (it doesn’t appear to be called right now). If you intend to run backfill, implement it in an explicit script that matches your Pinecone index dimension + supports ID iteration via your own source-of-truth.
sys.path.insert pattern

Several files do sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) to import canonical.*.
It works, but it’s a little brittle. If this service is packaged differently later, these imports can get weird.
If the repo is always run as a flat app on Cloud Run, this is probably fine. If you later package it, consider making it a proper module import layout.
Given the above: mergeable now, but treat Pinecone backfill as a separate operational concern.

Possible improvements (actionable)
Align nomenclature in rag_api_gemini.py docs vs reality

Root response says version "2.0-gemini-lattice", tests look for "gemini-lattice" substring. That’s fine.
Your earlier plan talked about house_id/sphere_id; in this PR, metadata keys are house and sphere (where sphere is actually the lattice address like H02.S11). That’s OK—just make sure downstream tooling agrees.
Ensure ontology-lock CI gate exists in this repo

VENDORED_FROM.md references an ontology-lock SHA-256 drift gate.
I didn’t see workflow changes in this PR file list. If the gate is not yet present in sheldonbrain-rag-api, it’s worth adding in a follow-up PR so the governance story is actually enforced here (not just documented).
Want me to…
Do a deeper file-by-file review of metadata_validator.py and rag_api_gemini.py logic for edge cases (E145 handling, missing metadata precedence, filter semantics).
Check whether this PR accidentally leaves any remaining imports/usages of grokbrain v4 across the repo (via code search).
Propose a safe Pinecone backfill script that matches your actual index dimension + operational constraints (rate limiting, dry-run, resumability), as a follow-up PR.