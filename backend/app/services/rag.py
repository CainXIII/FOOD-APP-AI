"""
RAG (Retrieval-Augmented Generation) service
Handles semantic search and context retrieval for AI chat
"""
from typing import List, Dict, Any, Optional, AsyncGenerator
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, text
from app.models.recipe import Recipe
from app.models.embedding import RecipeEmbedding
from app.services.openai_service import get_openai_service, chat_with_assistant, chat_with_assistant_stream


async def get_rag_context(
    query: str,
    db: AsyncSession,
    top_k: int = 5,
    min_similarity: float = 0.7,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Retrieve relevant context for RAG using semantic search
    
    Args:
        query: User query
        db: Database session
        top_k: Number of results to return
        min_similarity: Minimum similarity threshold (not used yet - placeholder for vector search)
        filters: Optional filters (category, difficulty, etc.)
        
    Returns:
        Dictionary with retrieved contexts and metadata
    """
    try:
        # Try to generate embedding for semantic search
        service = get_openai_service()
        query_embedding = await service.create_embedding(query)
        
        # Perform vector similarity search
        similar_recipes = await semantic_search_recipes(
            query_embedding=query_embedding,
            db=db,
            top_k=top_k,
            filters=filters
        )
        
        if similar_recipes:
            # Use vector search results
            contexts = []
            for recipe_data in similar_recipes:
                contexts.append({
                    "recipe_id": str(recipe_data["recipe_id"]),
                    "title": recipe_data["title"],
                    "content": recipe_data["content"],
                    "similarity": recipe_data["similarity"],
                    "source_type": "recipe"
                })
            
            return {
                "query": query,
                "contexts": contexts,
                "total": len(contexts),
                "search_type": "vector"
            }
        else:
            # Fallback to text search if no vector results
            print("⚠️  No vector search results, falling back to text search")
            return await get_rag_context_text_search(query, db, top_k, filters)
            
    except Exception as e:
        print(f"❌ Vector search failed: {e}, falling back to text search")
        # Fallback to text search on error (including budget exceeded)
        return await get_rag_context_text_search(query, db, top_k, filters)


async def get_rag_context_text_search(
    query: str,
    db: AsyncSession,
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fallback text search for RAG context
    """
    search_term = f"%{query}%"
    query_stmt = select(Recipe).where(
        Recipe.is_published == True,
        or_(
            Recipe.title_vi.ilike(search_term),
            Recipe.title_en.ilike(search_term),
            Recipe.description_vi.ilike(search_term),
            Recipe.description_en.ilike(search_term)
        )
    ).limit(top_k)
    
    # Apply filters
    if filters:
        if filters.get("category_id"):
            query_stmt = query_stmt.where(Recipe.category_id == filters["category_id"])
        if filters.get("difficulty"):
            query_stmt = query_stmt.where(Recipe.difficulty == filters["difficulty"])
        if filters.get("is_vegetarian"):
            query_stmt = query_stmt.where(Recipe.is_vegetarian == True)
        if filters.get("is_vegan"):
            query_stmt = query_stmt.where(Recipe.is_vegan == True)
    
    result = await db.execute(query_stmt)
    recipes = result.scalars().all()
    
    contexts = []
    for recipe in recipes:
        # Build context text
        context_text = f"Công thức: {recipe.title_vi}\n"
        context_text += f"Mô tả: {recipe.description_vi}\n"
        context_text += f"Thời gian: {recipe.total_time_minutes} phút\n"
        context_text += f"Khẩu phần: {recipe.servings} người\n"
        context_text += f"Độ khó: {recipe.difficulty.value}\n"
        
        contexts.append({
            "recipe_id": str(recipe.id),
            "title": recipe.title_vi,
            "content": context_text,
            "similarity": 1.0,  # Placeholder for text search
            "source_type": "recipe"
        })
    
    return {
        "query": query,
        "contexts": contexts,
        "total": len(contexts),
        "search_type": "text"
    }


async def generate_chat_response(
    messages: List[Dict[str, str]],
    rag_context: Optional[Dict[str, Any]] = None,
    stream: bool = False
) -> Any:
    """
    Generate AI chat response using OpenAI
    
    Args:
        messages: Chat history
        rag_context: Retrieved context from RAG
        stream: Whether to stream response
        
    Returns:
        AI generated response (string or async generator)
    """
    # Get the last user message
    user_message = messages[-1]["content"] if messages else ""
    
    # Build context string from RAG results
    context = None
    if rag_context and rag_context.get("contexts"):
        context_parts = []
        for ctx in rag_context["contexts"]:
            context_parts.append(f"--- {ctx['title']} ---\n{ctx['content']}")
        context = "\n\n".join(context_parts)
    
    # Get conversation history (all messages except system and last user message)
    conversation_history = messages[:-1] if len(messages) > 1 else None
    
    # Generate response using OpenAI
    if stream:
        return chat_with_assistant_stream(user_message, context, conversation_history)
    else:
        return await chat_with_assistant(user_message, context, conversation_history)


async def embed_text(text: str) -> List[float]:
    """
    Generate embedding vector for text using OpenAI
    
    Args:
        text: Input text
        
    Returns:
        Embedding vector (1536 dimensions for text-embedding-3-small)
    """
    service = get_openai_service()
    return await service.create_embedding(text)


async def embed_recipe(recipe: Recipe) -> List[float]:
    """
    Generate embedding for a recipe
    
    Args:
        recipe: Recipe object
        
    Returns:
        Embedding vector
    """
    # Combine recipe information for embedding
    recipe_text = f"{recipe.title_vi} {recipe.title_en or ''}\n"
    recipe_text += f"{recipe.description_vi} {recipe.description_en or ''}\n"
    recipe_text += f"Độ khó: {recipe.difficulty.value}\n"
    recipe_text += f"Thời gian: {recipe.total_time_minutes} phút\n"
    
    if recipe.is_vegetarian:
        recipe_text += "Món chay "
    if recipe.is_vegan:
        recipe_text += "Món thuần chay "
    if recipe.is_gluten_free:
        recipe_text += "Không chứa gluten "
    
    return await embed_text(recipe_text)


async def semantic_search_recipes(
    query_embedding: List[float],
    db: AsyncSession,
    top_k: int = 5,
    min_similarity: float = 0.7,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search recipes using semantic similarity with SQLite

    Calculates cosine similarity in Python since SQLite doesn't have vector operations.
    Uses RecipeEmbedding table for efficient storage and retrieval.

    Args:
        query_embedding: Query embedding vector
        db: Database session
        top_k: Number of results to return
        min_similarity: Minimum similarity threshold
        filters: Optional filters

    Returns:
        List of matching recipes with similarity scores
    """
    try:
        # Get all embeddings from database
        query_stmt = select(RecipeEmbedding, Recipe).join(
            Recipe, RecipeEmbedding.recipe_id == Recipe.id
        ).where(Recipe.is_published == True)

        # Apply filters
        if filters:
            if filters.get("category_id"):
                query_stmt = query_stmt.where(Recipe.category_id == filters["category_id"])
            if filters.get("difficulty"):
                query_stmt = query_stmt.where(Recipe.difficulty == filters["difficulty"])
            if filters.get("is_vegetarian"):
                query_stmt = query_stmt.where(Recipe.is_vegetarian == True)
            if filters.get("is_vegan"):
                query_stmt = query_stmt.where(Recipe.is_vegan == True)

        result = await db.execute(query_stmt)
        rows = result.all()

        # Calculate cosine similarity for each embedding
        similarities = []
        for row in rows:
            embedding_record, recipe = row

            # Calculate cosine similarity
            similarity = cosine_similarity(query_embedding, embedding_record.embedding)

            if similarity >= min_similarity:
                # Build context text based on content type
                context_text = f"Công thức: {recipe.title_vi}\n"
                context_text += f"Mô tả: {recipe.description_vi}\n"
                context_text += f"Thời gian: {recipe.total_time_minutes} phút\n"
                context_text += f"Khẩu phần: {recipe.servings} người\n"
                context_text += f"Độ khó: {recipe.difficulty.value}\n"

                # Add specific content based on embedding type
                if embedding_record.content_type == "ingredients":
                    context_text += f"Nguyên liệu: {embedding_record.content_text}\n"
                elif embedding_record.content_type == "step":
                    context_text += f"Bước thực hiện: {embedding_record.content_text}\n"
                elif embedding_record.content_type == "nutrition":
                    context_text += f"Dinh dưỡng: {embedding_record.content_text}\n"

                similarities.append({
                    "recipe_id": str(recipe.id),
                    "title": recipe.title_vi,
                    "content": context_text,
                    "similarity": float(similarity),
                    "content_type": embedding_record.content_type,
                    "embedding_id": str(embedding_record.id)
                })

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]

    except Exception as e:
        print(f"❌ Vector search error: {e}")
        return []


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    try:
        # Convert to numpy arrays for efficient calculation
        import numpy as np
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        # Calculate cosine similarity
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return dot_product / (norm_v1 * norm_v2)
    except Exception as e:
        print(f"❌ Cosine similarity calculation error: {e}")
        return 0.0