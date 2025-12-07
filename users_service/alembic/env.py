# users_service/alembic/env.py
from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

# allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.database import base  # убедитесь, export Base
target_metadata = base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# get DB url from env (docker-compose will set DATABASE_URL)
db_url = os.environ.get("DATABASE_USERS_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
