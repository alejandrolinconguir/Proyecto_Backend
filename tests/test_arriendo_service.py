import unittest
from datetime import date

from sqlalchemy.orm import Session

from app.domain.categoria import Categoria
from app.domain.cliente import Cliente
from app.domain.videojuego import Videojuego
from app.infrastructure.database import engine
from app.repositories import cliente_repository, videojuego_repository
from app.repositories.categoria_repository import categoria_repository
from app.schemas.arriendo import ArriendoCreate, ArriendoUpdate
from app.services.arriendo_service import (
    arriendo_service,
    ClienteTieneArriendoActivoError,
    VideojuegoNoDisponibleError,
)


class TestArriendoService(unittest.TestCase):
    """
    Estas pruebas usan la base de datos PostgreSQL real (hay que tener
    Docker levantado y las migraciones aplicadas).

    Todo se hace dentro de una transacción que se deshace al terminar cada
    prueba, así no se modifican ni se ensucian los datos de la base.
    """

    def setUp(self):
        self.conexion = engine.connect()
        self.transaccion = self.conexion.begin()
        # Con "create_savepoint", los db.commit() de los services no cierran
        # la transacción externa y el rollback final lo deshace todo.
        self.db = Session(
            bind=self.conexion,
            autoflush=False,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        categoria = categoria_repository.crear(
            self.db,
            Categoria(
                id_categoria=0,
                nombre="Categoria de prueba",
                descripcion="Solo para pruebas",
                edad_minima=3,
            ),
        )
        self.cliente1 = cliente_repository.crear(
            self.db,
            Cliente(0, "Cliente", "Uno", "prueba1@example.com", "+56900000001"),
        )
        self.cliente2 = cliente_repository.crear(
            self.db,
            Cliente(0, "Cliente", "Dos", "prueba2@example.com", "+56900000002"),
        )
        self.juego1 = videojuego_repository.crear(
            self.db,
            Videojuego(
                id_videojuego=0,
                titulo="Mario Kart 8",
                plataforma="SWITCH",
                año_lanzamiento=2017,
                id_categoria=categoria.id_categoria,
            ),
        )
        self.juego2 = videojuego_repository.crear(
            self.db,
            Videojuego(
                id_videojuego=0,
                titulo="Zelda BOTW",
                plataforma="SWITCH",
                año_lanzamiento=2017,
                id_categoria=categoria.id_categoria,
            ),
        )

    def tearDown(self):
        self.db.close()
        self.transaccion.rollback()
        self.conexion.close()

    def datos(self, cliente=None, juego=None, arriendo=date(2026, 9, 20), devolucion=date(2026, 9, 25)):
        cliente = cliente or self.cliente1
        juego = juego or self.juego1
        return ArriendoCreate(
            id_cliente=cliente.id_cliente,
            id_videojuego=juego.id_videojuego,
            fecha_arriendo=arriendo,
            fecha_devolucion=devolucion,
        )

    def test_crear_arriendo_exitoso(self):
        arriendo = arriendo_service.crear_arriendo(self.db, self.datos())
        self.assertGreater(arriendo.id_arriendo, 0)
        self.assertEqual(arriendo.estado, "Activo")
        juego = videojuego_repository.obtener_por_id(self.db, self.juego1.id_videojuego)
        self.assertEqual(juego.estado, "Arrendado")

    def test_no_se_puede_arrendar_videojuego_no_disponible(self):
        arriendo_service.crear_arriendo(self.db, self.datos())
        with self.assertRaises(VideojuegoNoDisponibleError):
            arriendo_service.crear_arriendo(self.db, self.datos(cliente=self.cliente2))

    def test_cliente_no_puede_tener_dos_arriendos_activos(self):
        arriendo_service.crear_arriendo(
            self.db, self.datos(cliente=self.cliente1, juego=self.juego1)
        )
        with self.assertRaises(ClienteTieneArriendoActivoError):
            arriendo_service.crear_arriendo(
                self.db, self.datos(cliente=self.cliente1, juego=self.juego2)
            )

    def test_fecha_invalida_rechazada_por_schema(self):
        with self.assertRaises(ValueError):
            self.datos(
                arriendo=date(2026, 9, 25),
                devolucion=date(2026, 9, 20),
            )

    def test_devolver_libera_videojuego(self):
        arriendo = arriendo_service.crear_arriendo(self.db, self.datos())
        actualizado = arriendo_service.actualizar_arriendo(
            self.db,
            arriendo.id_arriendo,
            ArriendoUpdate(estado="Devuelto", fecha_devolucion=date(2026, 9, 25)),
        )
        self.assertEqual(actualizado.estado, "Devuelto")
        juego = videojuego_repository.obtener_por_id(self.db, self.juego1.id_videojuego)
        self.assertEqual(juego.estado, "Disponible")


if __name__ == "__main__":
    unittest.main()
