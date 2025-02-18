"""added created_at column to jobs table

Revision ID: 174640fed63d
Revises: 6e075c61cbc0
Create Date: 2025-02-18 01:00:12.047253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '174640fed63d'
down_revision: Union[str, None] = '6e075c61cbc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
