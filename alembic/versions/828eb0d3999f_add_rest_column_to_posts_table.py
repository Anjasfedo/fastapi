"""add rest column to posts table

Revision ID: 828eb0d3999f
Revises: ec8805214b5a
Create Date: 2024-04-27 22:15:21.446519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '828eb0d3999f'
down_revision: Union[str, None] = 'ec8805214b5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'is_publish', sa.Boolean(), nullable=False, server_default='FALSE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'is_publish')
    op.drop_column('posts', 'created_at')
    pass
