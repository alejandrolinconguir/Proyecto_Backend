import unittest
from datetime import date

from app.domain.videojuego import Videojuego
from app.repositories import videojuego_repository
from app.repositories.arriendo_repository import arriendo_repository
from app.schemas.arriendo import ArriendoCreate
from app.services.arriendo_service import (
    arriendo_service,
    ClienteTieneArriendoActivoError,
    VideojuegoNoDisponibleError,
)


class TestArriendoService(unittest.TestCase):
    def setUp(self):
        videojuego_repository.videojuegos.clear()
        arriendo_repository.limpiar()
        videojuego_repository.crear(
            Videojuego(
                id_videojuego=1,
                titulo="Mario Kart 8",
                plataforma="SWITCH",
                año_lanzamiento=2017,
                id_categoria=1,
            )
        )
        videojuego_repository.crear(
            Videojuego(
                id_videojuego=2,
                titulo="Zelda BOTW",
                plataforma="SWITCH",
                año_lanzamiento=2017,
                id_categoria=1,
            )
        )

    def datos(self, cliente=1, juego=1, arriendo=date(2026, 9, 20), devolucion=date(2026, 9, 25)):
        return ArriendoCreate(
            id_cliente=cliente,
            id_videojuego=juego,
            fecha_arriendo=arriendo,
            fecha_devolucion=devolucion,
        )

    def test_crear_arriendo_exitoso(self):
        arriendo = arriendo_service.crear_arriendo(self.datos())
        self.assertEqual(arriendo.id_arriendo, 1)
        self.assertEqual(arriendo.estado, "Activo")
        self.assertEqual(videojuego_repository.obtener_por_id(1).estado, "Arrendado")

    def test_no_se_puede_arrendar_videojuego_no_disponible(self):
        arriendo_service.crear_arriendo(self.datos())
        with self.assertRaises(VideojuegoNoDisponibleError):
            arriendo_service.crear_arriendo(self.datos(cliente=2))

    def test_cliente_no_puede_tener_dos_arriendos_activos(self):
        arriendo_service.crear_arriendo(self.datos(cliente=1, juego=1))
        with self.assertRaises(ClienteTieneArriendoActivoError):
            arriendo_service.crear_arriendo(self.datos(cliente=1, juego=2))

    def test_fecha_invalida_rechazada_por_schema(self):
        with self.assertRaises(ValueError):
            self.datos(
                arriendo=date(2026, 9, 25),
                devolucion=date(2026, 9, 20),
            )

    def test_devolver_libera_videojuego(self):
        arriendo = arriendo_service.crear_arriendo(self.datos())
        actualizado = arriendo_service.actualizar_arriendo(
            arriendo.id_arriendo,
            __import__("app.schemas.arriendo", fromlist=["ArriendoUpdate"]).ArriendoUpdate(
                estado="Devuelto",
                fecha_devolucion=date(2026, 9, 25),
            ),
        )
        self.assertEqual(actualizado.estado, "Devuelto")
        self.assertEqual(videojuego_repository.obtener_por_id(1).estado, "Disponible")


if __name__ == "__main__":
    unittest.main()
