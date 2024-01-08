"""Empty init

Revision ID: c54d158658da
Revises: bb9547f406c7
Create Date: 2024-01-08 00:07:00.000000

"""
import sqlalchemy as sa
from adsputils import UTCDateTime, get_date

from alembic import op

# revision identifiers, used by Alembic.
revision = "c54d158658da"
down_revision = "bb9547f406c7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "affil_norm",
        sa.Column("norm_key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("norm_id", sa.String(), nullable=False),
        sa.Column("norm_string", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("norm_key"),
        sa.UniqueConstraint("norm_string"),
    )

    # end of Alembic upgrade


def downgrade() -> None:
    op.drop_table("affil_norm")

    # end of Alembic downgrade
