from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, Computed, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class TypingAttempt(Base):
    __tablename__ = "typing_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey("characters.id", ondelete="RESTRICT"), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    duration_ms: Mapped[int] = mapped_column(
        Integer,
        Computed("EXTRACT(EPOCH FROM (ended_at - started_at)) * 1000", persisted=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    keystrokes: Mapped[list["KeystrokeEvent"]] = relationship("KeystrokeEvent", back_populates="attempt", cascade="all, delete-orphan")
