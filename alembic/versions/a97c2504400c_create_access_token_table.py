"""create access token table

Revision ID: a97c2504400c
Revises: 2ffa6c9afe25
Create Date: 2023-11-21 15:20:03.344357

"""
from datetime import datetime, timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97c2504400c'
down_revision: Union[str, None] = '2ffa6c9afe25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('access_tokens',
                    sa.Column('id', sa.Integer(), autoincrement=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('token', sa.String(), nullable=False),
                    sa.Column('expires_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now() + interval '1 week'"), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    )


def downgrade() -> None:
    op.drop_table('access_tokens')
