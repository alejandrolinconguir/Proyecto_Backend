from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class CategoriaORM(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(200), nullable=False)
    edad_minima = Column(Integer, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="Activa",
        server_default="Activa",
    )

    # Una categoría puede tener varios videojuegos.
    videojuegos = relationship(
        "VideojuegoORM",
        back_populates="categoria",
        passive_deletes="all",
    )

    __table_args__ = (
        CheckConstraint(
            "edad_minima >= 0 AND edad_minima <= 18",
            name="ck_categoria_edad",
        ),
        CheckConstraint(
            "estado IN ('Activa', 'Inactiva')",
            name="ck_categoria_estado",
        ),
    )


class ClienteORM(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    correo = Column(String(254), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="Activo",
        server_default="Activo",
    )

    # Un cliente puede tener varios arriendos en su historial.
    arriendos = relationship(
        "ArriendoORM",
        back_populates="cliente",
        passive_deletes="all",
    )

    __table_args__ = (
        CheckConstraint(
            "estado IN ('Activo', 'Inactivo')",
            name="ck_cliente_estado",
        ),
    )


class VideojuegoORM(Base):
    __tablename__ = "videojuegos"

    id_videojuego = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    plataforma = Column(String(20), nullable=False)
    año_lanzamiento = Column(Integer, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="Disponible",
        server_default="Disponible",
    )

    id_categoria = Column(
        Integer,
        ForeignKey("categorias.id_categoria", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Cada videojuego pertenece a una categoría.
    categoria = relationship(
        "CategoriaORM",
        back_populates="videojuegos",
    )

    # Un videojuego puede aparecer en varios arriendos históricos.
    arriendos = relationship(
        "ArriendoORM",
        back_populates="videojuego",
        passive_deletes="all",
    )

    __table_args__ = (
        CheckConstraint(
            "estado IN ('Disponible', 'Arrendado', 'Dañado')",
            name="ck_videojuego_estado",
        ),
        CheckConstraint(
            "año_lanzamiento >= 1970",
            name="ck_videojuego_anio",
        ),
        CheckConstraint(
            "plataforma IN ('PS5', 'PS4', 'XBOX', 'PC', 'SWITCH', 'SNES', 'N64')",
            name="ck_videojuego_plataforma",
        ),
    )


class ArriendoORM(Base):
    __tablename__ = "arriendos"

    id_arriendo = Column(Integer, primary_key=True)

    id_cliente = Column(
        Integer,
        ForeignKey("clientes.id_cliente", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    id_videojuego = Column(
        Integer,
        ForeignKey("videojuegos.id_videojuego", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    fecha_arriendo = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="Activo",
        server_default="Activo",
    )

    cliente = relationship(
        "ClienteORM",
        back_populates="arriendos",
    )

    videojuego = relationship(
        "VideojuegoORM",
        back_populates="arriendos",
    )

    __table_args__ = (
        CheckConstraint(
            "fecha_devolucion >= fecha_arriendo",
            name="ck_arriendo_fechas",
        ),
        CheckConstraint(
            "estado IN ('Activo', 'Devuelto')",
            name="ck_arriendo_estado",
        ),
    )