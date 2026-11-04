# 🚗 Concesionaria de Vehículos — Backend API (FastAPI)

> **Evaluación Final Integradora (EFI)**  
> **Carrera:** Técnico Superior en Desarrollo de Software — ITEC Río Cuarto  
> **Espacio Curricular:** Práctica Profesionalizante 1: Python  
> **Docente:** Facundo Esteban Lemo  

---

## 👥 Integrantes
* **Facundo Albornoz**
* **Facundo Moriena**

---

## 📋 Descripción del Sistema
API REST profesional desarrollada en **Python** utilizando **FastAPI** y **SQLModel**, conectada a una base de datos relacional local en **SQLite**. El sistema gestiona integralmente el catálogo y stock de una concesionaria automotriz, incluyendo vehículos, marcas fabricantes, países de procedencia y tipos de vehículos.

Cuenta con control de versiones de base de datos automatizado mediante migraciones con **Alembic**, soporte para **CORS** para vincular con el Frontend de JavaScript, paginación nativa y documentación OpenAPI interactiva (Swagger UI).

---

## 🏗️ Arquitectura y Tecnologías
* **Lenguaje:** Python 3.12+ (Gestión de entornos ultra-rápida con `uv`).
* **Framework:** FastAPI (`fastapi[standard]`).
* **ORM & Modelado:** SQLModel (fusión de SQLAlchemy + Pydantic).
* **Base de Datos:** SQLite (`db_concesionaria_sqlmodel.db`).
* **Migraciones:** Alembic (`alembic.ini`, directorio `alembic/versions/`).
* **Paginación:** `fastapi-pagination`.

---

## 🗄️ Modelos de Datos y Relaciones

El sistema implementa 4 entidades principales divididas en esquemas `Base`, `table=True`, `Public` y `Nested`:

1. **`Vehiculo` (`src/models/vehiculo_models.py`)**:
   * Clave foránea `marca_id` ➔ Referencia a `Marca`.
   * Clave foránea `tipo_vehiculo_id` ➔ Referencia a `TipoVehiculo`.
   * Atributos: `nombre`, `precio`, `stock`, `modelo` (año), `estado_uso`, `url_image`, `descripcion`, `activo`.
2. **`Marca` (`src/models/marca_models.py`)**:
   * Clave foránea `pais_id` ➔ Referencia a `Pais`.
   * Atributos: `nombre`, `activo`.
3. **`Pais` (`src/models/pais_models.py`)**:
   * Atributos: `nombre`, `codigo`.
4. **`TipoVehiculo` (`src/models/tipo_vehiculo_models.py`)**:
   * Atributos: `nombre`, `descripcion`.

---

## 🛣️ Endpoints de la API (5 Operaciones por Modelo)

La API expone las operaciones CRUD completas documentadas con respuestas de error `404` (`NO_ENCONTRADO`):

| Método | Endpoint | Descripción | Formato Respuesta |
| :---: | :--- | :--- | :---: |
| `GET` | `/vehiculos/` | Obtener catálogo de vehículos paginado | `Page[VehiculoPublic]` |
| `GET` | `/vehiculos/{id}` | Obtener vehículo por ID con datos anidados de marca y tipo | `VehiculoPublicNested` |
| `POST` | `/vehiculos/` | Crear un nuevo vehículo | `VehiculoPublicNested` |
| `PUT` | `/vehiculos/{id}` | Actualizar datos de un vehículo existente | `VehiculoPublic` |
| `DELETE` | `/vehiculos/{id}` | Eliminar vehículo de la base de datos | `204 No Content` |

*(La misma estructura de 5 operaciones aplica a `/marcas/`, `/paises/` y `/tipo_vehiculos/`)*.

---

## ⚙️ Instalación y Ejecución Local

1. **Instalar el gestor `uv` (si aún no lo tienes):**
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Sincronizar el entorno virtual y dependencias:**
   ```bash
   uv sync
   ```

3. **Ejecutar el servidor con recarga automática:**
   ```bash
   uv run uvicorn src.main:app --reload
   ```

4. **Acceder a la documentación interactiva (Swagger UI):**
   * Abrir en el navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * Especificación OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 🔄 Migraciones con Alembic
Las migraciones se ejecutan de manera automática al levantar la aplicación mediante el `lifespan` configurado en `main.py`. Si se desea ejecutar manualmente:
```bash
uv run alembic upgrade head
```