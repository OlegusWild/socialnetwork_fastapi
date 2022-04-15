"""add column content to posts table

Revision ID: 7874fb46cab7
Revises: 8f7b1539225f
Create Date: 2022-02-20 13:36:46.303377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7874fb46cab7'
down_revision = '8f7b1539225f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
