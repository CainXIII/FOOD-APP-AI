"""
Food App Backend - Main Application
FastAPI application with async support, CORS, and comprehensive routing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import async_engine
from app.services.qdrant_service import qdrant_service
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan
    """
    # Startup
    logger.info("Starting Food App Backend...")
    
    try:
        # Initialize Qdrant collection
        collection_exists = await qdrant_service.collection_exists()
        if not collection_exists:
            await qdrant_service.create_collection()
            logger.info("Created Qdrant collection")
        else:
            logger.info("Qdrant collection already exists")
    except Exception as e:
        logger.warning(f"Could not initialize Qdrant: {e}")
    
    logger.info("Startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await async_engine.dispose()
    logger.info("Shutdown complete!")

# Initialize FastAPI app
app = FastAPI(
    title="Food App Backend API",
    description="Smart cooking assistant with AI-powered menu generation, RAG-based chat, and voice commands",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import API routers
from app.api import menu, chat, voice, sessions

# Include routers
app.include_router(menu.router, prefix="/api", tags=["Menu & Recipes"])
app.include_router(chat.router, prefix="/api", tags=["Chat Assistant"])
app.include_router(voice.router, tags=["Voice Commands"])
app.include_router(sessions.router, tags=["Cooking Sessions"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Food App Backend API",
        "version": "1.0.0",
        "description": "Smart cooking assistant with AI-powered features",
        "features": [
            "AI Menu Generation",
            "RAG-based Chat Assistant",
            "Cooking Instructions",
            "Recipe Search",
            "Menu Optimization",
            "Voice Commands & TTS",
            "Cooking Timers",
            "Session Management"
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "menu": "/api/menu",
            "cooking_instructions": "/api/cooking-instructions",
            "optimize_menu": "/api/optimize-menu",
            "evaluate_dish": "/api/evaluate-dish",
            "chat": "/api/chat",
            "chat_history": "/api/chat/history",
            "voice_transcribe": "/api/voice/transcribe",
            "voice_command": "/api/voice/command",
            "voice_speak": "/api/voice/speak",
            "voice_timers": "/api/voice/timers/{session_id}",
            "health": "/health"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns system status and service availability
    """
    try:
        # Check Qdrant connection
        qdrant_status = "connected"
        try:
            collection_info = await qdrant_service.get_collection_info()
            qdrant_points = collection_info.get("points_count", 0) if collection_info else 0
        except:
            qdrant_status = "disconnected"
            qdrant_points = 0
        
        return {
            "status": "healthy",
            "version": "1.0.0",
            "services": {
                "database": "configured",
                "qdrant": qdrant_status,
                "openai": "configured"
            },
            "qdrant_points": qdrant_points,
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "degraded",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )