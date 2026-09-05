import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "multilingual.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS city_aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alias TEXT NOT NULL,
            canonical_name TEXT NOT NULL,
            language TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_alias
        ON city_aliases(alias)
    """)

    connection.commit()
    connection.close()


def insert_alias(alias, canonical_name, language):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO city_aliases
        (alias, canonical_name, language)
        VALUES (?, ?, ?)
        """,
        (alias, canonical_name, language)
    )

    connection.commit()
    connection.close()


def resolve_alias(alias):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT alias, canonical_name, language
        FROM city_aliases
        WHERE alias = ?
        LIMIT 1
        """,
        (alias,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "alias": row["alias"],
        "canonical_name": row["canonical_name"],
        "language": row["language"]
    }


if __name__ == "__main__":
    initialize_database()
    print(f"Multilingual database created: {DATABASE_PATH}")