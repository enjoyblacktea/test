"""User model representing users table."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User account model.

    Attributes:
        id: Unique user identifier
        username: Unique username for login
        password_hash: Bcrypt hashed password
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row: tuple) -> 'User':
        """Create User instance from database row tuple.

        Args:
            row: Database row as tuple (id, username, password_hash, created_at, updated_at)

        Returns:
            User instance
        """
        return cls(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            created_at=row[3],
            updated_at=row[4]
        )

    def to_dict(self, include_password=False) -> dict:
        """Convert User to dictionary (for JSON responses).

        Args:
            include_password: Whether to include password_hash (default False for security)

        Returns:
            Dictionary representation
        """
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_password:
            data['password_hash'] = self.password_hash
        return data
