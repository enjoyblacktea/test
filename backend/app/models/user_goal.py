from datetime import date, datetime
from sqlalchemy import Integer, SmallInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class UserGoal(Base):
    __tablename__ = "user_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    daily_target: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
