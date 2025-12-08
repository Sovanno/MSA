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
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'])

    op.add_column('users', sa.Column('subscription_key', sa.Text(), nullable=True))

    op.create_table(
        'subscribers',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('subscriber_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_index(op.f('ix_subscribers_id'), 'subscribers', ['id'])
    op.create_index(op.f('ix_subscribers_subscriber_id'), 'subscribers', ['subscriber_id'])
    op.create_index(op.f('ix_subscribers_author_id'), 'subscribers', ['author_id'])

    op.create_unique_constraint('ux_subscriber_author', 'subscribers', ['subscriber_id', 'author_id'])

    try:
        # Для монолитной БД можно добавить FK
        op.create_foreign_key(
            'fk_subscribers_subscriber_id_users',
            'subscribers', 'users',
            ['subscriber_id'], ['id'],
            ondelete='CASCADE'
        )
        op.create_foreign_key(
            'fk_subscribers_author_id_users',
            'subscribers', 'users',
            ['author_id'], ['id'],
            ondelete='CASCADE'
        )
    except Exception:
        # Если базы разделены, просто пропускаем FK
        pass

def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    try:
        op.drop_constraint('ux_subscriber_author', 'subscribers', type_='unique')
        op.drop_constraint('fk_subscribers_subscriber_id_users', 'subscribers', type_='foreignkey')
        op.drop_constraint('fk_subscribers_author_id_users', 'subscribers', type_='foreignkey')
    except Exception:
        pass

    op.drop_index(op.f('ix_subscribers_author_id'), table_name='subscribers')
    op.drop_index(op.f('ix_subscribers_subscriber_id'), table_name='subscribers')
    op.drop_index(op.f('ix_subscribers_id'), table_name='subscribers')

    op.drop_table('subscribers')
    op.drop_table('users')
