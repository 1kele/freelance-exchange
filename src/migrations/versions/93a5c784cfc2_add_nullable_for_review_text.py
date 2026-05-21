"""add nullable for review text

Revision ID: 93a5c784cfc2
Revises: c85f8d36dc79
Create Date: 2026-05-13 09:27:50.244860

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "93a5c784cfc2"
down_revision: Union[str, Sequence[str], None] = "c85f8d36dc79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column("is_overdue", sa.Boolean(), nullable=False, server_default="false"),
    )


def downgrade() -> None:
    op.drop_column("orders", "is_overdue")
