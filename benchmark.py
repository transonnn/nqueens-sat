import csv
import platform
import statistics
import sys
import time

from nqueens_sat import solve_nqueens as solve_sat
from nqueens_cpsat import solve_nqueens as solve_cpsat


SIZES = [4, 8, 12, 16, 20, 24, 28, 32]
REPEATS = 3


def is_valid(board, n):
    if board is None or len(board) != n:
        return False

    if any(len(row) != n or sum(row) != 1 for row in board):
        return False

    if any(
        sum(board[r][c] for r in range(n)) != 1
        for c in range(n)
    ):
        return False

    positions = [row.index(1) for row in board]

    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            if abs(positions[r1] - positions[r2]) == r2 - r1:
                return False

    return True


def main():
    print("Python:", sys.version.split()[0])
    print("OS:", platform.platform())
    print("Warming up solvers...")

    solve_sat(4)
    solve_cpsat(4)

    results = []

    for n in SIZES:
        for repetition in range(1, REPEATS + 1):
            methods = [
                ("SAT", solve_sat),
                ("CP-SAT", solve_cpsat),
            ]

            if repetition % 2 == 0:
                methods.reverse()

            for name, solve in methods:
                start = time.perf_counter()
                board = solve(n)
                elapsed = time.perf_counter() - start

                if not is_valid(board, n):
                    raise RuntimeError(
                        f"{name} produced an invalid solution for N={n}"
                    )

                results.append({
                    "n": n,
                    "solver": name,
                    "repetition": repetition,
                    "time_seconds": f"{elapsed:.9f}",
                    "solution_valid": True,
                })

                print(
                    f"N={n:2d} | {name:6s} | "
                    f"run={repetition} | {elapsed:.6f} seconds"
                )

    filename = "benchmark_results.csv"
    fields = [
        "n",
        "solver",
        "repetition",
        "time_seconds",
        "solution_valid",
    ]

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\nMedian execution time (seconds)")
    print(f"{'N':>4} {'SAT':>14} {'CP-SAT':>14}")

    for n in SIZES:
        sat_times = [
            float(row["time_seconds"])
            for row in results
            if row["n"] == n and row["solver"] == "SAT"
        ]

        cpsat_times = [
            float(row["time_seconds"])
            for row in results
            if row["n"] == n and row["solver"] == "CP-SAT"
        ]

        print(
            f"{n:4d} "
            f"{statistics.median(sat_times):14.6f} "
            f"{statistics.median(cpsat_times):14.6f}"
        )

    print(f"\nSaved results to {filename}")


if __name__ == "__main__":
    main()
