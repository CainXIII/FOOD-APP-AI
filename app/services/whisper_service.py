"""
Whisper Service - Audio transcription and intent detection
Handles voice-to-text conversion using OpenAI Whisper API
"""

from openai import AsyncOpenAI
from app.core.config import settings
from typing import Dict, Any, Optional
import logging
import io

logger = logging.getLogger(__name__)


class WhisperService:
    """Service for audio transcription using OpenAI Whisper"""
    
    # Supported audio formats
    SUPPORTED_FORMATS = [
        "mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"
    ]
    
    # Vietnamese cooking intents
    COOKING_INTENTS = {
        "timer": ["hẹn giờ", "đặt giờ", "báo thức", "timer", "đếm ngược"],
        "recipe": ["công thức", "cách làm", "nấu như thế nào", "hướng dẫn", "recipe"],
        "ingredient": ["nguyên liệu", "cần gì", "thành phần", "ingredient"],
        "technique": ["kỹ thuật", "cách", "phương pháp", "technique"],
        "substitute": ["thay thế", "thay bằng", "substitute", "alternative"],
        "nutrition": ["dinh dưỡng", "calories", "năng lượng", "nutrition"],
        "menu": ["thực đơn", "menu", "món ăn hôm nay"],
        "help": ["giúp", "help", "trợ giúp", "hỗ trợ"]
    }
    
    def __init__(self):
        """Initialize Whisper service with configured base_url"""
        self.client = AsyncOpenAI(
            api_key=settings.VOICE_API_KEY,
            base_url=settings.VOICE_BASE_URL
        )
        self.model = settings.VOICE_WHISPER_MODEL
    
    def validate_audio_format(self, filename: str) -> bool:
        """
        Validate if audio format is supported
        
        Args:
            filename: Audio filename
            
        Returns:
            True if format is supported
        """
        extension = filename.lower().split('.')[-1]
        return extension in self.SUPPORTED_FORMATS
    
    def get_supported_formats(self) -> list:
        """Get list of supported audio formats"""
        return self.SUPPORTED_FORMATS.copy()
    
    async def transcribe_from_bytes(
        self,
        audio_data: bytes,
        filename: str,
        language: str = "vi"
    ) -> Dict[str, Any]:
        """
        Transcribe audio from bytes
        
        Args:
            audio_data: Audio file bytes
            filename: Original filename
            language: Language code (default: vi)
            
        Returns:
            Dict with transcription results
        """
        try:
            # Create file-like object
            audio_file = io.BytesIO(audio_data)
            audio_file.name = filename
            
            # Call Whisper API
            response = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json"
            )
            
            # Extract text
            text = response.text.strip()
            
            # Detect intent
            intent = self._detect_intent(text)
            
            result = {
                "text": text,
                "language": language,
                "duration": getattr(response, 'duration', None),
                "intent": intent
            }
            
            logger.info(f"Transcribed audio: {text[:50]}... (intent: {intent})")
            return result
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise
    
    def _detect_intent(self, text: str) -> str:
        """
        Detect cooking intent from transcribed text
        
        Args:
            text: Transcribed text
            
        Returns:
            Detected intent or 'general'
        """
        text_lower = text.lower()
        
        for intent, keywords in self.COOKING_INTENTS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "general"
    
    async def transcribe_from_file(
        self,
        file_path: str,
        language: str = "vi"
    ) -> Dict[str, Any]:
        """
        Transcribe audio from file path
        
        Args:
            file_path: Path to audio file
            language: Language code
            
        Returns:
            Dict with transcription results
        """
        try:
            with open(file_path, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json"
                )
            
            text = response.text.strip()
            intent = self._detect_intent(text)
            
            return {
                "text": text,
                "language": language,
                "duration": getattr(response, 'duration', None),
                "intent": intent
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise


# Global instance
whisper_service = WhisperService()
