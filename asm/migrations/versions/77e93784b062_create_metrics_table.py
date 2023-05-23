"""create Metrics table

Revision ID: 77e93784b062
Revises: 57ba06080afd
Create Date: 2023-05-22 18:15:52.850521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77e93784b062'
down_revision = '57ba06080afd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "metrics",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("instance_id", sa.String(120), nullable=False),
        sa.Column("cpu_usage", sa.Integer, nullable=False),
        sa.Column("ram_usage", sa.Integer, nullable=False),
        sa.Column("disk_usage", sa.Integer, nullable=False),
        sa.Column("network_usage", sa.String(60), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("metrics")
