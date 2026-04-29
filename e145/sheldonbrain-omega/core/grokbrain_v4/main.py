#!/usr/bin/env python3
"""
Grokbrain v4.0 - Main Execution
Complete pipeline orchestration
"""

import sys
sys.path.insert(0, '.')

from grokbrain_v4 import *
from grokbrain_core import *
from xai_integration import *

def init_grokbrain():
    """Initialize Grokbrain environment"""
    logger.info("grokbrain_initialization_started")

    # Create directory structure
    dirs = [
        './exports', './clean_exports', './quarantine',
        './parsed/by_god', './parsed/code_spheres',
        './parsed/white_papers', './parsed/gamma_apps',
        './logs', './qdrant_db'
    ]

    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

    logger.info("directories_created", count=len(dirs))

def run_full_pipeline():
    """Run complete Grokbrain pipeline"""
    logger.info("==== GROKBRAIN V4.0 FULL PIPELINE ====")

    # Step 1: Quarantine filter
    logger.info("STEP_1: Quarantine filtering")
    clean_dir = quarantine_filter('./exports/')

    # Step 2: Create artifacts
    logger.info("STEP_2: Artifact creation")
    artifacts = artifact_creation(clean_dir)

    if not artifacts:
        logger.warning("no_artifacts_found")
        print("⚠️  No artifacts created. Check your export files.")
        return

    # Step 3: Auto-parse to 144-sphere grid
    logger.info("STEP_3: Auto-parsing to 144-sphere grid")
    parsed_grid, vectorstore = auto_parse_exports(artifacts, persist_path="./qdrant_db")

    # Step 4: Project detection
    logger.info("STEP_4: Project detection")
    proj_docs = [
        Document(page_content=a['input'] + ' ' + a['output'], metadata={'timestamp': a['timestamp']})
        for a in artifacts
    ]
    project_data = project_detector(proj_docs)

    # Step 5: Create aggregates
    logger.info("STEP_5: Creating aggregates")
    create_aggregates(project_data, parsed_grid)

    # Step 6: Phase 1.5 - God fork
    logger.info("STEP_6: Phase 1.5 god fork")
    phase_1_5_fork(parsed_grid)

    # Step 7: Generate code spheres
    logger.info("STEP_7: Code sphere generation")
    code_sphere_gen(parsed_grid)

    # Step 8: Generate white paper spheres
    logger.info("STEP_8: White paper sphere generation")
    white_paper_sphere_gen(parsed_grid)

    # Step 9: Generate gamma.app spheres
    logger.info("STEP_9: Gamma.app sphere generation")
    gamma_app_sphere_gen(parsed_grid)

    # Save final stats
    stats = {
        "total_artifacts": len(artifacts),
        "total_items_categorized": sum(len(sub) for cat in parsed_grid for sub in cat),
        "projects_detected": len([p for p, items in project_data.items() if items]),
        "spheres_populated": sum(1 for cat in parsed_grid for sub in cat if sub),
        "timestamp": datetime.datetime.now().isoformat()
    }

    with open('./logs/pipeline_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

    logger.info("pipeline_complete", **stats)

    print("\n" + "="*70)
    print("✅ GROKBRAIN V4.0 PIPELINE COMPLETE")
    print("="*70)
    print(f"📊 Total artifacts: {stats['total_artifacts']}")
    print(f"🌐 Items categorized: {stats['total_items_categorized']}")
    print(f"📁 Projects detected: {stats['projects_detected']}")
    print(f"🔮 Spheres populated: {stats['spheres_populated']}/144")
    print(f"\n📂 Outputs saved to ./parsed/")
    print(f"🗄️  Vector DB saved to ./qdrant_db/")
    print("="*70)

    return parsed_grid, vectorstore

def run_sample():
    """Run sample/test mode with minimal data"""
    logger.info("==== GROKBRAIN V4.0 SAMPLE MODE ====")

    # Create sample artifact
    sample_artifacts = [
        {
            "input": "Explain quantum entanglement for Mars terraforming H_SG simulations",
            "output": "Quantum entanglement in H_SG (Sheldonium) systems shows promise for Mars ecosuit viability curves. The binding energy calculations suggest 75% sovereign equity lock is achievable.",
            "timestamp": datetime.datetime.now().isoformat(),
            "source_file": "sample_quantum_mars.json"
        },
        {
            "input": "Design x-wing helicarrier squad deployment algorithm",
            "output": "X-wing helicarrier formations optimize for aerodynamic efficiency. Squad deployments use V-formation with 2-3 wingspan spacing for drag reduction while maintaining tactical flexibility.",
            "timestamp": datetime.datetime.now().isoformat(),
            "source_file": "sample_xwing.json"
        }
    ]

    with open('./artifacts.json', 'w') as f:
        json.dump(sample_artifacts, f, indent=2)

    # Run pipeline
    return run_full_pipeline()

def run_upload(parsed_grid=None):
    """Upload to xAI Collections"""
    logger.info("==== XAI COLLECTIONS UPLOAD ====")

    if parsed_grid is None:
        # Load from file
        try:
            with open('./parsed/parsed_grids.json', 'r') as f:
                parsed_grid = json.load(f)
        except FileNotFoundError:
            print("❌ No parsed grid found. Run full pipeline first.")
            return

    result = upload_to_xai(parsed_grid)

    print("\n" + "="*70)
    print("📤 XAI COLLECTIONS UPLOAD COMPLETE")
    print("="*70)
    print(f"📊 Total documents: {result.get('total', 0)}")
    print(f"✅ Uploaded: {result.get('uploaded', 0)}")
    print(f"❌ Errors: {result.get('errors', 0)}")
    print(f"📈 Success rate: {result.get('success_rate', 'N/A')}")
    print("="*70)

def run_query(query_str):
    """Query xAI Collections"""
    logger.info("==== XAI COLLECTIONS QUERY ====")

    result = query_xai_collections(query_str=query_str)

    print("\n" + "="*70)
    print(f"🔍 QUERY: {query_str}")
    print("="*70)
    print("\n📊 DIRECT RESULTS:")
    for idx, res in enumerate(result['direct_results'][:3], 1):
        print(f"\n{idx}. {res.get('result', 'N/A')[:200]}...")

    print("\n🤖 DUAL AI CONSENSUS:")
    consensus = result['dual_consensus']
    print(f"\nGrok: {consensus['grok_response'][:200]}...")
    print(f"\nGPT: {consensus['gpt_response'][:200]}...")
    print(f"\nReferee: {consensus['referee_synthesis'][:300]}...")
    print("="*70)

def run_demo():
    """Run interactive demo"""
    logger.info("==== GROKBRAIN V4.0 DEMO ====")

    # Load parsed grid
    try:
        with open('./parsed/parsed_grids.json', 'r') as f:
            parsed_grid = json.load(f)
    except FileNotFoundError:
        print("❌ No parsed grid found. Running sample mode...")
        parsed_grid, vectorstore = run_sample()

    # Initialize Qdrant client
    client = QdrantClient(path="./qdrant_db")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = LangchainQdrant(
        client=client,
        collection_name="grokbrain_grid",
        embeddings=embedding_model
    )

    # Initialize nexus
    r2d2 = R2D2(vectorstore)
    c3po = C3PO(parsed_grid)
    terraformer = MarsTerraformer(parsed_grid)

    print("\n" + "="*70)
    print("🤖 GROKBRAIN V4.0 NEXUS DEMO")
    print("="*70)

    # R2D2 demo
    print("\n📡 R2D2 Processing Streams:")
    results = r2d2.process_streams("quantum entanglement")
    print(f"   Found {len(results)} results for 'quantum entanglement'")

    # C3PO demo
    print("\n🌐 C3PO Filtering:")
    filtered = c3po.filter_input("mars")
    if isinstance(filtered, list):
        print(f"   Found {len(filtered)} items matching 'mars'")
    else:
        print(f"   {filtered}")

    # Mars Terraformer demo
    print("\n🔴 Mars Terraformer H_SG Simulation:")
    sim_result = terraformer.run_h_sg_sim()
    if isinstance(sim_result, dict):
        print(f"   Status: {sim_result['status']}")
        print(f"   Equity Locked: {sim_result['equity_locked']}")
        print(f"   H_SG Records: {sim_result['h_sg_records_found']}")
        print(f"   Viability: {sim_result['viability']}")
    else:
        print(f"   {sim_result}")

    print("="*70)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Grokbrain v4.0 - 144-Sphere Knowledge Organization")
    parser.add_argument('--sample', action='store_true', help="Run sample/test mode")
    parser.add_argument('--full', action='store_true', help="Run full pipeline")
    parser.add_argument('--gdrive', type=str, help="Download from Google Drive folder URL or ID")
    parser.add_argument('--gdrive-setup', action='store_true', help="Show Google Drive setup instructions")
    parser.add_argument('--upload-xai', action='store_true', help="Upload to xAI Collections")
    parser.add_argument('--query', type=str, help="Query xAI Collections")
    parser.add_argument('--demo', action='store_true', help="Run interactive demo")
    parser.add_argument('--gui', action='store_true', help="Launch Streamlit GUI")

    args = parser.parse_args()

    # Initialize
    init_grokbrain()

    if args.gdrive_setup:
        from gdrive_integration import setup_gdrive_instructions
        setup_gdrive_instructions()
    elif args.gdrive:
        from gdrive_integration import download_from_gdrive, get_gdrive_folder_id_from_url

        # Extract folder ID from URL if needed
        folder_id = get_gdrive_folder_id_from_url(args.gdrive)
        if not folder_id:
            folder_id = args.gdrive  # Assume it's already an ID

        print(f"\n📥 Downloading from Google Drive folder: {folder_id}")
        count = download_from_gdrive(folder_id, output_dir='./exports')

        if count > 0:
            print(f"\n✅ Downloaded {count} files to ./exports/")
            print("\n🚀 Running full pipeline...")
            run_full_pipeline()
        else:
            print("\n❌ No files downloaded. Check folder ID and credentials.")
    elif args.sample:
        run_sample()
    elif args.full:
        run_full_pipeline()
    elif args.upload_xai:
        run_upload()
    elif args.query:
        run_query(args.query)
    elif args.demo:
        run_demo()
    elif args.gui:
        print("🚀 Launching Streamlit GUI...")
        print("Run: streamlit run app.py")
    else:
        print("Grokbrain v4.0 - 144-Sphere Knowledge Organization")
        print("\nUsage:")
        print("  python main.py --sample                     # Run with sample data")
        print("  python main.py --full                       # Run full pipeline")
        print("  python main.py --gdrive <URL>               # Download from Google Drive + run")
        print("  python main.py --gdrive-setup               # Show Google Drive setup guide")
        print("  python main.py --upload-xai                 # Upload to xAI Collections")
        print("  python main.py --query 'text'               # Query xAI Collections")
        print("  python main.py --demo                       # Run interactive demo")
        print("  python main.py --gui                        # Launch GUI")
