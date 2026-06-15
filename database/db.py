import os
from datetime import datetime
from databases import Database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "visionlog.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

database = Database(DATABASE_URL)


async def connect_database():
    if not database.is_connected:
        await database.connect()
        print("Banco conectado")


async def disconnect_database():
    if database.is_connected:
        await database.disconnect()
        print("Banco desconectado")


async def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS rejections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        camera TEXT,
        status TEXT,
        defect TEXT,
        time TEXT,
        filename TEXT UNIQUE,
        created_at TEXT
    )
    """

    await database.execute(query)

    # Migração para bancos antigos sem created_at
    try:
        await database.execute(
            "ALTER TABLE rejections ADD COLUMN created_at TEXT"
        )
    except Exception:
        pass

    print("Tabela pronta")


async def insert_rejection(rejection):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
    INSERT OR IGNORE INTO rejections (
        camera,
        status,
        defect,
        time,
        filename,
        created_at
    )
    VALUES (
        :camera,
        :status,
        :defect,
        :time,
        :filename,
        :created_at
    )
    """

    values = {
        "camera": rejection.camera,
        "status": rejection.status,
        "defect": rejection.defect,
        "time": rejection.time,
        "filename": rejection.filename,
        "created_at": created_at
    }

    await database.execute(query, values)


async def get_all_filenames():
    query = "SELECT filename FROM rejections"

    rows = await database.fetch_all(query)

    return [row["filename"] for row in rows]


async def get_rejections():
    query = """
    SELECT *
    FROM rejections
    ORDER BY id DESC
    """

    return await database.fetch_all(query)