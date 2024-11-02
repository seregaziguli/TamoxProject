"""initial

Revision ID: f511ed0c5f9b
Revises: 
Create Date: 2024-11-02 11:16:33.180909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f511ed0c5f9b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('scheduled_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('status', sa.Enum('NEW', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='orderstatus'), 
                  nullable=False, default='NEW'),
        sa.Column('service_type_name', sa.String, nullable=True)
    )

    op.create_table(
        'order_assignments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('provider_id', sa.Integer, nullable=False),
        sa.Column('satus', sa.Enum('PENGIND', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='orderassignmentstatus'),
                  nullable=False, default='PENGIND'),
        sa.Column('completion_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('order_assignments')
    op.drop_table('orders')
    op.execute('DROP TYPE orderstatus')
    op.execute('DROP TYPE orderassignmentstatus')