
import pandas as pd
import pytest

from src.data_generator import (
    NUM_DAYS,
    NUM_LTE_CELLS,
    NUM_NR_CELLS,
    generate_dataset,
    get_traffic_factor,
)


@pytest.fixture(scope="module")
def dataset():
    return generate_dataset()


def test_dataset_row_count(dataset):
    expected = (
        (NUM_LTE_CELLS + NUM_NR_CELLS)
        * NUM_DAYS
        * 24
    )
    assert len(dataset) == expected


def test_unique_cell_count(dataset):
    assert dataset["cell_id"].nunique() == 20


def test_technology_values(dataset):
    assert set(dataset["technology"]) == {"LTE", "NR"}


def test_prb_range(dataset):
    assert dataset["prb_utilization_pct"].between(
        0, 100
    ).all()


def test_bler_range(dataset):
    assert dataset["bler_pct"].between(0, 100).all()


def test_throughput_nonnegative(dataset):
    assert (dataset["dl_throughput_mbps"] >= 0).all()
    assert (dataset["ul_throughput_mbps"] >= 0).all()


def test_no_missing_values(dataset):
    assert dataset.isnull().sum().sum() == 0


def test_unique_cell_timestamp_pairs(dataset):
    assert not dataset.duplicated(
        subset=["timestamp", "cell_id"]
    ).any()


def test_congestion_event_count(dataset):
    assert dataset["congestion_event"].sum() == 16


def test_traffic_factor_invalid_hour():
    with pytest.raises(ValueError):
        get_traffic_factor(24)


def test_reproducible_generation(dataset):
    second = generate_dataset()
    pd.testing.assert_frame_equal(dataset, second)
