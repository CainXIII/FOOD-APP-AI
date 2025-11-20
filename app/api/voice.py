"""
Voice API - Voice command and TTS endpoints
Handles voice transcription, command execution, and speech synthesis
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.services.whisper_service import whisper_service
from app.services.tts_service import tts_service
from app.services.timer_service import timer_service
from app.services.session_service import session_service
from app.models.database import VoiceCommand
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice", tags=["voice"])


# Request/Response Models
class TranscribeResponse(BaseModel):
    """Transcription response"""
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None
    
    class Config:
        from_attributes = True


class CommandRequest(BaseModel):
    """Voice command request"""
    session_id: int
    transcript: str


class CommandResponse(BaseModel):
    """Voice command response"""
    intent: str
    action: str
    message: str
    data: Optional[dict] = None
    audio_url: Optional[str] = None


class SpeakRequest(BaseModel):
    """Text-to-speech request"""
    text: str
    voice: Optional[str] = None
    speed: Optional[float] = 1.0


class TimerResponse(BaseModel):
    """Timer response"""
    id: int
    name: str
    duration_seconds: int
    remaining_seconds: Optional[int]
    status: str
    started_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "vi"
):
    """
    Transcribe audio file to text
    
    Args:
        audio: Audio file (mp3, mp4, wav, etc.)
        language: Language code (default: vi for Vietnamese)
        
    Returns:
        Transcription result
    """
    try:
        # Validate audio format
        if not whisper_service.validate_audio_format(audio.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Supported: {', '.join(whisper_service.get_supported_formats())}"
            )
        
        # Read audio data
        audio_data = await audio.read()
        
        # Transcribe
        result = await whisper_service.transcribe_from_bytes(
            audio_data,
            audio.filename,
            language
        )
        
        return TranscribeResponse(
            text=result["text"],
            language=result.get("language"),
            duration=result.get("duration")
        )
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/command", response_model=CommandResponse)
async def execute_voice_command(
    request: CommandRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute voice command with intent detection
    
    Args:
        request: Command request with session ID and transcript
        db: Database session
        
    Returns:
        Command execution result
    """
    try:
        # Get session
        session = await session_service.get_session(db, request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Detect intent
        intent_data = await whisper_service.detect_intent(request.transcript)
        intent = intent_data["intent"]
        
        # Log voice command
        voice_command = VoiceCommand(
            session_id=request.session_id,
            command_text=request.transcript,
            intent=intent,
            executed_at=datetime.utcnow()
        )
        db.add(voice_command)
        
        # Execute command based on intent
        response_text = ""
        action = ""
        data = {}
        
        if intent == "next_step":
            session = await session_service.next_step(db, request.session_id)
            action = "next_step"
            
            if session.status == "completed":
                response_text = "Chúc mừng! Bạn đã hoàn thành món ăn."
            else:
                instruction = await session_service.get_current_instruction(db, request.session_id)
                if instruction:
                    response_text = f"Bước {instruction['current_step']}: {instruction['instruction']}"
                    data["instruction"] = instruction
        
        elif intent == "previous_step":
            session = await session_service.previous_step(db, request.session_id)
            action = "previous_step"
            instruction = await session_service.get_current_instruction(db, request.session_id)
            if instruction:
                response_text = f"Quay lại bước {instruction['current_step']}: {instruction['instruction']}"
                data["instruction"] = instruction
        
        elif intent == "repeat":
            action = "repeat"
            instruction = await session_service.get_current_instruction(db, request.session_id)
            if instruction:
                response_text = f"Bước {instruction['current_step']}: {instruction['instruction']}"
                data["instruction"] = instruction
        
        elif intent == "timer":
            action = "timer"
            
            if intent_data.get("action") == "set":
                duration = intent_data.get("duration", 300)  # Default 5 minutes
                
                # Create timer with TTS callback
                async def timer_callback(timer_id: int):
                    # Generate alert
                    await tts_service.speak_timer_alert(intent_data.get("name"))
                
                timer = await timer_service.create_timer(
                    db,
                    request.session_id,
                    intent_data.get("name", "Timer"),
                    duration,
                    timer_callback
                )
                
                response_text = f"Đã đặt hẹn giờ {timer_service.format_duration(duration)}."
                data["timer"] = {
                    "id": timer.id,
                    "duration": duration,
                    "name": timer.name
                }
            
            elif intent_data.get("action") == "stop":
                # Stop all active timers
                timers = await timer_service.get_active_timers(db, request.session_id)
                for timer in timers:
                    await timer_service.stop_timer(db, timer.id)
                
                response_text = "Đã dừng tất cả hẹn giờ."
        
        elif intent == "pause":
            session = await session_service.pause_session(db, request.session_id)
            action = "pause"
            response_text = "Đã tạm dừng phiên nấu ăn."
        
        elif intent == "resume":
            session = await session_service.resume_session(db, request.session_id)
            action = "resume"
            response_text = "Đã tiếp tục phiên nấu ăn."
        
        elif intent == "help":
            action = "help"
            response_text = """Bạn có thể nói:
- Bước tiếp theo
- Bước trước
- Lặp lại
- Hẹn giờ 5 phút
- Dừng giờ
- Tạm dừng
- Hoặc hỏi câu hỏi về nấu ăn"""
        
        else:  # question
            action = "question"
            response_text = "Hãy đặt câu hỏi cụ thể về nấu ăn, tôi sẽ cố gắng giúp bạn."
        
        # Update voice command with response
        voice_command.response_text = response_text
        await db.commit()
        
        return CommandResponse(
            intent=intent,
            action=action,
            message=response_text,
            data=data if data else None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        logger.error(f"Error executing voice command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/speak")
async def speak_text(request: SpeakRequest):
    """
    Convert text to speech
    
    Args:
        request: Text and voice options
        
    Returns:
        Audio file (mp3)
    """
    try:
        from fastapi.responses import Response
        
        # Generate speech
        audio_bytes = await tts_service.speak(
            request.text,
            request.voice,
            request.speed
        )
        
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timers/{session_id}", response_model=List[TimerResponse])
async def get_session_timers(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all active timers for a session
    
    Args:
        session_id: Cooking session ID
        db: Database session
        
    Returns:
        List of active timers
    """
    try:
        timers = await timer_service.get_active_timers(db, session_id)
        return [
            TimerResponse(
                id=timer.id,
                name=timer.name,
                duration_seconds=timer.duration_seconds,
                remaining_seconds=timer.remaining_seconds,
                status=timer.status,
                started_at=timer.started_at
            )
            for timer in timers
        ]
    except Exception as e:
        logger.error(f"Error getting timers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/voices")
async def get_available_voices():
    """
    Get list of available TTS voices
    
    Returns:
        List of available voices with descriptions
    """
    return tts_service.get_available_voices()
