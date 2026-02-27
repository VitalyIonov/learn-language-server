"""drop question_types and levels_question_types tables

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-02-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8c9d0e1f2a3"
down_revision: Union[str, None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("levels_question_types")
    op.drop_table("question_types")


def downgrade() -> None:
    op.create_table(
        "question_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
    )
    op.create_index("ix_question_types_name", "question_types", ["name"])
    op.create_table(
        "levels_question_types",
        sa.Column(
            "level_id",
            sa.Integer(),
            sa.ForeignKey("levels.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "question_type_id",
            sa.Integer(),
            sa.ForeignKey("question_types.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
