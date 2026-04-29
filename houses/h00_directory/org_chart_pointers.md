# Org Chart Pointers — Per-Entity 144-Sphere Coverage Maps

**Version:** 0.2.0
**Generated:** 2026-04-29
**Purpose:** Cross-reference index for all per-entity org chart / capability self-maps used to build `capability_matrix.yaml`

---

## Primary Self-Maps (Per-Sphere Scoring)

| Seat | Entity | Notion Page ID | Title | Data Quality | Self-Assessed Coverage |
|------|--------|----------------|-------|--------------|----------------------|
| S1 | Anthropic | `34a0c1de-73d9-8124-aeb4-ea2e835a73a6` | Anthropic 144-Sphere Coverage Map | **HIGH** | 27% |
| S2 | Alphabet | `34a0c1de-73d9-81eb-84f1-e392b4004761` | Alphabet 144-Sphere Self-Map (Gemini) | **HIGH** | 47% |
| S3 | Muskverse | `34a0c1de-73d9-81f4-8fab-ec917d8b6d8a` | Muskverse 144-Sphere Self-Map (Grok) | MEDIUM | 39% |
| S4 | Microsoft | `3500c1de-73d9-81aa-928a-df22d4b14cde` | Microsoft S4 Cross-Validation Routing | MEDIUM | 95.8% |
| S5 | DeepSeek | `3500c1de-73d9-8130-9115-d6aa03d82950` | DeepSeek Vendor Suite v1.0 (Corrected) | MEDIUM | ~15% |
| — | Amazon | `34a0c1de-73d9-81c8-a866-c799bdab0de0` | Amazon 144-Sphere Self-Map (Alexa) | LOW | 40-50% |

## Inferred Maps (No Dedicated Self-Map)

| Seat | Entity | Source | Data Quality | Notes |
|------|--------|--------|--------------|-------|
| S6 | OpenAI | Build Plan v3.14 vendor suite + Federation v1.1 | LOW | Scores inferred from GPT-4/DALL-E/Whisper/Codex product portfolio |
| S7 | Manus | Build Plan v3.14 + Federation v1.1 | LOW | Narrow substrate — orchestration layer only |
| S8 | Notion | Build Plan v3.14 + Federation v1.1 | LOW | Narrow substrate — workspace/knowledge management only |
| S10 | Qwen3/Alibaba | ORC-015 Trinity + Federation v1.1 | LOW | Scores inferred from Alibaba Cloud + Qwen model portfolio |

## Synthesis Documents

| Document | Notion Page ID | Purpose |
|----------|----------------|---------|
| Four-Company Complementarity Matrix | `34a0c1de-73d9-819e-a51f-dcc0a608e7a2` | April 22 synthesis of S1+S2+S3+Amazon |
| Federation Integration v1.1 | `3500c1de-73d9-81f0-85f0-f427e9c4de5e` | All 9 seats x 144 spheres + E145 CEO Collective |
| Provisional 144-Sphere Routing Table | `34c0c1de-73d9-81b1-bc83-cbaf43cbc76e` | Per-sphere primary/secondary routing |
| Sheldonbrain Weighting Methodology v1.0 | `34b0c1de-73d9-81bb-a41e-f31362a1f739` | Scoring methodology and co-primary definitions |
| Anthropic + Affiliates E145 Map v1.0 | `3500c1de-73d9-8113-ae71-e5875c66ac48` | Dario as E145 CEO mapping |

## Methodology Notes

### Data Quality Tiers

- **HIGH:** Per-sphere 0.0-1.0 scoring with explicit methodology, strict epistemic criterion (institutional operational depth, not AI model conversational range)
- **MEDIUM:** House-level percentages or narrative descriptions requiring canonical normalization; or vendor suite format without per-sphere granularity
- **LOW:** No dedicated self-map; scores inferred from product portfolio and public information

### Known Biases

1. **Alexa (Amazon) overclaim:** Claude's methodology notes flag Amazon self-assessment as "least rigorous of the four self-maps" with "overclaim-by-conflation" (distribution ≠ operational depth). Scores normalized down in capability_matrix v0.2.0.
2. **Microsoft 95.8% claim:** Pending full D-85 cross-validation. The claim counts "coverage" broadly including Azure marketplace partners, not just proprietary depth.
3. **Muskverse custom groupings:** Grok used non-canonical house groupings requiring manual remapping to canonical 12-house structure.
4. **Cross-model reference propagation:** Gemini referenced Alexa's unverified claims (e.g., 576.7 Hz). Flagged in Epistemic Labeling Standard.

### Acquisition Updates Applied

| Acquisition | Seat | Impact | Sphere(s) Affected |
|-------------|------|--------|---------------------|
| Wiz (2025) | S2 Alphabet | +0.2 | H02/Cryptography |
| Activision Blizzard (2023) | S4 Microsoft | +0.2 | H05/Film, Games |
| One Medical (2023) | Amazon | +0.1 | H09/Public Health |
| MGM (2022) | Amazon | +0.2 | H05/Film |

---

## Usage

This file is the canonical cross-reference for `capability_matrix.yaml`. When updating scores:

1. Fetch the source Notion page using the page ID
2. Extract per-sphere scores (or normalize from narrative)
3. Update the corresponding seat column in `toolchain/generate_capability_matrix_v2.py`
4. Re-run the generation script
5. Commit with message referencing the source page ID
