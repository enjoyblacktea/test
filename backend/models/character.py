"""Character model representing characters table."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Character:
    """Chinese character with input method mapping.

    Attributes:
        id: Unique character identifier
        character: The Chinese character text
        input_code: Space-separated keyboard keys (e.g., "s u 3")
        input_method: Input method type (e.g., "bopomofo")
        created_at: Record creation timestamp
    """
    id: Optional[int] = None
    character: str = ""
    input_code: str = ""
    input_method: str = "bopomofo"
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Character':
        """Create Character instance from database row tuple.

        Args:
            row: Database row as tuple (id, character, input_code, input_method, created_at)

        Returns:
            Character instance
        """
        return cls(
            id=row[0],
            character=row[1],
            input_code=row[2],
            input_method=row[3],
            created_at=row[4]
        )

    def to_dict(self) -> dict:
        """Convert Character to dictionary (for JSON responses).

        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'character': self.character,
            'input_code': self.input_code,
            'input_method': self.input_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
