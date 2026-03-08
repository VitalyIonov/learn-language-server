"""remove server_default from categories.language

Revision ID: 3bf66e842243
Revises: a73ef62389c0
Create Date: 2026-03-08 11:45:18.813672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bf66e842243'
down_revision: Union[str, Sequence[str], None] = 'a73ef62389c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('categories', 'language', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('categories', 'language', server_default='EN')
