"""
OpenAI Service - Wrapper for OpenAI API calls
Handles menu generation, cooking instructions, and dish evaluation
"""

from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        """Initialize OpenAI client with configured base_url"""
        self.client = AsyncOpenAI(
            api_key=settings.CHAT_API_KEY,
            base_url=settings.CHAT_BASE_URL
        )
        self.model = settings.CHAT_MODEL
        self.max_tokens = settings.CHAT_MAX_TOKENS
        self.temperature = settings.CHAT_TEMPERATURE
    
    async def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call OpenAI API with system and user prompts
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            
        Returns:
            Generated text response
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def generate_menu(
        self,
        season: str,
        weather: str,
        allergies: str = None,
        budget: int = None,
        calories: int = None
    ) -> str:
        """
        Generate personalized menu based on parameters
        
        Args:
            season: Season (xuân, hạ, thu, đông)
            weather: Weather conditions
            allergies: Food allergies (optional)
            budget: Budget in VND (optional)
            calories: Target calories (optional)
            
        Returns:
            Generated menu text
        """
        system_prompt = """Bạn là một chuyên gia dinh dưỡng và đầu bếp chuyên nghiệp người Việt Nam.
Nhiệm vụ của bạn là tạo thực đơn cá nhân hóa chi tiết cho người dùng.
Thực đơn cần phù hợp với văn hóa ẩm thực Việt Nam, có cân đối dinh dưỡng và dễ thực hiện."""
        
        user_prompt = f"""Tạo một thực đơn cá nhân hóa cho 1 ngày với các thông tin sau:

- Mùa: {season}
- Thời tiết: {weather}"""
        
        if allergies:
            user_prompt += f"\n- Dị ứng/không ăn được: {allergies}"
        if budget:
            user_prompt += f"\n- Ngân sách: {budget:,} VNĐ/ngày"
        if calories:
            user_prompt += f"\n- Mục tiêu calories: {calories} kcal/ngày"
        
        user_prompt += """

Vui lòng đề xuất thực đơn cho 3 bữa (sáng, trưa, tối) với:
1. Tên món ăn
2. Nguyên liệu chính
3. Ước tính calories mỗi món
4. Ước tính giá tiền (nếu có ngân sách)
5. Lý do phù hợp với mùa và thời tiết

Trả lời bằng tiếng Việt, định dạng dễ đọc."""
        
        return await self._call_openai(system_prompt, user_prompt)
    
    async def get_cooking_instructions(
        self,
        dish_name: str,
        difficulty: str = None,
        servings: int = 2
    ) -> str:
        """
        Get detailed cooking instructions for a dish
        
        Args:
            dish_name: Name of the dish
            difficulty: Difficulty level (optional)
            servings: Number of servings
            
        Returns:
            Step-by-step cooking instructions
        """
        system_prompt = """Bạn là một đầu bếp chuyên nghiệp người Việt Nam.
Nhiệm vụ của bạn là cung cấp hướng dẫn nấu ăn chi tiết, dễ hiểu và chính xác."""
        
        user_prompt = f"""Hướng dẫn cách nấu món: {dish_name}

- Số người ăn: {servings} người"""
        
        if difficulty:
            user_prompt += f"\n- Độ khó mong muốn: {difficulty}"
        
        user_prompt += """

Vui lòng cung cấp:
1. Danh sách nguyên liệu chi tiết (có định lượng)
2. Các bước chuẩn bị
3. Các bước nấu nướng chi tiết
4. Mẹo và lưu ý quan trọng
5. Thời gian chuẩn bị và nấu

Trả lời bằng tiếng Việt, định dạng rõ ràng từng bước."""
        
        return await self._call_openai(system_prompt, user_prompt)
    
    async def optimize_menu(
        self,
        current_menu: str,
        user_feedback: str
    ) -> str:
        """
        Optimize menu based on user feedback
        
        Args:
            current_menu: Current menu content
            user_feedback: User requirements and feedback
            
        Returns:
            Optimized menu
        """
        system_prompt = """Bạn là một chuyên gia dinh dưỡng và đầu bếp chuyên nghiệp.
Nhiệm vụ của bạn là tối ưu hóa thực đơn dựa trên phản hồi của người dùng."""
        
        user_prompt = f"""Thực đơn hiện tại:
{current_menu}

Yêu cầu thay đổi:
{user_feedback}

Vui lòng tối ưu hóa thực đơn theo yêu cầu, giữ nguyên format và bổ sung giải thích cho các thay đổi.
Trả lời bằng tiếng Việt."""
        
        return await self._call_openai(system_prompt, user_prompt)
    
    async def evaluate_dish(
        self,
        dish_description: str
    ) -> str:
        """
        Evaluate a dish and provide nutritional feedback
        
        Args:
            dish_description: Description of the dish
            
        Returns:
            Dish evaluation and nutritional analysis
        """
        system_prompt = """Bạn là một chuyên gia dinh dưỡng chuyên nghiệp.
Nhiệm vụ của bạn là đánh giá món ăn về mặt dinh dưỡng và sức khỏe."""
        
        user_prompt = f"""Đánh giá món ăn sau:
{dish_description}

Vui lòng phân tích:
1. Giá trị dinh dưỡng tổng quan
2. Ưu điểm cho sức khỏe
3. Điểm cần lưu ý hoặc cải thiện
4. Phù hợp với nhóm đối tượng nào
5. Đề xuất điều chỉnh (nếu cần)

Trả lời bằng tiếng Việt, định dạng dễ đọc."""
        
        return await self._call_openai(system_prompt, user_prompt)


# Global instance
openai_service = OpenAIService()
