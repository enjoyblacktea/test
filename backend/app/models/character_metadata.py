from sqlalchemy import Integer, SmallInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class CharacterMetadata(Base):
    __tablename__ = "character_metadata"

    character_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True
    )
    initial: Mapped[str | None] = mapped_column(String(5), nullable=True)
    final: Mapped[str | None] = mapped_column(String(10), nullable=True)
    tone: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    difficulty: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    frequency_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
