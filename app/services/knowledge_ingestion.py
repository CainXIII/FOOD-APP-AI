"""
Knowledge Ingestion Service - Batch process and upload to Qdrant
Handles recipe and document ingestion with embeddings
"""

from typing import List, Dict, Any, Optional
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
from app.services.text_chunker import text_chunker, TextChunk
from app.models.database import Recipe, KnowledgeDocument
import logging
import asyncio

logger = logging.getLogger(__name__)

class KnowledgeIngestion:
    """Service for ingesting knowledge into vector database"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service
        self.text_chunker = text_chunker
    
    async def ingest_recipe(self, recipe: Recipe) -> int:
        """
        Ingest a single recipe into Qdrant
        
        Args:
            recipe: Recipe model instance
            
        Returns:
            Number of chunks ingested
        """
        try:
            # Convert recipe to dict
            recipe_data = {
                "id": str(recipe.id),
                "title": recipe.title,
                "description": recipe.description or "",
                "ingredients": recipe.ingredients or [],
                "steps": recipe.steps or [],
                "tips": recipe.tips or "",
                "difficulty": recipe.difficulty or "medium",
                "prep_time": recipe.prep_time or 0,
                "cook_time": recipe.cook_time or 0
            }
            
            # Chunk recipe
            chunks = self.text_chunker.chunk_recipe(recipe_data)
            
            if not chunks:
                logger.warning(f"No chunks generated for recipe '{recipe.title}'")
                return 0
            
            # Generate embeddings
            texts = [chunk.text for chunk in chunks]
            embeddings = await self.embedding_service.embed_batch(texts)
            
            # Prepare payloads
            payloads = []
            for chunk in chunks:
                payload = {
                    **chunk.metadata,
                    "text": chunk.text,
                    "chunk_type": chunk.chunk_type,
                    "chunk_index": chunk.chunk_index
                }
                payloads.append(payload)
            
            # Upsert to Qdrant
            ids = [f"recipe_{recipe.id}_chunk_{chunk.chunk_index}" for chunk in chunks]
            await self.qdrant_service.upsert(
                vectors=embeddings,
                payloads=payloads,
                ids=ids
            )
            
            logger.info(f"Ingested recipe '{recipe.title}' with {len(chunks)} chunks")
            return len(chunks)
        except Exception as e:
            logger.error(f"Error ingesting recipe: {e}")
            raise
    
    async def ingest_recipes(
        self,
        recipes: List[Recipe],
        batch_size: int = 10
    ) -> Dict[str, int]:
        """
        Ingest multiple recipes in batches
        
        Args:
            recipes: List of Recipe model instances
            batch_size: Number of recipes to process concurrently
            
        Returns:
            Dictionary with ingestion statistics
        """
        total_chunks = 0
        successful = 0
        failed = 0
        
        # Process in batches
        for i in range(0, len(recipes), batch_size):
            batch = recipes[i:i + batch_size]
            
            # Process batch concurrently
            tasks = [self.ingest_recipe(recipe) for recipe in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for recipe, result in zip(batch, results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to ingest recipe '{recipe.title}': {result}")
                    failed += 1
                else:
                    total_chunks += result
                    successful += 1
        
        stats = {
            "total_recipes": len(recipes),
            "successful": successful,
            "failed": failed,
            "total_chunks": total_chunks
        }
        
        logger.info(f"Ingestion complete: {stats}")
        return stats
    
    async def ingest_document(
        self,
        document: KnowledgeDocument
    ) -> int:
        """
        Ingest a knowledge document into Qdrant
        
        Args:
            document: KnowledgeDocument model instance
            
        Returns:
            Number of chunks ingested
        """
        try:
            # Prepare metadata
            metadata = {
                "doc_id": str(document.id),
                "doc_type": document.doc_type,
                "title": document.title,
                "category": document.category or "general",
                "content_type": "knowledge_document"
            }
            
            # Chunk document
            chunks = self.text_chunker.chunk_document(
                doc_text=document.content,
                doc_type=document.doc_type,
                doc_metadata=metadata
            )
            
            if not chunks:
                logger.warning(f"No chunks generated for document '{document.title}'")
                return 0
            
            # Generate embeddings
            texts = [chunk.text for chunk in chunks]
            embeddings = await self.embedding_service.embed_batch(texts)
            
            # Prepare payloads
            payloads = []
            for chunk in chunks:
                payload = {
                    **chunk.metadata,
                    "text": chunk.text,
                    "chunk_type": chunk.chunk_type,
                    "chunk_index": chunk.chunk_index
                }
                payloads.append(payload)
            
            # Upsert to Qdrant
            ids = [f"doc_{document.id}_chunk_{chunk.chunk_index}" for chunk in chunks]
            await self.qdrant_service.upsert(
                vectors=embeddings,
                payloads=payloads,
                ids=ids
            )
            
            logger.info(f"Ingested document '{document.title}' with {len(chunks)} chunks")
            return len(chunks)
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            raise
    
    async def ingest_documents(
        self,
        documents: List[KnowledgeDocument],
        batch_size: int = 10
    ) -> Dict[str, int]:
        """
        Ingest multiple documents in batches
        
        Args:
            documents: List of KnowledgeDocument instances
            batch_size: Number of documents to process concurrently
            
        Returns:
            Dictionary with ingestion statistics
        """
        total_chunks = 0
        successful = 0
        failed = 0
        
        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Process batch concurrently
            tasks = [self.ingest_document(doc) for doc in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for doc, result in zip(batch, results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to ingest document '{doc.title}': {result}")
                    failed += 1
                else:
                    total_chunks += result
                    successful += 1
        
        stats = {
            "total_documents": len(documents),
            "successful": successful,
            "failed": failed,
            "total_chunks": total_chunks
        }
        
        logger.info(f"Ingestion complete: {stats}")
        return stats
    
    async def delete_recipe_chunks(self, recipe_id: str) -> bool:
        """
        Delete all chunks for a recipe
        
        Args:
            recipe_id: Recipe ID
            
        Returns:
            True if successful
        """
        try:
            # Find all chunk IDs for this recipe
            # This is a simplified version - in production, you'd query Qdrant
            # to find all points with this recipe_id
            logger.info(f"Deleting chunks for recipe {recipe_id}")
            
            # For now, we'll need to implement a search by metadata
            # This requires Qdrant to support filtering
            # Placeholder implementation
            return True
        except Exception as e:
            logger.error(f"Error deleting recipe chunks: {e}")
            return False
    
    async def reindex_all(
        self,
        recipes: List[Recipe],
        documents: List[KnowledgeDocument]
    ) -> Dict[str, Any]:
        """
        Reindex all knowledge (delete and recreate collection)
        
        Args:
            recipes: List of all recipes
            documents: List of all documents
            
        Returns:
            Combined statistics
        """
        try:
            # Delete and recreate collection
            await self.qdrant_service.delete_collection()
            await self.qdrant_service.create_collection()
            
            # Ingest recipes
            recipe_stats = await self.ingest_recipes(recipes)
            
            # Ingest documents
            doc_stats = await self.ingest_documents(documents)
            
            stats = {
                "recipes": recipe_stats,
                "documents": doc_stats,
                "total_chunks": recipe_stats["total_chunks"] + doc_stats["total_chunks"]
            }
            
            logger.info(f"Reindexing complete: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error reindexing: {e}")
            raise


# Singleton instance
knowledge_ingestion = KnowledgeIngestion()
