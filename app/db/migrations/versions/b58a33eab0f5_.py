"""empty message

Revision ID: b58a33eab0f5
Revises: 9240e7effe56
Create Date: 2026-02-18 15:59:53.633142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b58a33eab0f5'
down_revision: Union[str, Sequence[str], None] = '9240e7effe56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    interfacelanguagecode = sa.Enum('EN', 'RU', 'ES', 'FR', 'IT', name='interfacelanguagecode')
    interfacelanguagecode.create(op.get_bind(), checkfirst=True)
    op.execute("UPDATE users SET interface_lang = UPPER(interface_lang)")
    op.alter_column('users', 'interface_lang', server_default=None)
    op.alter_column('users', 'interface_lang',
               existing_type=sa.VARCHAR(),
               type_=interfacelanguagecode,
               existing_nullable=False,
               postgresql_using="interface_lang::interfacelanguagecode")
    op.alter_column('users', 'interface_lang', server_default=sa.text("'RU'::interfacelanguagecode"))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'interface_lang', server_default=sa.text("'ru'::character varying"))
    op.execute("UPDATE users SET interface_lang = LOWER(interface_lang)")
    op.alter_column('users', 'interface_lang',
               existing_type=sa.Enum('EN', 'RU', 'ES', 'FR', 'IT', name='interfacelanguagecode'),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               postgresql_using="interface_lang::text")
    sa.Enum(name='interfacelanguagecode').drop(op.get_bind(), checkfirst=True)
