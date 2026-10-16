from nqueens_sat import solve_nqueens


def is_valid(board):
    n = len(board)

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
    test_sizes = [1, 2, 3, 4, 5, 8, 10]

    for n in test_sizes:
        board = solve_nqueens(n)
        should_have_solution = n == 1 or n >= 4

        if should_have_solution:
            assert board is not None, f"N={n}: Không tìm thấy nghiệm"
            assert is_valid(board), f"N={n}: Nghiệm không hợp lệ"
        else:
            assert board is None, f"N={n}: Kết quả không đúng"

        print(f"N={n}: PASS")


if __name__ == "__main__":
    main()
