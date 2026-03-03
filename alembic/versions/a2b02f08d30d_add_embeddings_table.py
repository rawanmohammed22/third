"""add embeddings table

Revision ID: a2b02f08d30d
Revises: b57f1905f093
Create Date: 2026-03-03 00:09:01.102040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a2b02f08d30d'
down_revision: Union[str, Sequence[str], None] = 'b57f1905f093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        'embeddings',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('embedding', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute("ALTER TABLE embeddings ALTER COLUMN embedding TYPE vector(1024) USING embedding::vector")


def downgrade() -> None:
    op.drop_table('embeddings')