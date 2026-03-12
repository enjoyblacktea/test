from datetime import datetime
from sqlalchemy import String, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[str] = mapped_column(String(10), nullable=False)
    input_code: Mapped[str] = mapped_column(String(50), nullable=False)
    input_method: Mapped[str] = mapped_column(String(20), nullable=False, default="bopomofo", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("character", "input_method"),)
