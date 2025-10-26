"""empty message

Revision ID: 0f95640c7525
Revises: 0c75eedf19d0
Create Date: 2025-10-08 16:18:42.523338
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0f95640c7525"
down_revision: Union[str, Sequence[str], None] = "0c75eedf19d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "public"
TABLE = "translations"
COL = "context"
IX = op.f("ix_translations_context")


def _has_table(insp: sa.Inspector, table: str, schema: str) -> bool:
    return insp.has_table(table_name=table, schema=schema)


def _has_column(insp: sa.Inspector, table: str, col: str, schema: str) -> bool:
    return any(c["name"] == col for c in insp.get_columns(table, schema=schema))


def _has_index(insp: sa.Inspector, table: str, index_name: str, schema: str) -> bool:
    return any(
        ix["name"] == index_name for ix in insp.get_indexes(table, schema=schema)
    )


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if _has_table(insp, TABLE, SCHEMA):
        if not _has_column(insp, TABLE, COL, SCHEMA):
            op.add_column(
                TABLE, sa.Column(COL, sa.String(), nullable=True), schema=SCHEMA
            )

        if not _has_index(insp, TABLE, IX, SCHEMA):
            op.create_index(IX, TABLE, [COL], unique=False, schema=SCHEMA)


def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if _has_table(insp, TABLE, SCHEMA):
        if _has_index(insp, TABLE, IX, SCHEMA):
            op.drop_index(IX, table_name=TABLE, schema=SCHEMA)

        if _has_column(insp, TABLE, COL, SCHEMA):
            op.drop_column(TABLE, COL, schema=SCHEMA)
