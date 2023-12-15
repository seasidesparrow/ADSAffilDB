"""Empty init

Revision ID: bb9547f406c7
Revises: 00ac51e83198
Create Date: 2023-11-16 15:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb9547f406c7'
down_revision = '00ac51e83198'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('affil_identifiers',
                    sa.Column('masterid', sa.Integer(), autoincrement=True,
                              nullable=False),
                    sa.Column('parent_id', sa.String(), nullable=True),
                    sa.Column('affil_id', sa.String(), nullable=False),
                    sa.Column('inst_abbrev', sa.String(), nullable=False),
                    sa.Column('affil', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('created', UTCDateTime, nullable=True,
                              default=get_date),
                    sa.Column('updated', UTCDateTime, nullable=True,
                              onupdate=get_date),
                    sa.PrimaryKeyConstraint('masterid')
                    sa.UniqueConstraint('masterid'))

    op.create_table('affil_matches',
                    sa.Column('matchid', sa.Integer(), autoincrement=True,
                              nullable=False),
                    sa.Column('affil_id', sa.String(), nullable=False),
                    sa.Column('affil_text', sa.String(), nullable=False),
                    sa.Column('affil_norm', sa.String(), nullable=False),
                    sa.Column('counts', sa.Integer(), nullable=False),
                    sa.Column('created', UTCDateTime, nullable=True,
                              default=get_date),
                    sa.Column('updated', UTCDateTime, nullable=True,
                              onupdate=get_date),
                    sa.ForeignKeyConstraint(['affil_id'], ['affil_identifiers.affil_id']),
                    sa.PrimaryKeyConstraint('matchid')
                    sa.UniqueConstraint('matchid', 'affil_text'))
                   
    # end of Alembic upgrade


def downgrade() -> None:

    op.drop_table('affil_matches')
    op.drop_table('affil_identifiers')

    # end of Alembic downgrade
