"""
dataset_builder.py
-------------------------------------------------------
Build master AE and MTS datasets from all specimens.

Training Pipeline

PRIDB + MTS
      │
      ▼
DatabaseReader
      │
      ▼
Master AE Dataset
Master MTS Dataset
      │
      ▼
processed/
"""

import pandas as pd

from config import PROCESSED_DIR
from database_reader import DatabaseReader


class MasterDatasetBuilder:

    def __init__(self):

        self.reader = DatabaseReader()

        self.datasets = self.reader.load_all()

        self.master_hits = []

        self.master_mts = []

    # =====================================================

    def build(self):

        print("\nBuilding Master Dataset...\n")

        for specimen, data in self.datasets.items():

            print(f"Processing {specimen}")

            # -------------------------
            # AE Data
            # -------------------------

            hits = data["ae"].copy()

            hits["specimen"] = specimen

            hits["damage_mode"] = data["damage_mode"]

            self.master_hits.append(hits)

            # -------------------------
            # MTS Data
            # -------------------------

            mts = data["mts"].copy()

            mts["specimen"] = specimen

            mts["damage_mode"] = data["damage_mode"]

            self.master_mts.append(mts)

        self.master_hits = pd.concat(self.master_hits, ignore_index=True)

        self.master_mts = pd.concat(self.master_mts, ignore_index=True)

        return self.master_hits, self.master_mts

    # =====================================================

    def save(self):

        self.master_hits.to_csv(PROCESSED_DIR / "master_hits.csv", index=False)

        self.master_mts.to_csv(PROCESSED_DIR / "master_mts.csv", index=False)

        print("\nSaved")

        print("master_hits.csv")

        print("master_mts.csv")

    # =====================================================

    def process(self):

        hits, mts = self.build()

        self.save()

        print("\nMaster Hits Shape :", hits.shape)

        print("Master MTS Shape  :", mts.shape)

        return hits, mts


# =========================================================

if __name__ == "__main__":

    builder = MasterDatasetBuilder()

    builder.process() 