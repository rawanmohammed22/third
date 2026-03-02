"""missing migration

Revision ID: 32822cb792ef
Revises: feb39eaabab8
Create Date: 2026-03-01 00:00:00.000000

"""
from typing import Sequence, Union

revision: str = '32822cb792ef'
down_revision: Union[str, Sequence[str], None] = 'feb39eaabab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass