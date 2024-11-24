"""initial

Revision ID: a3108a2bea9b
Revises: 
Create Date: 2024-11-24 18:58:01.564069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3108a2bea9b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('creator_id', sa.Integer, nullable=False),
        sa.Column('executor_id', sa.Integer, nullable=False),
        sa.Column('message', sa.String(length=255), nullable=False),
        sa.Column('is_read', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('notifications')
