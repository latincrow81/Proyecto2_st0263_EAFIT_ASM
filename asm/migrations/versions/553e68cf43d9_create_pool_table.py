"""create Pool table

Revision ID: 553e68cf43d9
Revises: 
Create Date: 2023-05-22 18:15:35.800974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '553e68cf43d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pool",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("pool_name", sa.String(60), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("pool")

