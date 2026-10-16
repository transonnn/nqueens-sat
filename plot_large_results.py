import csv
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt

INPUT_FILE = "benchmark_large.csv"
OUTPUT_IMAGE = "benchmark_large.png"
OUTPUT_SUMMARY = "benchmark_large_medians.csv"

solvers = ["SAT", "CP-SAT", "CPLEX MIP", "Gurobi", "CPLEX CP"]
data = defaultdict(list)

with open(INPUT_FILE, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["status"] != "OK":
            continue

        if row["solution_valid"].strip().lower() != "true":
            continue

        n = int(row["n"])
        solver = row["solver"]
        elapsed = float(row["time_seconds"])

        data[(n, solver)].append(elapsed)

sizes = sorted({n for n, _ in data})

if not sizes:
    raise SystemExit("Không tìm thấy kết quả benchmark hợp lệ.")

summary = []
fig, ax = plt.subplots(figsize=(10, 6))

for solver in solvers:
    solver_sizes = []
    medians = []
    lower_errors = []
    upper_errors = []

    for n in sizes:
        times = data.get((n, solver), [])

        if not times:
            continue

        median = statistics.median(times)

        solver_sizes.append(n)
        medians.append(median)
        lower_errors.append(median - min(times))
        upper_errors.append(max(times) - median)

        summary.append({
            "n": n,
            "solver": solver,
            "successful_runs": len(times),
            "median_seconds": f"{median:.9f}",
            "min_seconds": f"{min(times):.9f}",
            "max_seconds": f"{max(times):.9f}",
        })

    if solver_sizes:
        ax.errorbar(
            solver_sizes,
            medians,
            yerr=[lower_errors, upper_errors],
            marker="o",
            capsize=4,
            label=solver,
        )

ax.set_yscale("log")
ax.set_xlabel("Board size N")
ax.set_ylabel("End-to-end runtime (seconds, log scale)")
ax.set_title("N-Queens: Large-Scale Solver Comparison")
ax.set_xticks(sizes)
ax.grid(True, which="both", linestyle="--", alpha=0.35)
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT_IMAGE, dpi=200)
plt.close(fig)

with open(
    OUTPUT_SUMMARY, "w", newline="", encoding="utf-8-sig"
) as file:
    fields = [
        "n",
        "solver",
        "successful_runs",
        "median_seconds",
        "min_seconds",
        "max_seconds",
    ]

    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(summary)

print(f"Saved chart: {OUTPUT_IMAGE}")
print(f"Saved summary: {OUTPUT_SUMMARY}")
