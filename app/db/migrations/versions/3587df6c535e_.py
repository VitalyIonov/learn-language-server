"""empty message

Revision ID: 3587df6c535e
Revises: d10a465e1839
Create Date: 2026-03-04 19:40:15.770092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3587df6c535e'
down_revision: Union[str, Sequence[str], None] = 'd10a465e1839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('meanings_progress_info', sa.Column('language', sa.String(), server_default='ES', nullable=False))
    op.drop_constraint('meanings_progress_info_pkey', 'meanings_progress_info', type_='primary')
    op.create_primary_key('meanings_progress_info_pkey', 'meanings_progress_info', ['user_id', 'meaning_id', 'level_id', 'language'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('meanings_progress_info_pkey', 'meanings_progress_info', type_='primary')
    op.create_primary_key('meanings_progress_info_pkey', 'meanings_progress_info', ['user_id', 'meaning_id', 'level_id'])
    op.drop_column('meanings_progress_info', 'language')
