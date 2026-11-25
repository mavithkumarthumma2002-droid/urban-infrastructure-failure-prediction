import pandas as pd
import pytest

from src.data import EXPECTED_COLUMNS, load_data, summarise


def test_load_real_data():
    df = load_data()
    assert df.shape == (456, 12)
    assert set(EXPECTED_COLUMNS) == set(df.columns)


def test_missing_file_gives_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "not_here.csv")


def test_missing_column_is_reported(tmp_path):
    df = load_data().drop(columns=["moisture_stress"])
    path = tmp_path / "broken.csv"
    df.to_csv(path, index=False)

    with pytest.raises(ValueError, match="moisture_stress"):
        load_data(path)


def test_empty_file_is_rejected(tmp_path):
    path = tmp_path / "empty.csv"
    pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(path, index=False)

    with pytest.raises(ValueError, match="no rows"):
        load_data(path)


def test_summary_mentions_failure_rate():
    text = summarise(load_data())
    assert "Failure rate: 36.8%" in text
