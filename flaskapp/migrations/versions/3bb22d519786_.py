"""empty message

Revision ID: 3bb22d519786
Revises: 8cec083b10fc
Create Date: 2021-02-10 03:40:58.799862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb22d519786'
down_revision = '8cec083b10fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('operation', sa.Column('currency_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'operation', 'currency', ['currency_id'], ['id'])
    op.create_foreign_key(None, 'operation', 'operation_type', ['type_id'], ['id'])
    op.add_column('operation', sa.Column('from_saving'), sa.Boolean(), nullable=False, server_default=0)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'operation', type_='foreignkey')
    op.drop_constraint(None, 'operation', type_='foreignkey')
    op.drop_column('operation', 'currency_id')
    op.drop_column('operation', 'from_saving')
    # ### end Alembic commands ###