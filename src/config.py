"""Paths and settings used across the project."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = ROOT / "data" / "urbandata.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "outputs" / "figures"
TABLES_DIR = ROOT / "outputs" / "tables"
