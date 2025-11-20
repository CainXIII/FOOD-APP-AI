"""
RAG Service - Retrieval Augmented Generation
Handles semantic search and context assembly for chat assistant
"""

from typing import List, Dict, Any, Optional
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
import logging

logger = logging.getLogger(__name__)

class SearchResult:
    """Represents a search result with relevance"""
    
    def __init__(
        self,
        text: str,
        score: float,
        metadata: Dict[str, Any],
        result_id: str
    ):
        self.text = text
        self.score = score
        self.metadata = metadata
        self.result_id = result_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.result_id,
            "text": self.text,
            "score": self.score,
            "metadata": self.metadata
        }


class RAGService:
    """RAG service for semantic search and context assembly"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service
        self.default_limit = 5
        self.min_score = 0.7  # Minimum relevance score
    
    async def search_knowledge(
        self,
        query: str,
        limit: int = None,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search knowledge base for relevant information
        
        Args:
            query: Search query
            limit: Maximum number of results (default: 5)
            score_threshold: Minimum relevance score (default: 0.7)
            filters: Optional metadata filters
            
        Returns:
            List of SearchResult objects
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
        
        limit = limit or self.default_limit
        score_threshold = score_threshold or self.min_score
        
        try:
            # Generate query embedding
            query_vector = await self.embedding_service.embed_query(query)
            
            # Search Qdrant
            results = await self.qdrant_service.search(
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                filters=filters
            )
            
            # Convert to SearchResult objects
            search_results = [
                SearchResult(
                    text=result["payload"].get("text", ""),
                    score=result["score"],
                    metadata=result["payload"],
                    result_id=result["id"]
                )
                for result in results
            ]
            
            logger.info(f"Found {len(search_results)} results for query: {query[:50]}...")
            return search_results
        except Exception as e:
            logger.error(f"Error searching knowledge: {e}")
            raise
    
    async def search_recipes(
        self,
        query: str,
        limit: int = 5,
        difficulty: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Search specifically for recipes
        
        Args:
            query: Search query
            limit: Maximum number of results
            difficulty: Optional difficulty filter
            
        Returns:
            List of SearchResult objects for recipes
        """
        filters = {"content_type": "recipe"}
        if difficulty:
            filters["difficulty"] = difficulty
        
        return await self.search_knowledge(
            query=query,
            limit=limit,
            filters=filters
        )
    
    async def search_techniques(
        self,
        query: str,
        limit: int = 3
    ) -> List[SearchResult]:
        """
        Search for cooking techniques
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of SearchResult objects for techniques
        """
        filters = {
            "content_type": "knowledge_document",
            "doc_type": "technique"
        }
        
        return await self.search_knowledge(
            query=query,
            limit=limit,
            filters=filters
        )
    
    async def search_tips(
        self,
        query: str,
        limit: int = 3
    ) -> List[SearchResult]:
        """
        Search for cooking tips
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of SearchResult objects for tips
        """
        filters = {
            "content_type": "knowledge_document",
            "doc_type": "tip"
        }
        
        return await self.search_knowledge(
            query=query,
            limit=limit,
            filters=filters
        )
    
    async def get_context_for_query(
        self,
        query: str,
        max_context_length: int = 2000,
        include_recipes: bool = True,
        include_techniques: bool = True,
        include_tips: bool = True
    ) -> str:
        """
        Assemble context from multiple sources
        
        Args:
            query: User query
            max_context_length: Maximum context length in characters
            include_recipes: Include recipe results
            include_techniques: Include technique results
            include_tips: Include tip results
            
        Returns:
            Assembled context string
        """
        context_parts = []
        current_length = 0
        
        try:
            # Search different types of content
            results_by_type = []
            
            if include_recipes:
                recipe_results = await self.search_recipes(query, limit=3)
                results_by_type.extend([("RECIPE", r) for r in recipe_results])
            
            if include_techniques:
                technique_results = await self.search_techniques(query, limit=2)
                results_by_type.extend([("TECHNIQUE", r) for r in technique_results])
            
            if include_tips:
                tip_results = await self.search_tips(query, limit=2)
                results_by_type.extend([("TIP", r) for r in tip_results])
            
            # Sort by relevance score
            results_by_type.sort(key=lambda x: x[1].score, reverse=True)
            
            # Assemble context
            for content_type, result in results_by_type:
                # Format based on type
                if content_type == "RECIPE":
                    title = result.metadata.get("recipe_title", "Unknown")
                    section = result.metadata.get("section", "")
                    part_text = f"\n[CÔNG THỨC: {title} - {section}]\n{result.text}\n"
                elif content_type == "TECHNIQUE":
                    title = result.metadata.get("title", "Unknown")
                    part_text = f"\n[KỸ THUẬT: {title}]\n{result.text}\n"
                elif content_type == "TIP":
                    title = result.metadata.get("title", "Unknown")
                    part_text = f"\n[MẸO: {title}]\n{result.text}\n"
                else:
                    part_text = f"\n{result.text}\n"
                
                # Check length
                if current_length + len(part_text) > max_context_length:
                    break
                
                context_parts.append(part_text)
                current_length += len(part_text)
            
            if not context_parts:
                return ""
            
            context = "".join(context_parts)
            logger.info(f"Assembled context with {len(context_parts)} parts, {current_length} characters")
            return context
        except Exception as e:
            logger.error(f"Error assembling context: {e}")
            return ""
    
    async def get_similar_recipes(
        self,
        recipe_title: str,
        limit: int = 5
    ) -> List[SearchResult]:
        """
        Find similar recipes based on title
        
        Args:
            recipe_title: Recipe title to find similar recipes for
            limit: Maximum number of results
            
        Returns:
            List of similar recipes
        """
        return await self.search_recipes(
            query=f"món ăn tương tự {recipe_title}",
            limit=limit
        )
    
    async def find_ingredient_substitutes(
        self,
        ingredient: str
    ) -> List[SearchResult]:
        """
        Find substitute ingredients
        
        Args:
            ingredient: Ingredient to find substitutes for
            
        Returns:
            List of relevant knowledge
        """
        query = f"thay thế nguyên liệu {ingredient}"
        return await self.search_knowledge(query, limit=3)
    
    async def get_cooking_troubleshooting(
        self,
        problem: str
    ) -> List[SearchResult]:
        """
        Get troubleshooting advice for cooking problems
        
        Args:
            problem: Description of the problem
            
        Returns:
            List of relevant solutions
        """
        query = f"khắc phục sửa chữa {problem}"
        return await self.search_knowledge(query, limit=5)
    
    async def search_by_ingredients(
        self,
        ingredients: List[str],
        limit: int = 5
    ) -> List[SearchResult]:
        """
        Search recipes by ingredients
        
        Args:
            ingredients: List of ingredient names
            limit: Maximum number of results
            
        Returns:
            List of matching recipes
        """
        query = "công thức với " + ", ".join(ingredients)
        return await self.search_recipes(query, limit=limit)
    
    def format_context_for_prompt(
        self,
        context: str,
        query: str
    ) -> str:
        """
        Format context for inclusion in LLM prompt
        
        Args:
            context: Retrieved context
            query: User query
            
        Returns:
            Formatted prompt section
        """
        if not context:
            return ""
        
        formatted = f"""
THÔNG TIN TỪ CƠ SỞ KIẾN THỨC:

{context}

---

Dựa trên thông tin trên, hãy trả lời câu hỏi sau:
{query}
"""
        return formatted
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get RAG service statistics
        
        Returns:
            Dictionary with stats
        """
        try:
            collection_info = await self.qdrant_service.get_collection_info()
            embedding_stats = self.embedding_service.get_cache_stats()
            
            return {
                "qdrant": collection_info,
                "embedding_cache": embedding_stats,
                "config": {
                    "default_limit": self.default_limit,
                    "min_score": self.min_score
                }
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}


# Singleton instance
rag_service = RAGService()
