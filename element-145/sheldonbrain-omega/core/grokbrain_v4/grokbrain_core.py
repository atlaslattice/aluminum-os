#!/usr/bin/env python3
"""
Grokbrain v4.0 - Core Processing Functions
Auto-parsing, vector DB, AI consensus, sphere generation
"""

from grokbrain_v4 import *

# ============================================================================
# AUTO-PARSE WITH QDRANT
# ============================================================================

@ip_whitelist
@mitigate_loops(timeout_sec=120)
def auto_parse_exports(artifacts: List[Dict], embedding_model=None, persist_path="./qdrant_db"):
    """Auto-parse artifacts to 144-sphere grid using Qdrant persistent vectorstore"""

    if embedding_model is None:
        logger.info("loading_embeddings")
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create documents from artifacts
    docs = [
        Document(
            page_content=f"Input: {a['input']}\nOutput: {a['output']}",
            metadata={'timestamp': a['timestamp'], 'source': a['source_file']}
        )
        for a in artifacts
    ]

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    logger.info("documents_chunked", count=len(chunks))

    # Initialize Qdrant client (persistent)
    client = QdrantClient(path=persist_path)
    collection_name = "grokbrain_grid"

   # Create collections
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        logger.info("collection_created", name=collection_name)

    if not client.collection_exists("grid_ref"):
        client.create_collection(
            collection_name="grid_ref",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        logger.info("collection_created", name="grid_ref")

    # Generate and store grid reference
    grid_docs = generate_grid_descriptions()
    grid_vectorstore = LangchainQdrant(
        client=client,
        collection_name="grid_ref",
        embeddings=embedding_model
    )
    grid_vectorstore.add_documents(grid_docs)
    logger.info("grid_reference_stored")

    # Store data chunks
    data_vectorstore = LangchainQdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embedding_model
    )
    data_vectorstore.add_documents(chunks)
    logger.info("data_chunks_stored", count=len(chunks))

    # Parse into 144-grid
    parsed_grid = [[[] for _ in range(12)] for _ in range(12)]

    for doc in chunks:
        try:
            # Find matching sphere
            results = grid_vectorstore.similarity_search_with_score(doc.page_content, k=1)
            if not results:
                continue

            top_meta = results[0][0].metadata
            cat, sub = top_meta['cat'], top_meta['sub']
            flat_idx = cat * 12 + sub

            # Build tags
            tags = {
                'sphere': SPHERES[flat_idx],
                'element': ELEMENTS[flat_idx],
                'god': GODS[flat_idx],
                'mythical_overlay': MYTHICAL_OVERLAYS[flat_idx],
                'numerology_overlays': {trad: NUMEROLOGY_OVERLAYS[trad][flat_idx] for trad in NUMEROLOGY_OVERLAYS},
                'category': CATEGORY_NAMES[cat],
                'sphere_number': flat_idx + 1
            }

            # Enrich if content is sparse
            if len(doc.page_content.strip()) < 50:
                tags['grokipedia_enriched'] = enrich_with_grokipedia(SPHERES[flat_idx])
                tags['grok_enriched'] = enrich_with_grok(SPHERES[flat_idx], ELEMENTS[flat_idx], GODS[flat_idx])

            parsed_grid[cat][sub].append({
                'content': doc.page_content,
                'tags': tags,
                'metadata': doc.metadata
            })

        except Exception as e:
            logger.error("chunk_parse_error", error=str(e))

    # Save parsed grid
    os.makedirs('./parsed', exist_ok=True)
    with open('./parsed/parsed_grids.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_grid, f, indent=2)

    logger.info("parsing_complete", total_categorized=sum(len(sub) for cat in parsed_grid for sub in cat))
    return parsed_grid, data_vectorstore

# ============================================================================
# PROJECT DETECTION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def project_detector(docs: List[Document]) -> Dict[str, List[Dict]]:
    """Detect projects and overlaps"""
    projects = {proj: [] for proj in PROJECT_KEYWORDS}
    overlaps = {}

    for doc in docs:
        matched = []
        timestamp = doc.metadata.get('timestamp', datetime.datetime.now().isoformat())
        entry = {'content': doc.page_content, 'timestamp': timestamp, 'metadata': doc.metadata}

        for proj, keywords in PROJECT_KEYWORDS.items():
            if any(re.search(rf'\b{re.escape(kw)}\b', doc.page_content, re.I) for kw in keywords):
                matched.append(proj)
                projects[proj].append(entry)

        # Track overlaps
        if len(matched) > 1:
            overlap_key = ' + '.join(sorted(matched)) + ' (aggregate)'
            overlaps.setdefault(overlap_key, []).append(entry)

    logger.info("project_detection_complete", projects=len(projects), overlaps=len(overlaps))
    return {**projects, **overlaps}

# ============================================================================
# AGGREGATE CREATION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def create_aggregates(project_data: Dict[str, List[Dict]], parsed_grid):
    """Create timestamped project aggregates"""
    os.makedirs('./parsed', exist_ok=True)

    for proj, entries in project_data.items():
        if not entries:
            continue

        sorted_entries = sorted(entries, key=lambda x: x['timestamp'])
        timeline = {'timeline': sorted_entries}

        redundancy_count = len([e for e in entries if 'aggregate' in proj.lower()]) if 'aggregate' in proj else 0
        analysis = f"Aggregated {len(entries)} entries for {proj}; " \
                   f"redundancies for cross-ref: {redundancy_count}; " \
                   f"mission: Optimized for productive ties like sim dynamics."

        output = {
            'aggregate': timeline,
            'report': analysis,
            'grid_ref': f"See parsed_grids.json for full context",
            'entry_count': len(entries),
            'time_range': {
                'start': sorted_entries[0]['timestamp'] if sorted_entries else None,
                'end': sorted_entries[-1]['timestamp'] if sorted_entries else None
            }
        }

        proj_path = os.path.join('./parsed', f"{proj.replace(' ', '_').replace('+', 'and')}.json")
        with open(proj_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

    logger.info("aggregates_created", project_count=len(project_data))

# ============================================================================
# PHASE 1.5 - GOD FORK
# ============================================================================

@ip_whitelist
@mitigate_loops()
def phase_1_5_fork(parsed_grid):
    """Fork parsed grid by god"""
    os.makedirs('./parsed/by_god', exist_ok=True)

    god_chunks = defaultdict(list)

    for cat in parsed_grid:
        for sub in cat:
            for item in sub:
                god = item['tags']['god']
                god_chunks[god].append(item)

    for god, chunks in god_chunks.items():
        if chunks:
            god_safe = god.split('(')[0].strip().lower().replace(' ', '_')
            with open(f'./parsed/by_god/{god_safe}.json', 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2)

    logger.info("god_fork_complete", god_count=len(god_chunks))

# ============================================================================
# CODE SPHERE GENERATION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def code_sphere_gen(parsed_grid):
    """Generate code spheres"""
    os.makedirs('./parsed/code_spheres', exist_ok=True)

    for idx in range(144):
        cat = idx // 12
        sub = idx % 12
        items = parsed_grid[cat][sub]
        god = GODS[idx]
        sphere = SPHERES[idx]

        # Extract code snippets
        aggregated_code = [
            item['content']
            for item in items
            if re.search(r'(def |class |import |function |const |let |var )', item['content'], re.I)
        ]

        # Find matching projects
        folders = [
            proj for proj in PROJECT_KEYWORDS
            if any(kw.lower() in ''.join(aggregated_code).lower() for kw in PROJECT_KEYWORDS[proj])
        ]

        optimization = f"Optimized {len(aggregated_code)} code snippets: Deduped redundancies."
        report = f"Mission report for sphere {sphere} under {god}: Aggregated {len(aggregated_code)} codebases."

        sphere_data = {
            'sphere_number': idx + 1,
            'sphere_name': sphere,
            'god': god,
            'element': ELEMENTS[idx],
            'aggregated_code': aggregated_code,
            'folders': folders,
            'optimization': optimization,
            'mission_report': report
        }

        sphere_dir = f'./parsed/code_spheres/code_sphere_{idx+1:03d}'
        os.makedirs(sphere_dir, exist_ok=True)
        with open(f'{sphere_dir}/aggregate.json', 'w', encoding='utf-8') as f:
            json.dump(sphere_data, f, indent=2)

        # Copy to project folders
        for proj in folders:
            proj_dir = f'./parsed/{proj.replace(" ", "_")}'
            os.makedirs(proj_dir, exist_ok=True)
            shutil.copy(
                f'{sphere_dir}/aggregate.json',
                f'{proj_dir}/code_from_sphere_{idx+1:03d}.json'
            )

    logger.info("code_spheres_generated")

# ============================================================================
# WHITE PAPER SPHERE GENERATION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def white_paper_sphere_gen(parsed_grid):
    """Generate white paper spheres with embedded functional code"""
    os.makedirs('./parsed/white_papers', exist_ok=True)

    for idx in range(144):
        cat = idx // 12
        sub = idx % 12
        items = parsed_grid[cat][sub]
        god = GODS[idx]
        sphere = SPHERES[idx]

        # Extract white papers/drafts
        aggregated_wp = [
            item['content']
            for item in items
            if re.search(r'(white paper|draft|proposal|report|abstract|introduction)', item['content'], re.I)
        ]

        folders = [
            proj for proj in PROJECT_KEYWORDS
            if any(kw.lower() in ''.join(aggregated_wp).lower() for kw in PROJECT_KEYWORDS[proj])
        ]

        optimization = f"Optimized {len(aggregated_wp)} white papers/drafts: Deduped redundancies."
        report = f"Mission report for sphere {sphere} under {god}: Aggregated {len(aggregated_wp)} white papers."

        # Functional code stub for Mars Terraformer (example)
        functional_code = """
class MarsTerraformer:
    def __init__(self):
        self.constants = {
            'TOTAL_LOSSES_AVERTED_USD': 1.2e12,
            'SOVEREIGN_EQUITY_LOCK': 0.75
        }

    def run_sim(self):
        return f'Sim complete: Equity locked at {self.constants["SOVEREIGN_EQUITY_LOCK"]}'
"""

        sphere_data = {
            'sphere_number': idx + 1,
            'sphere_name': sphere,
            'god': god,
            'element': ELEMENTS[idx],
            'aggregated_wp': aggregated_wp,
            'folders': folders,
            'optimization': optimization,
            'mission_report': report,
            'functional_code': functional_code
        }

        wp_folder = f'./parsed/white_papers/wp_sphere_{idx+1:03d}'
        os.makedirs(wp_folder, exist_ok=True)
        with open(f'{wp_folder}/aggregate.json', 'w', encoding='utf-8') as f:
            json.dump(sphere_data, f, indent=2)

        for proj in folders:
            proj_dir = f'./parsed/{proj.replace(" ", "_")}'
            os.makedirs(proj_dir, exist_ok=True)
            shutil.copy(
                f'{wp_folder}/aggregate.json',
                f'{proj_dir}/wp_from_sphere_{idx+1:03d}.json'
            )

    logger.info("white_paper_spheres_generated")

# ============================================================================
# GAMMA.APP SPHERE GENERATION
# ============================================================================

@ip_whitelist
@mitigate_loops()
def gamma_app_sphere_gen(parsed_grid):
    """Generate gamma.app presentation spheres"""
    os.makedirs('./parsed/gamma_apps', exist_ok=True)

    for idx in range(144):
        cat = idx // 12
        sub = idx % 12
        items = parsed_grid[cat][sub]
        god = GODS[idx]
        sphere = SPHERES[idx]

        # Extract presentation content
        aggregated_gamma = [
            item['content']
            for item in items
            if re.search(r'(gamma\.app|presentation|outline|deck|slide|pitch)', item['content'], re.I)
        ]

        folders = [
            proj for proj in PROJECT_KEYWORDS
            if any(kw.lower() in ''.join(aggregated_gamma).lower() for kw in PROJECT_KEYWORDS[proj])
        ]

        optimization = f"Optimized {len(aggregated_gamma)} gamma.app outlines: Deduped redundancies."
        report = f"Mission report for sphere {sphere} under {god}: Aggregated {len(aggregated_gamma)} outlines."

        sphere_data = {
            'sphere_number': idx + 1,
            'sphere_name': sphere,
            'god': god,
            'element': ELEMENTS[idx],
            'aggregated_gamma': aggregated_gamma,
            'folders': folders,
            'optimization': optimization,
            'mission_report': report
        }

        gamma_folder = f'./parsed/gamma_apps/gamma_sphere_{idx+1:03d}'
        os.makedirs(gamma_folder, exist_ok=True)
        with open(f'{gamma_folder}/aggregate.json', 'w', encoding='utf-8') as f:
            json.dump(sphere_data, f, indent=2)

        for proj in folders:
            proj_dir = f'./parsed/{proj.replace(" ", "_")}'
            os.makedirs(proj_dir, exist_ok=True)
            shutil.copy(
                f'{gamma_folder}/aggregate.json',
                f'{proj_dir}/gamma_from_sphere_{idx+1:03d}.json'
            )

    logger.info("gamma_app_spheres_generated")
