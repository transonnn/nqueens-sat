import sys
import time
from docplex.cp.model import CpoModel


CP_OPTIMIZER_PATH = (
    r"C:\Program Files\IBM\ILOG\CPLEX_Studio_Community222"
    r"\cpoptimizer\bin\x64_win64\cpoptimizer.exe"
)


def solve_nqueens(n):
    if n < 1:
        raise ValueError("N phải là số nguyên dương.")

    model = CpoModel(name="NQueens")

    queens = [
        model.integer_var(0, n - 1, name=f"q_{r}")
        for r in range(n)
    ]

    model.add(model.all_diff(queens))
    model.add(model.all_diff([
        queens[r] + r for r in range(n)
    ]))
    model.add(model.all_diff([
        queens[r] - r for r in range(n)
    ]))

    solution = model.solve(
        execfile=CP_OPTIMIZER_PATH,
        Workers=1,
        LogVerbosity="Quiet"
    )

    if solution is None:
        return None

    status = solution.get_solve_status()

    if status == "Infeasible":
        return None

    if status not in ("Feasible", "Optimal"):
        raise RuntimeError(
            f"CP Optimizer không hoàn tất. Status={status}"
        )

    positions = [solution.get_value(q) for q in queens]

    return [
        [
            1 if positions[r] == c else 0
            for c in range(n)
        ]
        for r in range(n)
    ]


def main():
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    except ValueError:
        raise SystemExit("N phải là một số nguyên.")

    if n < 1:
        raise SystemExit("N phải lớn hơn hoặc bằng 1.")

    start = time.perf_counter()
    board = solve_nqueens(n)
    elapsed = time.perf_counter() - start

    print(f"N = {n}")

    if board is None:
        print("Không tồn tại lời giải.")
    else:
        print("Tìm thấy lời giải:")
        for row in board:
            print(" ".join("Q" if cell else "." for cell in row))

    print(f"Thời gian chạy: {elapsed:.6f} giây")


if __name__ == "__main__":
    main()
