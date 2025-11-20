"""
Session Service - Cooking session management
Manages cooking session state, steps, and progress
"""

from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.database import CookingSession, Recipe
import logging
import json

logger = logging.getLogger(__name__)

class SessionService:
    """Service for managing cooking sessions"""
    
    async def create_session(
        self,
        db: AsyncSession,
        user_id: int,
        recipe_id: int
    ) -> CookingSession:
        """
        Create a new cooking session
        
        Args:
            db: Database session
            user_id: User ID
            recipe_id: Recipe ID
            
        Returns:
            Created session instance
        """
        try:
            # Get recipe
            result = await db.execute(
                select(Recipe).where(Recipe.id == recipe_id)
            )
            recipe = result.scalar_one_or_none()
            
            if not recipe:
                raise ValueError(f"Recipe {recipe_id} not found")
            
            # Parse instructions
            instructions = []
            if recipe.instructions:
                try:
                    instructions = json.loads(recipe.instructions)
                except:
                    # If instructions is string, split by newlines
                    instructions = [
                        {"step": i+1, "instruction": line.strip()}
                        for i, line in enumerate(recipe.instructions.split('\n'))
                        if line.strip()
                    ]
            
            # Create session
            session = CookingSession(
                user_id=user_id,
                recipe_id=recipe_id,
                status="active",
                current_step=1,
                total_steps=len(instructions),
                started_at=datetime.utcnow()
            )
            
            db.add(session)
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session created: {session.id} for recipe {recipe_id}")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating session: {e}")
            raise
    
    async def get_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> Optional[CookingSession]:
        """
        Get session by ID
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Session instance or None
        """
        try:
            result = await db.execute(
                select(CookingSession).where(CookingSession.id == session_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            raise
    
    async def get_active_session(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Optional[CookingSession]:
        """
        Get active session for user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Active session or None
        """
        try:
            result = await db.execute(
                select(CookingSession).where(
                    and_(
                        CookingSession.user_id == user_id,
                        CookingSession.status == "active"
                    )
                ).order_by(CookingSession.started_at.desc())
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting active session: {e}")
            raise
    
    async def update_step(
        self,
        db: AsyncSession,
        session_id: int,
        step_number: int
    ) -> CookingSession:
        """
        Update current step in session
        
        Args:
            db: Database session
            session_id: Session ID
            step_number: New step number
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            if step_number < 1 or step_number > session.total_steps:
                raise ValueError(f"Invalid step number: {step_number}")
            
            session.current_step = step_number
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} updated to step {step_number}")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating session step: {e}")
            raise
    
    async def next_step(
        self,
        db: AsyncSession,
        session_id: int
    ) -> CookingSession:
        """
        Move to next step
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            if session.current_step >= session.total_steps:
                # Complete session if on last step
                return await self.complete_session(db, session_id)
            
            session.current_step += 1
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} moved to step {session.current_step}")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error moving to next step: {e}")
            raise
    
    async def previous_step(
        self,
        db: AsyncSession,
        session_id: int
    ) -> CookingSession:
        """
        Move to previous step
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            if session.current_step <= 1:
                raise ValueError("Already at first step")
            
            session.current_step -= 1
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} moved to step {session.current_step}")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error moving to previous step: {e}")
            raise
    
    async def pause_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> CookingSession:
        """
        Pause a session
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            if session.status != "active":
                raise ValueError(f"Session {session_id} is not active")
            
            session.status = "paused"
            session.paused_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} paused")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error pausing session: {e}")
            raise
    
    async def resume_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> CookingSession:
        """
        Resume a paused session
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            if session.status != "paused":
                raise ValueError(f"Session {session_id} is not paused")
            
            session.status = "active"
            session.paused_at = None
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} resumed")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error resuming session: {e}")
            raise
    
    async def complete_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> CookingSession:
        """
        Complete a session
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Updated session
        """
        try:
            session = await self.get_session(db, session_id)
            
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} completed")
            return session
        except Exception as e:
            await db.rollback()
            logger.error(f"Error completing session: {e}")
            raise
    
    async def get_current_instruction(
        self,
        db: AsyncSession,
        session_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get current instruction for session
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Current instruction dict or None
        """
        try:
            # Get session with recipe
            result = await db.execute(
                select(CookingSession, Recipe).join(
                    Recipe, CookingSession.recipe_id == Recipe.id
                ).where(CookingSession.id == session_id)
            )
            row = result.first()
            
            if not row:
                return None
            
            session, recipe = row
            
            # Parse instructions
            instructions = []
            if recipe.instructions:
                try:
                    instructions = json.loads(recipe.instructions)
                except:
                    instructions = [
                        {"step": i+1, "instruction": line.strip()}
                        for i, line in enumerate(recipe.instructions.split('\n'))
                        if line.strip()
                    ]
            
            # Get current instruction
            if session.current_step <= len(instructions):
                current = instructions[session.current_step - 1]
                current["current_step"] = session.current_step
                current["total_steps"] = session.total_steps
                return current
            
            return None
        except Exception as e:
            logger.error(f"Error getting current instruction: {e}")
            raise


# Singleton instance
session_service = SessionService()
