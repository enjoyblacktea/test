import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.dependencies import require_auth
from app.schemas.attempt import RecordAttemptRequest, AttemptResponse, AttemptsListResponse
from app.services import attempt_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", status_code=202, response_model=AttemptResponse)
async def record_attempt(
    body: RecordAttemptRequest,
    user_id: int = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    keystrokes = [k.model_dump() for k in body.keystrokes] if body.keystrokes else None
    attempt_id = await attempt_service.record_attempt(
        db=db,
        user_id=user_id,
        character_id=body.character_id,
        started_at=body.started_at,
        ended_at=body.ended_at,
        is_correct=body.is_correct,
        keystrokes=keystrokes,
    )
    if attempt_id is None:
        return AttemptResponse(message="Attempt received (recording in progress)", attempt_id=None)
    return AttemptResponse(message="Attempt recorded", attempt_id=attempt_id)


@router.get("")
async def get_attempts(
    user_id: int = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
    is_correct: str = Query(default=None),
    character_id: int = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
):
    filters = {}
    if is_correct is not None:
        filters["is_correct"] = is_correct.lower() in ("true", "1", "yes")
    if character_id is not None:
        filters["character_id"] = character_id
    if start_date:
        filters["start_date"] = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    if end_date:
        filters["end_date"] = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

    result = await attempt_service.get_user_attempts(db, user_id=user_id, page=page, limit=limit, filters=filters)
    return result
