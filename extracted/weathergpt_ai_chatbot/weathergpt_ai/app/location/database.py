import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "cities.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            geoname_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ascii_name TEXT,
            country_code TEXT,
            state TEXT,
            latitude REAL,
            longitude REAL,
            population INTEGER
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_city_name
        ON cities(name)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_city_ascii_name
        ON cities(ascii_name)
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DATABASE_PATH}")