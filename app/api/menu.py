"""
Menu API - Menu generation, cooking instructions, optimization, and evaluation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.openai_service import openai_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models
class MenuRequest(BaseModel):
    season: str = Field(..., description="Mùa (xuân, hạ, thu, đông)", example="đông")
    weather: str = Field(..., description="Thời tiết (nắng, mưa, lạnh, nóng)", example="lạnh")
    allergies: Optional[str] = Field(None, description="Dị ứng thực phẩm", example="hải sản")
    budget: Optional[int] = Field(None, description="Ngân sách (VND/ngày)", example=150000)
    calories: Optional[int] = Field(None, description="Mục tiêu calories/ngày", example=1800)

class CookingInstructionsRequest(BaseModel):
    dish_name: str = Field(..., description="Tên món ăn", example="Phở bò")
    difficulty: Optional[str] = Field(None, description="Độ khó (easy, medium, hard)", example="medium")
    servings: int = Field(2, description="Số phần ăn", example=2)

class OptimizeMenuRequest(BaseModel):
    current_menu: str = Field(..., description="Thực đơn hiện tại")
    user_feedback: str = Field(..., description="Yêu cầu thay đổi", example="Tôi muốn giảm carbs")

class EvaluateDishRequest(BaseModel):
    dish_description: str = Field(..., description="Mô tả món ăn", example="Cơm chiên dương châu")

# Response Models
class MenuResponse(BaseModel):
    success: bool
    data: str
    generated_at: str

class InstructionsResponse(BaseModel):
    success: bool
    dish_name: str
    instructions: str

class OptimizeResponse(BaseModel):
    success: bool
    optimized_menu: str

class EvaluationResponse(BaseModel):
    success: bool
    evaluation: str

# Endpoints
@router.post("/menu", response_model=MenuResponse)
async def generate_menu(request: MenuRequest):
    """
    Generate personalized menu based on season, weather, allergies, budget, and calories
    
    - **season**: Current season (xuân, hạ, thu, đông)
    - **weather**: Weather conditions (nắng, mưa, lạnh, nóng)
    - **allergies**: Food allergies (optional)
    - **budget**: Daily budget in VND (optional)
    - **calories**: Target daily calories (optional)
    """
    try:
        logger.info(f"Generating menu: season={request.season}, weather={request.weather}")
        
        menu = await openai_service.generate_menu(
            season=request.season,
            weather=request.weather,
            allergies=request.allergies,
            budget=request.budget,
            calories=request.calories
        )
        
        return MenuResponse(
            success=True,
            data=menu,
            generated_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error generating menu: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể tạo thực đơn: {str(e)}")

@router.post("/cooking-instructions", response_model=InstructionsResponse)
async def get_cooking_instructions(request: CookingInstructionsRequest):
    """
    Get detailed step-by-step cooking instructions for a dish
    
    - **dish_name**: Name of the dish
    - **difficulty**: Difficulty level (optional)
    - **servings**: Number of servings
    """
    try:
        logger.info(f"Getting instructions for: {request.dish_name}")
        
        instructions = await openai_service.get_cooking_instructions(
            dish_name=request.dish_name,
            difficulty=request.difficulty,
            servings=request.servings
        )
        
        return InstructionsResponse(
            success=True,
            dish_name=request.dish_name,
            instructions=instructions
        )
    except Exception as e:
        logger.error(f"Error getting cooking instructions: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể lấy hướng dẫn: {str(e)}")

@router.post("/optimize-menu", response_model=OptimizeResponse)
async def optimize_menu(request: OptimizeMenuRequest):
    """
    Optimize existing menu based on user feedback
    
    - **current_menu**: Current menu content
    - **user_feedback**: User requirements and feedback
    """
    try:
        logger.info(f"Optimizing menu with feedback: {request.user_feedback[:50]}...")
        
        optimized = await openai_service.optimize_menu(
            current_menu=request.current_menu,
            user_feedback=request.user_feedback
        )
        
        return OptimizeResponse(
            success=True,
            optimized_menu=optimized
        )
    except Exception as e:
        logger.error(f"Error optimizing menu: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể tối ưu thực đơn: {str(e)}")

@router.post("/evaluate-dish", response_model=EvaluationResponse)
async def evaluate_dish(request: EvaluateDishRequest):
    """
    Evaluate a dish and provide nutritional feedback
    
    - **dish_description**: Description of the dish to evaluate
    """
    try:
        logger.info(f"Evaluating dish: {request.dish_description[:50]}...")
        
        evaluation = await openai_service.evaluate_dish(
            dish_description=request.dish_description
        )
        
        return EvaluationResponse(
            success=True,
            evaluation=evaluation
        )
    except Exception as e:
        logger.error(f"Error evaluating dish: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể đánh giá món ăn: {str(e)}")
