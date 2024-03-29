"""empty message

Revision ID: 18febd054222
Revises: 52d86cf9214a
Create Date: 2022-03-16 21:27:47.929756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18febd054222'
down_revision = '52d86cf9214a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=250), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
