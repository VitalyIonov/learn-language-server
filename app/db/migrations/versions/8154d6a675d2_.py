"""empty message

Revision ID: 8154d6a675d2
Revises: d872cf896c08
Create Date: 2026-02-22 10:33:54.833430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8154d6a675d2'
down_revision: Union[str, Sequence[str], None] = 'd872cf896c08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Drop enum-typed defaults
    op.execute("ALTER TABLE definitions ALTER COLUMN language DROP DEFAULT")
    op.execute("ALTER TABLE meanings ALTER COLUMN language DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN target_language DROP DEFAULT")

    # 2. Change column types from enum to varchar
    op.execute("ALTER TABLE definitions ALTER COLUMN language TYPE VARCHAR USING language::text")
    op.execute("ALTER TABLE meanings ALTER COLUMN language TYPE VARCHAR USING language::text")
    op.execute("ALTER TABLE users ALTER COLUMN target_language TYPE VARCHAR USING target_language::text")

    # 3. Set new plain string defaults
    op.execute("ALTER TABLE definitions ALTER COLUMN language SET DEFAULT 'ES'")
    op.execute("ALTER TABLE meanings ALTER COLUMN language SET DEFAULT 'ES'")
    op.execute("ALTER TABLE users ALTER COLUMN target_language SET DEFAULT 'ES'")

    # 4. Drop the enum type
    op.execute("DROP TYPE IF EXISTS targetlanguagecode")


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Recreate enum type
    op.execute("CREATE TYPE targetlanguagecode AS ENUM ('EN', 'ES')")

    # 2. Drop plain defaults
    op.execute("ALTER TABLE definitions ALTER COLUMN language DROP DEFAULT")
    op.execute("ALTER TABLE meanings ALTER COLUMN language DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN target_language DROP DEFAULT")

    # 3. Change columns back to enum
    op.execute("ALTER TABLE definitions ALTER COLUMN language TYPE targetlanguagecode USING language::targetlanguagecode")
    op.execute("ALTER TABLE meanings ALTER COLUMN language TYPE targetlanguagecode USING language::targetlanguagecode")
    op.execute("ALTER TABLE users ALTER COLUMN target_language TYPE targetlanguagecode USING target_language::targetlanguagecode")

    # 4. Restore enum-typed defaults
    op.execute("ALTER TABLE definitions ALTER COLUMN language SET DEFAULT 'ES'::targetlanguagecode")
    op.execute("ALTER TABLE meanings ALTER COLUMN language SET DEFAULT 'ES'::targetlanguagecode")
    op.execute("ALTER TABLE users ALTER COLUMN target_language SET DEFAULT 'ES'::targetlanguagecode")
