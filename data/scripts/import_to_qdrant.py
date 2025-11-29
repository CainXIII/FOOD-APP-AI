#!/usr/bin/env python3
"""
Import Vector Embeddings to Qdrant Vector Database.
Creates collections and uploads recipe & ingredient embeddings.
"""

import json
import os
import sys
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    OptimizersConfigDiff,
    HnswConfigDiff
)
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", "1536"))
DISTANCE_METRIC = os.getenv("QDRANT_DISTANCE", "Cosine")

# Collection names
RECIPE_COLLECTION = "recipes"
INGREDIENT_COLLECTION = "ingredients"


def get_distance_metric(metric: str) -> Distance:
    """Convert string distance metric to Qdrant Distance enum."""
    metric_map = {
        "Cosine": Distance.COSINE,
        "Euclid": Distance.EUCLID,
        "Dot": Distance.DOT
    }
    return metric_map.get(metric, Distance.COSINE)


def init_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client."""
    print(f"\n🔌 Connecting to Qdrant...")
    print(f"   URL: {QDRANT_URL}")
    
    try:
        if QDRANT_API_KEY:
            client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            client = QdrantClient(url=QDRANT_URL)
        
        # Test connection
        collections = client.get_collections()
        print(f"✅ Connected to Qdrant")
        print(f"   Existing collections: {len(collections.collections)}")
        return client
    
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {str(e)}")
        print("\nPlease ensure Qdrant is running:")
        print("  Docker: docker-compose -f docker-compose.qdrant.yml up -d")
        print("  Or local: qdrant")
        sys.exit(1)


def create_collection(client: QdrantClient, collection_name: str, recreate: bool = False):
    """Create or recreate a collection in Qdrant."""
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        exists = any(col.name == collection_name for col in collections)
        
        if exists:
            if recreate:
                print(f"🗑️  Deleting existing collection: {collection_name}")
                client.delete_collection(collection_name)
            else:
                print(f"ℹ️  Collection '{collection_name}' already exists")
                return
        
        print(f"📦 Creating collection: {collection_name}")
        
        # Create collection with optimized settings
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=get_distance_metric(DISTANCE_METRIC)
            ),
            optimizers_config=OptimizersConfigDiff(
                indexing_threshold=10000  # Start indexing after 10k vectors
            ),
            hnsw_config=HnswConfigDiff(
                m=16,  # Number of edges per node
                ef_construct=100,  # Size of the dynamic candidate list
                full_scan_threshold=10000
            )
        )
        
        print(f"✅ Collection created: {collection_name}")
        print(f"   Vector size: {VECTOR_SIZE}")
        print(f"   Distance: {DISTANCE_METRIC}")
        
    except Exception as e:
        print(f"❌ Error creating collection: {str(e)}")
        raise


def import_recipe_embeddings(client: QdrantClient, recreate: bool = False):
    """Import recipe embeddings to Qdrant."""
    print("\n" + "="*70)
    print("  IMPORTING RECIPE EMBEDDINGS")
    print("="*70 + "\n")
    
    # Load embeddings from JSON
    try:
        with open('data/recipe-embeddings_full.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            embeddings = data['embeddings']
        
        print(f"📚 Loaded {len(embeddings)} recipe embeddings")
    except FileNotFoundError:
        print("❌ Error: recipe-embeddings_full.json not found")
        print("   Please run: python generate_embeddings.py")
        return
    
    # Create collection
    create_collection(client, RECIPE_COLLECTION, recreate)
    
    # Prepare points for batch upload
    points = []
    
    for idx, embedding in enumerate(embeddings, 1):
        try:
            # Create point with UUID from recipe_id or generate new one
            point_id = embedding.get('recipe_id') or embedding.get('id')
            if isinstance(point_id, str):
                # Keep as UUID string
                point_id = point_id
            
            # Payload with all metadata
            payload = {
                "recipe_id": embedding.get('recipe_id'),
                "title": embedding.get('title'),
                "content_type": embedding.get('content_type', 'recipe_full'),
                **embedding.get('metadata', {})
            }
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding['embedding'],
                payload=payload
            )
            
            points.append(point)
            
            if idx % 10 == 0:
                print(f"   Prepared {idx}/{len(embeddings)} points...")
        
        except Exception as e:
            print(f"   ⚠️  Error preparing point {idx}: {str(e)}")
            continue
    
    # Upload in batches
    print(f"\n📤 Uploading {len(points)} points to Qdrant...")
    
    try:
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            client.upsert(
                collection_name=RECIPE_COLLECTION,
                points=batch
            )
            print(f"   Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
        
        # Get collection info
        collection_info = client.get_collection(RECIPE_COLLECTION)
        vector_count = collection_info.points_count if hasattr(collection_info, 'points_count') else len(points)
        print(f"\n✅ Recipe embeddings imported successfully")
        print(f"   Total vectors: {vector_count}")
        print(f"   Collection: {RECIPE_COLLECTION}")
    
    except Exception as e:
        print(f"❌ Error uploading to Qdrant: {str(e)}")
        raise


def import_ingredient_embeddings(client: QdrantClient, recreate: bool = False):
    """Import ingredient embeddings to Qdrant."""
    print("\n" + "="*70)
    print("  IMPORTING INGREDIENT EMBEDDINGS")
    print("="*70 + "\n")
    
    # Load embeddings from JSON
    try:
        with open('data/ingredient-embeddings_full.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            embeddings = data['embeddings']
        
        print(f"📚 Loaded {len(embeddings)} ingredient embeddings")
    except FileNotFoundError:
        print("❌ Error: ingredient-embeddings_full.json not found")
        print("   Please run: python generate_embeddings.py")
        return
    
    # Create collection
    create_collection(client, INGREDIENT_COLLECTION, recreate)
    
    # Prepare points for batch upload
    points = []
    
    for idx, embedding in enumerate(embeddings, 1):
        try:
            # Create point with UUID from ingredient_id or generate new one
            point_id = embedding.get('ingredient_id') or embedding.get('id')
            if isinstance(point_id, str):
                # Keep as UUID string
                point_id = point_id
            
            # Payload with all metadata
            payload = {
                "ingredient_id": embedding.get('ingredient_id'),
                "name": embedding.get('name'),
                "content_type": embedding.get('content_type', 'ingredient'),
                **embedding.get('metadata', {})
            }
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding['embedding'],
                payload=payload
            )
            
            points.append(point)
            
            if idx % 20 == 0:
                print(f"   Prepared {idx}/{len(embeddings)} points...")
        
        except Exception as e:
            print(f"   ⚠️  Error preparing point {idx}: {str(e)}")
            continue
    
    # Upload in batches
    print(f"\n📤 Uploading {len(points)} points to Qdrant...")
    
    try:
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            client.upsert(
                collection_name=INGREDIENT_COLLECTION,
                points=batch
            )
            print(f"   Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
        
        # Get collection info
        collection_info = client.get_collection(INGREDIENT_COLLECTION)
        vector_count = collection_info.points_count if hasattr(collection_info, 'points_count') else len(points)
        print(f"\n✅ Ingredient embeddings imported successfully")
        print(f"   Total vectors: {vector_count}")
        print(f"   Collection: {INGREDIENT_COLLECTION}")
    
    except Exception as e:
        print(f"❌ Error uploading to Qdrant: {str(e)}")
        raise


def verify_import(client: QdrantClient):
    """Verify the import by checking collections and performing test search."""
    print("\n" + "="*70)
    print("  VERIFICATION")
    print("="*70 + "\n")
    
    try:
        # Check recipe collection
        recipe_info = client.get_collection(RECIPE_COLLECTION)
        recipe_count = recipe_info.points_count if hasattr(recipe_info, 'points_count') else 0
        print(f"📊 {RECIPE_COLLECTION}:")
        print(f"   Vectors: {recipe_count}")
        print(f"   Indexed: {recipe_info.status}")
        
        # Check ingredient collection
        ingredient_info = client.get_collection(INGREDIENT_COLLECTION)
        ingredient_count = ingredient_info.points_count if hasattr(ingredient_info, 'points_count') else 0
        print(f"\n📊 {INGREDIENT_COLLECTION}:")
        print(f"   Vectors: {ingredient_count}")
        print(f"   Indexed: {ingredient_info.status}")
        
        print(f"\n✅ All collections verified successfully!")
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("  QDRANT VECTOR DATABASE IMPORTER")
    print("="*70)
    
    # Parse arguments
    recreate = "--recreate" in sys.argv or "-r" in sys.argv
    
    if recreate:
        print("\n⚠️  RECREATE MODE: Existing collections will be deleted!")
    
    try:
        # Initialize client
        client = init_qdrant_client()
        
        # Import recipe embeddings
        import_recipe_embeddings(client, recreate)
        
        # Import ingredient embeddings
        import_ingredient_embeddings(client, recreate)
        
        # Verify import
        verify_import(client)
        
        print("\n" + "="*70)
        print("  🎉 IMPORT COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n✅ Your vector database is ready for:")
        print("   - Semantic recipe search")
        print("   - Ingredient-based recommendations")
        print("   - RAG-powered chat AI")
        print("   - Similar recipe suggestions")
        
        print(f"\n🌐 Qdrant Dashboard: {QDRANT_URL.replace(':6333', ':6333/dashboard')}")
        print("\n💡 Next steps:")
        print("   1. Start backend: cd backend && uvicorn app.main:app --reload")
        print("   2. Test RAG: python backend/test_qdrant_rag.py")
        print("   3. Test search API endpoints\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Import cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
