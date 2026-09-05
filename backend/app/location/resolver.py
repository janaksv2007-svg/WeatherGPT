import re
from typing import Optional

from app.location.database import get_connection
from app.location.multilingual_database import resolve_alias


def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def resolve_city(city_name: str, country_code: Optional[str] = None):
    if not city_name:
        return None

    # Check multilingual alias
    alias_result = resolve_alias(city_name)

    if alias_result:
        city_name = alias_result["canonical_name"]

    normalized = normalize_name(city_name)

    # Always create the database connection here
    connection = get_connection()

    try:
        if country_code:
            country_code = country_code.upper()

            query = (
                "SELECT * FROM cities "
                "WHERE (LOWER(name) = ? OR LOWER(ascii_name) = ?) "
                "AND country_code = ? "
                "ORDER BY population DESC LIMIT 1"
            )

            row = connection.execute(
                query,
                (normalized, normalized, country_code)
            ).fetchone()

        else:
            query = (
                "SELECT * FROM cities "
                "WHERE LOWER(name) = ? OR LOWER(ascii_name) = ? "
                "ORDER BY population DESC LIMIT 1"
            )

            row = connection.execute(
                query,
                (normalized, normalized)
            ).fetchone()

    finally:
        connection.close()

    if row is None:
        return None

    return dict(row)


def search_cities(city_name: str, limit: int = 10):
    if not city_name:
        return []

    normalized = normalize_name(city_name)

    connection = get_connection()

    try:
        query = (
            "SELECT * FROM cities "
            "WHERE LOWER(name) LIKE ? "
            "OR LOWER(ascii_name) LIKE ? "
            "ORDER BY population DESC "
            "LIMIT ?"
        )

        pattern = f"%{normalized}%"

        rows = connection.execute(
            query,
            (pattern, pattern, limit)
        ).fetchall()

    finally:
        connection.close()

    return [dict(row) for row in rows]