from logging.config import fileConfig

from alembic import context

from app.infrastructure.database import engine
from app.infrastructure.models import Base


# Lee la configuración de Alembic.
config = context.config

# Configura los mensajes que se muestran en la terminal.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Contiene las definiciones de nuestras cuatro tablas.
# Importar Base desde models también carga los modelos ORM.
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Genera SQL sin conectarse a PostgreSQL.
    """
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Ejecuta las migraciones conectado a PostgreSQL.
    """
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()