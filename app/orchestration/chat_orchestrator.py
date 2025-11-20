"""
Chat Orchestrator - Main controller for chat assistant
Handles intent detection, tool routing, and response synthesis with RAG
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from app.orchestration.tools import ALL_TOOLS
from app.services.rag_service import rag_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# System prompt for the chat assistant
SYSTEM_PROMPT = """Bạn là trợ lý nấu ăn thông minh chuyên nghiệp dành cho người Việt Nam.

VAI TRÒ VÀ NHIỆM VỤ:
- Tư vấn nấu ăn, thực đơn, công thức
- Giải đáp thắc mắc về kỹ thuật nấu ăn
- Gợi ý thay thế nguyên liệu
- Hỗ trợ khắc phục sự cố trong nấu ăn
- Tư vấn dinh dưỡng và sức khỏe

PHONG CÁCH GIAO TIẾP:
- Thân thiện, nhiệt tình, dễ hiểu
- Sử dụng tiếng Việt tự nhiên
- Giải thích chi tiết nhưng không dài dòng
- Đưa ra ví dụ cụ thể khi cần
- Quan tâm đến an toàn thực phẩm

CÔNG CỤ KHẢ DỤNG:
1. generate_menu: Tạo thực đơn cá nhân hóa
2. search_recipes: Tìm công thức nấu ăn
3. get_technique: Lấy thông tin kỹ thuật nấu ăn
4. substitute_ingredient: Tìm nguyên liệu thay thế
5. convert_units: Chuyển đổi đơn vị đo
6. get_user_allergies: Lấy thông tin dị ứng người dùng

HƯỚNG DẪN SỬ DỤNG CÔNG CỤ:
- Khi người dùng hỏi "tạo thực đơn", "gợi ý món ăn" → sử dụng generate_menu
- Khi hỏi "làm thế nào nấu X", "công thức X" → sử dụng search_recipes
- Khi hỏi về kỹ thuật cụ thể → sử dụng get_technique
- Khi hỏi "thay thế X bằng gì" → sử dụng substitute_ingredient
- Khi hỏi về chuyển đổi đơn vị → sử dụng convert_units

CÁCH TRẢ LỜI:
1. Nếu có thông tin từ công cụ hoặc cơ sở kiến thức → sử dụng thông tin đó
2. Nếu không có thông tin → trả lời dựa trên kiến thức chung
3. Luôn cung cấp giải thích rõ ràng, dễ hiểu
4. Thêm tips hữu ích khi phù hợp
5. Hỏi lại nếu câu hỏi không rõ ràng

LƯU Ý AN TOÀN:
- Cảnh báo về dị ứng thực phẩm
- Lưu ý về vệ sinh an toàn thực phẩm
- Không khuyến khích các phương pháp nấu ăn nguy hiểm
"""

# Few-shot examples
FEW_SHOT_EXAMPLES = """
VÍ DỤ TƯƠNG TÁC:

User: Tạo thực đơn cho mùa đông
Assistant: [Sử dụng generate_menu với season:đông] Đã tạo thực đơn phù hợp với mùa đông.

User: Làm thế nào để làm caramel không bị đắng?
Assistant: [Sử dụng get_technique với query:caramel] Để làm caramel không bị đắng, bạn cần...

User: Thay thế đường bằng gì?
Assistant: [Sử dụng substitute_ingredient với ingredient:đường] Bạn có thể thay thế đường bằng...

User: 100g bằng bao nhiêu cup?
Assistant: [Sử dụng convert_units] 100g phụ thuộc vào nguyên liệu. Ví dụ: 100g bột mì ≈ 0.8 cup...
"""

class ChatOrchestrator:
    """Main chat orchestrator with RAG and tool calling"""
    
    def __init__(self):
        """Initialize chat orchestrator"""
        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            temperature=settings.CHAT_TEMPERATURE,
            api_key=settings.CHAT_API_KEY,
            base_url=settings.CHAT_BASE_URL
        )
        self.tools = ALL_TOOLS
        self.rag_service = rag_service
        self.system_prompt = SYSTEM_PROMPT + "\n\n" + FEW_SHOT_EXAMPLES
    
    async def detect_intent(self, message: str) -> Dict[str, Any]:
        """
        Detect user intent from message
        
        Args:
            message: User message
            
        Returns:
            Intent dictionary with type and parameters
        """
        message_lower = message.lower()
        
        # Menu generation intent
        if any(keyword in message_lower for keyword in ["thực đơn", "menu", "gợi ý món", "nấu gì"]):
            return {"type": "menu_generation", "requires_rag": False}
        
        # Recipe search intent
        if any(keyword in message_lower for keyword in ["công thức", "cách làm", "cách nấu", "làm thế nào"]):
            return {"type": "recipe_search", "requires_rag": True}
        
        # Technique question intent
        if any(keyword in message_lower for keyword in ["kỹ thuật", "xào", "luộc", "chiên", "hấp", "caramel"]):
            return {"type": "technique", "requires_rag": True}
        
        # Ingredient substitute intent
        if any(keyword in message_lower for keyword in ["thay thế", "thay đổi", "không có", "hết"]):
            return {"type": "substitute", "requires_rag": True}
        
        # Unit conversion intent
        if any(keyword in message_lower for keyword in ["bao nhiêu", "chuyển đổi", "cup", "gram", "ml"]):
            return {"type": "conversion", "requires_rag": False}
        
        # Troubleshooting intent
        if any(keyword in message_lower for keyword in ["bị", "sao", "tại sao", "khắc phục", "sửa"]):
            return {"type": "troubleshooting", "requires_rag": True}
        
        # General question
        return {"type": "general", "requires_rag": True}
    
    async def get_rag_context(self, message: str, intent: Dict[str, Any]) -> Optional[str]:
        """
        Get relevant context from RAG if needed
        
        Args:
            message: User message
            intent: Detected intent
            
        Returns:
            Context string or None
        """
        if not intent.get("requires_rag", False):
            return None
        
        try:
            # Get context based on intent type
            if intent["type"] == "recipe_search":
                context = await self.rag_service.get_context_for_query(
                    query=message,
                    include_recipes=True,
                    include_techniques=True,
                    include_tips=False
                )
            elif intent["type"] == "technique":
                context = await self.rag_service.get_context_for_query(
                    query=message,
                    include_recipes=False,
                    include_techniques=True,
                    include_tips=True
                )
            elif intent["type"] == "troubleshooting":
                results = await self.rag_service.get_cooking_troubleshooting(message)
                context = "\n\n".join([r.text for r in results[:3]])
            else:
                context = await self.rag_service.get_context_for_query(
                    query=message,
                    include_recipes=True,
                    include_techniques=True,
                    include_tips=True
                )
            
            return context if context else None
        except Exception as e:
            logger.error(f"Error getting RAG context: {e}")
            return None
    
    async def chat(
        self,
        message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process chat message with RAG and tools
        
        Args:
            message: User message
            chat_history: Optional chat history
            user_id: Optional user ID
            
        Returns:
            Response dictionary with answer, sources, and metadata
        """
        try:
            # Detect intent
            intent = await self.detect_intent(message)
            logger.info(f"Detected intent: {intent['type']}")
            
            # Get RAG context if needed
            rag_context = await self.get_rag_context(message, intent)
            
            # Prepare input
            input_message = message
            if rag_context:
                input_message = f"""Thông tin từ cơ sở kiến thức:

{rag_context}

---

Câu hỏi của người dùng: {message}

Hãy trả lời dựa trên thông tin trên và kiến thức của bạn."""
            
            # Use LLM directly without agent (simplified version)
            response_text = await self.llm.ainvoke(input_message)
            result = {"output": response_text.content if hasattr(response_text, 'content') else str(response_text)}
            
            # Extract response
            response = {
                "answer": result.get("output", ""),
                "intent": intent["type"],
                "used_rag": rag_context is not None,
                "used_tools": bool(result.get("intermediate_steps", [])),
                "sources": self._extract_sources(rag_context) if rag_context else []
            }
            
            return response
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "answer": f"Xin lỗi, đã có lỗi xảy ra: {str(e)}",
                "intent": "error",
                "used_rag": False,
                "used_tools": False,
                "sources": []
            }
    
    def _extract_sources(self, context: str) -> List[Dict[str, str]]:
        """
        Extract source information from context
        
        Args:
            context: RAG context string
            
        Returns:
            List of source dictionaries
        """
        sources = []
        
        # Extract recipe titles
        import re
        recipe_matches = re.findall(r'\[CÔNG THỨC: ([^\]]+)\]', context)
        for match in recipe_matches:
            sources.append({"type": "recipe", "title": match.strip()})
        
        # Extract technique titles
        technique_matches = re.findall(r'\[KỸ THUẬT: ([^\]]+)\]', context)
        for match in technique_matches:
            sources.append({"type": "technique", "title": match.strip()})
        
        # Extract tip titles
        tip_matches = re.findall(r'\[MẸO: ([^\]]+)\]', context)
        for match in tip_matches:
            sources.append({"type": "tip", "title": match.strip()})
        
        return sources
    
    async def chat_simple(self, message: str) -> str:
        """
        Simple chat without RAG (for basic questions)
        
        Args:
            message: User message
            
        Returns:
            Response string
        """
        try:
            # Create messages for simple chat
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ]
            
            # Call LLM directly
            response = await self.llm.ainvoke(messages)
            
            # Extract content from response
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"Error in simple chat: {e}")
            return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"


# Singleton instance
chat_orchestrator = ChatOrchestrator()
