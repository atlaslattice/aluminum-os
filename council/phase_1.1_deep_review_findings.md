# Deep File Review — metadata_validator.py + rag_api_gemini.py

## metadata_validator.py — Edge Cases Found

### Issue 1: auto_assign_sphere() truncates content at 2000 chars
- Line 86: `classify_input = f"{filename} {content[:2000]}"`
- For very large documents, the first 2000 chars may be boilerplate (imports, license headers)
- **Fix:** Sample from multiple positions: first 1000 + middle 500 + last 500

### Issue 2: normalize_sphere() silently passes through invalid codes
- Line 81: `return sphere` — if sphere is neither lattice nor legacy format, it's returned as-is
- This means a typo like "H02.S99" would pass normalization but fail validation at line 162
- **Assessment:** Acceptable — validation catches it downstream. No fix needed.

### Issue 3: novelty heuristic is word-count-only
- Lines 133-140: novelty = f(word_count) only
- No semantic analysis, no reference counting, no comparison to existing corpus
- **Assessment:** Known limitation, documented. Acceptable for Phase 1.1.

### Issue 4: category assignment is filename-only
- Lines 143-150: category = f(filename keywords)
- Doesn't analyze content, just filename stems
- **Assessment:** Known limitation. Acceptable for Phase 1.1.

### Issue 5: YAML frontmatter parsing has no size limit
- Line 68: `yaml.safe_load(parts[1].strip())` — no max size
- A malicious file with a huge YAML block could cause memory issues
- **Fix:** Add `if len(parts[1]) > 100000: raise ValueError("frontmatter too large")`

## rag_api_gemini.py — Edge Cases Found

### Issue 1: No input text length limit on /store
- Line 344-355: text is validated for emptiness but not max length
- Gemini embedding model has a token limit (~2048 tokens for text-embedding-004)
- Very long texts will either fail silently or get truncated by the model
- **Fix:** Add `if len(text) > 50000: return jsonify({"error": "Text too long (max 50000 chars)"}), 400`

### Issue 2: No rate limiting on any endpoint
- All endpoints are unprotected — no API key, no rate limit
- Cloud Run provides some protection but not application-level
- **Assessment:** Known limitation. Should add API key auth in Phase 2.

### Issue 3: RAGMemory() instantiated at module level (line 239)
- If Pinecone or Gemini credentials are missing, the import fails at module load
- This means even the /health endpoint won't work
- **Fix:** Wrap in try/except and return degraded health status

### Issue 4: /query filter_dict is passed directly to Pinecone
- Line 310: `filter_dict = data.get("filter")` — no validation
- Malformed filter dicts could cause Pinecone errors
- **Fix:** Add basic validation (must be dict, must contain valid operators)

### Issue 5: /classify with_context=True returns different schema than with_context=False
- Lines 416-429: Different response shapes depending on flag
- **Assessment:** Documented in docstring. Acceptable but should be noted in API docs.

### Issue 6: No CORS origin restriction
- Line 46: `CORS(app)` — allows all origins
- **Assessment:** Acceptable for internal service. Should restrict in production.

## Summary

| File | Critical Issues | Medium Issues | Low Issues |
|------|----------------|---------------|------------|
| metadata_validator.py | 0 | 1 (content sampling) | 3 |
| rag_api_gemini.py | 0 | 2 (text length, module-level init) | 4 |

No blocking issues. Two medium fixes recommended for the current PR.
