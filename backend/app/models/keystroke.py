from datetime import datetime
from sqlalchemy import Integer, SmallInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class KeystrokeEvent(Base):
    __tablename__ = "keystroke_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(Integer, ForeignKey("typing_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    key_value: Mapped[str] = mapped_column(String(10), nullable=False)
    key_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    typed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_correct_key: Mapped[bool] = mapped_column(Boolean, nullable=False)

    attempt: Mapped["TypingAttempt"] = relationship("TypingAttempt", back_populates="keystrokes")
