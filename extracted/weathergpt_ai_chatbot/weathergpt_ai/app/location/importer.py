import csv
import sqlite3
import zipfile
from pathlib import Path

from app.location.database import DATABASE_PATH, initialize_database


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
ZIP_PATH = DATA_DIR / "cities1000.zip"


def import_cities():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            f"GeoNames file not found: {ZIP_PATH}"
        )

    initialize_database()

    connection = sqlite3.connect(DATABASE_PATH)

    print("Opening cities1000.zip...")

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:

        txt_files = [
            name for name in archive.namelist()
            if name.endswith(".txt")
        ]

        if not txt_files:
            raise RuntimeError("No .txt file found inside cities1000.zip")

        txt_name = txt_files[0]

        print(f"Reading {txt_name}...")

        with archive.open(txt_name) as file:

            reader = csv.reader(
                (line.decode("utf-8") for line in file),
                delimiter="\t"
            )

            rows = []

            for row in reader:

                if len(row) < 19:
                    continue

                try:
                    geoname_id = int(row[0])
                    name = row[1]
                    ascii_name = row[2]
                    country_code = row[8]

                    state = row[10]

                    latitude = float(row[4])
                    longitude = float(row[5])

                    population = int(row[14])

                except (ValueError, IndexError):
                    continue

                rows.append(
                    (
                        geoname_id,
                        name,
                        ascii_name,
                        country_code,
                        state,
                        latitude,
                        longitude,
                        population,
                    )
                )

                if len(rows) >= 5000:
                    connection.executemany(
                        """
                        INSERT OR REPLACE INTO cities
                        (
                            geoname_id,
                            name,
                            ascii_name,
                            country_code,
                            state,
                            latitude,
                            longitude,
                            population
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        rows,
                    )

                    connection.commit()

                    print(f"Imported {len(rows)} records...")
                    rows.clear()

            if rows:
                connection.executemany(
                    """
                    INSERT OR REPLACE INTO cities
                    (
                        geoname_id,
                        name,
                        ascii_name,
                        country_code,
                        state,
                        latitude,
                        longitude,
                        population
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    rows,
                )

                connection.commit()

    connection.close()

    print()
    print("===================================")
    print("GeoNames import completed!")
    print(f"Database: {DATABASE_PATH}")
    print("===================================")


if __name__ == "__main__":
    import_cities()