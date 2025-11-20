from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MenuRequest(BaseModel):
    """Request model để tạo thực đơn cá nhân hóa"""
    season: Optional[str] = Field(None, description="Mùa hiện tại (xuân, hạ, thu, đông)")
    weather: Optional[str] = Field(None, description="Thời tiết (nắng, mưa, lạnh, nóng)")
    allergies: Optional[str] = Field(None, description="Dị ứng hoặc không ăn được gì")
    health: Optional[str] = Field(None, description="Tình trạng sức khỏe đặc biệt")
    budget: Optional[float] = Field(None, description="Ngân sách cho bữa ăn (VNĐ)", ge=0)
    calories: Optional[int] = Field(None, description="Mục tiêu calories mỗi ngày", ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "season": "đông",
                "weather": "lạnh",
                "allergies": "hải sản",
                "health": "tiểu đường",
                "budget": 150000,
                "calories": 1800
            }
        }

class DishInfo(BaseModel):
    """Thông tin chi tiết về một món ăn"""
    name: str = Field(..., description="Tên món ăn")
    ingredients: List[str] = Field(..., description="Danh sách nguyên liệu")
    calories: Optional[int] = Field(None, description="Calories ước tính")
    prep_time: Optional[int] = Field(None, description="Thời gian chuẩn bị (phút)")
    cook_time: Optional[int] = Field(None, description="Thời gian nấu (phút)")
    
class MenuResponse(BaseModel):
    """Response model cho thực đơn được tạo"""
    success: bool
    data: str
    generated_at: datetime = Field(default_factory=datetime.now)

class CookingInstructionsRequest(BaseModel):
    """Request model để lấy hướng dẫn nấu ăn"""
    dish_name: str = Field(..., description="Tên món ăn cần hướng dẫn", min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "dish_name": "Phở bò"
            }
        }

class CookingInstructionsResponse(BaseModel):
    """Response model cho hướng dẫn nấu ăn"""
    success: bool
    dish_name: str
    instructions: str
    
class OptimizeMenuRequest(BaseModel):
    """Request model để tối ưu hóa thực đơn"""
    current_menu: str = Field(..., description="Thực đơn hiện tại cần tối ưu", min_length=1)
    user_feedback: Optional[str] = Field(
        None, 
        description="Phản hồi hoặc yêu cầu thay đổi cụ thể"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "current_menu": "Sáng: Phở bò\nTrưa: Cơm gà\nTối: Bún chả",
                "user_feedback": "Tôi muốn giảm carbs và tăng protein"
            }
        }

class OptimizeMenuResponse(BaseModel):
    """Response model cho thực đơn đã tối ưu"""
    success: bool
    optimized_menu: str

class EvaluateDishRequest(BaseModel):
    """Request model để đánh giá món ăn"""
    dish_description: str = Field(
        ..., 
        description="Mô tả chi tiết về món ăn cần đánh giá",
        min_length=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "dish_description": "Cơm chiên dương châu với tôm, trứng, xúc xích, cà rốt, đậu Hà Lan"
            }
        }

class EvaluateDishResponse(BaseModel):
    """Response model cho đánh giá món ăn"""
    success: bool
    evaluation: str

class ErrorResponse(BaseModel):
    """Response model cho lỗi"""
    success: bool = False
    error: str
    detail: Optional[str] = None
