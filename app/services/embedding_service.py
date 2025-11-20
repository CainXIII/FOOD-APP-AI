"""
Embedding Service - Text embedding generation
Handles text-to-vector conversion using OpenAI embeddings or GPT-based fallback
"""

from openai import AsyncOpenAI
from app.core.config import settings
from typing import List, Dict, Any
import logging
import hashlib
import json

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using OpenAI"""
    
    def __init__(self):
        """Initialize embedding service with configured base_url"""
        self.client = AsyncOpenAI(
            api_key=settings.EMBEDDING_API_KEY,
            base_url=settings.EMBEDDING_BASE_URL
        )
        self.model = settings.EMBEDDING_MODEL
        self.cache: Dict[str, List[float]] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.use_fallback = False  # Will switch to True if embedding model fails
    
    def _generate_simple_embedding(self, text: str) -> List[float]:
        """
        Generate a simple hash-based embedding as fallback
        
        Args:
            text: Text to embed
            
        Returns:
            Pseudo-embedding vector (1536 dimensions)
        """
        # Create a deterministic hash-based vector
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Expand to 1536 dimensions using multiple hashes
        vector = []
        for i in range(48):  # 48 * 32 bytes = 1536 dimensions
            seed = f"{text}_{i}"
            h = hashlib.sha256(seed.encode()).digest()
            for byte in h:
                vector.append((byte / 255.0) * 2 - 1)  # Normalize to [-1, 1]
        
        return vector[:1536]
    
    async def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Check cache
        cache_key = f"query:{text.strip()}"
        if cache_key in self.cache:
            self.cache_hits += 1
            logger.debug(f"Cache hit for query: {text[:50]}...")
            return self.cache[cache_key]
        
        self.cache_misses += 1
        
        # Use fallback if previous attempts failed
        if self.use_fallback:
            logger.debug(f"Using fallback embedding for: {text[:50]}...")
            embedding = self._generate_simple_embedding(text.strip())
            self.cache[cache_key] = embedding
            return embedding
        
        try:
            # Try to generate real embedding
            response = await self.client.embeddings.create(
                model=self.model,
                input=text.strip()
            )
            
            embedding = response.data[0].embedding
            
            # Cache the result
            self.cache[cache_key] = embedding
            
            logger.debug(f"Generated embedding for query: {text[:50]}... (dimension: {len(embedding)})")
            return embedding
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "key_model_access_denied" in error_msg:
                logger.warning(f"Embedding model not accessible, switching to fallback mode: {e}")
                self.use_fallback = True
                embedding = self._generate_simple_embedding(text.strip())
                self.cache[cache_key] = embedding
                return embedding
            else:
                logger.error(f"Embedding generation error: {e}")
                raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Filter empty texts
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        
        if not valid_texts:
            raise ValueError("No valid texts to embed")
        
        # Use fallback if previous attempts failed
        if self.use_fallback:
            logger.debug(f"Using fallback embedding for {len(valid_texts)} texts")
            return [self._generate_simple_embedding(text) for text in valid_texts]
        
        try:
            # Check which texts are in cache
            uncached_texts = []
            uncached_indices = []
            results = [None] * len(valid_texts)
            
            for i, text in enumerate(valid_texts):
                cache_key = f"batch:{text}"
                if cache_key in self.cache:
                    self.cache_hits += 1
                    results[i] = self.cache[cache_key]
                else:
                    self.cache_misses += 1
                    uncached_texts.append(text)
                    uncached_indices.append(i)
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                logger.info(f"Generating embeddings for {len(uncached_texts)} texts")
                
                response = await self.client.embeddings.create(
                    model=self.model,
                    input=uncached_texts
                )
                
                # Process and cache results
                for i, embedding_data in enumerate(response.data):
                    embedding = embedding_data.embedding
                    original_index = uncached_indices[i]
                    text = uncached_texts[i]
                    
                    # Cache the result
                    cache_key = f"batch:{text}"
                    self.cache[cache_key] = embedding
                    
                    # Store in results
                    results[original_index] = embedding
                
                logger.info(f"Generated {len(uncached_texts)} embeddings (dimension: {len(embedding)})")
            
            return results
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "key_model_access_denied" in error_msg:
                logger.warning(f"Embedding model not accessible, switching to fallback mode: {e}")
                self.use_fallback = True
                # Generate fallback embeddings for uncached texts
                for i in uncached_indices:
                    text = valid_texts[i]
                    embedding = self._generate_simple_embedding(text)
                    cache_key = f"batch:{text}"
                    self.cache[cache_key] = embedding
                    results[i] = embedding
                return results
            else:
                logger.error(f"Batch embedding error: {e}")
                raise
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dict with cache statistics
        """
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests
        }
    
    def clear_cache(self):
        """Clear the embedding cache"""
        cache_size = len(self.cache)
        self.cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info(f"Cleared embedding cache ({cache_size} entries)")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get embedding model information
        
        Returns:
            Dict with model information
        """
        return {
            "model": self.model,
            "dimension": 1536,  # text-embedding-3-small dimension
            "base_url": settings.EMBEDDING_BASE_URL,
            "fallback_mode": self.use_fallback
        }


# Global instance
embedding_service = EmbeddingService()
