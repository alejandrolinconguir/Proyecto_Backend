# RetroGames API — Sistema de Arriendo de Videojuegos Clásicos

API REST desarrollada con **Python**, **FastAPI**, **SQLAlchemy** y **PostgreSQL** para la gestión de arriendos de videojuegos, clientes y categorías en el contexto de la asignatura *Desarrollo de Backend (ICINF1108)*.

---

## Integrantes y Responsabilidades

| Integrante | Área Principal | Responsabilidades |
| :--- | :--- | :--- |
| **Alejandro Linconguir** | Coordinación + Integración y Documentación | Coordinación del backlog, integración técnica, README, diagramas y soporte en desarrollo. |
| **Byron** | Dominio y Datos | Modelos ORM, esquema de BD PostgreSQL, migraciones con Alembic y seeders. |
| **Vicente Barrientos** | API y Lógica de Negocio | Routers, servicios, adaptación de repositorios a la BD y reglas de negocio. |
| **Benjamín Jara** | Calidad y Pruebas | Pruebas de endpoints, colección de Postman/HTTP, validaciones de errores y evidencias. |

---

## Arquitectura por Capas

El proyecto está organizado en 4 capas según los requisitos técnicos de la asignatura:

1. **Presentation (`app/routers`, `app/schemas`)**: Recibe las peticiones HTTP, valida datos de entrada y salida mediante esquemas Pydantic y gestiona la inyección de dependencias.
2. **Application (`app/services`)**: Contiene la lógica de negocio y coordina el flujo de los casos de uso entre la capa de presentación y la infraestructura.
3. **Domain (`app/domain`)**: Define las entidades de negocio independientes del framework o del motor de base de datos.
4. **Infrastructure (`app/infrastructure`)**: Maneja la conexión a PostgreSQL, la configuración de SQLAlchemy, los modelos ORM (`models.py`), las migraciones (`migrations/`) y los seeders (`seed.py`).

---

## Instalación y Ejecución en Entorno Limpio

### Requisitos previos
- Python 3.10+
- Docker y Docker Compose

### 1. Configurar variables de entorno
Crea un archivo `.env` en la raíz tomando como base la plantilla `.env.example`:

```bash
cp .env.example .env