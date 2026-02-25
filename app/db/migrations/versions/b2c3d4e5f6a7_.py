"""set default group for existing definitions

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-02-25 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE definitions SET \"group\" = 'ILLUSTRATION' WHERE type::text = 'IMAGE'")
    op.execute("UPDATE definitions SET \"group\" = 'PHRASE' WHERE type::text = 'TEXT'")


def downgrade() -> None:
    op.execute("UPDATE definitions SET \"group\" = NULL WHERE type::text IN ('IMAGE', 'TEXT')")
