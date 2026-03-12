from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    daily_target: int = Field(..., ge=1, description="每日目標題數，最少 1 題")


class GoalTodayResponse(BaseModel):
    daily_target: int | None
    completed_today: int
