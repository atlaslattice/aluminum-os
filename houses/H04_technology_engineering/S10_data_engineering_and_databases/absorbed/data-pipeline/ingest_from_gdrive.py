#!/usr/bin/env python3
"""
Ingest content from Google Drive

Fetches files from specified folder and adds to staging for processing
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

from connectors import GoogleDriveConnector
from ingestion.ingestion_pipeline import StagingLayer
from config import get_ontology

load_dotenv()


def main():
    """Main CLI"""
    parser = argparse.ArgumentParser(
        description="Ingest content from Google Drive"
    )
    parser.add_argument(
        "--folder-id",
        default=os.getenv("GDRIVE_FOLDER_ID"),
        help="Google Drive folder ID"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=50,
        help="Maximum files to fetch"
    )
    parser.add_argument(
        "--modified-after",
        help="Only fetch files modified after this time (ISO format)"
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Auto-approve all fetched files"
    )
    parser.add_argument(
        "--staging-dir",
        default="./staging/gdrive",
        help="Staging directory"
    )
    parser.add_argument(
        "--credentials",
        default="credentials.json",
        help="OAuth2 credentials file"
    )

    args = parser.parse_args()

    if not args.folder_id:
        print("❌ Error: --folder-id required (or set GDRIVE_FOLDER_ID in .env)")
        sys.exit(1)

    print("=" * 70)
    print("GOOGLE DRIVE INGESTION")
    print("=" * 70)
    print()
    print(f"📁 Folder ID: {args.folder_id}")
    print(f"📦 Max Files: {args.max_files}")
    print(f"📂 Staging: {args.staging_dir}")
    if args.modified_after:
        print(f"⏰ Modified After: {args.modified_after}")
    print()

    try:
        # Initialize connector
        print("🔐 Authenticating with Google Drive...")
        connector = GoogleDriveConnector(credentials_file=args.credentials)
        print("✅ Authenticated")
        print()

        # Initialize staging
        staging = StagingLayer(staging_dir=args.staging_dir)

        # Initialize ontology
        ontology = get_ontology()

        # Fetch files
        print(f"📥 Fetching files from folder...")
        files = connector.fetch_folder(
            folder_id=args.folder_id,
            modified_after=args.modified_after,
            max_files=args.max_files
        )

        if not files:
            print("⚠️  No files found")
            return

        print()
        print(f"✅ Fetched {len(files)} files")
        print()

        # Preview categorization
        print("🏛️  Auto-categorization preview:")
        for file_data in files[:5]:  # First 5
            content = file_data['title'] + " " + file_data['content']
            sphere = ontology.categorize_content(content, method="keyword")

            if sphere:
                print(f"   ✓ '{file_data['title'][:40]}...'")
                print(f"     → {sphere.full_name}")
            else:
                print(f"   ⚠️  '{file_data['title'][:40]}...' → Could not categorize")

        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more")
        print()

        # Add to staging
        print("📝 Adding to staging...")
        count = staging.add_to_staging(files, source="gdrive")
        print(f"✅ Added {count} files to staging")
        print()

        # Auto-approve if requested
        if args.auto_approve:
            print("✅ Auto-approving...")
            pending = staging.get_pending()
            item_ids = [item['id'] for item in pending]
            approved_count = staging.approve(item_ids)
            print(f"✅ Approved {approved_count} items")
            print()

        print("=" * 70)
        print("✅ INGESTION COMPLETE")
        print("=" * 70)
        print()
        print("📍 Next steps:")
        print()
        if not args.auto_approve:
            print("1. Review staged items:")
            print(f"   python -c 'from ingestion.ingestion_pipeline import StagingLayer; s = StagingLayer(staging_dir=\"{args.staging_dir}\"); print(len(s.get_pending()), \"pending\")'")
            print()
            print("2. Approve items:")
            print("   # Manually or via Zapier/Notion workflow")
            print()
        print(f"{'2' if not args.auto_approve else '1'}. Populate vector database:")
        print(f"   python scripts/populate_vector_db.py --staging-dir {args.staging_dir}")
        print()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print()
        print("💡 Setup required:")
        print("   See GDRIVE_SETUP_GUIDE.md for instructions")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
