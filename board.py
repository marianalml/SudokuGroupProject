import pygame
from cell import Cell, cell_size

board_size = cell_size * 9

class Board:

    def __init__(self, screen, board, solution):
        self.screen = screen
        self.board = board
        self.original = board
        self.solution = solution
        self.selected = None

        self.cells = []
        for r in range(9):
            row_list = []
            for c in range(9):
                value = board[r][c]
                row_list.append(Cell(value, r, c, screen))
            self.cells.append(row_list)


    def draw(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw()

        for i in range (10):
            thickness = 3 if i % 3 == 0 else 1

            pygame.draw.line(
                self.screen,(0,0,0),
                (0, i * cell_size),
                (board_size, i * cell_size),
                thickness
            )

            pygame.draw.line(
                self.screen,(0,0,0),
                (i * cell_size, 0),
                (i * cell_size, board_size),
                thickness
            )

    def select(self, row, col):
        if self.selected is not None:
            old_r, old_c = self.selected
            self.cells[old_r][old_c].selected = False

        self.selected = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        if x < 0 or x >= board_size or y < 0 or y >= board_size:
            return None

        row = y // cell_size
        col = x // cell_size
        return (row, col)

    def sketch(self, value):
        if self.selected is None:
            return

        r, c = self.selected

        if self.original[r][c] != 0:
            return

        self.cells[r][c].set_sketched_value(value)


    def place_number(self, value):
        if self.selected is None:
            return

        r, c = self.selected
        if self.original[r][c] != 0:
            return

        self.cells[r][c].set_cell_value(value)
        self.update_board()

    def clear(self):
        if self.selected is None:
            return

        r, c = self.selected

        if self.original[r][c] != 0:
            return

        self.cells[r][c].set_cell_value(0)
        self.cells[r][c].set_sketched_value(0)

    def update_board(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return False
        return True

    def check_board(self):
        if self.solution is None:
            return False

        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value !=  self.solution[r][c]:
                    return False
        return True


