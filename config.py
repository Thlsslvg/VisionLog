from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOG_FOLDER = BASE_DIR / "logs" / "log"
DATABASE_FOLDER = BASE_DIR / "database"
DATABASE_PATH = DATABASE_FOLDER / "visionlog.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"