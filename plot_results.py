import csv
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt


filename = "benchmark_results.csv"
data = defaultdict(list)

with open(filename, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        n = int(row["n"])
        solver = row["solver"]
        runtime = float(row["time_seconds"])
        data[(n, solver)].append(runtime)

sizes = sorted({n for n, solver in data})
solvers = ["SAT", "CP-SAT"]

plt.figure(figsize=(9, 5.5))

for solver in solvers:
    medians = []
    lower_errors = []
    upper_errors = []

    for n in sizes:
        times = data[(n, solver)]
        median = statistics.median(times)

        medians.append(median)
        lower_errors.append(median - min(times))
        upper_errors.append(max(times) - median)

    plt.errorbar(
        sizes,
        medians,
        yerr=[lower_errors, upper_errors],
        marker="o",
        capsize=4,
        label=solver,
    )

plt.yscale("log")
plt.xlabel("Board size N")
plt.ylabel("Runtime in seconds (log scale)")
plt.title("N-Queens: SAT vs CP-SAT")
plt.xticks(sizes)
plt.grid(True, which="both", linestyle="--", alpha=0.4)
plt.legend()
plt.tight_layout()

output = "benchmark_median.png"
plt.savefig(output, dpi=200)
plt.show()

print(f"Saved chart to {output}")
