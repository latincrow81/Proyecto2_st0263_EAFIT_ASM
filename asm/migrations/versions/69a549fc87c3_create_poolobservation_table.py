"""create PoolObservation table

Revision ID: 69a549fc87c3
Revises: 77e93784b062
Create Date: 2023-05-22 18:16:01.917939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69a549fc87c3'
down_revision = '77e93784b062'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pool_observation",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("pool_id", sa.Integer, nullable=False),
        sa.Column("healthy_count", sa.Integer, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("pool_observation")
