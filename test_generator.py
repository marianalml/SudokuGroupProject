from sudoku_generator import generate_sudoku


def test_levels():
    for removed in [30, 40, 50]:
        print(f"\nTesting difficulty with {removed} removed cells:")
        board = generate_sudoku(9, removed)

        empty_count = sum(row.count(0) for row in board)
        print(f"Empty cells: {empty_count}")

        for row in board:
            print(row)


if __name__ == "__main__":
    test_levels()