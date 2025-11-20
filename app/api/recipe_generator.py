from app.services.openai_service import OpenAIService

class RecipeGenerator:
    def __init__(self, openai_service: OpenAIService = None):
        self.openai_service = openai_service or OpenAIService()

    def generate_menu(self, season: str = None, weather: str = None, allergies: str = None, 
                     health: str = None, budget: float = None, calories: int = None):
        """
        Tạo thực đơn cá nhân hóa dựa trên nhiều yếu tố
        """
        system_prompt = """Bạn là một chuyên gia dinh dưỡng và đầu bếp chuyên nghiệp. 
        Nhiệm vụ của bạn là tạo thực đơn cá nhân hóa chi tiết cho người dùng."""
        
        prompt_parts = ["Tạo một thực đơn cá nhân hóa với các thông tin sau:"]
        
        if season:
            prompt_parts.append(f"- Mùa: {season}")
        if weather:
            prompt_parts.append(f"- Thời tiết: {weather}")
        if allergies:
            prompt_parts.append(f"- Dị ứng/không ăn được: {allergies}")
        if health:
            prompt_parts.append(f"- Tình trạng sức khỏe: {health}")
        if budget:
            prompt_parts.append(f"- Ngân sách: {budget} VNĐ")
        if calories:
            prompt_parts.append(f"- Mục tiêu calories: {calories} kcal/ngày")
        
        prompt_parts.append("\nVui lòng đề xuất thực đơn cho 3 bữa (sáng, trưa, tối) với:")
        prompt_parts.append("1. Tên món ăn")
        prompt_parts.append("2. Nguyên liệu chính")
        prompt_parts.append("3. Calories ước tính")
        prompt_parts.append("4. Lý do phù hợp với yêu cầu")
        
        prompt = "\n".join(prompt_parts)
        response = self.openai_service.call_openai_api(prompt, system_prompt)
        return self.openai_service.process_response(response)

    def get_cooking_instructions(self, dish_name: str):
        """
        Lấy hướng dẫn nấu ăn chi tiết theo từng bước
        """
        system_prompt = """Bạn là một đầu bếp chuyên nghiệp, hãy hướng dẫn nấu ăn rõ ràng, 
        chi tiết từng bước để người mới cũng có thể làm được."""
        
        prompt = f"""Hãy cung cấp hướng dẫn nấu món '{dish_name}' với:
        
        1. **Nguyên liệu cần thiết** (với số lượng cụ thể)
        2. **Công cụ cần dùng**
        3. **Các bước thực hiện** (chi tiết, dễ hiểu)
        4. **Thời gian chuẩn bị và nấu**
        5. **Mẹo hay để món ăn ngon hơn**
        6. **Giá trị dinh dưỡng ước tính**
        
        Vui lòng trình bày rõ ràng, dễ theo dõi."""
        
        response = self.openai_service.call_openai_api(prompt, system_prompt)
        return self.openai_service.process_response(response)

    def optimize_menu(self, current_menu: str, user_feedback: str = None):
        """
        Tối ưu hóa thực đơn theo yêu cầu người dùng
        """
        system_prompt = """Bạn là chuyên gia dinh dưỡng, hãy phân tích và tối ưu hóa thực đơn 
        theo phản hồi của người dùng."""
        
        prompt = f"""Thực đơn hiện tại:
{current_menu}

Yêu cầu thay đổi/tối ưu: {user_feedback if user_feedback else 'Cải thiện tổng thể'}

Hãy:
1. Phân tích thực đơn hiện tại
2. Đề xuất các thay đổi cụ thể
3. Giải thích lý do cho mỗi thay đổi
4. Đưa ra thực đơn đã được tối ưu hóa"""
        
        response = self.openai_service.call_openai_api(prompt, system_prompt)
        return self.openai_service.process_response(response)

    def evaluate_dish(self, dish_description: str):
        """
        Đánh giá và chỉnh sửa món ăn người dùng nhập vào
        """
        system_prompt = """Bạn là chuyên gia ẩm thực và dinh dưỡng, hãy đánh giá món ăn 
        một cách chuyên nghiệp và đưa ra gợi ý cải thiện."""
        
        prompt = f"""Món ăn cần đánh giá:
{dish_description}

Hãy cung cấp:
1. **Đánh giá tổng quan** về món ăn
2. **Giá trị dinh dưỡng** ước tính
3. **Ưu điểm** của món ăn
4. **Điểm cần cải thiện** (nếu có)
5. **Gợi ý chỉnh sửa** để món ăn ngon và healthy hơn
6. **Phù hợp với** đối tượng nào (người ăn kiêng, người tập gym, trẻ em...)"""
        
        response = self.openai_service.call_openai_api(prompt, system_prompt)
        return self.openai_service.process_response(response)