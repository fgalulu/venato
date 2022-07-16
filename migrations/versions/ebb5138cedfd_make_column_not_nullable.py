"""make column not nullable

Revision ID: ebb5138cedfd
Revises: ff97a3226a72
Create Date: 2022-07-16 12:36:20.483579

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ebb5138cedfd'
down_revision = 'ff97a3226a72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'supervised_by',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'supervised_by',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
