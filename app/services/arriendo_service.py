from sqlalchemy.orm import Session

from app.domain.arriendo import Arriendo
from app.repositories import videojuego_repository
from app.repositories.arriendo_repository import arriendo_repository
from app.repositories.cliente_repository import obtener_por_id
from app.schemas.arriendo import ArriendoUpdate
from app.core.errors import (
    ClienteNoEncontradoError,
    ArriendoNoEncontradoError,
    VideojuegoNoDisponibleError,
    ClienteTieneArriendoActivoError,
    FechaDevolucionInvalidaError,
    VideojuegoNoEncontradoEnArriendoError,
    SolicitudInvalidaError,
)

class ArriendoService:
    """Lógica de negocio de los arriendos."""

    def listar_arriendos(self, db: Session) -> list[Arriendo]:
        return arriendo_repository.listar(db)

    def obtener_arriendo(self, db: Session, id_arriendo: int) -> Arriendo:
        arriendo = arriendo_repository.buscar_por_id(db, id_arriendo)
        if arriendo is None:
            raise ArriendoNoEncontradoError(
                "No existe un arriendo con el ID solicitado"
            )
        return arriendo

    def crear_arriendo(self, db: Session, datos) -> Arriendo:
        # Relación: el videojuego debe existir.
        videojuego = videojuego_repository.obtener_por_id(db, datos.id_videojuego)
        if videojuego is None:
            raise VideojuegoNoEncontradoEnArriendoError(
                "No existe un videojuego con el ID indicado"
            )
        # Relación: el cliente debe existir.
        cliente = obtener_por_id(db, datos.id_cliente)
        if cliente is None:
            raise ClienteNoEncontradoError(datos.id_cliente)


        # REGLA 1: solo se puede arrendar un videojuego disponible.
        if not videojuego.esta_disponible():
            raise VideojuegoNoDisponibleError(
                "El videojuego no está disponible para arriendo"
            )

        # REGLA 2: un cliente no puede tener dos arriendos activos.
        arriendo_activo = arriendo_repository.buscar_activo_por_cliente(
            db, datos.id_cliente
        )
        if arriendo_activo is not None:
            raise ClienteTieneArriendoActivoError(
                "El cliente ya tiene un arriendo activo"
            )

        # REGLA 3: la validación de fechas ya ocurre en ArriendoCreate
        # y nuevamente en el dominio Arriendo como invariante.
        nuevo_arriendo = Arriendo(
            id_arriendo=0,
            id_cliente=datos.id_cliente,
            id_videojuego=datos.id_videojuego,
            fecha_arriendo=datos.fecha_arriendo,
            fecha_devolucion=datos.fecha_devolucion,
            estado="Activo",
        )

        # El cambio de estado del videojuego ocurre solo cuando el arriendo
        # ya pasó todas las validaciones anteriores.
        # El arriendo y el cambio de estado del videojuego se guardan juntos
        # (un solo commit): o se guardan los dos o no se guarda ninguno.
        videojuego.marcar_arrendado()
        arriendo_creado = arriendo_repository.crear(db, nuevo_arriendo)
        videojuego_repository.actualizar(db, videojuego)
        db.commit()
        return arriendo_creado

    def actualizar_arriendo(
        self, db: Session, id_arriendo: int, datos: ArriendoUpdate
    ) -> Arriendo:
        arriendo = self.obtener_arriendo(db, id_arriendo)
        videojuego = videojuego_repository.obtener_por_id(db, arriendo.id_videojuego)

        if videojuego is None:
            raise VideojuegoNoEncontradoEnArriendoError(
                "No existe el videojuego asociado al arriendo"
            )

        nueva_fecha_devolucion = (
            datos.fecha_devolucion
            if datos.fecha_devolucion is not None
            else arriendo.fecha_devolucion
        )
        nuevo_estado = datos.estado if datos.estado is not None else arriendo.estado

        # REGLA 3 también se mantiene al actualizar la fecha.
        if nueva_fecha_devolucion < arriendo.fecha_arriendo:
            raise FechaDevolucionInvalidaError(
                "La fecha de devolución no puede ser anterior a la fecha de arriendo"
            )

        # Si se marca como devuelto, se libera el videojuego.
        if nuevo_estado == "Devuelto" and arriendo.estado == "Activo":
            arriendo.fecha_devolucion = nueva_fecha_devolucion
            arriendo.marcar_devuelto()
            videojuego.marcar_disponible()
            videojuego_repository.actualizar(db, videojuego)

        # No permitimos reabrir un arriendo ya devuelto, porque eso dejaría
        # el estado del videojuego inconsistente con el historial.
        elif nuevo_estado == "Activo" and arriendo.estado == "Devuelto":
            raise SolicitudInvalidaError("No se puede reactivar un arriendo ya devuelto")
        else:
            arriendo.fecha_devolucion = nueva_fecha_devolucion

        arriendo_actualizado = arriendo_repository.actualizar(db, arriendo)
        db.commit()
        return arriendo_actualizado

    def eliminar_arriendo(self, db: Session, id_arriendo: int) -> Arriendo:
        arriendo = self.obtener_arriendo(db, id_arriendo)

        # Si se elimina un arriendo activo, liberamos el videojuego para no
        # dejarlo en estado 'Arrendado' sin un arriendo que lo respalde.
        if arriendo.esta_activo():
            videojuego = videojuego_repository.obtener_por_id(db, arriendo.id_videojuego)
            if videojuego is not None:
                videojuego.marcar_disponible()
                videojuego_repository.actualizar(db, videojuego)

        eliminado = arriendo_repository.eliminar(db, id_arriendo)
        db.commit()
        return eliminado


arriendo_service = ArriendoService()
