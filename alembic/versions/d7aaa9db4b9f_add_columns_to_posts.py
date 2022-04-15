"""add columns to posts

Revision ID: d7aaa9db4b9f
Revises: 78803921d0e8
Create Date: 2022-02-20 13:58:57.527509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7aaa9db4b9f'
down_revision = '78803921d0e8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
