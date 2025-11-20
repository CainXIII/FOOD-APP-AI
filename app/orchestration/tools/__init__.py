"""
LangChain Tools for Food App Chat Assistant
"""

from typing import Optional, List
from app.services.openai_service import openai_service
from app.services.rag_service import rag_service
import logging

logger = logging.getLogger(__name__)

# Simple tool wrapper since LangChain imports are having issues
class SimpleTool:
    def __init__(self, name: str, func, description: str):
        self.name = name
        self.func = func
        self.description = description

# Tool 1: Generate Menu
async def generate_menu_tool(query: str) -> str:
    """
    Generate personalized menu based on requirements
    
    Args:
        query: Requirements in format "season:đông,weather:lạnh,allergies:hải sản,budget:150000,calories:1800"
    """
    try:
        # Parse query
        params = {}
        for part in query.split(","):
            if ":" in part:
                key, value = part.split(":", 1)
                params[key.strip()] = value.strip()
        
        # Generate menu
        menu = await openai_service.generate_menu(
            season=params.get("season", ""),
            weather=params.get("weather", ""),
            allergies=params.get("allergies"),
            budget=int(params.get("budget")) if params.get("budget") else None,
            calories=int(params.get("calories")) if params.get("calories") else None
        )
        return menu
    except Exception as e:
        logger.error(f"Error in generate_menu_tool: {e}")
        return f"Lỗi khi tạo thực đơn: {str(e)}"

generate_menu = SimpleTool(
    name="generate_menu",
    func=generate_menu_tool,
    description="Tạo thực đơn cá nhân hóa dựa trên mùa, thời tiết, dị ứng, ngân sách và calories. "
                "Input format: 'season:đông,weather:lạnh,allergies:hải sản,budget:150000,calories:1800'"
)

# Tool 2: Search Recipes
async def search_recipes_tool(query: str) -> str:
    """
    Search for recipes in knowledge base
    
    Args:
        query: Search query (e.g., "món ăn với thịt gà")
    """
    try:
        results = await rag_service.search_recipes(query, limit=5)
        
        if not results:
            return "Không tìm thấy công thức phù hợp."
        
        response = "Các công thức tìm thấy:\n\n"
        for i, result in enumerate(results, 1):
            title = result.metadata.get("recipe_title", "Unknown")
            section = result.metadata.get("section", "")
            response += f"{i}. {title} ({section})\n"
            response += f"   {result.text[:200]}...\n\n"
        
        return response
    except Exception as e:
        logger.error(f"Error in search_recipes_tool: {e}")
        return f"Lỗi khi tìm kiếm công thức: {str(e)}"

search_recipes = SimpleTool(
    name="search_recipes",
    func=search_recipes_tool,
    description="Tìm kiếm công thức nấu ăn trong cơ sở kiến thức. "
                "Sử dụng khi người dùng hỏi về cách nấu một món cụ thể."
)

# Tool 3: Get Cooking Technique
async def get_technique_tool(query: str) -> str:
    """
    Get cooking technique information
    
    Args:
        query: Technique name (e.g., "xào", "luộc", "caramel")
    """
    try:
        results = await rag_service.search_techniques(query, limit=3)
        
        if not results:
            return f"Không tìm thấy thông tin về kỹ thuật '{query}'."
        
        response = f"Kỹ thuật '{query}':\n\n"
        for result in results:
            title = result.metadata.get("title", "Unknown")
            response += f"[{title}]\n{result.text}\n\n"
        
        return response
    except Exception as e:
        logger.error(f"Error in get_technique_tool: {e}")
        return f"Lỗi khi tìm kỹ thuật: {str(e)}"

get_technique = SimpleTool(
    name="get_technique",
    func=get_technique_tool,
    description="Lấy thông tin về kỹ thuật nấu ăn cụ thể (xào, luộc, chiên, caramel, v.v.). "
                "Sử dụng khi người dùng hỏi về cách thực hiện kỹ thuật nấu ăn."
)

# Tool 4: Substitute Ingredient
async def substitute_ingredient_tool(ingredient: str) -> str:
    """
    Find ingredient substitutes
    
    Args:
        ingredient: Ingredient to find substitute for
    """
    try:
        results = await rag_service.find_ingredient_substitutes(ingredient)
        
        if not results:
            return f"Không tìm thấy thông tin thay thế cho '{ingredient}'."
        
        response = f"Thay thế cho {ingredient}:\n\n"
        for result in results:
            response += f"{result.text}\n\n"
        
        return response
    except Exception as e:
        logger.error(f"Error in substitute_ingredient_tool: {e}")
        return f"Lỗi khi tìm nguyên liệu thay thế: {str(e)}"

substitute_ingredient = SimpleTool(
    name="substitute_ingredient",
    func=substitute_ingredient_tool,
    description="Tìm nguyên liệu thay thế khi không có nguyên liệu gốc. "
                "Sử dụng khi người dùng hỏi 'thay thế X bằng gì', 'không có X thì dùng gì'."
)

# Tool 5: Convert Units
async def convert_units_tool(query: str) -> str:
    """
    Convert cooking units
    
    Args:
        query: Conversion query (e.g., "100g sang cup", "1 cup sang ml")
    """
    try:
        # Common conversions
        conversions = {
            # Weight
            "g to kg": lambda x: x / 1000,
            "kg to g": lambda x: x * 1000,
            "g to oz": lambda x: x * 0.035274,
            "oz to g": lambda x: x / 0.035274,
            # Volume
            "ml to l": lambda x: x / 1000,
            "l to ml": lambda x: x * 1000,
            "cup to ml": lambda x: x * 240,
            "ml to cup": lambda x: x / 240,
            "tbsp to ml": lambda x: x * 15,
            "ml to tbsp": lambda x: x / 15,
            "tsp to ml": lambda x: x * 5,
            "ml to tsp": lambda x: x / 5,
        }
        
        query_lower = query.lower().replace("sang", "to").replace("ra", "to")
        
        # Parse number and units
        parts = query_lower.split()
        if len(parts) >= 3:
            try:
                value = float(parts[0])
                from_unit = parts[1]
                to_unit = parts[3] if len(parts) > 3 else parts[2]
                
                conversion_key = f"{from_unit} to {to_unit}"
                if conversion_key in conversions:
                    result = conversions[conversion_key](value)
                    return f"{value} {from_unit} = {result:.2f} {to_unit}"
            except ValueError:
                pass
        
        return "Không thể chuyển đổi. Ví dụ: '100 g to kg', '1 cup to ml'"
    except Exception as e:
        logger.error(f"Error in convert_units_tool: {e}")
        return f"Lỗi khi chuyển đổi: {str(e)}"

convert_units = SimpleTool(
    name="convert_units",
    func=convert_units_tool,
    description="Chuyển đổi đơn vị đo lường (g, kg, ml, l, cup, tbsp, tsp). "
                "Sử dụng khi người dùng hỏi về chuyển đổi đơn vị."
)

# Tool 6: Get User Allergies (placeholder - needs database integration)
async def get_user_allergies_tool(user_id: str) -> str:
    """
    Get user's allergies from database
    
    Args:
        user_id: User ID
    """
    # This will be implemented with database integration
    return "Chức năng này cần kết nối cơ sở dữ liệu người dùng."

get_user_allergies = SimpleTool(
    name="get_user_allergies",
    func=get_user_allergies_tool,
    description="Lấy thông tin dị ứng của người dùng từ hồ sơ."
)

# All tools list
ALL_TOOLS = [
    generate_menu,
    search_recipes,
    get_technique,
    substitute_ingredient,
    convert_units,
    get_user_allergies
]
