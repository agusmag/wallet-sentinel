"""Adding exchange_rates field in user_configuration

Revision ID: e35c7cf01cb4
Revises: 14d490af928c
Create Date: 2021-10-01 18:36:29.791815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e35c7cf01cb4'
down_revision = '14d490af928c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_configuration', sa.Column('exchange_rates', sa.String(length=100), nullable=True))
    op.execute('UPDATE user_configuration SET exchange_rates = "[1,1,1,1]"')
    op.alter_column('user_configuration', 'exchange_rates', nullable=False, existing_type=sa.VARCHAR)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_configuration', 'exchange_rates')
    # ### end Alembic commands ###
