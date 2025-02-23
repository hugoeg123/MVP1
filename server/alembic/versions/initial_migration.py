"""initial migration

Revision ID: 001
Revises: 
Create Date: 2023-11-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=func.now())
    )


def downgrade():
    op.drop_table('users')