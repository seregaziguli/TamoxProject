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

order_status_enum = sa.Enum('NEW', 'IN PROGRESS', 'COMPLETED', 'CANCELLED', name='orderstatus')
order_assignment_status_enum = sa.Enum('PENDING', 'IN PROGRESS', 'COMPLETED', 'CANCELLED', name='orderassignmentstatus')
order_assignment_policy_enum = sa.Enum('EXCLUSIVE', 'MULTIPLE', name='orderassignmentpolicy')


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('scheduled_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('status', order_status_enum, default='NEW', nullable=False),
        sa.Column('service_type_name', sa.String(), nullable=True),
        sa.Column('assignment_policy', order_assignment_policy_enum, default='MULTIPLE', nullable=False),
    )

    op.create_table(
        'order_assignments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('provider_id', sa.Integer(), nullable=False),
        sa.Column('status', order_assignment_status_enum, default='PENDING', nullable=False),
        sa.Column('completion_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('is_confirmed', sa.Boolean(), default=False),
    )


def downgrade() -> None:
    op.drop_table('order_assignments')

    op.drop_table('orders')

    order_status_enum.drop(op.get_bind(), checkfirst=False)
    order_assignment_status_enum.drop(op.get_bind(), checkfirst=False)
    order_assignment_policy_enum.drop(op.get_bind(), checkfirst=False)