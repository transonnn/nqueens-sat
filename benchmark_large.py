import csv
import importlib
import platform
import statistics
import sys
import time


SIZES = [32, 40, 48, 64]
REPEATS = 3
OUTPUT_FILE = "benchmark_large.csv"

SOLVER_SPECS = [
    ("SAT", "nqueens_sat"),
    ("CP-SAT", "nqueens_cpsat"),
    ("CPLEX MIP", "nqueens_cplex_mip"),
    ("Gurobi", "nqueens_gurobi"),
    ("CPLEX CP", "nqueens_cplex_cp"),
]


def is_valid(board, n):
    if board is None or len(board) != n:
        return False

    if any(
        len(row) != n or sum(row) != 1
        for row in board
    ):
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


def make_record(n, solver, repetition, elapsed, status,
                valid, error=""):
    return {
        "python_version": sys.version.split()[0],
        "operating_system": platform.platform(),
        "n": n,
        "solver": solver,
        "repetition": repetition,
        "time_seconds": (
            "" if elapsed is None else f"{elapsed:.9f}"
        ),
        "status": status,
        "solution_valid": valid,
        "error": error,
    }


def main():
    print("Python:", sys.version.split()[0])
    print("OS:", platform.platform())
    print("Loading and checking solvers...\n")

    solvers = {}
    preflight_errors = {}

    for name, module_name in SOLVER_SPECS:
        try:
            module = importlib.import_module(module_name)
            solve = getattr(module, "solve_nqueens")

            board = solve(4)

            if not is_valid(board, 4):
                raise RuntimeError(
                    "Solver returned an invalid solution for N=4"
                )

            solvers[name] = solve
            print(f"{name}: READY")

        except Exception as exc:
            preflight_errors[name] = (
                f"{type(exc).__name__}: {exc}"
            )
            print(f"{name}: FAILED - {preflight_errors[name]}")

    if not solvers:
        raise SystemExit(
            "No solver passed the initial check. "
            "Fix the errors before benchmarking."
        )

    results = []

    for n in SIZES:
        for repetition in range(1, REPEATS + 1):
            enabled_names = [
                name for name, _ in SOLVER_SPECS
                if name in solvers
            ]

            shift = (repetition - 1) % len(enabled_names)
            ordered_names = (
                enabled_names[shift:] + enabled_names[:shift]
            )

            for name in ordered_names:
                start = time.perf_counter()
                elapsed = None

                try:
                    board = solvers[name](n)
                    elapsed = time.perf_counter() - start

                    valid = is_valid(board, n)

                    if valid:
                        status = "OK"
                        error = ""
                    else:
                        status = "INVALID"
                        error = (
                            "No valid solution was returned; "
                            "all tested N values are expected to be solvable."
                        )

                except Exception as exc:
                    elapsed = time.perf_counter() - start
                    valid = False
                    status = "ERROR"
                    error = f"{type(exc).__name__}: {exc}"

                results.append(
                    make_record(
                        n, name, repetition, elapsed,
                        status, valid, error
                    )
                )

                elapsed_text = (
                    "N/A" if elapsed is None
                    else f"{elapsed:.6f} s"
                )

                print(
                    f"N={n:2d} | {name:9s} | "
                    f"run={repetition} | "
                    f"{elapsed_text:>12s} | {status}"
                )

            for name, _ in SOLVER_SPECS:
                if name not in solvers:
                    results.append(
                        make_record(
                            n, name, repetition, None,
                            "SKIPPED", False,
                            preflight_errors[name]
                        )
                    )

    fields = [
        "python_version",
        "operating_system",
        "n",
        "solver",
        "repetition",
        "time_seconds",
        "status",
        "solution_valid",
        "error",
    ]

    with open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\nMedian execution time (seconds)")
    print(f"{'N':>4}", end="")

    for name, _ in SOLVER_SPECS:
        print(f"{name:>14}", end="")

    print()

    for n in SIZES:
        print(f"{n:4d}", end="")

        for name, _ in SOLVER_SPECS:
            times = [
                float(row["time_seconds"])
                for row in results
                if row["n"] == n
                and row["solver"] == name
                and row["status"] == "OK"
                and row["solution_valid"] is True
                and row["time_seconds"] != ""
            ]

            if times:
                value = f"{statistics.median(times):.6f}"
            else:
                value = "N/A"

            print(f"{value:>14}", end="")

        print()

    print(f"\nSaved raw results to {OUTPUT_FILE}")

    errors = [
        row for row in results
        if row["status"] in ("ERROR", "INVALID", "SKIPPED")
    ]

    print(
        f"Successful runs: "
        f"{sum(row['status'] == 'OK' for row in results)}"
    )
    print(f"Failed or skipped runs: {len(errors)}")


if __name__ == "__main__":
    main()
