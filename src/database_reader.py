"""
database_reader.py
--------------------------------------------------------
Unified database reader for training and deployment.

Features
--------
✓ Read a single PRIDB file
✓ Read MTS CSV
✓ Read all specimens from config.py 
✓ Automatically locate AE hit table
✓ Reusable for both training and inference
"""

from pathlib import Path
import sqlite3
import pandas as pd

from config import FILES, SKIP_TABLES


class DatabaseReader:

    def __init__(self):
        pass

    # =====================================================
    # SQLite Utilities
    # =====================================================

    @staticmethod
    def available_tables(database_path):
        """
        Return all tables present inside a PRIDB database.
        """

        database_path = Path(database_path)

        if not database_path.exists():
            raise FileNotFoundError(database_path)

        with sqlite3.connect(database_path) as conn:

            tables = pd.read_sql_query(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                """,
                conn
            )

        return tables["name"].tolist()

    # =====================================================

    @staticmethod
    def find_hit_table(database_path):
        """
        Locate the AE hit table automatically.
        """

        tables = DatabaseReader.available_tables(database_path)

        candidates = [

            "ae_data",
            "view_ae_data",
            "AEData",
            "AE_Hits",
            "HitData",
            "Hits",
            "ae_hits",
            "AE_DATA",
            "hits"

        ]

        for table in candidates:

            if table in tables:

                return table

        raise ValueError(
            "No AE hit table found.\n"
            f"Available tables:\n{tables}"
        )

    # =====================================================

    @staticmethod
    def read_pridb(database_path):
        """
        Read only the AE hit table from a PRIDB database.
        """

        database_path = Path(database_path)

        table = DatabaseReader.find_hit_table(database_path)

        with sqlite3.connect(database_path) as conn:

            df = pd.read_sql_query(

                f"SELECT * FROM [{table}]",

                conn

            )

        return df

    # =====================================================

    @staticmethod
    def read_mts(csv_path):
        """
        Read MTS CSV file.
        """

        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(csv_path)

        return pd.read_csv(csv_path)

    # =====================================================

    def load_single(self, pridb_path):
        """
        Deployment mode.

        Read one PRIDB file.
        """

        return self.read_pridb(pridb_path)

    # =====================================================

    def load_all(self):
        """
        Training mode.

        Read every specimen defined in config.py.
        """

        datasets = {}

        for specimen, info in FILES.items():

            print("=" * 60)
            print(f"Loading {specimen}")

            ae = self.read_pridb(info["pridb"])

            mts = self.read_mts(info["mts"])

            datasets[specimen] = {

                "damage_mode": info["damage_mode"],

                "ae": ae,

                "mts": mts

            }

            print(f"Damage Mode : {info['damage_mode']}")
            print(f"AE Shape    : {ae.shape}")
            print(f"MTS Shape   : {mts.shape}")

        return datasets


# =====================================================
# Standalone Test
# =====================================================

if __name__ == "__main__":

    reader = DatabaseReader()

    datasets = reader.load_all()

    print("\nLoaded Specimens")

    print(list(datasets.keys()))