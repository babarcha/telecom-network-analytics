
import numpy as np
import pandas as pd

# Reproducible random generator
rng = np.random.default_rng(42)

# Generate synthetic cell-level measurements
num_cells = 10

data = {
    "cell_id": [f"NR_CELL_{i:03d}" for i in range(1, num_cells + 1)],
    "dl_throughput_mbps": rng.uniform(40, 150, num_cells),
    "ul_throughput_mbps": rng.uniform(10, 60, num_cells),
    "prb_utilization_pct": rng.uniform(20, 95, num_cells),
    "latency_ms": rng.uniform(8, 35, num_cells),
    "connected_ues": rng.integers(30, 300, num_cells),
}

df = pd.DataFrame(data)

# Round floating-point measurements
df = df.round(2)

print("\n=== Telecom Network KPI Dataset ===")
print(df.to_string(index=False))

print("\n=== Network Performance Summary ===")
print(f"Total cells: {len(df)}")
print(f"Average DL throughput: {df['dl_throughput_mbps'].mean():.2f} Mbps")
print(f"Average UL throughput: {df['ul_throughput_mbps'].mean():.2f} Mbps")
print(f"Average PRB utilization: {df['prb_utilization_pct'].mean():.2f}%")
print(f"Average latency: {df['latency_ms'].mean():.2f} ms")

# Simple congestion rule for demonstration
congested_cells = df[df["prb_utilization_pct"] > 80]

print("\n=== High PRB Utilization Cells ===")
if congested_cells.empty:
    print("No cells exceed the 80% threshold.")
else:
    print(congested_cells.to_string(index=False))

# Save dataset
df.to_csv("data/raw/telecom_kpi_sample.csv", index=False)

print("\nDataset saved successfully.")
