"""initial

Revision ID: aaa0980f7110
Revises: 
Create Date: 2024-11-02 11:59:46.340063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision: str = 'aaa0980f7110'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enums
order_status_enum = sa.Enum('NEW', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='orderstatus')
order_assignment_status_enum = sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='orderassignmentstatus')
order_assignment_policy_enum = sa.Enum('EXCLUSIVE', 'MULTIPLE', name='orderassignmentpolicy')

def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('scheduled_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('status', order_status_enum, nullable=False),
        sa.Column('service_type_name', sa.String(), nullable=True),
        sa.Column('assignment_policy', order_assignment_policy_enum, nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_orders_user_id', 'user_id'),
        sa.Index('ix_orders_status', 'status'),
        sa.Index('ix_orders_assignment_policy', 'assignment_policy'),
    )

    op.create_table(
        'order_assignments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('provider_id', sa.Integer(), nullable=False),
        sa.Column('status', order_assignment_status_enum, nullable=False),
        sa.Column('completion_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('is_confirmed', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('order_assignments')
    op.drop_table('orders')

    order_status_enum.drop(op.get_bind(), checkfirst=False)
    order_assignment_status_enum.drop(op.get_bind(), checkfirst=False)
    order_assignment_policy_enum.drop(op.get_bind(), checkfirst=False)
