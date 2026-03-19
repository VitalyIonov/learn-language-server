"""normalize translation lang codes to uppercase

Revision ID: e3ff2ea2c840
Revises: 24ae86d0b547
Create Date: 2026-03-19 15:54:29.185250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3ff2ea2c840'
down_revision: Union[str, Sequence[str], None] = '24ae86d0b547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DELETE FROM translations t1
        USING translations t2
        WHERE t1.id < t2.id
          AND t1.text = t2.text
          AND UPPER(t1.lang_from) = UPPER(t2.lang_from)
          AND UPPER(t1.lang_to) = UPPER(t2.lang_to)
    """)
    op.execute(
        "UPDATE translations SET lang_from = UPPER(lang_from), lang_to = UPPER(lang_to)"
    )


def downgrade() -> None:
    pass
