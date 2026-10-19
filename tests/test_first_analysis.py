
from pathlib import Path

import pandas as pd


def test_sample_dataset_exists():
    path = Path("data/raw/telecom_kpi_sample.csv")
    assert path.exists()


def test_sample_dataset_has_ten_cells():
    df = pd.read_csv("data/raw/telecom_kpi_sample.csv")
    assert len(df) == 10


def test_prb_utilization_is_valid():
    df = pd.read_csv("data/raw/telecom_kpi_sample.csv")

    assert df["prb_utilization_pct"].between(0, 100).all()


def test_cell_ids_are_unique():
    df = pd.read_csv("data/raw/telecom_kpi_sample.csv")

    assert df["cell_id"].is_unique
