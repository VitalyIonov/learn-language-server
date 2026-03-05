"""empty message

Revision ID: a8568815ed59
Revises: 8771d7a6681e
Create Date: 2026-03-05 15:09:22.419655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8568815ed59'
down_revision: Union[str, Sequence[str], None] = '8771d7a6681e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('text_definitions', 'language', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('text_definitions', 'language', server_default='ES')
