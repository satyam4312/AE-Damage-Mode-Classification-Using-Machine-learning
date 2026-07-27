"""
preprocessing.py
-------------------------------------------------------
Data preprocessing for Damage Mode Classification.

Responsibilities
----------------
1. Load master dataset
2. Clean dataset
3. Save clean_dataset.csv

This module performs ONLY preprocessing.
No encoding, scaling, feature selection or model loading.
"""

from pathlib import Path

import pandas as pd

from config import PROCESSED_DIR


class DataPreprocessor:
    """
    Clean the master AE dataset before training.
    """

    def __init__(self):

        self.df = None

        self.drop_columns = [
            "SetID",
            "SetType",
            "Time",
            "Status",
            "ParamID",
            "Chan",
            "Thr",
            "specimen",
            "TRAI",
            "PCTD",
            "PCTA",
            "PA0",
            "PA1"
        ]

    # ==========================================================
    # Cleaning Functions
    # ==========================================================

    def drop_unused_columns(self):

        self.df = self.df.drop(
            columns = self.drop_columns,
            errors = "ignore"
        )

    # ==========================================================

    def remove_duplicates(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        after = len(self.df)

        print(f"Rows before : {before}")

        print(f"Rows after  : {after}")

    # ==========================================================

    def remove_empty_columns(self):

        self.df = self.df.dropna(axis = 1, how = "all")

    # ==========================================================

    def convert_numeric(self):

        ignore = ["damage_mode"]

        for col in self.df.columns:

            if col in ignore:
                continue

            self.df[col] = pd.to_numeric(self.df[col], errors = "coerce")

    # ==========================================================

    def fill_missing_values(self):

        numeric = self.df.select_dtypes(include="number").columns

        self.df[numeric] = self.df[numeric].fillna(self.df[numeric].median())

    # ==========================================================

    def preprocess_dataframe(self, dataframe: pd.DataFrame):

        """
        Clean a dataframe.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """

        self.df = dataframe.copy()

        self.drop_unused_columns()

        self.remove_duplicates()

        self.remove_empty_columns()

        self.convert_numeric()

        self.fill_missing_values()

        return self.df

    # ==========================================================

    def save(self):

        output_path = PROCESSED_DIR / "clean_dataset.csv"

        self.df.to_csv(output_path, index=False)

        print(f"\nSaved : {output_path}")

    # ==========================================================

    def process(self):

        print("=" * 60)

        print("Preprocessing Dataset")

        print("=" * 60)

        input_path = PROCESSED_DIR / "master_hits.csv"

        self.df = pd.read_csv(input_path)

        self.preprocess_dataframe(self.df)

        self.save()

        print()

        print("Dataset Shape :", self.df.shape)

        print()

        return self.df


# ==========================================================

if __name__ == "__main__":

    processor = DataPreprocessor()

    clean_df = processor.process()

    print("\nColumns\n")

    print(clean_df.columns.tolist())