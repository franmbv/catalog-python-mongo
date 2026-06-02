import asyncio
from datetime import datetime, timezone

from app.config.database import db

# ===================================================================
# COLECCIONES
# ===================================================================
COL_CATEGORIES = "categories"
COL_ARTISTS = "artists"
COL_ARTWORKS = "artworks"

# ===================================================================
# CATEGORÍAS (5)
# ===================================================================
CATEGORIES = [
    {
        "id_sql": 1,
        "detalles": ["tecnica", "soporte", "alto_cm", "ancho_cm"],
    },
    {
        "id_sql": 2,
        "detalles": ["material", "peso_kg", "largo_cm", "ancho_cm", "profundidad_cm"],
    },
    {
        "id_sql": 3,
        "detalles": ["tecnica", "papel", "alto_cm", "ancho_cm", "edicion"],
    },
    {
        "id_sql": 4,
        "detalles": ["tipo_arcilla", "tecnica_coccion", "peso_kg", "alto_cm", "ancho_cm", "profundidad_cm", "esmaltado"],
    },
    {
        "id_sql": 5,
        "detalles": ["material", "tecnica", "peso_g", "alto_cm", "ancho_cm", "profundidad_cm", "quilates"],
    },
]

# ===================================================================
# ARTISTAS (10)
# ===================================================================
ARTISTS = [
    {
        "id_sql": 1,
        "nombre": "Carlos",
        "apellido": "Mendoza",
        "fecha_nac": "1975-03-12",
        "fecha_fal": None,
        "nacionalidad": "Mexicana",
        "descripcion": "Pintor contemporáneo especializado en óleo y acrílico",
        "fotografia": "https://ejemplo.com/carlos_mendoza.jpg",
        "estado": "Activo",
    },
]

# ===================================================================
# OBRAS (15 — 3 por cada género)
# ===================================================================
ARTWORKS = [
    # --- PINTURA (id_sql 1 — genero_id 1) ---
    {
        "id_sql": 1,
        "genero_id": 1,
        "autor_id": 1,
        "nombre": "El Sueño Dorado",
        "fecha_creacion": "2022-06-15",
        "precio_obra": 12500.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/sueno_dorado.jpg",
        "detalles": {
            "tecnica": "óleo",
            "soporte": "lienzo",
            "alto_cm": "80",
            "ancho_cm": "60",
        },
    },
    # --- ESCULTURA (id_sql 4-6 — genero_id 2) ---
    {
        "id_sql": 4,
        "genero_id": 2,
        "autor_id": 3,
        "nombre": "El Pensador Moderno",
        "fecha_creacion": "2021-11-05",
        "precio_obra": 35000.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/pensador_moderno.jpg",
        "detalles": {
            "material": "bronce",
            "peso_kg": "120",
            "largo_cm": "90",
            "ancho_cm": "55",
            "profundidad_cm": "50",
        },
    },
    # --- FOTOGRAFÍA (id_sql 7-9 — genero_id 3) ---
    {
        "id_sql": 7,
        "genero_id": 3,
        "autor_id": 5,
        "nombre": "Silencio Urbano",
        "fecha_creacion": "2023-05-18",
        "precio_obra": 3200.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/silencio_urbano.jpg",
        "detalles": {
            "tecnica": "digital",
            "papel": "Hahnemühle FineArt",
            "alto_cm": "60",
            "ancho_cm": "90",
            "edicion": "3",
        },
    },
    # --- CERÁMICA (id_sql 10-12 — genero_id 4) ---
    {
        "id_sql": 10,
        "genero_id": 4,
        "autor_id": 7,
        "nombre": "Vasija del Tiempo",
        "fecha_creacion": "2023-08-22",
        "precio_obra": 2200.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/vasija_tiempo.jpg",
        "detalles": {
            "tipo_arcilla": "gres",
            "tecnica_coccion": "esmaltado",
            "peso_kg": "4.5",
            "alto_cm": "40",
            "ancho_cm": "25",
            "profundidad_cm": "25",
            "esmaltado": "true",
        },
    },
    # --- ORFEBRERÍA (id_sql 13-15 — genero_id 5) ---
    {
        "id_sql": 13,
        "genero_id": 5,
        "autor_id": 9,
        "nombre": "Collar Estelar",
        "fecha_creacion": "2023-11-30",
        "precio_obra": 9500.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/collar_estelar.jpg",
        "detalles": {
            "material": "plata",
            "tecnica": "filigrana",
            "peso_g": "85",
            "alto_cm": "25",
            "ancho_cm": "8",
            "profundidad_cm": "0.5",
            "quilates": "",
        },
    },
]


async def seed():
    print("=" * 50)
    print("  SEED — Atrium Catalog")
    print("=" * 50)

    # ── Categorías ────────────────────────────────────────────────
    print("\n[CATEGORÍAS] Insertando...")
    for cat in CATEGORIES:
        existing = await db[COL_CATEGORIES].find_one({"id_sql": cat["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={cat['id_sql']} ya existe")
            continue
        await db[COL_CATEGORIES].insert_one(cat)
        print(f"   [OK] id_sql={cat['id_sql']} insertada")

    # ── Artistas ──────────────────────────────────────────────────
    print("\n[ARTISTAS] Insertando...")
    for art in ARTISTS:
        existing = await db[COL_ARTISTS].find_one({"id_sql": art["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={art['id_sql']} — {art['nombre']} {art['apellido']} ya existe")
            continue
        await db[COL_ARTISTS].insert_one(art)
        print(f"   [OK] id_sql={art['id_sql']} — {art['nombre']} {art['apellido']}")

    # ── Obras ─────────────────────────────────────────────────────
    print("\n[OBRAS] Insertando...")
    for obra in ARTWORKS:
        existing = await db[COL_ARTWORKS].find_one({"id_sql": obra["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={obra['id_sql']} — '{obra['nombre']}' ya existe")
            continue
        await db[COL_ARTWORKS].insert_one(obra)
        print(f"   [OK] id_sql={obra['id_sql']} — '{obra['nombre']}'")

    # ── Resumen ───────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  [COMPLETADO] Seed finalizado exitosamente")
    print(f"     Categorías: {len(CATEGORIES)}")
    print(f"     Artistas:   {len(ARTISTS)}")
    print(f"     Obras:      {len(ARTWORKS)}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(seed())
