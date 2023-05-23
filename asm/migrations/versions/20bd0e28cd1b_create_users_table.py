"""create users table

Revision ID: 20bd0e28cd1b
Revises: 69a549fc87c3
Create Date: 2023-05-22 20:28:26.759877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20bd0e28cd1b'
down_revision = '69a549fc87c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(60), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("activated", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("users")
