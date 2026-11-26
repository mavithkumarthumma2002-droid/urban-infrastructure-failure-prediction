import numpy as np
import pandas as pd
import pytest

from src.cleaning import clean_data, fix_typos, remove_impossible_values, variables_table
from src.data import load_data


@pytest.fixture
def raw():
    return load_data()


def test_typos_are_fixed(raw):
    fixed = fix_typos(raw)
    assert "sumer" not in fixed["inspection_season"].values
    assert "morni7ng" not in fixed["inspection_window"].values
    assert (fixed["inspection_season"] == "summer").sum() == 134


def test_unknown_category_raises():
    df = pd.DataFrame({"inspection_season": ["wintr"], "inspection_window": ["night"]})
    with pytest.raises(ValueError, match="wintr"):
        fix_typos(df)


def test_impossible_values_become_missing(raw):
    cleaned, n_bad = remove_impossible_values(raw)
    assert n_bad == 2
    assert cleaned["material_flexibility"].max() < 50
    assert cleaned["material_flexibility"].isna().sum() == 2


def test_wrong_column_name_raises(raw):
    with pytest.raises(KeyError):
        remove_impossible_values(raw, col="not_a_column")


def test_clean_data_does_not_change_the_input(raw):
    before = raw.copy()
    clean_data(raw)
    pd.testing.assert_frame_equal(raw, before)


def test_clean_data_drops_id_and_keeps_rows(raw):
    cleaned, _ = clean_data(raw)
    assert "inspector_id" not in cleaned.columns
    assert len(cleaned) == len(raw)
    # 11 empty cells in the raw file + the 2 removed values
    assert cleaned.isna().sum().sum() == 13


def test_variables_table_covers_every_column(raw):
    table = variables_table()
    assert set(table["Variable"]) == set(raw.columns)
    assert not np.any(table["Treated as"].isna())
