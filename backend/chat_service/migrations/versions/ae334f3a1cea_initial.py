"""initial

Revision ID: ae334f3a1cea
Revises: 
Create Date: 2024-12-06 19:54:17.475196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae334f3a1cea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('from_user_id', sa.Integer, nullable=False),
        sa.Column('to_user_id', sa.Integer, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('edited_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('messages')
