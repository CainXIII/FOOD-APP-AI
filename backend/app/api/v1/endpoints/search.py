"""
Advanced Search endpoints - semantic search, filters, recommendations
"""
from typing import Any, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from pydantic import BaseModel

from app.database import get_db
from app.models.recipe import Recipe, DifficultyLevel
from app.models.user import User
from app.core.deps import get_optional_current_user
from app.services.langchain_rag import qdrant_client, embeddings
from app.config import settings


router = APIRouter()


class SearchResult(BaseModel):
    """Search result item."""
    id: UUID
    title_vi: str
    title_en: str
    slug: str
    description_vi: str
    thumbnail_url: Optional[str]
    category_id: Optional[UUID]
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    difficulty: DifficultyLevel
    avg_rating: float
    score: float  # Relevance score


class SearchResponse(BaseModel):
    """Search response."""
    query: str
    total: int
    results: List[SearchResult]
    search_type: str  # 'semantic', 'keyword', 'hybrid'


@router.get("/semantic", response_model=SearchResponse)
async def semantic_search(
    q: str = Query(..., description="Search query", min_length=2),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="Filter by difficulty"),
    max_prep_time: Optional[int] = Query(None, description="Max prep time in minutes"),
    is_vegetarian: Optional[bool] = Query(None, description="Vegetarian only"),
    is_vegan: Optional[bool] = Query(None, description="Vegan only"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Semantic search for recipes using vector embeddings.
    
    - **q**: Natural language query (e.g., "món ăn với bò", "healthy salad")
    - **limit**: Maximum number of results
    - **category_id**: Optional category filter
    - **difficulty**: Optional difficulty filter (easy, medium, hard)
    - **max_prep_time**: Maximum preparation time
    - **is_vegetarian/is_vegan**: Dietary filters
    """
    try:
        # Generate query embedding
        query_vector = embeddings.embed_query(q)
        
        # Search in Qdrant recipes collection
        search_results = qdrant_client.query_points(
            collection_name="recipes",
            query=query_vector,
            limit=limit * 2
        )
        
        if not search_results or not search_results.points:
            return SearchResponse(
                query=q,
                total=0,
                results=[],
                search_type="semantic"
            )
        
        # Extract recipe IDs and scores from payload
        recipe_ids = []
        score_map = {}
        
        for point in search_results.points:
            if point.payload and 'recipe_id' in point.payload:
                recipe_id = UUID(point.payload['recipe_id'])
                recipe_ids.append(recipe_id)
                score_map[recipe_id] = float(point.score)
        
        # Build query with filters
        query = select(Recipe).where(
            Recipe.id.in_(recipe_ids),
            Recipe.is_published == True
        )
        
        if category_id:
            query = query.where(Recipe.category_id == category_id)
        if difficulty:
            query = query.where(Recipe.difficulty == difficulty)
        if max_prep_time:
            query = query.where(Recipe.prep_time_minutes <= max_prep_time)
        if is_vegetarian:
            query = query.where(Recipe.is_vegetarian == True)
        if is_vegan:
            query = query.where(Recipe.is_vegan == True)
        
        # Execute query
        result = await db.execute(query)
        recipes = result.scalars().all()
        
        # Build response with scores
        search_results_list = []
        for recipe in recipes:
            search_results_list.append(SearchResult(
                id=recipe.id,
                title_vi=recipe.title_vi,
                title_en=recipe.title_en,
                slug=recipe.slug,
                description_vi=recipe.description_vi,
                thumbnail_url=recipe.thumbnail_url,
                category_id=recipe.category_id,
                prep_time_minutes=recipe.prep_time_minutes,
                cook_time_minutes=recipe.cook_time_minutes,
                servings=recipe.servings,
                difficulty=recipe.difficulty,
                avg_rating=recipe.average_rating,
                score=score_map.get(recipe.id, 0.0)
            ))
        
        # Sort by score
        search_results_list.sort(key=lambda x: x.score, reverse=True)
        
        # Limit results
        search_results_list = search_results_list[:limit]
        
        return SearchResponse(
            query=q,
            total=len(search_results_list),
            results=search_results_list,
            search_type="semantic"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/ingredients", response_model=SearchResponse)
async def search_by_ingredients(
    ingredients: str = Query(..., description="Comma-separated ingredient names or IDs"),
    limit: int = Query(20, ge=1, le=100),
    match_all: bool = Query(False, description="Require all ingredients (AND) or any (OR)"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Search recipes by ingredients.
    
    - **ingredients**: Comma-separated list (e.g., "tomato,egg,onion")
    - **match_all**: If true, recipes must contain all ingredients
    """
    try:
        # Split ingredients
        ingredient_list = [i.strip().lower() for i in ingredients.split(',')]
        query_text = " ".join(ingredient_list)
        
        # Generate embedding and search
        query_vector = embeddings.embed_query(query_text)
        search_results = qdrant_client.query_points(
            collection_name="recipes",
            query=query_vector,
            limit=limit
        )
        
        if not search_results or not search_results.points:
            return SearchResponse(
                query=ingredients,
                total=0,
                results=[],
                search_type="ingredient"
            )
        
        # Extract recipe IDs and scores
        recipe_ids = []
        score_map = {}
        
        for point in search_results.points:
            if point.payload and 'recipe_id' in point.payload:
                recipe_id = UUID(point.payload['recipe_id'])
                recipe_ids.append(recipe_id)
                score_map[recipe_id] = float(point.score)
        
        result = await db.execute(
            select(Recipe).where(
                Recipe.id.in_(recipe_ids),
                Recipe.is_published == True
            )
        )
        recipes = result.scalars().all()
        
        # Build response
        search_results_list = [
            SearchResult(
                id=recipe.id,
                title_vi=recipe.title_vi,
                title_en=recipe.title_en,
                slug=recipe.slug,
                description_vi=recipe.description_vi,
                thumbnail_url=recipe.thumbnail_url,
                category_id=recipe.category_id,
                prep_time_minutes=recipe.prep_time_minutes,
                cook_time_minutes=recipe.cook_time_minutes,
                servings=recipe.servings,
                difficulty=recipe.difficulty,
                avg_rating=recipe.average_rating,
                score=score_map.get(recipe.id, 0.0)
            )
            for recipe in recipes
        ]
        
        # Sort by score
        search_results_list.sort(key=lambda x: x.score, reverse=True)
        
        return SearchResponse(
            query=ingredients,
            total=len(search_results_list),
            results=search_results_list,
            search_type="ingredient"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingredient search failed: {str(e)}"
        )


@router.get("/recommendations", response_model=SearchResponse)
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Get personalized recipe recommendations.
    
    Based on:
    - User's favorite recipes
    - Dietary preferences
    - Cooking history
    - Popular recipes
    """
    try:
        # For now, return top-rated recipes
        # TODO: Implement personalization based on user history
        
        query = select(Recipe).where(
            Recipe.is_published == True
        ).order_by(
            Recipe.average_rating.desc(),
            Recipe.ratings_count.desc()
        ).limit(limit)
        
        result = await db.execute(query)
        recipes = result.scalars().all()
        
        # Build response
        recommendations = [
            SearchResult(
                id=recipe.id,
                title_vi=recipe.title_vi,
                title_en=recipe.title_en,
                slug=recipe.slug,
                description_vi=recipe.description_vi,
                thumbnail_url=recipe.thumbnail_url,
                category_id=recipe.category_id,
                prep_time_minutes=recipe.prep_time_minutes,
                cook_time_minutes=recipe.cook_time_minutes,
                servings=recipe.servings,
                difficulty=recipe.difficulty,
                avg_rating=recipe.average_rating,
                score=recipe.average_rating  # Use rating as score
            )
            for recipe in recipes
        ]
        
        return SearchResponse(
            query="recommendations",
            total=len(recommendations),
            results=recommendations,
            search_type="recommendation"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendations failed: {str(e)}"
        )
