"""add video_chunks table"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'cf4eeac37605'
down_revision: Union[str, Sequence[str], None] = 'ca98ef7a31d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'video_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.Integer(), nullable=False),
        sa.Column('video_name', sa.String(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('start_time', sa.Float(), nullable=False),
        sa.Column('end_time', sa.Float(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('embedding', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_video_chunks_id', 'video_chunks', ['id'], unique=False)
    op.execute("ALTER TABLE video_chunks ALTER COLUMN embedding TYPE vector(1024) USING embedding::vector")


def downgrade() -> None:
    op.drop_index('ix_video_chunks_id', table_name='video_chunks')
    op.drop_table('video_chunks')