"""
Qdrant Service - Vector database operations
Handles collection management, vector upsert, search, and deletion
"""

from typing import List, Dict, Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest
)
from app.core.config import settings
import logging
import uuid

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Qdrant service
        
        Args:
            url: Optional Qdrant URL override
            api_key: Optional API key override
        """
        self.url = url or settings.QDRANT_URL
        self.api_key = api_key or settings.QDRANT_API_KEY
        self.client = AsyncQdrantClient(
            url=self.url,
            api_key=self.api_key if self.api_key else None
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.vector_size = 1536  # text-embedding-3-small dimension
        
    async def collection_exists(self, collection_name: Optional[str] = None) -> bool:
        """
        Check if collection exists
        
        Args:
            collection_name: Optional collection name override
            
        Returns:
            True if collection exists
        """
        name = collection_name or self.collection_name
        try:
            collections = await self.client.get_collections()
            return any(c.name == name for c in collections.collections)
        except Exception as e:
            logger.error(f"Error checking collection existence: {e}")
            return False
    
    async def create_collection(
        self,
        collection_name: Optional[str] = None,
        vector_size: Optional[int] = None,
        distance: Distance = Distance.COSINE
    ) -> bool:
        """
        Create a new collection
        
        Args:
            collection_name: Optional collection name override
            vector_size: Optional vector size override
            distance: Distance metric (COSINE, EUCLID, DOT)
            
        Returns:
            True if successful
        """
        name = collection_name or self.collection_name
        size = vector_size or self.vector_size
        
        try:
            # Check if already exists
            if await self.collection_exists(name):
                logger.info(f"Collection '{name}' already exists")
                return True
            
            # Create collection
            await self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=size,
                    distance=distance
                )
            )
            logger.info(f"Created collection '{name}' with vector size {size}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    async def delete_collection(self, collection_name: Optional[str] = None) -> bool:
        """
        Delete a collection
        
        Args:
            collection_name: Optional collection name override
            
        Returns:
            True if successful
        """
        name = collection_name or self.collection_name
        try:
            await self.client.delete_collection(collection_name=name)
            logger.info(f"Deleted collection '{name}'")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False
    
    async def upsert(
        self,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
        collection_name: Optional[str] = None
    ) -> bool:
        """
        Insert or update vectors in collection
        
        Args:
            vectors: List of embedding vectors
            payloads: List of metadata payloads
            ids: Optional list of IDs (auto-generated if not provided)
            collection_name: Optional collection name override
            
        Returns:
            True if successful
        """
        name = collection_name or self.collection_name
        
        if len(vectors) != len(payloads):
            raise ValueError("Number of vectors must match number of payloads")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
        
        if len(ids) != len(vectors):
            raise ValueError("Number of IDs must match number of vectors")
        
        try:
            # Ensure collection exists
            if not await self.collection_exists(name):
                await self.create_collection(name)
            
            # Create points
            points = [
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
                for point_id, vector, payload in zip(ids, vectors, payloads)
            ]
            
            # Upsert points
            await self.client.upsert(
                collection_name=name,
                points=points
            )
            
            logger.info(f"Upserted {len(points)} points to collection '{name}'")
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise
    
    async def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None,
        collection_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0-1)
            filters: Optional metadata filters
            collection_name: Optional collection name override
            
        Returns:
            List of search results with id, score, and payload
        """
        name = collection_name or self.collection_name
        
        try:
            # Build filter if provided
            query_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    query_filter = Filter(must=conditions)
            
            # Search
            results = await self.client.search(
                collection_name=name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter
            )
            
            # Format results
            formatted_results = [
                {
                    "id": str(hit.id),
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ]
            
            logger.debug(f"Found {len(formatted_results)} results in collection '{name}'")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise
    
    async def delete(
        self,
        ids: List[str],
        collection_name: Optional[str] = None
    ) -> bool:
        """
        Delete vectors by IDs
        
        Args:
            ids: List of vector IDs to delete
            collection_name: Optional collection name override
            
        Returns:
            True if successful
        """
        name = collection_name or self.collection_name
        
        try:
            await self.client.delete(
                collection_name=name,
                points_selector=ids
            )
            logger.info(f"Deleted {len(ids)} points from collection '{name}'")
            return True
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False
    
    async def get_collection_info(
        self,
        collection_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get collection information
        
        Args:
            collection_name: Optional collection name override
            
        Returns:
            Collection info dict or None
        """
        name = collection_name or self.collection_name
        
        try:
            info = await self.client.get_collection(collection_name=name)
            return {
                "name": name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return None
    
    async def scroll_all(
        self,
        collection_name: Optional[str] = None,
        batch_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all points from collection
        
        Args:
            collection_name: Optional collection name override
            batch_size: Number of points per batch
            
        Returns:
            List of all points
        """
        name = collection_name or self.collection_name
        
        try:
            all_points = []
            offset = None
            
            while True:
                results, offset = await self.client.scroll(
                    collection_name=name,
                    limit=batch_size,
                    offset=offset
                )
                
                if not results:
                    break
                
                all_points.extend([
                    {
                        "id": str(point.id),
                        "vector": point.vector,
                        "payload": point.payload
                    }
                    for point in results
                ])
                
                if offset is None:
                    break
            
            logger.info(f"Retrieved {len(all_points)} points from collection '{name}'")
            return all_points
        except Exception as e:
            logger.error(f"Error scrolling collection: {e}")
            raise
    
    async def count(
        self,
        collection_name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count points in collection
        
        Args:
            collection_name: Optional collection name override
            filters: Optional metadata filters
            
        Returns:
            Number of points
        """
        name = collection_name or self.collection_name
        
        try:
            # Build filter if provided
            query_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    query_filter = Filter(must=conditions)
            
            result = await self.client.count(
                collection_name=name,
                count_filter=query_filter
            )
            
            return result.count
        except Exception as e:
            logger.error(f"Error counting points: {e}")
            return 0


# Singleton instance
qdrant_service = QdrantService()
