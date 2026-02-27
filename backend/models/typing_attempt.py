"""TypingAttempt model representing typing_attempts table."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TypingAttempt:
    """User practice attempt record.

    Attributes:
        id: Unique attempt identifier
        user_id: Foreign key to users table
        character_id: Foreign key to characters table
        started_at: When user started typing this character
        ended_at: When user finished typing this character
        is_correct: Whether the attempt was successful
        duration_ms: Computed duration in milliseconds
        created_at: Record creation timestamp
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    character_id: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    is_correct: bool = False
    duration_ms: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row: tuple) -> 'TypingAttempt':
        """Create TypingAttempt instance from database row tuple.

        Args:
            row: Database row as tuple (id, user_id, character_id, started_at,
                 ended_at, is_correct, duration_ms, created_at)

        Returns:
            TypingAttempt instance
        """
        return cls(
            id=row[0],
            user_id=row[1],
            character_id=row[2],
            started_at=row[3],
            ended_at=row[4],
            is_correct=row[5],
            duration_ms=row[6],
            created_at=row[7]
        )

    def to_dict(self) -> dict:
        """Convert TypingAttempt to dictionary (for JSON responses).

        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_correct': self.is_correct,
            'duration_ms': self.duration_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
