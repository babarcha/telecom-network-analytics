
from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

NUM_LTE_CELLS = 10
NUM_NR_CELLS = 10
NUM_DAYS = 7
RANDOM_SEED = 42

START_DATE = "2026-10-01"

OUTPUT_PATH = Path("data/raw/telecom_network_kpi.csv")


# --------------------------------------------------
# Traffic model
# --------------------------------------------------

def get_traffic_factor(hour: int) -> float:
    """
    Return normalized traffic demand for a given hour.
    """
    traffic_profile = [
        0.35, 0.28, 0.22, 0.18,
        0.17, 0.20, 0.30, 0.45,
        0.58, 0.65, 0.70, 0.73,
        0.76, 0.72, 0.68, 0.71,
        0.78, 0.85, 0.92, 0.98,
        1.00, 0.88, 0.70, 0.50,
    ]

    if not 0 <= hour <= 23:
        raise ValueError("Hour must be between 0 and 23")

    return traffic_profile[hour]


# --------------------------------------------------
# Dataset generation
# --------------------------------------------------

def generate_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)

    timestamps = pd.date_range(
        start=START_DATE,
        periods=NUM_DAYS * 24,
        freq="h",
        tz="UTC",
    )

    cells = (
        [(f"LTE_CELL_{i:03d}", "LTE")
         for i in range(1, NUM_LTE_CELLS + 1)]
        +
        [(f"NR_CELL_{i:03d}", "NR")
         for i in range(1, NUM_NR_CELLS + 1)]
    )

    records = []

    for cell_id, technology in cells:

        # Cell-specific characteristics
        if technology == "LTE":
            capacity_mbps = rng.uniform(80, 180)
            max_users = 180
        else:
            capacity_mbps = rng.uniform(250, 650)
            max_users = 300

        base_sinr = rng.uniform(8, 24)
        base_rsrp = rng.uniform(-105, -75)

        for timestamp in timestamps:

            hour = timestamp.hour
            traffic_factor = get_traffic_factor(hour)

            # Cell-specific and hourly load variations
            demand_factor = np.clip(
                traffic_factor * rng.normal(1.0, 0.10),
                0.05,
                1.20,
            )

            # Inject known congestion periods
            congestion_event = int(
                cell_id in {"LTE_CELL_003", "NR_CELL_007"}
                and timestamp.day in {3, 5}
                and 18 <= hour <= 21
            )

            if congestion_event:
                demand_factor *= 1.65

            connected_ues = int(
                np.clip(
                    max_users * demand_factor
                    + rng.normal(0, 5),
                    1,
                    max_users,
                )
            )

            # Radio quality
            sinr_db = float(np.clip(
                base_sinr + rng.normal(0, 3),
                -5,
                30,
            ))

            rsrp_dbm = float(np.clip(
                base_rsrp + rng.normal(0, 4),
                -120,
                -60,
            ))

            # Simplified radio efficiency
            radio_efficiency = float(np.clip(
                (sinr_db + 5) / 35,
                0.15,
                1.0,
            ))

            # Offered load and resource usage
            offered_load_mbps = (
                capacity_mbps
                * demand_factor
                * rng.uniform(0.75, 1.10)
            )

            effective_capacity_mbps = (
                capacity_mbps * radio_efficiency
            )

            dl_throughput = min(
                offered_load_mbps,
                effective_capacity_mbps,
            )

            prb_utilization = float(np.clip(
                100
                * offered_load_mbps
                / max(effective_capacity_mbps, 1),
                0,
                100,
            ))

            # Simplified BLER model
            bler_pct = float(np.clip(
                1.0
                + max(0, 12 - sinr_db) * 0.35
                + max(0, prb_utilization - 80) * 0.06
                + rng.normal(0, 0.5),
                0,
                30,
            ))

            # Latency increases with resource saturation
            latency_ms = float(np.clip(
                8
                + 0.12 * prb_utilization
                + max(0, prb_utilization - 75) * 0.8
                + congestion_event * 12
                + rng.normal(0, 2),
                2,
                150,
            ))

            ul_throughput = (
                dl_throughput * rng.uniform(0.15, 0.35)
            )

            records.append({
                "timestamp": timestamp,
                "cell_id": cell_id,
                "technology": technology,
                "connected_ues": connected_ues,
                "dl_throughput_mbps": round(
                    dl_throughput, 2
                ),
                "ul_throughput_mbps": round(
                    ul_throughput, 2
                ),
                "prb_utilization_pct": round(
                    prb_utilization, 2
                ),
                "bler_pct": round(bler_pct, 2),
                "sinr_db": round(sinr_db, 2),
                "rsrp_dbm": round(rsrp_dbm, 2),
                "latency_ms": round(latency_ms, 2),
                "congestion_event": congestion_event,
            })

    return pd.DataFrame(records)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    df = generate_dataset()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(OUTPUT_PATH, index=False)

    print("\n=== Dataset Generation Complete ===")
    print(f"Total records: {len(df)}")
    print(f"Unique cells: {df['cell_id'].nunique()}")
    print(f"LTE records: {(df['technology'] == 'LTE').sum()}")
    print(f"NR records: {(df['technology'] == 'NR').sum()}")
    print(f"Congestion records: {df['congestion_event'].sum()}")
    print(f"Output file: {OUTPUT_PATH}")

    print("\n=== First Five Records ===")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
