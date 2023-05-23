"""create Instance table

Revision ID: 57ba06080afd
Revises: 553e68cf43d9
Create Date: 2023-05-22 18:15:46.073443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57ba06080afd'
down_revision = '553e68cf43d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "instance",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("instance_id", sa.Integer, nullable=False),
        sa.Column("pool_id", sa.Integer, nullable=False),
        sa.Column("status", sa.String(60), nullable=False),
        sa.Column("instance_endpoint", sa.String(120), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("instance")
