from datetime import date, timedelta

from sqlalchemy import select

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import (
    ArriendoORM,
    CategoriaORM,
    ClienteORM,
    VideojuegoORM,
)


def cargar_datos():
    # La transacción guarda todo junto.
    # Si ocurre un error, se deshacen los cambios de esta carga.
    with SessionLocal.begin() as db:

        # Esta carga inicial se ejecuta solamente sobre tablas vacías.
        # Así no duplicamos registros ni modificamos datos existentes.
        modelos = (
            CategoriaORM,
            ClienteORM,
            VideojuegoORM,
            ArriendoORM,
        )

        for modelo in modelos:
            existente = db.execute(
                select(modelo).limit(1)
            ).first()

            if existente is not None:
                print(
                    "La base ya contiene datos. "
                    "No se realizó la carga inicial."
                )
                return

        # -------------------------
        # CATEGORÍAS
        # -------------------------
        aventura = CategoriaORM(
            nombre="Aventura",
            descripcion="Juegos de exploración y aventuras.",
            edad_minima=12,
            estado="Activa",
        )

        carreras = CategoriaORM(
            nombre="Carreras",
            descripcion="Juegos de conducción y competencias.",
            edad_minima=3,
            estado="Activa",
        )

        # -------------------------
        # CLIENTES
        # -------------------------
        ana = ClienteORM(
            nombre="Ana",
            apellido="Perez",
            correo="ana@example.com",
            telefono="+56911111111",
            estado="Activo",
        )

        diego = ClienteORM(
            nombre="Diego",
            apellido="Soto",
            correo="diego@example.com",
            telefono="+56922222222",
            estado="Activo",
        )

        # -------------------------
        # VIDEOJUEGOS
        # -------------------------
        zelda = VideojuegoORM(
            titulo="The Legend of Zelda: Breath of the Wild",
            plataforma="SWITCH",
            año_lanzamiento=2017,
            estado="Disponible",
            categoria=aventura,
        )

        minecraft = VideojuegoORM(
            titulo="Minecraft",
            plataforma="PC",
            año_lanzamiento=2011,
            estado="Arrendado",
            categoria=aventura,
        )

        mario_kart = VideojuegoORM(
            titulo="Mario Kart 8 Deluxe",
            plataforma="SWITCH",
            año_lanzamiento=2017,
            estado="Disponible",
            categoria=carreras,
        )

        # -------------------------
        # ARRIENDOS
        # -------------------------
        hoy = date.today()

        arriendo_devuelto = ArriendoORM(
            cliente=ana,
            videojuego=zelda,
            fecha_arriendo=hoy - timedelta(days=7),
            fecha_devolucion=hoy - timedelta(days=2),
            estado="Devuelto",
        )

        arriendo_activo = ArriendoORM(
            cliente=ana,
            videojuego=minecraft,
            fecha_arriendo=hoy,
            fecha_devolucion=hoy + timedelta(days=7),
            estado="Activo",
        )

        # PostgreSQL genera los identificadores.
        # SQLAlchemy guarda las relaciones usando esos identificadores.
        db.add_all([
            aventura,
            carreras,
            ana,
            diego,
            zelda,
            minecraft,
            mario_kart,
            arriendo_devuelto,
            arriendo_activo,
        ])

    # Se muestra después de confirmar la transacción.
    print("Carga inicial completada correctamente.")
    print("Categorías: 2")
    print("Clientes: 2")
    print("Videojuegos: 3")
    print("Arriendos: 2")


if __name__ == "__main__":
    cargar_datos()