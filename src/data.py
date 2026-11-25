"""Loading the urban infrastructure data.

Loads urbandata.csv and checks it has every column from the data dictionary.
"""
from pathlib import Path

import pandas as pd

from src.config import RAW_DATA

TARGET = "failure"
NUMERIC_COLS = [
    "material_flexibility",
    "structural_mass_ratio",
    "recent_precipitation",
    "infrastructure_age",
    "surface_debris",
    "vibration_exposure",
    "asset_density",
    "moisture_stress",
]
CATEGORICAL_COLS = ["inspection_season", "inspection_window"]
ID_COLS = ["inspector_id"]
EXPECTED_COLUMNS = ID_COLS + NUMERIC_COLS + CATEGORICAL_COLS + [TARGET]


def load_data(path=RAW_DATA):
    """Read the csv and check that every column from the data dictionary is there."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Could not find the data file at {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{path.name} has no rows")

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Columns missing from {path.name}: {missing}")
    return df

