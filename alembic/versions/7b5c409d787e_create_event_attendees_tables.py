"""create event attendees tables

Revision ID: 7b5c409d787e
Revises: 9d02adeef34e
Create Date: 2023-12-03 22:24:31.523082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b5c409d787e'
down_revision: Union[str, None] = '9d02adeef34e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('event_attendees',
                    sa.Column('event_id', sa.Integer(),
                              nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['event_id'], ['events.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('event_id', 'user_id')
                    )


def downgrade() -> None:
    op.drop_table('event_attendees')
