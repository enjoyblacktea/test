"""initial_migration

Revision ID: 8bc0d66d369e
Revises:
Create Date: 2026-03-11 16:31:35.149537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "8bc0d66d369e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "characters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("character", sa.String(10), nullable=False),
        sa.Column("input_code", sa.String(50), nullable=False),
        sa.Column("input_method", sa.String(20), server_default="bopomofo", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("character", "input_method"),
    )
    op.create_index("ix_characters_input_method", "characters", ["input_method"], unique=False)

    op.create_table(
        "typing_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column(
            "duration_ms",
            sa.Integer(),
            sa.Computed("EXTRACT(EPOCH FROM (ended_at - started_at)) * 1000", persisted=True),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_typing_attempts_user_id", "typing_attempts", ["user_id"], unique=False)
    op.create_index("ix_typing_attempts_character_id", "typing_attempts", ["character_id"], unique=False)

    op.create_table(
        "keystroke_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("attempt_id", sa.Integer(), nullable=False),
        sa.Column("key_value", sa.String(10), nullable=False),
        sa.Column("key_order", sa.SmallInteger(), nullable=False),
        sa.Column("typed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_correct_key", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["typing_attempts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_keystroke_events_attempt_id", "keystroke_events", ["attempt_id"], unique=False)

    op.execute("""
        INSERT INTO characters (character, input_code, input_method) VALUES
        ('你', 's u 3', 'bopomofo'), ('好', 'c l 3', 'bopomofo'), ('我', 'j i 3', 'bopomofo'),
        ('是', 'g 4', 'bopomofo'), ('的', '2 k 7', 'bopomofo'), ('了', 'x k 7', 'bopomofo'),
        ('人', 'b p 6', 'bopomofo'), ('在', 'y 9 4', 'bopomofo'), ('有', 'u . 3', 'bopomofo'),
        ('他', 'w 8  ', 'bopomofo'), ('這', '5 k 4', 'bopomofo'), ('中', '5 j /  ', 'bopomofo'),
        ('大', '2 8 4', 'bopomofo'), ('來', 'x 9 6', 'bopomofo'), ('上', 'g ; 4', 'bopomofo'),
        ('國', 'e j i 6', 'bopomofo'), ('個', 'e k 7', 'bopomofo'), ('到', '2 l 4', 'bopomofo'),
        ('說', 'g j i  ', 'bopomofo'), ('們', 'a p 7', 'bopomofo'), ('為', 'j o 4', 'bopomofo'),
        ('子', 'y 3', 'bopomofo'), ('學', 'v m , 6', 'bopomofo'), ('生', 'g /  ', 'bopomofo'),
        ('可', 'd k 3', 'bopomofo'), ('以', 'u 3', 'bopomofo'), ('會', 'c j o 4', 'bopomofo'),
        ('家', 'r u 8  ', 'bopomofo'), ('天', 'w u 0  ', 'bopomofo'), ('年', 's u 0 6', 'bopomofo')
        ON CONFLICT (character, input_method) DO NOTHING
    """)


def downgrade() -> None:
    op.drop_table("keystroke_events")
    op.drop_table("typing_attempts")
    op.drop_table("characters")
    op.drop_table("users")
