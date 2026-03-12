"""add character_metadata and user_goals

Revision ID: 7abab4152c4e
Revises: 8bc0d66d369e
Create Date: 2026-03-12 13:46:30.867359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7abab4152c4e'
down_revision: Union[str, Sequence[str], None] = '8bc0d66d369e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'character_metadata',
        sa.Column('character_id', sa.Integer(), nullable=False),
        sa.Column('initial', sa.String(length=5), nullable=True),
        sa.Column('final', sa.String(length=10), nullable=True),
        sa.Column('tone', sa.SmallInteger(), nullable=True),
        sa.Column('difficulty', sa.SmallInteger(), nullable=False),
        sa.Column('frequency_rank', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('character_id'),
    )
    op.create_table(
        'user_goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('daily_target', sa.SmallInteger(), nullable=False),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_goals_effective_date', 'user_goals', ['effective_date'], unique=False)
    op.create_index('ix_user_goals_user_id', 'user_goals', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_user_goals_user_id', table_name='user_goals')
    op.drop_index('ix_user_goals_effective_date', table_name='user_goals')
    op.drop_table('user_goals')
    op.drop_table('character_metadata')
