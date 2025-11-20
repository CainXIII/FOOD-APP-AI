from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Chat Configuration (GPT)
    CHAT_API_KEY: str = "sk-QEw3q1_bjVSoR_nIy6m2vA"
    CHAT_BASE_URL: str = "https://aiportalapi.stu-platform.live/jpe"
    CHAT_MODEL: str = "gpt-4o-mini"
    CHAT_MAX_TOKENS: int = 2000
    CHAT_TEMPERATURE: float = 0.7
    
    # Voice Configuration (Whisper + TTS)
    VOICE_API_KEY: str = "sk-QEw3q1_bjVSoR_nIy6m2vA"
    VOICE_BASE_URL: str = "https://aiportalapi.stu-platform.live/jpe"
    VOICE_WHISPER_MODEL: str = "whisper-1"
    VOICE_TTS_MODEL: str = "tts-1"
    VOICE_TTS_VOICE: str = "alloy"
    VOICE_TTS_SPEED: float = 1.0
    
    # Image Configuration (Vision)
    IMAGE_API_KEY: str = "sk-QEw3q1_bjVSoR_nIy6m2vA"
    IMAGE_BASE_URL: str = "https://aiportalapi.stu-platform.live/jpe"
    IMAGE_MODEL: str = "gpt-4o-mini"
    IMAGE_MAX_TOKENS: int = 1000
    
    # Embedding Configuration (RAG)
    EMBEDDING_API_KEY: str = "sk-QEw3q1_bjVSoR_nIy6m2vA"
    EMBEDDING_BASE_URL: str = "https://aiportalapi.stu-platform.live/jpe"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Database
    DATABASE_URL: str
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "knowledge_base"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Application
    APP_NAME: str = "Food App Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"
    
    # Features
    ENABLE_VOICE: bool = True
    ENABLE_IMAGE_ANALYSIS: bool = True
    ENABLE_CACHING: bool = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global settings instance
settings = get_settings()