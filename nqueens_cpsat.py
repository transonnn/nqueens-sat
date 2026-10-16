import sys
import time
from ortools.sat.python import cp_model


def solve_nqueens(n):
    if n < 1:
        raise ValueError("N phải là số nguyên dương.")

    model = cp_model.CpModel()

    x = [
        [model.NewBoolVar(f"x_{r}_{c}") for c in range(n)]
        for r in range(n)
    ]

    for r in range(n):
        model.AddExactlyOne(x[r])

    for c in range(n):
        model.AddExactlyOne([x[r][c] for r in range(n)])

    for diff in range(-(n - 1), n):
        diagonal = [
            x[r][c]
            for r in range(n)
            for c in range(n)
            if r - c == diff
        ]
        if len(diagonal) > 1:
            model.AddAtMostOne(diagonal)

    for total in range(2 * n - 1):
        diagonal = [
            x[r][c]
            for r in range(n)
            for c in range(n)
            if r + c == total
        ]
        if len(diagonal) > 1:
            model.AddAtMostOne(diagonal)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.INFEASIBLE:
        return None

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(
            f"CP-SAT không hoàn tất: {solver.StatusName(status)}"
        )

    board = [
        [solver.Value(x[r][c]) for c in range(n)]
        for r in range(n)
    ]

    return board


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
