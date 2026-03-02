"""add_file_url_to_user_cvs

Revision ID: baa1915905ad
Revises: 2eae5ffa64e9
Create Date: 2026-03-02 21:02:27.685348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baa1915905ad'
down_revision: Union[str, Sequence[str], None] = '2eae5ffa64e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
