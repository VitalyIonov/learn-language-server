"""split assets into image/audio

Revision ID: 2394f928752b
Revises: bb6a5dd85b1d
Create Date: 2025-09-06 14:22:16.295413

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2394f928752b"
down_revision: Union[str, Sequence[str], None] = "bb6a5dd85b1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ASSET_TYPE_ENUM_VALUES = ("AUDIO", "IMAGE")
ASSET_STATUS_ENUM_VALUES = ("pending", "ready", "failed")


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname = 'assetstatus' AND e.enumlabel = 'FAILED'
            ) THEN
                ALTER TYPE assetstatus ADD VALUE 'FAILED';
            END IF;
        END$$;
        """
        )

    with op.batch_alter_table("assets") as batch_op:
        batch_op.add_column(
            sa.Column(
                "type",
                sa.Enum(*ASSET_TYPE_ENUM_VALUES, name="assettype", native_enum=False),
                nullable=False,
                server_default="IMAGE",
            )
        )
        batch_op.create_index("ix_assets_type", ["type"])
        # Если status был нативным ENUM (Postgres native_enum=True), раскомментируйте ниже:
        # op.execute("ALTER TYPE assetstatus ADD VALUE IF NOT EXISTS 'failed'")

    # 2) create image_assets
    op.create_table(
        "image_assets",
        sa.Column(
            "id",
            sa.Integer(),
            sa.ForeignKey("assets.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("alt", sa.String(length=100), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "(width IS NULL) OR (width >= 0)", name="ck_img_width_nonneg"
        ),
        sa.CheckConstraint(
            "(height IS NULL) OR (height >= 0)", name="ck_img_height_nonneg"
        ),
    )

    # 3) create audio_assets (пока пустая схема; данных ещё нет)
    op.create_table(
        "audio_assets",
        sa.Column(
            "id",
            sa.Integer(),
            sa.ForeignKey("assets.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("duration", sa.Integer(), nullable=False, server_default="0"),
        sa.CheckConstraint("duration >= 0", name="ck_audio_duration_nonneg"),
    )

    # 4) copy data from old columns to image_assets
    # Эти колонки должны существовать в старой схеме assets:
    # alt (NOT NULL), width (NULL), height (NULL).
    # Если у вас их уже нет — этот шаг пропустится с ошибкой; тогда удалите execute-блок и шаг 6.
    op.execute(
        """
           INSERT INTO image_assets (id, alt, width, height)
           SELECT id, alt, width, height
           FROM assets
       """
    )

    # 5) set type='image' to all existing rows (на будущее)
    op.execute("UPDATE assets SET type = 'IMAGE' WHERE type IS NULL OR type <> 'IMAGE'")

    # 6) drop legacy columns from assets
    # В SQLite нужен batch_alter_table
    with op.batch_alter_table("assets") as batch_op:
        # удаляем старые поля, если они были
        try:
            batch_op.drop_column("alt")
        except Exception:
            pass
        try:
            batch_op.drop_column("width")
        except Exception:
            pass
        try:
            batch_op.drop_column("height")
        except Exception:
            pass

    # 7) remove server_default from assets.type
    with op.batch_alter_table("assets") as batch_op:
        batch_op.alter_column("type", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("assets") as batch_op:
        batch_op.add_column(
            sa.Column("alt", sa.String(length=100), nullable=False, server_default="")
        )
        batch_op.add_column(sa.Column("width", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("height", sa.Integer(), nullable=True))

    # Перекладка данных обратно
    op.execute(
        """
        UPDATE assets a
        SET alt = ia.alt,
            width = ia.width,
            height = ia.height
        FROM image_assets ia
        WHERE ia.id = a.id
    """
    )

    # Удаляем дочерние таблицы
    op.drop_table("audio_assets")
    op.drop_table("image_assets")

    # Удаляем индекс и колонку type
    with op.batch_alter_table("assets") as batch_op:
        try:
            batch_op.drop_index("ix_assets_type")
        except Exception:
            pass
        batch_op.drop_column("type")
