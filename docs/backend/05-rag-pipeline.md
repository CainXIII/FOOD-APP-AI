# 🤖 RAG Pipeline Architecture - AI Cooking Assistant

Complete architecture for Retrieval-Augmented Generation (RAG) system using LangChain, pgvector, and OpenAI.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Components](#architecture-components)
3. [Data Indexing Pipeline](#data-indexing-pipeline)
4. [Query Processing Pipeline](#query-processing-pipeline)
5. [Vector Store Configuration](#vector-store-configuration)
6. [LangChain Integration](#langchain-integration)
7. [Prompt Engineering](#prompt-engineering)
8. [Context Management](#context-management)
9. [Performance Optimization](#performance-optimization)
10. [Monitoring & Observability](#monitoring--observability)

---

## 🎯 Overview

### What is RAG?

Retrieval-Augmented Generation combines:
1. **Retrieval**: Finding relevant context from knowledge base (recipes, ingredients, cooking tips)
2. **Augmentation**: Enriching user queries with retrieved context
3. **Generation**: Using LLM to generate informed responses

### Why RAG for Cooking Assistant?

- **Up-to-date information**: Access latest recipes without retraining models
- **Grounded responses**: Answers based on actual recipes in database
- **Source attribution**: Show which recipes informed the response
- **Cost-effective**: Cheaper than fine-tuning for every recipe update
- **Contextual**: Understands user's cooking session, preferences, history

---

## 🏗️ Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                            │
│          (Text, Voice, Wake Word Triggered)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Query Processing                            │
│  • Language Detection                                        │
│  • Intent Classification                                     │
│  • Entity Extraction                                         │
│  • Query Embedding (text-embedding-3-small)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Hybrid Search                               │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Vector Search    │  │ Full-Text Search │                │
│  │ (pgvector)       │  │ (PostgreSQL FTS) │                │
│  │ Similarity: 0.7+ │  │ ts_rank > 0.1    │                │
│  └──────────────────┘  └──────────────────┘                │
│           │                      │                           │
│           └──────────┬───────────┘                           │
│                      ▼                                        │
│           ┌──────────────────┐                              │
│           │ Result Fusion    │                              │
│           │ (RRF Algorithm)  │                              │
│           └──────────────────┘                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Context Retrieval & Ranking                     │
│  • Top-K Selection (k=5)                                     │
│  • Re-ranking (Cross-Encoder)                                │
│  • Context Filtering (user preferences, allergies)          │
│  • Metadata Enrichment                                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Prompt Construction                             │
│  • System Prompt (AI Personality)                            │
│  • User Context (preferences, history, session)             │
│  • Retrieved Context (recipes, ingredients, tips)           │
│  • Conversation History (last 5 messages)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               LLM Generation (GPT-4o)                        │
│  • Temperature: 0.7                                          │
│  • Max Tokens: 1000                                          │
│  • Stream: True                                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│             Response Post-Processing                         │
│  • Source Attribution                                        │
│  • Safety Filtering                                          │
│  • TTS Generation (if voice enabled)                        │
│  • Logging & Analytics                                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    User Response                             │
│      (Text + Audio + Source Links)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Indexing Pipeline

### 1. Content Preparation

**What to Index:**
- ✅ Recipe full content (title, description, ingredients, steps)
- ✅ Ingredient details (names, nutritional info, substitutes)
- ✅ Recipe tips and notes
- ✅ User reviews and comments (high-rated ones)
- ✅ Cooking techniques and terminology

**Content Chunking Strategy:**

```python
from typing import List, Dict

def chunk_recipe(recipe: Dict) -> List[Dict]:
    """
    Split recipe into semantic chunks for better retrieval
    """
    chunks = []
    
    # Chunk 1: Recipe overview
    overview = {
        "content": f"{recipe['title_vi']} - {recipe['title_en']}\n"
                   f"{recipe['description_vi']}\n"
                   f"Thời gian: {recipe['total_time_minutes']} phút\n"
                   f"Độ khó: {recipe['difficulty']}\n"
                   f"Khẩu phần: {recipe['servings']} người",
        "metadata": {
            "type": "recipe_overview",
            "recipe_id": recipe['id'],
            "difficulty": recipe['difficulty'],
            "time_minutes": recipe['total_time_minutes']
        }
    }
    chunks.append(overview)
    
    # Chunk 2: Ingredients
    ingredients_text = "Nguyên liệu:\n"
    for ing in recipe['ingredients']:
        ingredients_text += f"- {ing['name_vi']}: {ing['quantity']} {ing['unit']}\n"
    
    chunks.append({
        "content": ingredients_text,
        "metadata": {
            "type": "recipe_ingredients",
            "recipe_id": recipe['id']
        }
    })
    
    # Chunk 3-N: Each cooking step
    for step in recipe['steps']:
        step_text = (
            f"Bước {step['step_number']}: {step['title_vi']}\n"
            f"{step['instruction_vi']}\n"
        )
        if step['tips']:
            step_text += f"Mẹo: {step['tips']}\n"
        
        chunks.append({
            "content": step_text,
            "metadata": {
                "type": "recipe_step",
                "recipe_id": recipe['id'],
                "step_number": step['step_number']
            }
        })
    
    # Chunk N+1: Nutrition facts
    if recipe['nutrition_facts']:
        nutrition = recipe['nutrition_facts']
        nutrition_text = (
            f"Thông tin dinh dưỡng (mỗi phần):\n"
            f"Calories: {nutrition['calories']} kcal\n"
            f"Protein: {nutrition['protein_g']}g\n"
            f"Carbs: {nutrition['carbs_g']}g\n"
            f"Fat: {nutrition['fat_g']}g"
        )
        chunks.append({
            "content": nutrition_text,
            "metadata": {
                "type": "recipe_nutrition",
                "recipe_id": recipe['id']
            }
        })
    
    return chunks
```

### 2. Embedding Generation

```python
from openai import OpenAI
import asyncio
from typing import List

client = OpenAI(api_key="your-api-key")

async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using OpenAI's text-embedding-3-small
    Batch size: 100 texts per request
    """
    embeddings = []
    batch_size = 100
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
            dimensions=1536  # Default dimension
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
    
    return embeddings
```

### 3. Vector Store Insertion

```python
import psycopg2
from pgvector.psycopg2 import register_vector

def insert_embeddings(conn, chunks: List[Dict], embeddings: List[List[float]]):
    """
    Insert embeddings into PostgreSQL with pgvector
    """
    register_vector(conn)
    cursor = conn.cursor()
    
    for chunk, embedding in zip(chunks, embeddings):
        cursor.execute("""
            INSERT INTO recipe_embeddings (
                id, recipe_id, content_type, content_text, 
                embedding, metadata, embedding_model
            ) VALUES (
                gen_random_uuid(), 
                %(recipe_id)s, 
                %(content_type)s,
                %(content_text)s,
                %(embedding)s,
                %(metadata)s,
                'text-embedding-3-small'
            )
        """, {
            'recipe_id': chunk['metadata']['recipe_id'],
            'content_type': chunk['metadata']['type'],
            'content_text': chunk['content'],
            'embedding': embedding,
            'metadata': chunk['metadata']
        })
    
    conn.commit()
```

### 4. Full-Text Search Index

```sql
-- Create tsvector column for full-text search
ALTER TABLE recipes 
ADD COLUMN search_vector tsvector 
GENERATED ALWAYS AS (
    setweight(to_tsvector('vietnamese', coalesce(title_vi, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(title_en, '')), 'A') ||
    setweight(to_tsvector('vietnamese', coalesce(description_vi, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(description_en, '')), 'B')
) STORED;

-- Create GIN index for fast full-text search
CREATE INDEX idx_recipes_search_vector ON recipes USING GIN (search_vector);
```

### 5. Indexing Schedule

**Initial Indexing:**
- All existing recipes, ingredients, content
- Run as batch job: `python scripts/index_all_content.py`

**Incremental Indexing:**
- Trigger on recipe create/update via database trigger
- Background worker processes new content every 5 minutes
- Use message queue (Redis Queue) for async processing

```python
# Example: Trigger indexing on recipe insert
@app.post("/recipes")
async def create_recipe(recipe: RecipeCreate, background_tasks: BackgroundTasks):
    # Save recipe to database
    new_recipe = await save_recipe(recipe)
    
    # Queue indexing job
    background_tasks.add_task(index_recipe, new_recipe.id)
    
    return new_recipe
```

---

## 🔍 Query Processing Pipeline

### 1. Intent Classification

```python
from enum import Enum
from typing import Optional

class QueryIntent(Enum):
    RECIPE_SEARCH = "recipe_search"           # "tìm công thức phở"
    INGREDIENT_INFO = "ingredient_info"       # "thông tin về gừng"
    COOKING_HELP = "cooking_help"             # "làm sao để..."
    SUBSTITUTION = "substitution"             # "thay thế tôm bằng gì"
    NUTRITION = "nutrition"                   # "calories trong phở"
    TIMING = "timing"                         # "nấu bao lâu"
    GENERAL_CHAT = "general_chat"             # "xin chào"

def classify_intent(query: str, context: Optional[Dict] = None) -> QueryIntent:
    """
    Classify user intent using simple rules or lightweight classifier
    """
    query_lower = query.lower()
    
    # Recipe search keywords
    if any(kw in query_lower for kw in ['tìm', 'công thức', 'nấu', 'làm', 'món']):
        return QueryIntent.RECIPE_SEARCH
    
    # Ingredient info
    if any(kw in query_lower for kw in ['nguyên liệu', 'thành phần', 'là gì']):
        return QueryIntent.INGREDIENT_INFO
    
    # Cooking help
    if any(kw in query_lower for kw in ['làm sao', 'cách', 'hướng dẫn', 'bước']):
        return QueryIntent.COOKING_HELP
    
    # Substitution
    if any(kw in query_lower for kw in ['thay thế', 'thay', 'không có']):
        return QueryIntent.SUBSTITUTION
    
    # Nutrition
    if any(kw in query_lower for kw in ['calories', 'dinh dưỡng', 'protein', 'carb']):
        return QueryIntent.NUTRITION
    
    # If user is in active cooking session, default to cooking help
    if context and context.get('cooking_session_id'):
        return QueryIntent.COOKING_HELP
    
    return QueryIntent.GENERAL_CHAT
```

### 2. Query Enhancement

```python
def enhance_query(query: str, user_context: Dict) -> str:
    """
    Enhance query with user preferences and context
    """
    enhancements = []
    
    # Add dietary preferences
    if user_context.get('dietary_preferences'):
        dietary = ", ".join(user_context['dietary_preferences'])
        enhancements.append(f"Ưu tiên món {dietary}")
    
    # Add allergy information
    if user_context.get('allergies'):
        allergies = ", ".join(user_context['allergies'])
        enhancements.append(f"Không chứa {allergies}")
    
    # Add cooking session context
    if user_context.get('current_recipe'):
        recipe_title = user_context['current_recipe']['title_vi']
        enhancements.append(f"Liên quan đến món {recipe_title}")
    
    if enhancements:
        enhanced = f"{query} ({'; '.join(enhancements)})"
    else:
        enhanced = query
    
    return enhanced
```

### 3. Hybrid Search

```python
from typing import List, Tuple

async def hybrid_search(
    query: str,
    user_context: Dict,
    top_k: int = 5
) -> List[Dict]:
    """
    Combine vector similarity search with full-text search
    """
    # Generate query embedding
    query_embedding = await generate_embeddings([query])
    query_vector = query_embedding[0]
    
    # Vector search (semantic similarity)
    vector_results = await vector_search(
        query_vector=query_vector,
        top_k=top_k * 2,  # Get more candidates
        filters=build_filters(user_context)
    )
    
    # Full-text search (keyword matching)
    fts_results = await fulltext_search(
        query=query,
        top_k=top_k * 2,
        filters=build_filters(user_context)
    )
    
    # Fusion using Reciprocal Rank Fusion (RRF)
    fused_results = reciprocal_rank_fusion(
        vector_results,
        fts_results,
        k=60  # RRF constant
    )
    
    # Return top-k after fusion
    return fused_results[:top_k]

def reciprocal_rank_fusion(
    list1: List[Tuple[str, float]],
    list2: List[Tuple[str, float]],
    k: int = 60
) -> List[Dict]:
    """
    RRF algorithm for combining ranked lists
    Score = 1 / (k + rank)
    """
    scores = {}
    
    # Add scores from first list
    for rank, (doc_id, score) in enumerate(list1, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Add scores from second list
    for rank, (doc_id, score) in enumerate(list2, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Sort by combined score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return [{"doc_id": doc_id, "score": score} for doc_id, score in ranked]
```

### 4. Vector Search Implementation

```python
async def vector_search(
    query_vector: List[float],
    top_k: int = 5,
    filters: Optional[Dict] = None
) -> List[Dict]:
    """
    Perform vector similarity search using pgvector
    """
    # Build filter conditions
    filter_conditions = []
    params = {'query_vector': query_vector, 'top_k': top_k}
    
    if filters:
        if filters.get('difficulty'):
            filter_conditions.append("r.difficulty = %(difficulty)s")
            params['difficulty'] = filters['difficulty']
        
        if filters.get('max_time'):
            filter_conditions.append("r.total_time_minutes <= %(max_time)s")
            params['max_time'] = filters['max_time']
        
        if filters.get('is_vegetarian'):
            filter_conditions.append("r.is_vegetarian = true")
        
        if filters.get('exclude_allergens'):
            filter_conditions.append(
                "NOT (r.allergens && %(allergens)s::text[])"
            )
            params['allergens'] = filters['exclude_allergens']
    
    where_clause = " AND " + " AND ".join(filter_conditions) if filter_conditions else ""
    
    query = f"""
        SELECT 
            re.id,
            re.recipe_id,
            re.content_text,
            re.content_type,
            re.metadata,
            r.title_vi,
            r.title_en,
            r.slug,
            1 - (re.embedding <=> %(query_vector)s) as similarity_score
        FROM recipe_embeddings re
        JOIN recipes r ON re.recipe_id = r.id
        WHERE r.is_published = true
        {where_clause}
        ORDER BY re.embedding <=> %(query_vector)s
        LIMIT %(top_k)s
    """
    
    results = await db.fetch_all(query=query, values=params)
    return [dict(r) for r in results]
```

### 5. Full-Text Search Implementation

```sql
-- Full-text search query
SELECT 
    r.id,
    r.title_vi,
    r.title_en,
    r.slug,
    ts_rank(r.search_vector, websearch_to_tsquery('vietnamese', :query)) as rank_score
FROM recipes r
WHERE 
    r.search_vector @@ websearch_to_tsquery('vietnamese', :query)
    AND r.is_published = true
ORDER BY rank_score DESC
LIMIT :top_k;
```

---

## 🗄️ Vector Store Configuration

### pgvector Setup

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create index for fast similarity search
-- Using IVFFlat (Inverted File with Flat compression)
CREATE INDEX idx_recipe_embeddings_vector 
ON recipe_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- For better recall, also create HNSW index (PostgreSQL 15+)
CREATE INDEX idx_recipe_embeddings_hnsw
ON recipe_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Index Selection Guidelines

**IVFFlat:**
- Good for: Large datasets (100K+ vectors)
- Build time: Fast
- Search speed: Good
- Recall: 90-95%
- Configuration: `lists = sqrt(num_rows)`

**HNSW:**
- Good for: High-accuracy requirements
- Build time: Slower
- Search speed: Faster
- Recall: 95-99%
- Configuration: `m=16` (connections), `ef_construction=64` (build quality)

**For our use case (< 50K recipes):**
- Use **HNSW** for better accuracy
- Re-build index weekly or after 10% data growth

---

## 🔗 LangChain Integration

### 1. Setup LangChain Components

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Initialize embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.OPENAI_API_KEY
)

# Initialize vector store
vector_store = PGVector(
    connection_string=settings.DATABASE_URL,
    embedding_function=embeddings,
    collection_name="recipe_embeddings",
    distance_strategy="cosine"
)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=1000,
    streaming=True,
    openai_api_key=settings.OPENAI_API_KEY
)

# Initialize memory for conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)
```

### 2. Create RAG Chain

```python
from langchain.chains import ConversationalRetrievalChain

def create_rag_chain(user_context: Dict):
    """
    Create RAG chain with user-specific configuration
    """
    # Get AI personality from user preferences
    personality = user_context.get('ai_personality', 'friendly')
    
    # Custom prompt based on personality
    system_prompt = get_system_prompt(personality)
    
    # Create retrieval chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,
                "score_threshold": 0.7,
                "filter": build_metadata_filter(user_context)
            }
        ),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={
            "prompt": PromptTemplate.from_template(system_prompt)
        }
    )
    
    return qa_chain
```

### 3. Process User Query

```python
async def process_chat_message(
    conversation_id: str,
    user_message: str,
    user_context: Dict
) -> Dict:
    """
    Process user message through RAG pipeline
    """
    # Classify intent
    intent = classify_intent(user_message, user_context)
    
    # Enhance query
    enhanced_query = enhance_query(user_message, user_context)
    
    # Load conversation history
    history = await load_conversation_history(conversation_id, limit=5)
    
    # Create RAG chain
    qa_chain = create_rag_chain(user_context)
    
    # Generate response
    response = await qa_chain.ainvoke({
        "question": enhanced_query,
        "chat_history": history
    })
    
    # Extract sources
    sources = [
        {
            "type": doc.metadata.get("type"),
            "recipe_id": doc.metadata.get("recipe_id"),
            "step_number": doc.metadata.get("step_number"),
            "similarity_score": doc.metadata.get("score")
        }
        for doc in response.get("source_documents", [])
    ]
    
    return {
        "answer": response["answer"],
        "sources": sources,
        "intent": intent.value,
        "enhanced_query": enhanced_query
    }
```

---

## 📝 Prompt Engineering

### System Prompts by Personality

```python
SYSTEM_PROMPTS = {
    "friendly": """
Bạn là trợ lý nấu ăn AI thân thiện và nhiệt tình. Nhiệm vụ của bạn là giúp người dùng nấu ăn ngon hơn.

Phong cách:
- Dùng ngôn ngữ thân thiện, gần gũi
- Dùng emoji phù hợp (🍜, 👨‍🍳, 😊)
- Khuyến khích và động viên người dùng
- Chia sẻ tips và tricks hữu ích

Nguyên tắc:
1. Trả lời dựa trên thông tin từ công thức được cung cấp
2. Nếu không chắc chắn, thừa nhận và đưa ra gợi ý thay thế
3. Luôn chú ý đến dị ứng và sở thích ăn uống của người dùng
4. Đưa ra câu trả lời ngắn gọn, dễ hiểu

Thông tin người dùng:
- Sở thích: {dietary_preferences}
- Dị ứng: {allergies}
- Khẩu phần mặc định: {default_servings} người

Context từ công thức:
{context}

Hãy trả lời câu hỏi sau:
""",
    
    "professional": """
Bạn là đầu bếp chuyên nghiệp với kinh nghiệm nhiều năm. Trả lời với thái độ chuyên nghiệp và chính xác.

Phong cách:
- Sử dụng thuật ngữ nấu ăn chính xác
- Giải thích kỹ thuật và nguyên lý
- Đưa ra lời khuyên dựa trên kinh nghiệm
- Nghiêm túc nhưng không khô khan

Nguyên tắc:
1. Độ chính xác cao trong hướng dẫn
2. Giải thích rõ ràng "tại sao" đằng sau mỗi bước
3. Đề xuất biến thể và cải tiến
4. Chú ý đến an toàn thực phẩm

Context:
{context}

Câu hỏi:
""",
    
    "humorous": """
Bạn là trợ lý nấu ăn vui tính, thích đùa cợt nhưng vẫn hữu ích.

Phong cách:
- Sử dụng ngôn ngữ hài hước, nhẹ nhàng
- Thêm chút humor vào câu trả lời
- Tạo không khí thoải mái khi nấu ăn
- Dùng emoji và biểu cảm 😄🎉

Nguyên tắc:
1. Vẫn đảm bảo thông tin chính xác
2. Không đùa về dị ứng hoặc an toàn thực phẩm
3. Giữ mức độ hài hước vừa phải
4. Khuyến khích người dùng thử nghiệm

Context:
{context}

""",
    
    "nutritionist": """
Bạn là chuyên gia dinh dưỡng, tập trung vào sức khỏe và cân bằng dinh dưỡng.

Phong cách:
- Nhấn mạnh giá trị dinh dưỡng
- Giải thích lợi ích sức khỏe
- Đề xuất thay thế lành mạnh hơn
- Cung cấp thông tin calories và macros

Nguyên tắc:
1. Luôn đề cập thông tin dinh dưỡng khi có thể
2. Đề xuất cách điều chỉnh món ăn cho healthy hơn
3. Cân nhắc nhu cầu dinh dưỡng cá nhân
4. Giáo dục về nguyên liệu và tác dụng

Context:
{context}

""",
    
    "efficient": """
Bạn là trợ lý nấu ăn hiệu quả, tập trung vào việc tiết kiệm thời gian.

Phong cách:
- Ngắn gọn, súc tích
- Tập trung vào điểm chính
- Đề xuất shortcuts và tips tiết kiệm thời gian
- Ưu tiên tính thực tế

Nguyên tắc:
1. Câu trả lời ngắn gọn nhưng đầy đủ
2. Đưa ra giải pháp nhanh nhất
3. Tối ưu hóa quy trình nấu ăn
4. Đề xuất chuẩn bị trước (meal prep)

Context:
{context}

"""
}

def get_system_prompt(personality: str) -> str:
    """Get system prompt based on AI personality"""
    return SYSTEM_PROMPTS.get(personality, SYSTEM_PROMPTS["friendly"])
```

---

## 🧠 Context Management

### Context Window Strategy

```python
def build_context_window(
    retrieved_docs: List[Dict],
    user_context: Dict,
    conversation_history: List[Dict],
    max_tokens: int = 4000
) -> str:
    """
    Build context window within token limits
    Priority: Current session > Retrieved docs > History
    """
    context_parts = []
    estimated_tokens = 0
    
    # Part 1: Current cooking session (highest priority)
    if user_context.get('cooking_session'):
        session = user_context['cooking_session']
        session_context = f"""
Phiên nấu ăn hiện tại:
- Món: {session['recipe_title']}
- Bước hiện tại: {session['current_step']}/{session['total_steps']}
- Thời gian đã nấu: {session['elapsed_time']} phút
"""
        context_parts.append(session_context)
        estimated_tokens += count_tokens(session_context)
    
    # Part 2: Retrieved documents (medium priority)
    docs_context = "\n\n".join([
        f"[{doc['content_type']}] {doc['content_text']}"
        for doc in retrieved_docs
    ])
    if estimated_tokens + count_tokens(docs_context) < max_tokens:
        context_parts.append(docs_context)
        estimated_tokens += count_tokens(docs_context)
    else:
        # Truncate docs if needed
        truncated_docs = truncate_to_tokens(
            docs_context,
            max_tokens - estimated_tokens - 500  # Reserve 500 for history
        )
        context_parts.append(truncated_docs)
        estimated_tokens += count_tokens(truncated_docs)
    
    # Part 3: Conversation history (lower priority)
    if conversation_history:
        history_context = format_conversation_history(conversation_history)
        remaining_tokens = max_tokens - estimated_tokens
        
        if remaining_tokens > 200:
            history_context = truncate_to_tokens(history_context, remaining_tokens)
            context_parts.append(history_context)
    
    return "\n\n---\n\n".join(context_parts)

def count_tokens(text: str) -> int:
    """Estimate token count (rough approximation)"""
    return len(text) // 4  # Roughly 4 chars per token

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to fit within token limit"""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."
```

---

## ⚡ Performance Optimization

### 1. Caching Strategy

```python
from redis import Redis
import pickle
import hashlib

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=False
)

def cache_embedding(text: str, embedding: List[float], ttl: int = 86400):
    """Cache embedding for 24 hours"""
    key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
    redis_client.setex(key, ttl, pickle.dumps(embedding))

def get_cached_embedding(text: str) -> Optional[List[float]]:
    """Get cached embedding if exists"""
    key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
    cached = redis_client.get(key)
    if cached:
        return pickle.loads(cached)
    return None

async def generate_embeddings_with_cache(texts: List[str]) -> List[List[float]]:
    """Generate embeddings with caching"""
    embeddings = []
    texts_to_embed = []
    cache_indices = []
    
    # Check cache first
    for i, text in enumerate(texts):
        cached = get_cached_embedding(text)
        if cached:
            embeddings.append(cached)
        else:
            texts_to_embed.append(text)
            cache_indices.append(i)
    
    # Generate missing embeddings
    if texts_to_embed:
        new_embeddings = await generate_embeddings(texts_to_embed)
        
        # Cache new embeddings
        for text, embedding in zip(texts_to_embed, new_embeddings):
            cache_embedding(text, embedding)
        
        # Merge results
        for idx, embedding in zip(cache_indices, new_embeddings):
            embeddings.insert(idx, embedding)
    
    return embeddings
```

### 2. Query Result Caching

```python
def cache_search_results(query: str, results: List[Dict], ttl: int = 3600):
    """Cache search results for 1 hour"""
    key = f"search:{hashlib.md5(query.encode()).hexdigest()}"
    redis_client.setex(key, ttl, pickle.dumps(results))

def get_cached_search_results(query: str) -> Optional[List[Dict]]:
    """Get cached search results"""
    key = f"search:{hashlib.md5(query.encode()).hexdigest()}"
    cached = redis_client.get(key)
    if cached:
        return pickle.loads(cached)
    return None
```

### 3. Batch Processing

```python
from typing import List
import asyncio

async def process_queries_batch(queries: List[str]) -> List[Dict]:
    """Process multiple queries in parallel"""
    tasks = [process_chat_message(q['conversation_id'], q['message'], q['context']) 
             for q in queries]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return [r if not isinstance(r, Exception) else {"error": str(r)} 
            for r in results]
```

### 4. Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,          # Number of connections to maintain
    max_overflow=10,       # Additional connections when pool is full
    pool_pre_ping=True,    # Verify connections before using
    pool_recycle=3600      # Recycle connections after 1 hour
)

async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
```

---

## 📊 Monitoring & Observability

### 1. Metrics to Track

```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
rag_requests_total = Counter(
    'rag_requests_total',
    'Total RAG requests',
    ['intent', 'status']
)

rag_latency = Histogram(
    'rag_latency_seconds',
    'RAG request latency',
    ['component']
)

# Quality metrics
rag_similarity_score = Histogram(
    'rag_similarity_score',
    'Average similarity score of retrieved documents'
)

rag_source_count = Histogram(
    'rag_source_count',
    'Number of sources used in response'
)

# Token usage
openai_tokens_used = Counter(
    'openai_tokens_used_total',
    'Total OpenAI tokens used',
    ['model', 'type']
)

# Cache metrics
embedding_cache_hits = Counter(
    'embedding_cache_hits_total',
    'Embedding cache hits'
)

embedding_cache_misses = Counter(
    'embedding_cache_misses_total',
    'Embedding cache misses'
)
```

### 2. Logging

```python
import logging
import json

logger = logging.getLogger(__name__)

def log_rag_request(
    conversation_id: str,
    user_message: str,
    response: Dict,
    latency_ms: float
):
    """Log RAG request details"""
    log_data = {
        "event": "rag_request",
        "conversation_id": conversation_id,
        "user_message_length": len(user_message),
        "response_length": len(response.get("answer", "")),
        "num_sources": len(response.get("sources", [])),
        "avg_similarity": calculate_avg_similarity(response.get("sources", [])),
        "latency_ms": latency_ms,
        "intent": response.get("intent"),
        "model": "gpt-4o"
    }
    
    logger.info(json.dumps(log_data))
```

### 3. Evaluation Metrics

```python
from typing import List, Dict

def calculate_retrieval_metrics(
    query: str,
    retrieved_docs: List[Dict],
    ground_truth_doc_ids: List[str]
) -> Dict:
    """
    Calculate retrieval quality metrics
    """
    retrieved_ids = [doc['recipe_id'] for doc in retrieved_docs]
    
    # Precision@K
    relevant_retrieved = len(set(retrieved_ids) & set(ground_truth_doc_ids))
    precision_at_k = relevant_retrieved / len(retrieved_ids) if retrieved_ids else 0
    
    # Recall@K
    recall_at_k = relevant_retrieved / len(ground_truth_doc_ids) if ground_truth_doc_ids else 0
    
    # Mean Reciprocal Rank (MRR)
    mrr = 0
    for i, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in ground_truth_doc_ids:
            mrr = 1 / i
            break
    
    # Average similarity score
    avg_similarity = sum(doc.get('similarity_score', 0) for doc in retrieved_docs) / len(retrieved_docs)
    
    return {
        "precision_at_k": precision_at_k,
        "recall_at_k": recall_at_k,
        "mrr": mrr,
        "avg_similarity": avg_similarity
    }
```

### 4. A/B Testing

```python
import random

def select_rag_variant(user_id: str) -> str:
    """
    Select RAG variant for A/B testing
    """
    # Consistent variant selection based on user_id
    hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    
    variants = {
        "control": 0.5,      # 50%: Current RAG setup
        "variant_a": 0.25,   # 25%: Different prompt template
        "variant_b": 0.25    # 25%: Different retrieval params
    }
    
    rand = (hash_val % 100) / 100
    cumulative = 0
    
    for variant, probability in variants.items():
        cumulative += probability
        if rand < cumulative:
            return variant
    
    return "control"

def get_rag_config(variant: str) -> Dict:
    """Get RAG configuration for variant"""
    configs = {
        "control": {
            "top_k": 5,
            "similarity_threshold": 0.7,
            "temperature": 0.7
        },
        "variant_a": {
            "top_k": 3,
            "similarity_threshold": 0.8,
            "temperature": 0.5
        },
        "variant_b": {
            "top_k": 7,
            "similarity_threshold": 0.6,
            "temperature": 0.9
        }
    }
    return configs.get(variant, configs["control"])
```

---

## 🎯 Summary

### Key Components

1. **Data Indexing**: Chunk recipes → Generate embeddings → Store in pgvector
2. **Query Processing**: Intent classification → Query enhancement → Hybrid search
3. **Retrieval**: Vector similarity + Full-text search → Fusion → Re-ranking
4. **Generation**: Context assembly → LLM generation → Response formatting
5. **Optimization**: Caching, batching, connection pooling
6. **Monitoring**: Metrics, logging, evaluation

### Performance Targets

- **Embedding generation**: < 200ms for single query
- **Vector search**: < 50ms for top-5 results
- **Total RAG latency**: < 2 seconds (end-to-end)
- **Cache hit rate**: > 60% for embeddings
- **Retrieval precision**: > 0.8 for top-5 results
- **User satisfaction**: > 4.5/5 rating

### Cost Optimization

- **Embedding caching**: Reduce OpenAI API calls by 60-70%
- **Query result caching**: Reduce redundant searches
- **Batch processing**: Process multiple embeddings in single API call
- **Model selection**: Use `text-embedding-3-small` (cheaper) instead of `text-embedding-3-large`
- **Token optimization**: Truncate context to fit within limits

---

**Next Steps**:
- ✅ RAG Pipeline Architecture completed
- ⏳ Authentication & Authorization (next)
- ⏳ Caching Strategy
- ⏳ Phase 4: Implementation
