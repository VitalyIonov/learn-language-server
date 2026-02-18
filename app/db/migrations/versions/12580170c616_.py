"""empty message

Revision ID: 12580170c616
Revises: 0dc212aabd1d
Create Date: 2026-02-18 13:10:48.939103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '12580170c616'
down_revision: Union[str, Sequence[str], None] = '0dc212aabd1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE languagecode RENAME TO targetlanguagecode")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE targetlanguagecode RENAME TO languagecode")
