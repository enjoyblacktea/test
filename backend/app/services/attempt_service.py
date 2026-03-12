import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attempt import TypingAttempt
from app.models.keystroke import KeystrokeEvent
from app.models.character import Character

logger = logging.getLogger(__name__)


async def record_attempt(
    db: AsyncSession,
    user_id: int,
    character_id: int,
    started_at: datetime,
    ended_at: datetime,
    is_correct: bool,
    keystrokes: Optional[List[Dict]] = None,
) -> Optional[int]:
    try:
        attempt = TypingAttempt(
            user_id=user_id,
            character_id=character_id,
            started_at=started_at,
            ended_at=ended_at,
            is_correct=is_correct,
        )
        db.add(attempt)
        await db.flush()  # 取得 attempt.id，但尚未 commit

        if keystrokes:
            db.add_all([
                KeystrokeEvent(
                    attempt_id=attempt.id,
                    key_value=k["key"],
                    key_order=k["order"],
                    typed_at=datetime.fromisoformat(k["typed_at"].replace("Z", "+00:00")),
                    is_correct_key=k["is_correct"],
                )
                for k in keystrokes
            ])

        await db.commit()
        logger.info(f"Recorded attempt: user={user_id}, char={character_id}, correct={is_correct}, id={attempt.id}")
        return attempt.id

    except Exception as e:
        await db.rollback()
        logger.error(f"Error recording attempt: {e}")
        return None


async def get_user_attempts(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    limit: int = 50,
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if filters is None:
        filters = {}

    page = max(1, page)
    limit = min(max(1, limit), 100)
    offset = (page - 1) * limit

    try:
        # Build base query
        base_q = (
            select(TypingAttempt, Character)
            .join(Character, TypingAttempt.character_id == Character.id)
            .where(TypingAttempt.user_id == user_id)
        )

        if "is_correct" in filters:
            base_q = base_q.where(TypingAttempt.is_correct == filters["is_correct"])
        if "character_id" in filters:
            base_q = base_q.where(TypingAttempt.character_id == filters["character_id"])
        if "start_date" in filters:
            base_q = base_q.where(TypingAttempt.created_at >= filters["start_date"])
        if "end_date" in filters:
            base_q = base_q.where(TypingAttempt.created_at <= filters["end_date"])

        # Count
        count_q = select(func.count()).select_from(base_q.subquery())
        total_count = (await db.execute(count_q)).scalar_one()

        # Paginate
        rows = (await db.execute(base_q.order_by(TypingAttempt.created_at.desc()).limit(limit).offset(offset))).all()

        attempts = [
            {
                "id": ta.id,
                "user_id": ta.user_id,
                "character_id": ta.character_id,
                "started_at": ta.started_at.isoformat(),
                "ended_at": ta.ended_at.isoformat(),
                "is_correct": ta.is_correct,
                "duration_ms": ta.duration_ms,
                "created_at": ta.created_at.isoformat(),
                "character": ch.character,
                "input_code": ch.input_code,
                "input_method": ch.input_method,
            }
            for ta, ch in rows
        ]

        total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0
        return {
            "attempts": attempts,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "has_more": page < total_pages,
            },
        }

    except Exception as e:
        logger.error(f"Error retrieving user attempts: {e}")
        return {
            "attempts": [],
            "pagination": {"total_count": 0, "page": page, "limit": limit, "total_pages": 0, "has_more": False},
        }
