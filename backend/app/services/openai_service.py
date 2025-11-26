"""
OpenAI service wrapper for chat and embeddings
"""
from typing import List, Optional, Dict, Any, AsyncGenerator
import openai
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()


class OpenAIService:
    """Wrapper for OpenAI API calls with custom base URL support"""
    
    def __init__(self):
        """Initialize OpenAI clients with settings"""
        # Chat client
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            timeout=60.0,
            max_retries=3
        )
        
        # Embedding client (separate API key if provided)
        embedding_api_key = settings.OPENAI_EMBEDDING_API_KEY or settings.OPENAI_API_KEY
        self.embedding_client = AsyncOpenAI(
            api_key=embedding_api_key,
            base_url=settings.OPENAI_EMBEDDING_BASE_URL,
            timeout=60.0,
            max_retries=3
        )
        
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Any:
        """
        Generate chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            stream: Enable streaming response
            
        Returns:
            Chat completion response or stream
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=stream
            )
            return response
        except Exception as e:
            print(f"❌ OpenAI chat completion error: {e}")
            raise
    
    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion
        
        Args:
            messages: List of message dicts
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Yields:
            Text chunks from streaming response
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"❌ OpenAI streaming error: {e}")
            raise
    
    async def create_embedding(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        Generate embedding for text
        
        Args:
            text: Input text to embed
            model: Override default embedding model
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            response = await self.embedding_client.embeddings.create(
                model=model or self.embedding_model,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ OpenAI embedding error: {e}")
            raise
    
    async def create_embeddings_batch(
        self,
        texts: List[str],
        model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of input texts
            model: Override default embedding model
            
        Returns:
            List of embedding vectors
        """
        try:
            response = await self.embedding_client.embeddings.create(
                model=model or self.embedding_model,
                input=texts,
                encoding_format="float"
            )
            # Sort by index to maintain order
            return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
        except Exception as e:
            print(f"❌ OpenAI batch embedding error: {e}")
            raise
    
    async def moderate_content(self, text: str) -> Dict[str, Any]:
        """
        Check content for policy violations
        
        Args:
            text: Text to moderate
            
        Returns:
            Moderation results with categories and scores
        """
        try:
            response = await self.client.moderations.create(input=text)
            result = response.results[0]
            return {
                "flagged": result.flagged,
                "categories": result.categories.model_dump(),
                "category_scores": result.category_scores.model_dump()
            }
        except Exception as e:
            print(f"❌ OpenAI moderation error: {e}")
            raise


# Global singleton instance
_openai_service: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """Get or create OpenAI service singleton"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service


# Example usage functions
async def generate_recipe_embedding(recipe_text: str) -> List[float]:
    """
    Generate embedding for recipe content
    
    Args:
        recipe_text: Combined recipe title, ingredients, and instructions
        
    Returns:
        1536-dimensional embedding vector
    """
    service = get_openai_service()
    return await service.create_embedding(recipe_text)


async def chat_with_assistant(
    user_message: str,
    context: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Chat with cooking assistant
    
    Args:
        user_message: User's question
        context: Retrieved context from RAG
        conversation_history: Previous messages
        
    Returns:
        Assistant's response
    """
    service = get_openai_service()
    
    # Build messages
    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý nấu ăn AI thông minh, hữu ích và thân thiện. "
                      "Bạn giúp người dùng với công thức nấu ăn, mẹo vặt, và câu hỏi về ẩm thực."
        }
    ]
    
    # Add conversation history
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add context if provided
    if context:
        messages.append({
            "role": "system",
            "content": f"Thông tin tham khảo:\n{context}"
        })
    
    # Add user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Generate response
        response = await service.chat_completion(messages)
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e).lower()
        if "budget" in error_message or "exceeded" in error_message:
            # Return fallback response when budget is exceeded
            return "Xin chào! Tôi là trợ lý nấu ăn AI. Hiện tại dịch vụ AI đang tạm thời không khả dụng do hạn mức sử dụng. " \
                   "Tôi có thể giúp bạn với một số mẹo nấu ăn cơ bản:\n\n" \
                   "🍳 Món ăn đơn giản:\n" \
                   "- Phở bò: Nấu nước dùng từ xương bò, thêm bún tươi và thịt bò tái chín\n" \
                   "- Cơm tấm: Nướng thịt heo và ướp gia vị đậm đà\n" \
                   "- Canh chua: Dùng cá và rau củ tạo vị chua thanh\n\n" \
                   "💡 Mẹo vặt:\n" \
                   "- Luôn nêm nếm thức ăn trong quá trình nấu\n" \
                   "- Dùng lửa nhỏ để thức ăn chín đều\n" \
                   "- Bảo quản thực phẩm đúng cách để giữ độ tươi ngon\n\n" \
                   "Vui lòng thử lại sau hoặc liên hệ hỗ trợ để được giúp đỡ thêm!"
        else:
            # Re-raise other errors
            raise


async def chat_with_assistant_stream(
    user_message: str,
    context: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AsyncGenerator[str, None]:
    """
    Chat with cooking assistant (streaming version)
    
    Args:
        user_message: User's question
        context: Retrieved context from RAG
        conversation_history: Previous messages
        
    Yields:
        Text chunks from assistant response
    """
    service = get_openai_service()
    
    # Build messages (same as above)
    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý nấu ăn AI thông minh, hữu ích và thân thiện. "
                      "Bạn giúp người dùng với công thức nấu ăn, mẹo vặt, và câu hỏi về ẩm thực."
        }
    ]
    
    if conversation_history:
        messages.extend(conversation_history)
    
    if context:
        messages.append({
            "role": "system",
            "content": f"Thông tin tham khảo:\n{context}"
        })
    
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Stream response
        async for chunk in service.chat_completion_stream(messages):
            yield chunk
    except Exception as e:
        error_message = str(e).lower()
        if "budget" in error_message or "exceeded" in error_message:
            # Return fallback response when budget is exceeded
            fallback_response = "Xin chào! Tôi là trợ lý nấu ăn AI. Hiện tại dịch vụ AI đang tạm thời không khả dụng do hạn mức sử dụng. " \
                               "Tôi có thể giúp bạn với một số mẹo nấu ăn cơ bản:\n\n" \
                               "🍳 Món ăn đơn giản:\n" \
                               "- Phở bò: Nấu nước dùng từ xương bò, thêm bún tươi và thịt bò tái chín\n" \
                               "- Cơm tấm: Nướng thịt heo và ướp gia vị đậm đà\n" \
                               "- Canh chua: Dùng cá và rau củ tạo vị chua thanh\n\n" \
                               "💡 Mẹo vặt:\n" \
                               "- Luôn nêm nếm thức ăn trong quá trình nấu\n" \
                               "- Dùng lửa nhỏ để thức ăn chín đều\n" \
                               "- Bảo quản thực phẩm đúng cách để giữ độ tươi ngon\n\n" \
                               "Vui lòng thử lại sau hoặc liên hệ hỗ trợ để được giúp đỡ thêm!"
            yield fallback_response
        else:
            # Re-raise other errors
            raise
