from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_main'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True, server_default=""),
        sa.Column('body', sa.String(), nullable=True, server_default=""),
        sa.Column('tag_list', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),  # no FK to users (separate DB)
    )
    op.create_index(op.f('ix_articles_id'), 'articles', ['id'])
    op.create_index(op.f('ix_articles_slug'), 'articles', ['slug'], unique=True)

    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'])

def downgrade() -> None:
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_articles_slug'), table_name='articles')
    op.drop_index(op.f('ix_articles_id'), table_name='articles')
    op.drop_table('articles')
