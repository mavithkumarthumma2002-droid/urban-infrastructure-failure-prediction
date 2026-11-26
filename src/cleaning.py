"""Cleaning the data.

Fixes the problems found when exploring the data, starting with the typos
in the two categorical columns.
"""
TYPO_FIXES = {
    "inspection_season": {"sumer": "summer"},
    "inspection_window": {"morni7ng": "morning"},
}
VALID_VALUES = {
    "inspection_season": {"winter", "spring", "summer", "autumn"},
    "inspection_window": {"morning", "afternoon", "evening", "night"},
}


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
