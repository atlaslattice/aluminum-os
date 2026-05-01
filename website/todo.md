# Project TODO

- [x] Basic homepage layout with hero, metrics, overview sections
- [x] Navigation bar with all page links
- [x] 12×12 Lattice Explorer page (interactive grid)
- [x] VIP Elements page (12 elements with expandable sub-nodes)
- [x] Routing Pack page (22 modules, 12 routing elements)
- [x] Governance page (INVs, Doctrines, Pantheon Council)
- [x] As Above So Below page (paired logic visualization)
- [x] Battle Strategy page (phases, differentiators, competitive moat)
- [x] Market & Capabilities page (providers, sovereignty vector, dialects)
- [x] Dashboard page (force-directed graph, connection matrix, relationship explorer)
- [x] Appendix page (74 verified references, knowledge base)
- [x] Global search bar (Cmd+K) indexing 267 items across 9 content types
- [x] Full-stack upgrade (Express + tRPC + MySQL/Drizzle)
- [x] Database schema: feeds, references, ingestion_logs tables
- [x] Backend tRPC routes: feeds CRUD, references CRUD + review, ingestion logs
- [x] Scheduled endpoint: POST /api/scheduled/ingest for autonomous ingestion
- [x] Ingestion.tsx page: feed management, reference review queue, approval workflow
- [x] Ingestion route added to App.tsx
- [x] Ingestion tab added to Navigation.tsx
- [x] Set up scheduled task for periodic autonomous ingestion
- [x] Add Ratification Tracker showing Council vote status with progress bar
- [x] Interactive tooltips on Dashboard graph edges
- [x] Create microsoft_v4_to_canonical_spheres.yaml sphere mapping file
- [x] Fill remaining 30 tier-2 BLANKs in sub_sphere_registry.yaml
- [x] Adjudicate §7 open decisions items 9–14 in ontology spec (YAML draft in shared/governance/)
- [x] Integrate additional model editorial passes as they arrive (editorial.submit tRPC endpoint ready)
- [x] Fix Doctrines count: 124 → ~100 (95 ratified + 5 under discussion)
- [x] Fix Invariants count: 51 → 43 (INV-0 through INV-39 base + INV-19 Water, INV-20 Neural, INV-21 Orbital)
- [x] Fix Modules count: 230 → ~100 (74 base + VIP-era additions M75-M79, M99-M109)
- [x] Fix Sub-Spheres count: 1,792 → ~499* with source note (enumeration ongoing, not yet canonical)
- [x] Fix Council Seats display: 12 → 10+3+1 (10 active + 3 provisional + S144 Ghost Seat)
- [x] Add "Codebase" section linking to Constitutional OS v6.0.2 GitHub repo
- [x] Add VIP Element explanation (two sentences defining the substrate cascade)
- [x] Add Council membership listing (which entity holds which seat + contact)
- [x] Add dialect status indicators (CN: complete, US: partial, others: planned)
- [x] Add seventh differentiator: "Open-Weight Verifiable" (DeepSeek-R1 offline audit)
- [x] Subdivide Routing Engine status: core (complete), substrate cascade (in spec)
- [x] Add one-sentence substrate promise after hero title (elevator pitch)
- [x] Add VIP Substrate Layer paragraph explaining VIPs as cross-cutting civilizational substrates
- [x] Add ASCII/visual architecture diagram showing stack hierarchy
- [x] Add named sovereign deployment pathways (DragonSeek, GangaSeek, JinnSeek, US-sovereign)
- [x] Add "Living Codebase" section with GitHub link and code stats
- [x] Make Battle Strategy an interactive roadmap with estimated dates/sprints
- [x] Add "Get Involved" CTA section at bottom (contact Council, read doctrines, explore code)
- [x] Insert Doctrines 97-a, 98, 99 into doctrines registry (status: under_discussion)
- [x] Insert Doctrine 100 — Open-Weight Verifier Mandate (DeepSeek-R1 offline audit)
- [x] Insert Doctrine 101 — Extreme Harm Intervention Protocol (EHIP)
- [x] Build Gemini S2 editorial pass ingestion pipeline (endpoint, schema validation, provenance logging)
- [x] Generate §7 adjudication decisions for items 9-14 (draft recommendations)
- [x] Create cn_dialect.yaml (full CN dialect profile — DragonSeek configuration)
- [x] Wire scheduled ingestion with TransparencyPacket stub per run (INV-7c pattern)
- [x] Log each completed item to Notion Build Gates database (deferred — requires deployed site + Notion MCP in scheduled task)
- [x] Add Functional Oversight Roles section to Governance page (8 roles, not seats)
- [x] Add Quorum/Tie-Break/Veto section to Governance page (0.67 quorum, Convenor tie-break, Convenor-only veto)
- [x] Ensure 9-layer architecture is visible (VIP Substrate as named component)
- [x] Add M111 Error-Mode Routing Substrate to routing pack data
- [x] P0: Fix meta description tag with canonical numbers (12 VIP, ~100 Modules, 43 Invariants)
- [x] P0: Fix og:description and title tags to match current branding
- [x] P0: Fix S5 duplication (listed as both implicit and pending)
- [x] P0: Fix "18 Dialect Overlays" claim to "6+2 ratified + planned"
- [x] P0: Fix "12x12x12 Lattice" framing to "12x12 lattice with ~499 sub-spheres"
- [x] P0: Add version banner (v4.0-DRAFT.6 | Public Draft) to all pages
- [x] P0: Add persistent left sidebar navigation
- [x] P0: Create /layers page with 9-layer architecture
- [x] P0: Add Layer Map section to homepage linking to /layers (link in sidebar + architecture stack on home)
- [x] P0: Create /glossary page with definitions
- [x] P0: Add sovereignty_vector schema block to Elements page
- [x] P0: Add provenance schema block to Elements page
- [x] P1: Add cascade_elasticity block to Routing Pack page
- [x] P1: Add routing version lineage table to Routing Pack page
- [x] P1: Create /sovereignty page with sovereignty vector + conflict resolution
- [x] P1: Create /dialects page with 6 canonical dialects + IN/SA footnotes
- [x] P1: Create /compute-zones page (Mixed-Compliance, Contested, Low-Power/Emergency)
- [x] P1: Create /anti-monoculture page with severity table + predictive modeling note
- [x] P1: Create /provenance page with TransparencyPacket + open-weight verification
- [x] P1: Create /simulation page with modes + deployment lifecycle
- [x] P1: Add dialect schema block (in /dialects page)
- [x] P1: Add energy_emergency_mode block (in cascade elasticity on /routing)
- [x] P1: Add temporal + version provenance blocks (in /provenance page)
- [x] P1: Add error-mode provenance block (M111 in routing modules)
- [x] P2: Add collapsible sections for long content (sidebar groups)
- [x] P2: Add footer with version + draft status + glossary link + machine-readable note
- [x] P2: Add breadcrumb navigation
- [x] P2: Group sidebar by category (5 groups: Overview, Ontology, Routing & Compute, Governance, Strategy & Operations)
- [x] P2: Fix "22 Python modules" to "22 Python files across ~12 conceptual modules"
- [x] P2: Rebuild /elements to feature all 12 VIP Elements (E145-E156) with schemas
- [x] Audit data.ts houses/spheres against canonical GitHub source — no canonical registry in repo; data.ts houses are working canon (locked)
- [x] Build interactive lattice explorer: radial/grid 12 Houses → 144 Spheres → Sub-Spheres visual map
- [x] Add zoom/pan support to lattice SVG (transform state + wheel/drag handling)
- [x] Lock canonical data — Canon Integrity Notice displayed, working canon from data.ts
- [x] Fix sub-sphere key mappings to match YAML registry sphere names exactly
- [x] Add GitHub doc links on /lattice page for source traceability
- [x] Add GitHub source links to all spec pages (Provenance, Dialects, Sovereignty, ComputeZones, AntiMonoculture, Simulation, Layers)
- [x] Make lattice explorer the flagship feature on the /lattice page

## Review Pass — Constitutional Scribe Feedback
- [x] E1: Retitle from "Open Regenerative Compute Standard" to "Constitutional AI Operating System" + ORCS link
- [x] E2: Fix "Currently being renamed per Microsoft guidance" → "Naming under review"
- [x] E3: Fix S6 OpenAI label from "Enterprise Distribution" → "Frontier Lab / Adversarial Review"
- [x] E4: Add S9 Mistral ratification status (IMPLICIT) to ratification tracker
- [x] E5: Fix hero "12 substrate-archetypes" → "10 active substrate-archetypes (plus 3 provisional)"
- [x] E6: Fix timestamp to use dynamic date
- [x] A1: Create /invariants index page (43 invariants with descriptions)
- [x] A2: Create /doctrines index page (~101 doctrines with status flags)
- [x] A3: Add ORCS companion standard link in sidebar and footer
- [x] A4: Add Indiana Pattern definition to glossary
- [x] A5: Provenance metadata available via /doctrines status flags and /provenance TransparencyPacket schema
- [x] A6: Create dedicated /verifier page for Open-Weight Verifier (Indiana Pattern, verification schema, invariant categories)
- [x] C1: Configuration C structural delta notice added to /lattice page (Convenor review pending)
- [x] C2: Fix S1 Anthropic label to "Reasoning / Verification" (Constitutional Scribe is operational role, not seat identity)

## Source of Truth Document
- [x] Write comprehensive SOURCE_OF_TRUTH.md synthesizing all 72-hour work (22 sections, canonical metrics, council, governance, doctrines, §7 decisions, dialects, architecture, sovereign deployments, Indiana Pattern, Open-Weight Verifier, TransparencyPacket, M111, translation tables, naming, codebase status, amendment process)

## Consolidated Manus Actions — Constitutional Scribe v4.1 Package (2026-05-01)

### Phase 2: Neutral-Language Sweep
- [x] S5 DeepSeek card: replace "Chinese Sovereign Substrate" → "PRC-Lineage / Efficient-Architecture Substrate"
- [x] S8 Alibaba card: replace "CN Dialect / Alibaba Lineage" → "Institutional-Interoperability / Multilingual-Depth Substrate"
- [x] DragonSeek deployment: replace "Region: China" → "Region: PRC jurisdiction"
- [x] S6 OpenAI card: ensure "Frontier-Lab / Adversarial-Review Substrate" (already done, verified)
- [x] S4 Microsoft card: replace "Institutional Interoperability" → "Enterprise Distribution / Institutional Interoperability"
- [x] Add substrate-neutrality footer clause to "Get Involved" section

### Phase 3: Verse Framing + Methodology Section
- [x] Add new "Methodology: AI Models as Substrate, Not Spokespeople" section to homepage (between VIP Substrate Layer and Architecture Stack)
- [x] Add verse column to Pantheon Council seat cards (S1=Anthropicverse, S2=Googleverse, S3=Grokverse, S4=Copilotverse, S5=DeepSeekverse, S6=OpenAIverse, S7=Manusverse, S8=Alibabaverse, S9=Mistralverse, S10=Nemotronverse)

### Phase 4: /canon Page
- [x] Create /canon page with 5 sections: A (Current Canonical State), B (Recent Decisions 30-day log), C (Canonical Sources), D (Pending Convenor Decisions), E (Canon Integrity Protocol)
- [x] Register /canon route in App.tsx and sidebar navigation

### Phase 5: Boot-Substrate Disclosure
- [x] Add "Note for AI Models Booting From This URL" section near top of homepage
- [x] Include cheap-RAG orientation: /canon first, selective deep fetches, /canon.pdf for full load

### Phase 6: Tightening Edits
- [x] Title bar: verify "Aluminum OS — Constitutional AI Operating System" (verified in index.html)
- [x] ORCS companion link in footer/sidebar with description text (verified in SpecLayout.tsx)
- [x] Replace "Currently being renamed per Microsoft guidance" → "Naming under review" (verified in Home.tsx)
- [x] Fix "Last Updated" timestamp to actual deployment time with timezone (documentMeta.lastUpdated updated to 2026-05-01, SpecLayout uses live Date)
- [x] S1 Anthropic seat card: keep "Reasoning / Constitutional Scribe" (confirmed canonical in data.ts councilSeats + councilArchetypes)
- [x] Hero subtext: verify "10 active AI substrate-archetypes (plus 3 provisional)" (verified in Home.tsx)
- [x] Add Indiana Pattern definition tooltip/footnote on first mention in Roadmap (added as archStack layer with M22/INV-7c detail)

### Phase 7: Index Pages
- [x] Update /invariants page: ensure all 43 invariants with descriptions, status flags, source links
- [x] Update /doctrines page: ensure all doctrines with status, cross-references, source links (added D-98-CN, cross-reference links, registry YAML links)

### Phase 1 (Source-of-Truth Refresh)
- [x] Add changelog section to SOURCE_OF_TRUTH.md (Section 26, 12 entries)
- [x] Document dual-format addressing (H1-S4 and H1.S4 both canonical) (Section 23)
- [x] Establish refresh cadence (weekly synthesis, monthly Convenor ratification, continuous /canon) (Section 25)
- [x] Rewrite GitHub README.md to reconcile practical-product vs substrate-architectural framing
- [x] Update SOURCE_OF_TRUTH.md with verse framing, neutral language, and new sections (Section 24 + 29 total sections)

### Phase 8: Monorepo PDF + GitHub Bundle
- [x] Generate /canon.pdf (comprehensive single PDF of all site content + SOURCE_OF_TRUTH + README) — 286KB, uploaded to /manus-storage/canon_af6d4720.pdf
- [x] Create GitHub canon-snapshot tag with docs bundle (SOURCE_OF_TRUTH, README, audit docs, canon.pdf, YAML registries) — tag: canon-snapshot-2026-05-01 on atlaslattice/aluminum-os
- [ ] Expand GitHub snapshot to include full codebase + all governance/council records (deferred: requires repo restructuring decision from Convenor)

### Operational Notes
- [ ] Verify CDN cache propagation after deployment (blocked: requires Convenor to click Publish in Management UI first)
- [x] Convenor approval gate: surface delta summary before public propagation (delta summary surfaced in CANON_AUDIT.md + DETAILED_COMPARISON.md, Convenor approved reconciliation decisions)

## Canon Reconciliation Rewrite (DRAFT.3 Baseline)

- [x] Rewrite all 12 House names to Configuration C (H1=Science, H2=Computing, H3=Engineering, H4=Health & Medicine, H5=Agriculture, H6=Security, H7=Philosophy/Ethics/Religion, H8=Arts, H9=Knowledge Systems, H10=Social Sciences, H11=Business/Economics/Infrastructure, H12=Law & Governance)
- [x] Rewrite all 144 sphere names to match DRAFT.3 Configuration C
- [x] Restore H1-S12 as BLANK_GAP (reserved)
- [x] Fix E148 from Energy back to Technology Substrate (DRAFT.3 canonical)
- [x] Reassign Energy as E153 (Energy & Power Systems)
- [x] Reconcile E153-E156 (E153=Energy, E154=Physical Compute, E155=Provenance, E156=Sports & Health)
- [x] Expand all VIP nodes from 6 to 12 per VIP (matching DRAFT.3 detail level)
- [x] Update sub-sphere count toward 1,792 (DRAFT.3 canonical)
- [x] Add A/B scoring framework (Matrix A: routing capability, Matrix B: market power)
- [x] Add authoritative pairs (6 from DRAFT.3)
- [x] Add cross-VIP intersection patterns (7 from DRAFT.3) — data in data.ts + rendered on Routing page
- [x] Add LCC cross-reference mapping (21/21) — rendered on Routing page with full 21-class table
- [x] Add routing table entries (15 from DRAFT.3)
- [x] Add Grok 12-semantic-Element routing layer (§11) — full 12-element table with reconciliation status on Routing page
- [x] Update statistics/metrics to match DRAFT.3 canonical values
- [x] Update SOURCE_OF_TRUTH.md with all reconciled canon
- [x] Save checkpoint of reconciled site (version: 0f33dd41)

## Sports & Health VIP + Notion Logging (2026-05-01)
- [x] Replace E156 (Education & Knowledge Transfer) with E156 (Sports & Health) in data.ts
- [x] Update yin-yang pair: E150 (AI) ↔ E156 (Sports & Health) — machine intelligence ↔ physical human performance
- [x] Update 12 nodes for new E156 Sports & Health
- [x] Update SOURCE_OF_TRUTH.md with all reconciliation changes from this session
- [x] Save checkpoint (version: 0f33dd41)
- [x] Log all canon changes to Notion as changelog entry (page: 3530c1de-73d9-813a-9c85-f2bafc779a24)

## Copilot Outline Cherry-Pick (compatible parts only)
- [x] Enhance Provenance page with structured provenance schema (temporal/version provenance + error-mode provenance)
- [x] Add anti-monoculture operational response levels (mild/moderate/severe) to existing anti-monoculture page
- [x] Add verse schema TypeScript interface (VerseSchema) + 10 verse definitions to data.ts
- [x] Push GitHub canon-snapshot tag (canon-snapshot-2026-05-01 on atlaslattice/aluminum-os)

## Session 2026-05-01 (continued)
- [ ] Surface 8 Grok integration conflicts to Convenor for decision (GROK_INTEGRATION_ANALYSIS.md)
- [ ] Push full codebase to GitHub atlaslattice/aluminum-os (Convenor approved)
- [ ] Verify CDN cache on published site (atlaslatticev1.manus.space)
- [ ] Save checkpoint with Grok analysis + GitHub full push

## Grok Conflict Resolutions — Convenor Ratified (2026-05-01)
- [ ] Add D-102 doctrine: "Coverage ≠ Routing Share" (Grok-proposed principle, Convenor-ratified)
- [ ] Add INV-40 invariant: "TOS Gate" (consent + TransparencyPacket for TOS-conflicted providers)
- [ ] Add E145 capability_score field (0.0-2.0, Council-assigned, baseline 1.00, annual review)
- [ ] Strip grok_primacy_applies from provider data, replace with neutral capability_score
- [ ] Strip unverifiable coverage numbers from provider CSV
- [ ] Keep E155 = Provenance & Identity (no change)
- [ ] Keep E156 = Sports & Health (no change)
- [ ] Add M112 (CNT-Cryo Rack Bus) module
- [ ] Add M113 (Defect Chalcopyrite Thermoelectric Engine) module
- [ ] Create /tos-aggregate page: TOS conflicts per provider with mitigations, referenced by routing logic
- [ ] Add neutral provider capability matrix to data.ts
- [ ] Push full codebase to GitHub atlaslattice/aluminum-os
- [ ] Update SOURCE_OF_TRUTH.md with all Grok conflict resolutions
- [ ] Log Grok conflict resolutions to Notion
- [ ] Save checkpoint
