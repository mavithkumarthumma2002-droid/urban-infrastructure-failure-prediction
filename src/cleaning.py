"""Cleaning the data.

Fixes the problems found when exploring the data:
  * typos in the two categorical columns
  * two impossible material_flexibility values (91.16)
  * inspector_id is dropped, it is only a record ID

Missing values are NOT filled here. They get the training-set median later,
inside the model pipeline, so nothing from the validation/test data leaks in.

    python main.py clean
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.config import FIGURES_DIR, PROCESSED_DIR, TABLES_DIR
from src.data import ID_COLS, load_data

CLEAN_FILE = PROCESSED_DIR / "cleaned_data.csv"

TYPO_FIXES = {
    "inspection_season": {"sumer": "summer"},
    "inspection_window": {"morni7ng": "morning"},
}
VALID_VALUES = {
    "inspection_season": {"winter", "spring", "summer", "autumn"},
    "inspection_window": {"morning", "afternoon", "evening", "night"},
}
# Every real material_flexibility value is between 25 and 40.5, so anything
# above 50 can only be a typing error.
FLEX_LIMIT = 50


def fix_typos(df):
    df = df.copy()
    for col, fixes in TYPO_FIXES.items():
        df[col] = df[col].replace(fixes)

    # stop here if a new spelling mistake shows up that the dictionary above misses
    for col, allowed in VALID_VALUES.items():
        unknown = set(df[col].dropna()) - allowed
        if unknown:
            raise ValueError(f"Unexpected values in {col}: {sorted(unknown)}")
    return df


def remove_impossible_values(df, col="material_flexibility", limit=FLEX_LIMIT):
    """Set values above the limit to missing. Returns the new frame and how many were changed."""
    if col not in df.columns:
        raise KeyError(f"{col} is not in the data")
    df = df.copy()
    bad = df[col] > limit
    df.loc[bad, col] = np.nan
    return df, int(bad.sum())


def clean_data(df):
    df = fix_typos(df)
    df, n_bad = remove_impossible_values(df)
    df = df.drop(columns=ID_COLS)
    return df, n_bad


def plot_before_after(raw, clean, out_file, col="material_flexibility"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.hist(raw[col].dropna(), bins=30, color="steelblue", edgecolor="white")
    ax1.set_title("Before cleaning")
    ax1.annotate("91.16 x2", xy=(91, 2), xytext=(65, 60),
                 arrowprops=dict(arrowstyle="->", color="red"), color="red")
    ax2.hist(clean[col].dropna(), bins=30, color="steelblue", edgecolor="white")
    ax2.set_title("After cleaning")
    for ax in (ax1, ax2):
        ax.set_xlabel(col)
    ax1.set_ylabel("Number of blocks")
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)


def main():
    for folder in (PROCESSED_DIR, FIGURES_DIR, TABLES_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    raw = load_data()
    clean, n_bad = clean_data(raw)

    clean.to_csv(CLEAN_FILE, index=False)
    plot_before_after(raw, clean, FIGURES_DIR / "material_flexibility_before_after.png")

    log = [
        "Cleaning log",
        "Fixed typos: 'sumer' -> 'summer', 'morni7ng' -> 'morning'",
        f"material_flexibility: {n_bad} values above {FLEX_LIMIT} set to missing",
        "Dropped inspector_id",
        f"Missing cells left (filled later in the pipeline): {int(clean.isna().sum().sum())}",
        f"Median material_flexibility after cleaning: {clean['material_flexibility'].median():.1f}",
    ]
    (TABLES_DIR / "cleaning_log.txt").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
