
from pathlib import Path

import pandas as pd
import plotly.express as px


def main():
    df = pd.read_csv(
        "data/raw/telecom_network_kpi.csv",
        parse_dates=["timestamp"],
    )

    # Mean PRB utilization across all cells
    hourly = (
        df.groupby("timestamp", as_index=False)
        ["prb_utilization_pct"]
        .mean()
    )

    fig = px.line(
        hourly,
        x="timestamp",
        y="prb_utilization_pct",
        title="Network PRB Utilization Over Time",
        labels={
            "timestamp": "Time (UTC)",
            "prb_utilization_pct": "Average DL PRB Utilization (%)",
        },
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
    )

    output = Path("reports/prb_utilization.html")
    output.parent.mkdir(parents=True, exist_ok=True)

    fig.write_html(str(output))

    print(f"Chart saved to: {output}")


if __name__ == "__main__":
    main()
