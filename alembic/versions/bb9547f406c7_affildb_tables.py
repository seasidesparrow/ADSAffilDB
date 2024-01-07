"""Empty init

Revision ID: bb9547f406c7
Revises: 00ac51e83198
Create Date: 2023-11-16 15:00:00.000000

"""
import sqlalchemy as sa
from adsputils import UTCDateTime, get_date

from alembic import op

# revision identifiers, used by Alembic.
revision = "bb9547f406c7"
down_revision = "00ac51e83198"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "affil_inst",
        sa.Column("inst_key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("inst_id", sa.String(), nullable=False),
        sa.Column("inst_parents", sa.String(), nullable=True),
        sa.Column("inst_canonical", sa.String(), nullable=False),
        sa.Column("inst_abbreviated", sa.String(), nullable=False),
        sa.Column("inst_location", sa.String(), nullable=True),
        sa.Column("inst_country", sa.String(), nullable=True),
        sa.Column("inst_rorid", sa.String(), nullable=True),
        sa.Column("created", UTCDateTime, nullable=True, default=get_date),
        sa.PrimaryKeyConstraint("inst_key"),
        sa.UniqueConstraint("inst_key", "inst_id"),
    )

    op.create_table(
        "affil_data",
        sa.Column("data_key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("data_id", sa.String(), nullable=False),
        sa.Column("data_pubstring", sa.String(), nullable=False),
        sa.Column("created", UTCDateTime, nullable=True, default=get_date),
        sa.Column("updated", UTCDateTime, nullable=True, onupdate=get_date),
        sa.ForeignKeyConstraint(["data_id"], ["affil_inst.inst_id"]),
        sa.PrimaryKeyConstraint("data_key"),
        sa.UniqueConstraint("data_key", "data_pubstring"),
    )

    # end of Alembic upgrade


def downgrade() -> None:
    op.drop_table("affil_matches")
    op.drop_table("affil_identifiers")

    # end of Alembic downgrade
