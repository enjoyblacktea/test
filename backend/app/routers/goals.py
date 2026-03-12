from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.dependencies import require_auth
from app.schemas.goal import GoalCreate, GoalTodayResponse
from app.services import goal_service

router = APIRouter()


@router.get("/today", response_model=GoalTodayResponse)
async def get_today_goal(
    user_id: int = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    return await goal_service.get_today_goal(db, user_id)


@router.post("", status_code=201)
async def create_goal(
    body: GoalCreate,
    user_id: int = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    await goal_service.create_goal(db, user_id, body.daily_target)
    return {"message": "目標已設定"}
