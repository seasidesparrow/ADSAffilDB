""" Add ROR table

Revision ID: 75098bacbee6
Revises: 9eefa14e3211
Create Date: 2024-01-08 00:07:00.000000

"""
import sqlalchemy as sa
from adsputils import UTCDateTime, get_date

from alembic import op

# revision identifiers, used by Alembic.
revision = "75098bacbee6"
down_revision = "9eefa14e3211"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ror_idents",
        sa.Column("ror_key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ror_id", sa.String(), nullable=True),
        sa.Column("ror_country", sa.String(), nullable=True),
        sa.Column("ror_name", sa.String(), nullable=True),
        sa.Column("ror_relations", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("ror_key"),
        sa.Index("id_name", "ror_key", "ror_id", "ror_name"),
        sa.Index("id_relations", "ror_key", "ror_id", "ror_name", "ror_relations"),
    )

    # end of Alembic upgrade


def downgrade() -> None:
    op.drop_table("ror_idents")

    # end of Alembic downgrade
