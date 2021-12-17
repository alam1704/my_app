"""second migration

Revision ID: 96a9251fbd9d
Revises: f95708c40a40
Create Date: 2021-12-17 21:35:01.156819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96a9251fbd9d'
down_revision = 'f95708c40a40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'staff', 'pharmacy', ['creator_id'], ['pharmacy_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff', type_='foreignkey')
    op.drop_column('staff', 'creator_id')
    # ### end Alembic commands ###