"""empty message

Revision ID: c2ea3198dbdc
Revises: e0cec502caa3
Create Date: 2021-08-05 21:24:08.897819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ea3198dbdc'
down_revision = 'e0cec502caa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'listbuku', 'user_tbl', ['id_peminjam'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'listbuku', type_='foreignkey')
    # ### end Alembic commands ###