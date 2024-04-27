"""add content columnt to posts table

Revision ID: f6b6f62ce491
Revises: f6355cec85cb
Create Date: 2024-04-27 21:54:03.024113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6b6f62ce491'
down_revision: Union[str, None] = 'f6355cec85cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
