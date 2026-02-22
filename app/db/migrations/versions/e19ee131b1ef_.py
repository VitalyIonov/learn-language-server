"""empty message

Revision ID: e19ee131b1ef
Revises: 8154d6a675d2
Create Date: 2026-02-22 10:42:42.514148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e19ee131b1ef'
down_revision: Union[str, Sequence[str], None] = '8154d6a675d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang TYPE VARCHAR USING interface_lang::text")
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang SET DEFAULT 'RU'")
    op.execute("DROP TYPE IF EXISTS interfacelanguagecode")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("CREATE TYPE interfacelanguagecode AS ENUM ('EN', 'RU', 'ES', 'FR', 'IT')")
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang TYPE interfacelanguagecode USING interface_lang::interfacelanguagecode")
    op.execute("ALTER TABLE users ALTER COLUMN interface_lang SET DEFAULT 'RU'::interfacelanguagecode")
