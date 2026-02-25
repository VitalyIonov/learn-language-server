"""add category_id to meanings_progress_info

Revision ID: a1b2c3d4e5f6
Revises: 80e9bd70e171
Create Date: 2026-02-25 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "80e9bd70e171"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Phase 1: Add column as nullable
    op.add_column(
        "meanings_progress_info",
        sa.Column("category_id", sa.Integer(), nullable=True),
    )

    # Phase 2: Backfill from meanings table
    op.execute(
        """
        UPDATE meanings_progress_info
        SET category_id = meanings.category_id
        FROM meanings
        WHERE meanings_progress_info.meaning_id = meanings.id
        """
    )

    # Safety: remove rows where meaning has no category
    op.execute(
        """
        DELETE FROM meanings_progress_info
        WHERE category_id IS NULL
        """
    )

    # Phase 3: Set NOT NULL, add FK and index
    op.alter_column(
        "meanings_progress_info",
        "category_id",
        nullable=False,
    )
    op.create_foreign_key(
        "fk_meanings_progress_info_category_id_categories",
        "meanings_progress_info",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        op.f("ix_meanings_progress_info_category_id"),
        "meanings_progress_info",
        ["category_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_meanings_progress_info_category_id"),
        table_name="meanings_progress_info",
    )
    op.drop_constraint(
        "fk_meanings_progress_info_category_id_categories",
        "meanings_progress_info",
        type_="foreignkey",
    )
    op.drop_column("meanings_progress_info", "category_id")
