"""create posts table

Revision ID: 8f7b1539225f
Revises: 
Create Date: 2022-02-20 13:23:19.965313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f7b1539225f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                        sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
