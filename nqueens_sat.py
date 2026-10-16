import sys
import time
from pysat.solvers import Solver


def var_id(row, col, n):
    return row * n + col + 1


def solve_nqueens(n):
    if n < 1:
        raise ValueError("N phải là số nguyên dương.")

    with Solver(name="g3") as solver:
        for r in range(n):
            solver.add_clause([var_id(r, c, n) for c in range(n)])

            for c1 in range(n):
                for c2 in range(c1 + 1, n):
                    solver.add_clause([
                        -var_id(r, c1, n),
                        -var_id(r, c2, n)
                    ])

        for c in range(n):
            solver.add_clause([var_id(r, c, n) for r in range(n)])

            for r1 in range(n):
                for r2 in range(r1 + 1, n):
                    solver.add_clause([
                        -var_id(r1, c, n),
                        -var_id(r2, c, n)
                    ])

        for r1 in range(n):
            for c1 in range(n):
                for r2 in range(r1 + 1, n):
                    d = r2 - r1

                    for c2 in (c1 - d, c1 + d):
                        if 0 <= c2 < n:
                            solver.add_clause([
                                -var_id(r1, c1, n),
                                -var_id(r2, c2, n)
                            ])

        if not solver.solve():
            return None

        model = {
            literal
            for literal in solver.get_model()
            if literal > 0
        }

        board = [
            [
                1 if var_id(r, c, n) in model else 0
                for c in range(n)
            ]
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
