"""add document_chunks table

Revision ID: ca98ef7a31d7
Revises: a2b02f08d30d
Create Date: 2026-03-03 02:44:29.728646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca98ef7a31d7'
down_revision: Union[str, Sequence[str], None] = 'a2b02f08d30d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'document_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pdf_name', sa.String(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_chunks_id', 'document_chunks', ['id'], unique=False)
    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1024) USING embedding::vector")


def downgrade() -> None:
    op.drop_index('ix_document_chunks_id', table_name='document_chunks')
    op.drop_table('document_chunks')