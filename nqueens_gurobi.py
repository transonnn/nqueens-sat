import sys
import time
import gurobipy as gp
from gurobipy import GRB


def solve_nqueens(n):
    if n < 1:
        raise ValueError("N phải là số nguyên dương.")

    with gp.Env(params={"OutputFlag": 0}) as env:
        with gp.Model("NQueens", env=env) as model:
            model.Params.Threads = 1

            x = model.addVars(
                range(n), range(n),
                vtype=GRB.BINARY,
                name="x"
            )

            for r in range(n):
                model.addConstr(
                    gp.quicksum(x[r, c] for c in range(n)) == 1
                )

            for c in range(n):
                model.addConstr(
                    gp.quicksum(x[r, c] for r in range(n)) == 1
                )

            for diff in range(-(n - 1), n):
                diagonal = [
                    x[r, c]
                    for r in range(n)
                    for c in range(n)
                    if r - c == diff
                ]

                if len(diagonal) > 1:
                    model.addConstr(gp.quicksum(diagonal) <= 1)

            for total in range(2 * n - 1):
                diagonal = [
                    x[r, c]
                    for r in range(n)
                    for c in range(n)
                    if r + c == total
                ]

                if len(diagonal) > 1:
                    model.addConstr(gp.quicksum(diagonal) <= 1)

            model.setObjective(0.0, GRB.MINIMIZE)
            model.optimize()

            if model.Status == GRB.INFEASIBLE:
                return None

            if model.SolCount == 0:
                raise RuntimeError(
                    f"Gurobi không tìm được nghiệm. Status={model.Status}"
                )

            return [
                [
                    int(x[r, c].X > 0.5)
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