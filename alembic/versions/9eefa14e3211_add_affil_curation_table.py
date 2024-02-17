"""Empty init

Revision ID: 9eefa14e3211
Revises: c54d158658da
Create Date: 2024-01-08 00:07:00.000000

"""
import sqlalchemy as sa
from adsputils import UTCDateTime, get_date

from alembic import op

# revision identifiers, used by Alembic.
revision = "9eefa14e3211"
down_revision = "c54d158658da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "affil_curation",
        sa.Column("curation_key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("curation_count", sa.Integer(), nullable=True)
        sa.Column("curation_id", sa.String(), nullable=True),
        sa.Column("curation_string", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("curation_key"),
        sa.UniqueConstraint("curation_string"),
    )

    # end of Alembic upgrade


def downgrade() -> None:
    op.drop_table("affil_curation")

    # end of Alembic downgrade
