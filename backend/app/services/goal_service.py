import logging
from datetime import date, datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_goal import UserGoal
from app.models.attempt import TypingAttempt

logger = logging.getLogger(__name__)


async def get_today_goal(db: AsyncSession, user_id: int) -> dict:
    """取今日有效目標與已完成題數。

    有效目標：effective_date <= 今日，取 id 最大（最新）的一筆。
    已完成題數：今日（UTC）的 typing_attempts 筆數。
    """
    today = date.today()
    today_start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

    # 查今日有效目標
    goal_result = await db.execute(
        select(UserGoal)
        .where(UserGoal.user_id == user_id, UserGoal.effective_date <= today)
        .order_by(UserGoal.id.desc())
        .limit(1)
    )
    goal = goal_result.scalar_one_or_none()

    # 查今日已完成題數
    count_result = await db.execute(
        select(func.count()).where(
            TypingAttempt.user_id == user_id,
            TypingAttempt.created_at >= today_start,
        )
    )
    completed_today = count_result.scalar_one()

    return {
        "daily_target": goal.daily_target if goal else None,
        "completed_today": completed_today,
    }


async def create_goal(db: AsyncSession, user_id: int, daily_target: int) -> UserGoal:
    """新增一筆目標記錄（append-only，保留歷史）。"""
    goal = UserGoal(
        user_id=user_id,
        daily_target=daily_target,
        effective_date=date.today(),
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    logger.info(f"Created goal: user={user_id}, daily_target={daily_target}")
    return goal
