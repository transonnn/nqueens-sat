import sys
import time
import cplex


def solve_nqueens(n):
    if n < 1:
        raise ValueError("N phải là số nguyên dương.")

    model = cplex.Cplex()

    try:
        model.set_log_stream(None)
        model.set_results_stream(None)
        model.set_warning_stream(None)
        model.set_error_stream(None)
        model.parameters.threads.set(1)
        model.objective.set_sense(model.objective.sense.minimize)

        names = [
            f"x_{r}_{c}"
            for r in range(n)
            for c in range(n)
        ]

        model.variables.add(
            obj=[0.0] * (n * n),
            types=[model.variables.type.binary] * (n * n),
            names=names
        )

        def var_id(r, c):
            return r * n + c

        def add_constraint(indices, sense, rhs):
            model.linear_constraints.add(
                lin_expr=[
                    cplex.SparsePair(
                        ind=indices,
                        val=[1.0] * len(indices)
                    )
                ],
                senses=[sense],
                rhs=[rhs]
            )

        for r in range(n):
            add_constraint(
                [var_id(r, c) for c in range(n)],
                "E",
                1.0
            )

        for c in range(n):
            add_constraint(
                [var_id(r, c) for r in range(n)],
                "E",
                1.0
            )

        for diff in range(-(n - 1), n):
            diagonal = [
                var_id(r, c)
                for r in range(n)
                for c in range(n)
                if r - c == diff
            ]

            if len(diagonal) > 1:
                add_constraint(diagonal, "L", 1.0)

        for total in range(2 * n - 1):
            diagonal = [
                var_id(r, c)
                for r in range(n)
                for c in range(n)
                if r + c == total
            ]

            if len(diagonal) > 1:
                add_constraint(diagonal, "L", 1.0)

        model.solve()

        if not model.solution.is_primal_feasible():
            if n in (2, 3):
                return None

            raise RuntimeError(
                "CPLEX không tìm được nghiệm. "
                f"Status={model.solution.get_status()}"
            )

        values = model.solution.get_values()

        return [
            [
                int(values[var_id(r, c)] > 0.5)
                for c in range(n)
            ]
            for r in range(n)
        ]

    finally:
        model.end()


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