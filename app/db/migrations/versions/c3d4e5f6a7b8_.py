"""add level_id and category_id to definitions_progress_info

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-02-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Phase 1: Add columns as nullable
    op.add_column(
        "definitions_progress_info",
        sa.Column("level_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "definitions_progress_info",
        sa.Column("category_id", sa.Integer(), nullable=True),
    )

    # Phase 2: Backfill from definitions table
    op.execute(
        """
        UPDATE definitions_progress_info
        SET level_id = d.level_id, category_id = d.category_id
        FROM definitions d
        WHERE definitions_progress_info.definition_id = d.id
        """
    )

    # Safety: remove rows where definition has no level/category
    op.execute(
        """
        DELETE FROM definitions_progress_info
        WHERE level_id IS NULL OR category_id IS NULL
        """
    )

    # Phase 3: Set NOT NULL, add FK constraints and indexes
    op.alter_column(
        "definitions_progress_info",
        "level_id",
        nullable=False,
    )
    op.alter_column(
        "definitions_progress_info",
        "category_id",
        nullable=False,
    )
    op.create_foreign_key(
        "fk_definitions_progress_info_level_id_levels",
        "definitions_progress_info",
        "levels",
        ["level_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_definitions_progress_info_category_id_categories",
        "definitions_progress_info",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        op.f("ix_definitions_progress_info_level_id"),
        "definitions_progress_info",
        ["level_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_definitions_progress_info_category_id"),
        "definitions_progress_info",
        ["category_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_definitions_progress_info_category_id"),
        table_name="definitions_progress_info",
    )
    op.drop_index(
        op.f("ix_definitions_progress_info_level_id"),
        table_name="definitions_progress_info",
    )
    op.drop_constraint(
        "fk_definitions_progress_info_category_id_categories",
        "definitions_progress_info",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_definitions_progress_info_level_id_levels",
        "definitions_progress_info",
        type_="foreignkey",
    )
    op.drop_column("definitions_progress_info", "category_id")
    op.drop_column("definitions_progress_info", "level_id")
