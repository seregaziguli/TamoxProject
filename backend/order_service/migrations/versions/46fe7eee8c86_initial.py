"""initial

Revision ID: 46fe7eee8c86
Revises: 
Create Date: 2024-10-17 20:08:29.092523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '46fe7eee8c86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ### creating order table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('service_type_name', sa.String(), nullable=True),
        sa.Column('scheduled_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('status', postgresql.ENUM('NEW', 'IN PROGRESS', 'COMPLETED', 'CANCELLED', name='orderstatus'), 
                nullable=False, server_default='NEW'),
        sa.Column('assigned_provider_id', sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    # ### drop order table
    op.drop_table('orders')

    # ### drop ENUM type if used in PostgreSQL
    op.execute('DROP TYPE orderstatus')