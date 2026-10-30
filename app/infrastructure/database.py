import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Busca el archivo .env en la raíz del proyecto.
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ_PROYECTO / ".env")


# Comprueba que estén configuradas las variables necesarias.
VARIABLES_REQUERIDAS = (
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
)

for variable in VARIABLES_REQUERIDAS:
    if not os.getenv(variable):
        raise RuntimeError(
            f"Falta configurar {variable} en el archivo .env"
        )


# Construye la dirección para conectarnos a PostgreSQL.
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
    port=int(os.getenv("POSTGRES_PORT", "5433")),
    database=os.environ["POSTGRES_DB"],
)


# Administra las conexiones y limita la espera al conectarse.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 5},
)


# Crea sesiones usando el mismo motor de conexión.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Los modelos ORM heredarán de esta clase.
class Base(DeclarativeBase):
    pass


# Entrega una sesión y la cierra cuando termina su uso.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()