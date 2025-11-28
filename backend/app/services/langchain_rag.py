"""
LangChain RAG implementation with Qdrant Vector Database
Production-ready RAG service for cooking assistant
"""
from typing import List, Dict, Any, Optional
import httpx
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.config import settings

# ============================================================================
# EMBEDDINGS & LLM INITIALIZATION
# ============================================================================

# Create HTTP client with SSL verification disabled for self-signed certificates
http_client = httpx.Client(verify=False)

# OpenAI Embeddings for vector generation
embeddings = OpenAIEmbeddings(
    model=settings.OPENAI_EMBEDDING_MODEL,
    openai_api_key=settings.OPENAI_EMBEDDING_API_KEY or settings.OPENAI_API_KEY,
    openai_api_base=settings.OPENAI_EMBEDDING_BASE_URL,
    http_client=http_client
)

# Chat LLM for response generation
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=settings.OPENAI_TEMPERATURE,
    max_tokens=settings.OPENAI_MAX_TOKENS,
    openai_api_key=settings.OPENAI_API_KEY,
    openai_api_base=settings.OPENAI_BASE_URL,
    streaming=True,
    http_client=http_client
)

# ============================================================================
# VECTOR STORE CONFIGURATION
# ============================================================================

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    timeout=60,
    prefer_grpc=False,  # Use REST API
    https=False  # Local HTTP connection
)

# Create collection if not exists
try:
    from qdrant_client.models import VectorParams, Distance
    
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    if settings.QDRANT_COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config={
                "text_vector": VectorParams(
                    size=settings.QDRANT_VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            }
        )
        print(f"✅ Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
except Exception as e:
    print(f"⚠️  Warning: Could not check/create collection: {e}")

# Initialize Qdrant vector store with LangChain
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=settings.QDRANT_COLLECTION_NAME,
    embedding=embeddings,
    vector_name="text_vector"  # Named vector for multi-vector support
)

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

# System prompt for cooking assistant
SYSTEM_PROMPT_TEMPLATE = """Bạn là trợ lý nấu ăn AI thông minh, hữu ích và thân thiện. 
Bạn giúp người dùng với công thức nấu ăn, mẹo vặt, và câu hỏi về ẩm thực Việt Nam.

Nguyên tắc:
1. Trả lời dựa trên context từ database công thức nấu ăn
2. Nếu không có thông tin, hãy thành thật nói không biết
3. Đưa ra câu trả lời ngắn gọn, dễ hiểu, thực tế
4. Sử dụng tiếng Việt tự nhiên và thân thiện
5. Đề xuất công thức cụ thể khi phù hợp

Context từ database:
{context}

Lịch sử hội thoại:
{chat_history}

Câu hỏi của người dùng:
{question}

Hãy trả lời dựa trên context và lịch sử hội thoại:"""

prompt_template = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=SYSTEM_PROMPT_TEMPLATE
)

# Alternative: Personality-based prompts
PERSONALITY_PROMPTS = {
    "friendly": "Bạn là trợ lý nấu ăn thân thiện, nhiệt tình, hay dùng emoji 🍜👨‍🍳",
    "professional": "Bạn là đầu bếp chuyên nghiệp, giải thích chi tiết kỹ thuật nấu ăn",
    "humorous": "Bạn là trợ lý vui tính, hay đùa cợt nhẹ nhàng khi nấu ăn 😄",
    "nutritionist": "Bạn là chuyên gia dinh dưỡng, tập trung vào giá trị dinh dưỡng",
    "efficient": "Bạn trả lời ngắn gọn, súc tích, tập trung vào điểm chính"
}


# ============================================================================
# RAG QUERY IMPLEMENTATION
# ============================================================================

async def query_rag(
    question: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    user_context: Optional[Dict[str, Any]] = None,
    personality: str = "friendly",
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Query RAG system with conversation context
    
    Args:
        question: User question
        conversation_history: Previous messages
        user_context: User preferences, allergies, etc.
        personality: AI personality type
        top_k: Number of documents to retrieve
        
    Returns:
        Dict with answer, sources, and metadata
    """
    try:
        # Enhance question with user context
        enhanced_question = question
        if user_context:
            context_parts = []
            if user_context.get('dietary_preferences'):
                context_parts.append(f"Ưu tiên: {', '.join(user_context['dietary_preferences'])}")
            if user_context.get('allergies'):
                context_parts.append(f"Dị ứng: {', '.join(user_context['allergies'])}")
            
            if context_parts:
                enhanced_question = f"{question} ({'; '.join(context_parts)})"
        
        # Retrieve relevant documents
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": top_k,
                "score_threshold": 0.7
            }
        )
        
        docs = retriever.invoke(enhanced_question)
        
        # Build context from retrieved documents
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # Build chat history
        messages = []
        messages.append(SystemMessage(content=SYSTEM_PROMPT_TEMPLATE.format(
            context=context_text,
            chat_history="",
            question=enhanced_question
        )))
        
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=enhanced_question))
        
        # Generate response
        response = llm.invoke(messages)
        
        # Format response
        return {
            "answer": response.content,
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": doc.metadata.get("score", 0.0)
                }
                for doc in docs
            ],
            "enhanced_question": enhanced_question,
            "total_sources": len(docs)
        }
        
    except Exception as e:
        print(f"❌ RAG query error: {e}")
        # Fallback response
        return {
            "answer": "Xin lỗi, tôi đang gặp vấn đề kỹ thuật. Vui lòng thử lại sau!",
            "sources": [],
            "error": str(e)
        }


def search_recipes_semantic(
    query: str,
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Semantic search across recipes using Qdrant
    
    Args:
        query: Search query
        top_k: Number of results
        filters: Optional metadata filters (difficulty, category, etc.)
        
    Returns:
        List of matching recipes with scores
    """
    try:
        # Build Qdrant filter
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        qdrant_filter = None
        if filters:
            conditions = []
            if filters.get('difficulty'):
                conditions.append(
                    FieldCondition(key="difficulty", match=MatchValue(value=filters['difficulty']))
                )
            if filters.get('category_id'):
                conditions.append(
                    FieldCondition(key="category_id", match=MatchValue(value=str(filters['category_id'])))
                )
            if filters.get('is_vegetarian'):
                conditions.append(
                    FieldCondition(key="is_vegetarian", match=MatchValue(value=True))
                )
            
            if conditions:
                qdrant_filter = Filter(must=conditions)
        
        # Semantic search with scores using Qdrant
        results = vector_store.similarity_search_with_score(
            query=query,
            k=top_k,
            filter=qdrant_filter
        )
        
        # Format results
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score),  # Qdrant returns similarity directly
                "recipe_id": doc.metadata.get("recipe_id"),
                "title": doc.metadata.get("title", "Unknown"),
                "content_type": doc.metadata.get("content_type", "unknown")
            }
            for doc, score in results
        ]
        
    except Exception as e:
        print(f"❌ Semantic search error: {e}")
        return []


# ============================================================================
# INDEXING FUNCTIONS
# ============================================================================

async def index_recipe(recipe_data: Dict[str, Any]) -> bool:
    """
    Index a recipe into vector store
    
    Args:
        recipe_data: Recipe dict with title, description, ingredients, etc.
        
    Returns:
        Success status
    """
    try:
        # Prepare text chunks for embedding
        chunks = []
        
        # Chunk 1: Overview
        overview_text = f"{recipe_data['title_vi']} - {recipe_data.get('title_en', '')}\n"
        overview_text += f"{recipe_data['description_vi']}\n"
        overview_text += f"Độ khó: {recipe_data['difficulty']}\n"
        overview_text += f"Thời gian: {recipe_data['total_time_minutes']} phút\n"
        
        chunks.append({
            "text": overview_text,
            "metadata": {
                "recipe_id": str(recipe_data["id"]),
                "title": recipe_data["title_vi"],
                "content_type": "overview",
                "difficulty": recipe_data["difficulty"],
                "total_time": recipe_data["total_time_minutes"]
            }
        })
        
        # Chunk 2: Ingredients (if available)
        if recipe_data.get('ingredients'):
            ingredients_text = "Nguyên liệu:\n"
            for ing in recipe_data['ingredients']:
                ingredients_text += f"- {ing.get('name_vi', 'N/A')}\n"
            
            chunks.append({
                "text": ingredients_text,
                "metadata": {
                    "recipe_id": str(recipe_data["id"]),
                    "title": recipe_data["title_vi"],
                    "content_type": "ingredients"
                }
            })
        
        # Add chunks to vector store
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        vector_store.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Indexing error for recipe {recipe_data.get('id')}: {e}")
        return False


async def batch_index_recipes(recipes: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Batch index multiple recipes
    
    Args:
        recipes: List of recipe dicts
        
    Returns:
        Stats dict with success/failure counts
    """
    stats = {"success": 0, "failed": 0}
    
    for recipe in recipes:
        success = await index_recipe(recipe)
        if success:
            stats["success"] += 1
        else:
            stats["failed"] += 1
    
    return stats


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def init_qdrant_collection():
    """Initialize Qdrant collection if not exists"""
    try:
        from qdrant_client.models import VectorParams, Distance
        
        # Check if collection exists
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            # Create collection
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config={
                    "text_vector": VectorParams(
                        size=settings.QDRANT_VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                }
            )
            print(f"✅ Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
        else:
            print(f"✅ Qdrant collection already exists: {settings.QDRANT_COLLECTION_NAME}")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing Qdrant collection: {e}")
        return False


def clear_vector_store():
    """Clear all vectors from store (use with caution!)"""
    try:
        # Delete and recreate collection
        qdrant_client.delete_collection(settings.QDRANT_COLLECTION_NAME)
        init_qdrant_collection()
        print("✅ Vector store cleared")
    except Exception as e:
        print(f"❌ Error clearing vector store: {e}")


def get_vector_store_stats() -> Dict[str, Any]:
    """Get statistics about vector store"""
    try:
        collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)
        
        return {
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "embedding_model": settings.OPENAI_EMBEDDING_MODEL,
            "dimensions": settings.QDRANT_VECTOR_SIZE,
            "distance": settings.QDRANT_DISTANCE,
            "status": collection_info.status
        }
    except Exception as e:
        return {"error": str(e)}
