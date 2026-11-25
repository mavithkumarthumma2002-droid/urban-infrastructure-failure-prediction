"""Loading the urban infrastructure data and a first look at it.

Loads urbandata.csv, prints a short summary and draws a histogram of every
numeric column so data errors are easy to spot.

    python -m src.data
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.config import FIGURES_DIR, RAW_DATA, TABLES_DIR

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


def plot_histograms(df, out_file):
    fig, axes = plt.subplots(2, 4, figsize=(16, 7))
    for ax, col in zip(axes.ravel(), NUMERIC_COLS):
        ax.hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="white")
        ax.set_title(col, fontsize=11)
    fig.suptitle("Raw data - histograms of the numeric columns")
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    summary = summarise(df)
    print(summary)
    (TABLES_DIR / "data_summary.txt").write_text(summary, encoding="utf-8")

    plot_histograms(df, FIGURES_DIR / "raw_histograms.png")
    print("\nSaved data_summary.txt and raw_histograms.png")


if __name__ == "__main__":
    main()
