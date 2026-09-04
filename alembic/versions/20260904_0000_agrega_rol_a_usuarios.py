"""Agrega rol a usuarios

Revision ID: 86ebd1ee34ca
Revises: 79e0d9454bf0
Create Date: 2026-09-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '86ebd1ee34ca'
down_revision: Union[str, Sequence[str], None] = '79e0d9454bf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role = postgresql.ENUM('customer', 'seller', 'admin', name='user_role')


def upgrade() -> None:
    """Upgrade schema."""
    user_role.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'users',
        sa.Column(
            'role',
            user_role,
            server_default='customer',
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    user_role.drop(op.get_bind(), checkfirst=True)
