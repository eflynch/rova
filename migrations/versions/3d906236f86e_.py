"""empty message

Revision ID: 3d906236f86e
Revises: None
Create Date: 2015-07-19 18:39:10.588662

"""

# revision identifiers, used by Alembic.
revision = '3d906236f86e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('passhash', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')
