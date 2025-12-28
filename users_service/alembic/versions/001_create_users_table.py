from alembic import op
import sqlalchemy as sa

revision = '001_users'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('bio', sa.String(), nullable=True, server_default=""),
        sa.Column('image', sa.String(), nullable=True, server_default=""),
        sa.Column('subscription_key', sa.String(), nullable=True),  # ← ЗДЕСЬ
    )

    # Создаем индексы
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'])

    # create subscribers table
    op.create_table(
        'subscribers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('subscriber_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_unique_constraint('ux_sub', 'subscribers', ['subscriber_id', 'author_id'])

    # create notifications_sent
    op.create_table(
        'notifications_sent',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('subscriber_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_unique_constraint('ux_notification', 'notifications_sent', ['subscriber_id', 'post_id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')

    op.drop_constraint('ux_notification', 'notifications_sent', type_='unique')
    op.drop_table('notifications_sent')

    op.drop_constraint('ux_sub', 'subscribers', type_='unique')
    op.drop_table('subscribers')

    op.drop_table('users')