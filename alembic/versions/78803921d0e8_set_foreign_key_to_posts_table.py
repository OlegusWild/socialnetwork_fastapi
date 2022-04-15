"""set foreign key to posts table

Revision ID: 78803921d0e8
Revises: ce7659db2b04
Create Date: 2022-02-20 13:51:57.983150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78803921d0e8'
down_revision = 'ce7659db2b04'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                            local_cols=['owner_id'], remote_cols=['id'],
                            ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
