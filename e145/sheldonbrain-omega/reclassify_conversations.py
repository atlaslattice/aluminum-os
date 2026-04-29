#!/usr/bin/env python3
"""
Re-classify existing Grok conversations with proper 144-sphere ontology tags
Updates the Qdrant database with AI-generated House/Sphere classifications
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.ontology_classifier import OntologyClassifier
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import structlog

structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger()


def reclassify_all_conversations(
    chat_file: str = "exports/grok_chats/ttl/30d/export_data/591ad8c2-a366-440e-9f69-f30db7a4ca1f/prod-grok-backend.json",
    db_path: str = "./qdrant_db",
    collection_name: str = "grokbrain_grid",
    use_vertex: bool = True,
    dry_run: bool = False
):
    """
    Re-classify all conversations and update their metadata in Qdrant

    Args:
        chat_file: Path to the Grok chat JSON export
        db_path: Path to Qdrant database
        collection_name: Qdrant collection name
        use_vertex: Use Vertex AI for classification
        dry_run: If True, only show classifications without updating DB
    """
    print("=" * 80)
    print("RECLASSIFYING GROK CONVERSATIONS WITH 144-SPHERE ONTOLOGY")
    print("=" * 80)
    print()

    # Load conversations
    print(f"📁 Loading conversations from {chat_file}...")
    with open(chat_file, 'r') as f:
        data = json.load(f)

    conversations = data.get('conversations', [])
    print(f"   Found {len(conversations)} conversations")
    print()

    # Initialize classifier
    print("🤖 Initializing AI classifier...")
    classifier = OntologyClassifier(use_vertex=use_vertex)
    if classifier.model:
        model_type = "Vertex AI" if classifier.use_vertex else "Generative AI"
        print(f"   ✅ Using {model_type}")
    else:
        print(f"   ⚠️  No AI available, using keyword fallback")
    print()

    # Initialize Qdrant client
    if not dry_run:
        print(f"💾 Connecting to Qdrant at {db_path}...")
        client = QdrantClient(path=db_path)
        print("   ✅ Connected")
        print()

    # Classify each conversation
    print("🔍 Classifying conversations...")
    print()

    classifications = []
    house_counts = {}
    sphere_counts = {}

    for idx, conv in enumerate(conversations):
        conv_id = conv['conversation']['id']
        title = conv['conversation'].get('title', 'Untitled')
        responses = conv.get('responses', [])

        # Build content sample (first 3-4 messages)
        content_sample = f"Conversation: {title}\n\n"
        for r in responses[:4]:  # Sample first few messages
            resp = r['response']
            sender = resp.get('sender', 'unknown')
            message = resp.get('message', '')
            if message:
                content_sample += f"{sender.upper()}: {message[:300]}...\n\n"

        # Classify
        house, sphere, confidence = classifier.classify_conversation(title, content_sample)

        # Track stats
        house_counts[house] = house_counts.get(house, 0) + 1
        sphere_key = f"{house} → {sphere}"
        sphere_counts[sphere_key] = sphere_counts.get(sphere_key, 0) + 1

        classifications.append({
            "conversation_id": conv_id,
            "title": title,
            "house": house,
            "sphere": sphere,
            "confidence": confidence
        })

        # Print progress
        if (idx + 1) % 10 == 0 or confidence < 0.5:
            conf_emoji = "✅" if confidence >= 0.7 else "⚠️" if confidence >= 0.5 else "❌"
            print(f"  [{idx + 1}/{len(conversations)}] {conf_emoji} {title[:50]}")
            print(f"      → {house} / {sphere} ({confidence:.2f})")

    print()
    print("=" * 80)
    print("CLASSIFICATION SUMMARY")
    print("=" * 80)
    print()

    print(f"📊 House Distribution ({len(house_counts)} houses):")
    for house, count in sorted(house_counts.items(), key=lambda x: -x[1]):
        pct = (count / len(conversations)) * 100
        print(f"   {house}: {count} ({pct:.1f}%)")

    print()
    print(f"🎯 Top 10 Spheres:")
    for sphere, count in sorted(sphere_counts.items(), key=lambda x: -x[1])[:10]:
        pct = (count / len(conversations)) * 100
        print(f"   {sphere}: {count} ({pct:.1f}%)")

    # Calculate average confidence
    avg_confidence = sum(c["confidence"] for c in classifications) / len(classifications)
    low_confidence = sum(1 for c in classifications if c["confidence"] < 0.5)

    print()
    print(f"📈 Confidence Metrics:")
    print(f"   Average confidence: {avg_confidence:.2f}")
    print(f"   Low confidence (<0.5): {low_confidence} ({(low_confidence/len(classifications)*100):.1f}%)")

    if dry_run:
        print()
        print("=" * 80)
        print("DRY RUN MODE - No database updates performed")
        print("=" * 80)
        print()
        print("Sample classifications:")
        for c in classifications[:5]:
            print(f"\n  📄 {c['title'][:60]}")
            print(f"     House: {c['house']}")
            print(f"     Sphere: {c['sphere']}")
            print(f"     Confidence: {c['confidence']:.2f}")
        return classifications

    # Update Qdrant metadata
    print()
    print("=" * 80)
    print("UPDATING QDRANT DATABASE")
    print("=" * 80)
    print()

    print("🔄 Updating metadata for each conversation...")

    # Get all points from collection
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=200,
        with_payload=True,
        with_vectors=False
    )

    points = scroll_result[0]
    print(f"   Found {len(points)} points in database")

    # Create mapping of conversation_id to classification
    classification_map = {c["conversation_id"]: c for c in classifications}

    updated = 0
    failed = 0

    for point in points:
        conv_id = point.payload.get("conversation_id")

        if conv_id in classification_map:
            classification = classification_map[conv_id]

            # Update payload with new classifications
            new_payload = point.payload.copy()
            new_payload["house"] = classification["house"]
            new_payload["sphere"] = classification["sphere"]
            new_payload["classification_confidence"] = classification["confidence"]

            try:
                client.set_payload(
                    collection_name=collection_name,
                    payload=new_payload,
                    points=[point.id]
                )
                updated += 1

                if updated % 25 == 0:
                    print(f"   Updated {updated}/{len(points)} conversations...")

            except Exception as e:
                logger.error("update_failed", point_id=point.id, error=str(e))
                failed += 1

    print()
    print(f"✅ Update complete!")
    print(f"   Successfully updated: {updated}")
    print(f"   Failed: {failed}")
    print()

    # Save classifications to file for reference
    output_file = "data/conversation_classifications.json"
    Path("data").mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            "total_conversations": len(conversations),
            "house_distribution": house_counts,
            "sphere_distribution": sphere_counts,
            "average_confidence": avg_confidence,
            "low_confidence_count": low_confidence,
            "classifications": classifications
        }, f, indent=2)

    print(f"💾 Saved detailed classification report to: {output_file}")
    print()

    return classifications


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Re-classify conversations with 144-sphere ontology")
    parser.add_argument("--dry-run", action="store_true", help="Show classifications without updating database")
    parser.add_argument("--no-vertex", action="store_true", help="Use generative AI instead of Vertex AI")
    parser.add_argument("--chat-file", default="exports/grok_chats/ttl/30d/export_data/591ad8c2-a366-440e-9f69-f30db7a4ca1f/prod-grok-backend.json",
                        help="Path to chat JSON file")

    args = parser.parse_args()

    use_vertex = not args.no_vertex

    classifications = reclassify_all_conversations(
        chat_file=args.chat_file,
        use_vertex=use_vertex,
        dry_run=args.dry_run
    )

    print("=" * 80)
    print("✅ RECLASSIFICATION COMPLETE!")
    print("=" * 80)
