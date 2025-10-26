"""empty message

Revision ID: 0c75eedf19d0
Revises: 87a13362d2ba
Create Date: 2025-10-08 13:00:09.260999
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0c75eedf19d0"
down_revision: Union[str, Sequence[str], None] = "87a13362d2ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "public"
TABLE = "translations"


def _has_table(insp, table: str, schema: str) -> bool:
    return insp.has_table(table_name=table, schema=schema)


def _has_index(insp, table: str, index_name: str, schema: str) -> bool:
    return any(
        ix["name"] == index_name for ix in insp.get_indexes(table, schema=schema)
    )


def upgrade() -> None:
    """Upgrade schema (idempotent)."""
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # реальные имена индексов с учётом naming_convention
    ix_text = op.f("ix_translations_text")
    ix_from = op.f("ix_translations_lang_from")
    ix_to = op.f("ix_translations_lang_to")

    if not _has_table(insp, TABLE, SCHEMA):
        op.create_table(
            TABLE,
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("text", sa.String(), nullable=False),
            sa.Column("translated_text", sa.String(), nullable=False),
            sa.Column("lang_from", sa.String(), nullable=False),
            sa.Column("lang_to", sa.String(), nullable=False),
            schema=SCHEMA,
        )
        # создаём индексы сразу после создания таблицы
        op.create_index(ix_from, TABLE, ["lang_from"], unique=False, schema=SCHEMA)
        op.create_index(ix_to, TABLE, ["lang_to"], unique=False, schema=SCHEMA)
        op.create_index(ix_text, TABLE, ["text"], unique=False, schema=SCHEMA)
    else:
        # таблица сохранена — создадим недостающие индексы (если их нет)
        if not _has_index(insp, TABLE, ix_from, SCHEMA):
            op.create_index(ix_from, TABLE, ["lang_from"], unique=False, schema=SCHEMA)
        if not _has_index(insp, TABLE, ix_to, SCHEMA):
            op.create_index(ix_to, TABLE, ["lang_to"], unique=False, schema=SCHEMA)
        if not _has_index(insp, TABLE, ix_text, SCHEMA):
            op.create_index(ix_text, TABLE, ["text"], unique=False, schema=SCHEMA)


def downgrade() -> None:
    """Downgrade schema (idempotent)."""
    bind = op.get_bind()
    insp = sa.inspect(bind)

    ix_text = op.f("ix_translations_text")
    ix_from = op.f("ix_translations_lang_from")
    ix_to = op.f("ix_translations_lang_to")

    # индексы удаляем только если есть
    if _has_table(insp, TABLE, SCHEMA):
        if _has_index(insp, TABLE, ix_text, SCHEMA):
            op.drop_index(ix_text, table_name=TABLE, schema=SCHEMA)
        if _has_index(insp, TABLE, ix_to, SCHEMA):
            op.drop_index(ix_to, table_name=TABLE, schema=SCHEMA)
        if _has_index(insp, TABLE, ix_from, SCHEMA):
            op.drop_index(ix_from, table_name=TABLE, schema=SCHEMA)
        # и саму таблицу — тоже только если есть
        op.drop_table(TABLE, schema=SCHEMA)
