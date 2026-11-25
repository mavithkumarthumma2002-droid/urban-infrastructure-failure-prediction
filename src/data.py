"""Loading the urban infrastructure data and a first look at it.

Loads urbandata.csv and prints a short summary of it (missing values,
class balance and the values of the categorical columns).

    python -m src.data
"""
from pathlib import Path

import pandas as pd

from src.config import RAW_DATA, TABLES_DIR

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


def summarise(df):
    """Return the basic facts about the data as a block of text."""
    lines = [
        f"Rows: {len(df)}, columns: {df.shape[1]}",
        "",
        "Missing values:",
        df.isna().sum().to_string(),
        "",
        f"Failure rate: {df[TARGET].mean():.1%}",
        df[TARGET].value_counts().to_string(),
        "",
    ]
    for col in CATEGORICAL_COLS:
        lines += [f"{col} values:", df[col].value_counts().to_string(), ""]
    lines += ["Numeric columns:", df[NUMERIC_COLS].describe().T.round(2).to_string()]
    return "\n".join(lines)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    summary = summarise(df)
    print(summary)
    (TABLES_DIR / "data_summary.txt").write_text(summary, encoding="utf-8")

    print("\nSaved data_summary.txt")


if __name__ == "__main__":
    main()
