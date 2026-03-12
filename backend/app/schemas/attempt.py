from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeystrokeEventIn(BaseModel):
    key: str
    order: int
    typed_at: str
    is_correct: bool


class RecordAttemptRequest(BaseModel):
    character_id: int
    started_at: datetime
    ended_at: datetime
    is_correct: bool
    keystrokes: Optional[list[KeystrokeEventIn]] = None


class AttemptOut(BaseModel):
    id: int
    user_id: int
    character_id: int
    started_at: datetime
    ended_at: datetime
    is_correct: bool
    duration_ms: Optional[int]
    created_at: datetime
    character: Optional[str] = None
    input_code: Optional[str] = None
    input_method: Optional[str] = None


class AttemptResponse(BaseModel):
    message: str
    attempt_id: Optional[int]


class AttemptsListResponse(BaseModel):
    attempts: list[AttemptOut]
    pagination: dict
