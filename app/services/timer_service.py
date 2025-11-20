"""
Timer Service - Cooking timer management
Manages multiple timers for cooking sessions
"""

from typing import Optional, List, Dict
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.database import SessionTimer
import logging
import asyncio

logger = logging.getLogger(__name__)

class TimerService:
    """Service for managing cooking timers"""
    
    def __init__(self):
        """Initialize timer service"""
        self._active_timers: Dict[int, asyncio.Task] = {}
        self._callbacks: Dict[int, callable] = {}
    
    async def create_timer(
        self,
        db: AsyncSession,
        session_id: int,
        name: str,
        duration_seconds: int,
        callback: Optional[callable] = None
    ) -> SessionTimer:
        """
        Create and start a new timer
        
        Args:
            db: Database session
            session_id: Cooking session ID
            name: Timer name/description
            duration_seconds: Duration in seconds
            callback: Optional callback when timer completes
            
        Returns:
            Created timer instance
        """
        try:
            # Create timer record
            timer = SessionTimer(
                session_id=session_id,
                name=name,
                duration_seconds=duration_seconds,
                status="running",
                started_at=datetime.utcnow()
            )
            
            db.add(timer)
            await db.commit()
            await db.refresh(timer)
            
            # Start background timer task
            if callback:
                self._callbacks[timer.id] = callback
            
            task = asyncio.create_task(self._run_timer(timer.id, duration_seconds))
            self._active_timers[timer.id] = task
            
            logger.info(f"Timer created: {name} for {duration_seconds}s")
            return timer
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating timer: {e}")
            raise
    
    async def _run_timer(self, timer_id: int, duration_seconds: int):
        """
        Background task to run timer
        
        Args:
            timer_id: Timer ID
            duration_seconds: Duration in seconds
        """
        try:
            await asyncio.sleep(duration_seconds)
            
            # Timer completed
            logger.info(f"Timer {timer_id} completed")
            
            # Execute callback if registered
            if timer_id in self._callbacks:
                callback = self._callbacks[timer_id]
                await callback(timer_id)
                del self._callbacks[timer_id]
            
            # Clean up
            if timer_id in self._active_timers:
                del self._active_timers[timer_id]
        except asyncio.CancelledError:
            logger.info(f"Timer {timer_id} cancelled")
        except Exception as e:
            logger.error(f"Error running timer {timer_id}: {e}")
    
    async def pause_timer(
        self,
        db: AsyncSession,
        timer_id: int
    ) -> SessionTimer:
        """
        Pause a running timer
        
        Args:
            db: Database session
            timer_id: Timer ID
            
        Returns:
            Updated timer instance
        """
        try:
            # Get timer
            result = await db.execute(
                select(SessionTimer).where(SessionTimer.id == timer_id)
            )
            timer = result.scalar_one_or_none()
            
            if not timer:
                raise ValueError(f"Timer {timer_id} not found")
            
            if timer.status != "running":
                raise ValueError(f"Timer {timer_id} is not running")
            
            # Calculate elapsed time
            elapsed = (datetime.utcnow() - timer.started_at).total_seconds()
            timer.remaining_seconds = timer.duration_seconds - int(elapsed)
            timer.status = "paused"
            timer.paused_at = datetime.utcnow()
            
            # Cancel background task
            if timer_id in self._active_timers:
                self._active_timers[timer_id].cancel()
                del self._active_timers[timer_id]
            
            await db.commit()
            await db.refresh(timer)
            
            logger.info(f"Timer {timer_id} paused with {timer.remaining_seconds}s remaining")
            return timer
        except Exception as e:
            await db.rollback()
            logger.error(f"Error pausing timer: {e}")
            raise
    
    async def resume_timer(
        self,
        db: AsyncSession,
        timer_id: int
    ) -> SessionTimer:
        """
        Resume a paused timer
        
        Args:
            db: Database session
            timer_id: Timer ID
            
        Returns:
            Updated timer instance
        """
        try:
            # Get timer
            result = await db.execute(
                select(SessionTimer).where(SessionTimer.id == timer_id)
            )
            timer = result.scalar_one_or_none()
            
            if not timer:
                raise ValueError(f"Timer {timer_id} not found")
            
            if timer.status != "paused":
                raise ValueError(f"Timer {timer_id} is not paused")
            
            # Resume timer
            timer.status = "running"
            timer.started_at = datetime.utcnow()
            
            # Start background task with remaining time
            callback = self._callbacks.get(timer_id)
            task = asyncio.create_task(
                self._run_timer(timer_id, timer.remaining_seconds)
            )
            self._active_timers[timer_id] = task
            
            await db.commit()
            await db.refresh(timer)
            
            logger.info(f"Timer {timer_id} resumed with {timer.remaining_seconds}s remaining")
            return timer
        except Exception as e:
            await db.rollback()
            logger.error(f"Error resuming timer: {e}")
            raise
    
    async def stop_timer(
        self,
        db: AsyncSession,
        timer_id: int
    ) -> SessionTimer:
        """
        Stop and complete a timer
        
        Args:
            db: Database session
            timer_id: Timer ID
            
        Returns:
            Updated timer instance
        """
        try:
            # Get timer
            result = await db.execute(
                select(SessionTimer).where(SessionTimer.id == timer_id)
            )
            timer = result.scalar_one_or_none()
            
            if not timer:
                raise ValueError(f"Timer {timer_id} not found")
            
            # Stop timer
            timer.status = "stopped"
            timer.completed_at = datetime.utcnow()
            timer.remaining_seconds = 0
            
            # Cancel background task
            if timer_id in self._active_timers:
                self._active_timers[timer_id].cancel()
                del self._active_timers[timer_id]
            
            # Remove callback
            if timer_id in self._callbacks:
                del self._callbacks[timer_id]
            
            await db.commit()
            await db.refresh(timer)
            
            logger.info(f"Timer {timer_id} stopped")
            return timer
        except Exception as e:
            await db.rollback()
            logger.error(f"Error stopping timer: {e}")
            raise
    
    async def get_active_timers(
        self,
        db: AsyncSession,
        session_id: int
    ) -> List[SessionTimer]:
        """
        Get all active timers for a session
        
        Args:
            db: Database session
            session_id: Cooking session ID
            
        Returns:
            List of active timers
        """
        try:
            result = await db.execute(
                select(SessionTimer).where(
                    and_(
                        SessionTimer.session_id == session_id,
                        SessionTimer.status.in_(["running", "paused"])
                    )
                )
            )
            timers = result.scalars().all()
            
            # Update remaining time for running timers
            for timer in timers:
                if timer.status == "running":
                    elapsed = (datetime.utcnow() - timer.started_at).total_seconds()
                    timer.remaining_seconds = max(0, timer.duration_seconds - int(elapsed))
            
            return list(timers)
        except Exception as e:
            logger.error(f"Error getting active timers: {e}")
            raise
    
    async def get_timer(
        self,
        db: AsyncSession,
        timer_id: int
    ) -> Optional[SessionTimer]:
        """
        Get timer by ID
        
        Args:
            db: Database session
            timer_id: Timer ID
            
        Returns:
            Timer instance or None
        """
        try:
            result = await db.execute(
                select(SessionTimer).where(SessionTimer.id == timer_id)
            )
            timer = result.scalar_one_or_none()
            
            # Update remaining time if running
            if timer and timer.status == "running":
                elapsed = (datetime.utcnow() - timer.started_at).total_seconds()
                timer.remaining_seconds = max(0, timer.duration_seconds - int(elapsed))
            
            return timer
        except Exception as e:
            logger.error(f"Error getting timer: {e}")
            raise
    
    def format_duration(self, seconds: int) -> str:
        """
        Format duration in human-readable format
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds} giây"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            if secs == 0:
                return f"{minutes} phút"
            return f"{minutes} phút {secs} giây"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes == 0:
                return f"{hours} giờ"
            return f"{hours} giờ {minutes} phút"


# Singleton instance
timer_service = TimerService()
