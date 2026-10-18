# Atrium Catalog API — Microservicio NoSQL

<p align="left">
  <a href="README.md">English</a> | <b>Español</b>
</p>

Microservicio especializado en la gestión de catálogos y consultas polimórficas dinámicas para el ecosistema **Atrium**, desarrollado con **FastAPI** y **MongoDB (Motor)**.

Diseñado como un **Modelo de Lectura / Servicio de Consultas desacoplado** (patrón CQRS) para liberar al núcleo transaccional SQL de las consultas sobre atributos polimórficos de las obras.

---

## 🏛️ Arquitectura Limpia en 3 Capas

El microservicio sigue estrictamente la **Regla de Dependencia** (el Dominio no tiene dependencias externas; Persistencia implementa los puertos del Dominio; Web actúa como mecanismo de entrega HTTP):

```text
app/
├── domain/                  # 🧠 Dominio Puro en Python
│   ├── models/              # Entidades del Dominio: Artist, Category, Artwork
│   ├── repositories/        # Interfaces / Puertos abstractos (ABC)
│   ├── exceptions/          # Excepciones tipadas del negocio (DomainException)
│   └── services/            # Servicios especializados: ArtistService, CategoryService, 
│                            # ArtworkService (Validación Polimórfica), CatalogService
│
├── persistence/             # 💾 Persistencia de Datos (MongoDB & Motor)
│   ├── config/              # Cliente asíncrono Motor y ciclo de vida (lifespan)
│   ├── entities/            # Esquemas físicos de BD (documentos Mongo con soporte _id/BSON)
│   ├── mappers/             # Data Mappers tipados (Entity <---> Domain Model)
│   ├── repositories/        # Repositorios concretos con Motor (consultas y agregaciones)
│   └── indexes.py           # Creación automática de índices únicos y compuestos
│
└── web/                     # 🌐 Mecanismo de Entrega Web (FastAPI)
    ├── routers/             # Routers REST (artists, categories, artworks, catalog, health)
    ├── schemas/             # DTOs Pydantic de entrada y salida
    ├── dependencies.py      # Proveedores de inyección de dependencias (Depends)
    └── error_handlers.py    # Mapeo global de DomainException -> Códigos HTTP (404, 409, 422)
```

---

## ⚙️ Configuración y Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `MONGO_URI` | Cadena de conexión a MongoDB Atlas o local | *Requerido* |
| `MONGO_DB_NAME` | Nombre de la base de datos | `atrium_db_ej` |
| `CORS_ORIGINS` | Orígenes permitidos separados por comas | `http://localhost:3000,http://localhost:5000` |

---

## 🚀 Puesta en Marcha

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar el Seed y crear índices:**
   ```bash
   python seed.py
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   uvicorn main.py:app --reload
   ```

La documentación Swagger interactiva estará disponible en:
`http://localhost:8000/docs`

---

## 🧪 Pruebas Unitarias

Ejecuta la suite de pruebas unitarias aisladas (valida servicios de dominio, reglas polimórficas y mappers sin requerir conexión a base de datos):

```bash
pytest tests/
```

---

## 📡 Resumen de Endpoints de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check del microservicio y ping a MongoDB |
| `POST` | `/artists/?sync=true` | Registra o sincroniza de forma idempotente un artista desde el núcleo |
| `GET` | `/artists/` | Listado paginado de artistas (`skip`, `limit`) |
| `GET` | `/artists/{id}` | Obtiene artista por su ID en SQL |
| `PUT` | `/artists/{id}` | Actualiza datos del artista |
| `DELETE`| `/artists/{id}` | Elimina artista (impide borrado si tiene obras activas) |
| `POST` | `/categories/` | Registra categoría con sus campos polimórficos requeridos |
| `GET` | `/categories/` | Lista categorías |
| `POST` | `/artworks/?sync=true` | Registra obra con validación de estructura polimórfica |
| `GET` | `/artworks/` | Lista obras |
| `GET` | `/artworks/{id}` | Obtiene obra por su ID en SQL |
| `GET` | `/catalog/search` | Búsqueda dinámica con agregación `$match`, `$lookup` y `$unwind` |

> *Nota: Las rutas legacy en singular (`/artist/`, `/category/`, `/artwork/`) se mantienen disponibles para garantizar total compatibilidad retroactiva.*
