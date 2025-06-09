from logging.config import fileConfig

from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine

from sqlalchemy import pool

from alembic import context

from app.database import DATABASE_URL, Base
from app.models import tournament, user

config = context.config

config.set_main_option("sqlalchemy.url", DATABASE_URL)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


is_offline = context.is_offline_mode()

print("Migration was performed in %s mode" % ("Offline" if is_offline else "Online"))

if is_offline:
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())