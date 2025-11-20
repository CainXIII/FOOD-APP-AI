from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    allergies = Column(JSONB, default=[])  # Simplified: only track allergies
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))
    
    # Relationships
    recipes = relationship("Recipe", back_populates="creator")
    sessions = relationship("CookingSession", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")


class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    cuisine_type = Column(String(100))
    difficulty = Column(String(50), default="medium")
    prep_time_minutes = Column(Integer, nullable=False)
    cook_time_minutes = Column(Integer, nullable=False)
    servings = Column(Integer, default=2)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    source = Column(String(100), default="user")
    is_public = Column(Boolean, default=False)
    image_url = Column(String(500))
    video_url = Column(String(500))
    steps = Column(JSONB, nullable=False)
    ingredients = Column(JSONB, nullable=False)  # Simplified: store directly
    tags = Column(JSONB, default=[])
    nutrition_info = Column(JSONB)
    tips = Column(JSONB, default=[])
    equipment_needed = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    view_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Relationships
    creator = relationship("User", back_populates="recipes")
    sessions = relationship("CookingSession", back_populates="recipe")


class CookingSession(Base):
    __tablename__ = "cooking_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id", ondelete="CASCADE"))
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    scaling_factor = Column(Float, default=1.0)
    status = Column(String(50), default="active")
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    voice_enabled = Column(Boolean, default=False)
    overrides = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    recipe = relationship("Recipe", back_populates="sessions")
    voice_commands = relationship("VoiceCommand", back_populates="session")
    timers = relationship("SessionTimer", back_populates="session")


class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    session_id = Column(UUID(as_uuid=True))
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    extra_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_history")


class VoiceCommand(Base):
    __tablename__ = "voice_commands"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cooking_sessions.id", ondelete="CASCADE"))
    transcript = Column(Text, nullable=False)
    confidence = Column(Float)
    intent = Column(String(100))
    entities = Column(JSONB, default={})
    command_result = Column(JSONB)
    transcription_method = Column(String(50))
    response_text = Column(Text)
    tts_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("CookingSession", back_populates="voice_commands")


class SessionTimer(Base):
    __tablename__ = "session_timers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cooking_sessions.id", ondelete="CASCADE"))
    label = Column(String(255))
    duration_minutes = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("CookingSession", back_populates="timers")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_type = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    extra_data = Column(JSONB, default={})
    source = Column(String(100), default="curated")
    language = Column(String(10), default="vi")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    view_count = Column(Integer, default=0)


class ImageAnalysis(Base):
    __tablename__ = "image_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    image_hash = Column(String(64), nullable=False)
    ingredients = Column(JSONB, nullable=False)
    nutrition_estimate = Column(JSONB)
    plating_score = Column(Integer)
    plating_tips = Column(JSONB, default=[])
    safety_flags = Column(JSONB, default=[])
    related_recipes = Column(JSONB, default=[])
    related_techniques = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
