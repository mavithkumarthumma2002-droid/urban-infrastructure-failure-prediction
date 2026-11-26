"""Cleaning the data.

Fixes the problems found when exploring the data:
  * typos in the two categorical columns
  * two impossible material_flexibility values (91.16)
"""
import numpy as np

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
