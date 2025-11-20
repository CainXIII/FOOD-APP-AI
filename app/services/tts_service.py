"""
TTS Service - Text-to-speech conversion
Handles text-to-speech using OpenAI TTS API
"""

from openai import AsyncOpenAI
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TTSService:
    """Service for text-to-speech using OpenAI TTS API"""
    
    # Available voices
    VOICES = {
        "alloy": "Neutral, balanced voice",
        "echo": "Male voice",
        "fable": "British accent",
        "onyx": "Deep male voice",
        "nova": "Female voice",
        "shimmer": "Soft female voice"
    }
    
    # TTS models
    MODELS = {
        "tts-1": "Standard quality, faster",
        "tts-1-hd": "High quality, slower"
    }
    
    def __init__(self):
        """Initialize TTS service with configured base_url"""
        self.client = AsyncOpenAI(
            api_key=settings.VOICE_API_KEY,
            base_url=settings.VOICE_BASE_URL
        )
        self.default_voice = settings.VOICE_TTS_VOICE
        self.default_model = settings.VOICE_TTS_MODEL
        self.default_speed = settings.VOICE_TTS_SPEED
    
    def get_available_voices(self) -> dict:
        """Get list of available voices with descriptions"""
        return self.VOICES.copy()
    
    def get_available_models(self) -> dict:
        """Get list of available TTS models"""
        return self.MODELS.copy()
    
    def validate_voice(self, voice: str) -> bool:
        """
        Validate if voice is available
        
        Args:
            voice: Voice name
            
        Returns:
            True if voice is valid
        """
        return voice in self.VOICES
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        speed: Optional[float] = None
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            voice: Voice to use (default from config)
            model: TTS model (default from config)
            speed: Speech speed (0.25 to 4.0, default from config)
            
        Returns:
            Audio data as bytes (mp3 format)
        """
        try:
            # Validate and set defaults
            voice = voice if voice and self.validate_voice(voice) else self.default_voice
            model = model if model in self.MODELS else self.default_model
            speed = speed if speed is not None else self.default_speed
            
            # Clamp speed
            speed = max(0.25, min(4.0, speed))
            
            logger.info(f"Synthesizing speech: {text[:50]}... (voice: {voice}, speed: {speed})")
            
            # Call TTS API
            response = await self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=speed
            )
            
            # Get audio bytes
            audio_data = response.content
            
            logger.info(f"Generated {len(audio_data)} bytes of audio")
            return audio_data
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            raise
    
    async def synthesize_streaming(
        self,
        text: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        speed: Optional[float] = None
    ):
        """
        Convert text to speech with streaming response
        
        Args:
            text: Text to convert
            voice: Voice to use (default from config)
            model: TTS model (default from config)
            speed: Speech speed (default from config)
            
        Yields:
            Audio data chunks
        """
        try:
            voice = voice if voice and self.validate_voice(voice) else self.default_voice
            model = model if model in self.MODELS else self.default_model
            speed = speed if speed is not None else self.default_speed
            speed = max(0.25, min(4.0, speed))
            
            logger.info(f"Streaming speech synthesis: {text[:50]}...")
            
            response = await self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=speed
            )
            
            # Stream the response
            async for chunk in response.iter_bytes(chunk_size=1024):
                yield chunk
                
        except Exception as e:
            logger.error(f"TTS streaming error: {e}")
            raise


# Global instance
tts_service = TTSService()
