# Atrium Catalog API — NoSQL Microservice

<p align="left">
  <b>English</b> | <a href="README.es.md">Español</a>
</p>

A specialized microservice for catalog management and dynamic polymorphic queries within the **Atrium** ecosystem, powered by **FastAPI** and **MongoDB (Motor)**. 

Designed as a decoupled **Read Model / Query Service** (CQRS pattern) to offload complex polymorphic artwork attributes from the transactional SQL core.

---

## 🏛️ 3-Layer Clean Architecture

The microservice strictly adheres to the **Dependency Rule** (Domain has zero external dependencies; Persistence implements Domain ports; Web acts as the delivery mechanism):

```text
app/
├── domain/                  # 🧠 Pure Python Business Domain
│   ├── models/              # Pure Domain Entities: Artist, Category, Artwork
│   ├── repositories/        # Abstract Interfaces / Ports (ABC)
│   ├── exceptions/          # Typed Domain Exceptions (DomainException)
│   └── services/            # Specialized Services: ArtistService, CategoryService, 
│                            # ArtworkService (Polymorphic Validation), CatalogService
│
├── persistence/             # 💾 Data Persistence (MongoDB & Motor)
│   ├── config/              # Async Motor Client & Application Lifespan
│   ├── entities/            # Physical DB Schemas (Mongo documents with _id/BSON support)
│   ├── mappers/             # Strongly-typed Data Mappers (Entity <---> Domain Model)
│   ├── repositories/        # Concrete Mongo Repositories (Async Motor queries & aggregations)
│   └── indexes.py           # Automated unique & compound MongoDB index creation
│
└── web/                     # 🌐 Delivery Mechanism (FastAPI)
    ├── routers/             # REST Routers (artists, categories, artworks, catalog, health)
    ├── schemas/             # Pydantic Request/Response DTOs
    ├── dependencies.py      # Dependency Injection Providers (Depends)
    └── error_handlers.py    # Global Domain Exception Mapping -> HTTP Status Codes (404, 409, 422)
```

---

## ⚙️ Configuration & Environment Variables

Copy `.env.example` to `.env` and configure your credentials:

```bash
cp .env.example .env
```

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MONGO_URI` | MongoDB Atlas / local connection string | *Required* |
| `MONGO_DB_NAME` | Target database name | `atrium_db_ej` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000,http://localhost:5000` |

---

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run data seeding & create indexes:**
   ```bash
   python seed.py
   ```

3. **Start the development server:**
   ```bash
   uvicorn main.py:app --reload
   ```

Interactive Swagger documentation is available at:
`http://localhost:8000/docs`

---

## 🧪 Running Unit Tests

Run the isolated test suite (tests domain services, business rules, and mappers without requiring an active database):

```bash
pytest tests/
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Microservice health check & MongoDB ping |
| `POST` | `/artists/?sync=true` | Create or idempotent upsert artist from core |
| `GET` | `/artists/` | Paginated list of artists (`skip`, `limit`) |
| `GET` | `/artists/{id}` | Retrieve artist by SQL ID |
| `PUT` | `/artists/{id}` | Update artist details |
| `DELETE`| `/artists/{id}` | Delete artist (prevents deletion if works are linked) |
| `POST` | `/categories/` | Register category with required polymorphic fields |
| `GET` | `/categories/` | List categories |
| `POST` | `/artworks/?sync=true` | Create artwork with polymorphic schema validation |
| `GET` | `/artworks/` | List artworks |
| `GET` | `/artworks/{id}` | Retrieve artwork by SQL ID |
| `GET` | `/catalog/search` | Dynamic aggregation search with `$match`, `$lookup`, and `$unwind` |

> *Note: Legacy singular routes (`/artist/`, `/category/`, `/artwork/`) are also supported for full backward compatibility.*
