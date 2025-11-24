import pygame
from board import Board
from sudoku_generator import generate_sudoku, SudokuGenerator

pygame.init()
screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption('Sudoku')

solution_generator = SudokuGenerator(9,0)
solution_generator.fill_values()
solution = solution_generator.get_board()

puzzle = generate_sudoku(9,30)

board = Board(screen, puzzle, solution)

running = True

while running:

    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MOUSE INPUTS
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 0 <= mouse_x < 600 and 0 <= mouse_y < 700:
                position = board.click(mouse_x, mouse_y)
                if position:
                    r, c = position
                    board.select(r,c)

    #keyboard inputs
        if event.type == pygame.KEYDOWN and board.selected:
            r,c = board.selected

            if event.key == pygame.K_UP and r > 0:
                board.select(r-1, c)
            if event.key == pygame.K_DOWN and r < 8:
                board.select(r+1, c)
            if event.key == pygame.K_RIGHT and c < 8:
                board.select(r, c+1)
            if event.key == pygame.K_LEFT and c < 0:
                board.select(r, c-1)


            if pygame.K_1 <= event.key <= pygame.K_9:
                value = event.key - pygame.K_0
                board.sketch(value)

            if event.key == pygame.K_BACKSPACE:
                board.clear()

    board.draw()
    pygame.display.update()

pygame.quit()
