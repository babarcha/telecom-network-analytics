
import pandas as pd

DATA_PATH = "data/raw/telecom_network_kpi.csv"


def main():
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["timestamp"],
    )

    print("\n=== Dataset Shape ===")
    print(df.shape)

    print("\n=== Column Data Types ===")
    print(df.dtypes)

    print("\n=== Missing Values ===")
    print(df.isnull().sum())

    print("\n=== Descriptive Statistics ===")
    print(df.describe().round(2))

    print("\n=== Average KPIs by Technology ===")
    summary = df.groupby("technology")[
        [
            "dl_throughput_mbps",
            "prb_utilization_pct",
            "bler_pct",
            "latency_ms",
        ]
    ].mean()

    print(summary.round(2))

    print("\n=== Highest PRB Utilization ===")
    print(
        df.nlargest(
            10,
            "prb_utilization_pct",
        )[
            [
                "timestamp",
                "cell_id",
                "prb_utilization_pct",
                "dl_throughput_mbps",
            ]
        ].to_string(index=False)
    )

    print("\n=== Congestion Event Summary ===")
    print(
        df.groupby("cell_id")[
            "congestion_event"
        ].sum().loc[lambda s: s > 0]
    )


if __name__ == "__main__":
    main()
