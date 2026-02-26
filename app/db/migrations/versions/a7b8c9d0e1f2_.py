"""change chance type to float in definitions_progress_info

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-02-26 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "definitions_progress_info",
        "chance",
        type_=sa.Float(),
        existing_server_default="100",
    )


def downgrade() -> None:
    op.alter_column(
        "definitions_progress_info",
        "chance",
        type_=sa.Integer(),
        existing_server_default="100",
    )
