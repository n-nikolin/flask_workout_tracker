"""empty message

Revision ID: 45bd3efc6bc2
Revises: 4f3b589d2a6e
Create Date: 2021-11-25 17:24:17.103698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45bd3efc6bc2'
down_revision = '4f3b589d2a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('set', sa.Column('duration', sa.Integer(), nullable=True))
    op.drop_column('set', 'durarion')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('set', sa.Column('durarion', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('set', 'duration')
    # ### end Alembic commands ###
