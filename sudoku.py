import pygame
from board import Board
from sudoku_generator import generate_sudoku, SudokuGenerator

pygame.init()
screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption("Sudoku")

FONT = pygame.font.SysFont("comicsans", 40)
SMALL = pygame.font.SysFont("comicsans", 28)

STATE_MENU = 0
STATE_PLAYING = 1
STATE_WIN = 2
STATE_LOSE = 3

game_state = STATE_MENU
board = None
solution = None
difficulty = None

clock = pygame.time.Clock()


def draw_menu():
    screen.fill((255, 255, 255))
    title = FONT.render("Sudoku", True, (0, 0, 0))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 80))

    easy_txt = SMALL.render("Easy (30 removed)", True, (0, 0, 0))
    med_txt = SMALL.render("Medium (40 removed)", True, (0, 0, 0))
    hard_txt = SMALL.render("Hard (50 removed)", True, (0, 0, 0))

    easy_rect = pygame.Rect(screen.get_width() // 2 - 150, 230, 300, 50)
    med_rect = pygame.Rect(screen.get_width() // 2 - 150, 310, 300, 50)
    hard_rect = pygame.Rect(screen.get_width() // 2 - 150, 390, 300, 50)

    # Draw buttons
    pygame.draw.rect(screen, (220, 220, 220), easy_rect)
    pygame.draw.rect(screen, (220, 220, 220), med_rect)
    pygame.draw.rect(screen, (220, 220, 220), hard_rect)
    pygame.draw.rect(screen, (0, 0, 0), easy_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), med_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), hard_rect, 2)

    # Draw text centered
    screen.blit(easy_txt, (easy_rect.centerx - easy_txt.get_width() // 2,
                           easy_rect.centery - easy_txt.get_height() // 2))
    screen.blit(med_txt, (med_rect.centerx - med_txt.get_width() // 2,
                          med_rect.centery - med_txt.get_height() // 2))
    screen.blit(hard_txt, (hard_rect.centerx - hard_txt.get_width() // 2,
                           hard_rect.centery - hard_txt.get_height() // 2))

    return {"easy": easy_rect, "medium": med_rect, "hard": hard_rect}


def draw_game_buttons():
    """Draw Restart, Reset, and Exit buttons during gameplay"""
    restart_rect = pygame.Rect(50, 660, 140, 50)
    reset_rect = pygame.Rect(230, 660, 140, 50)
    exit_rect = pygame.Rect(410, 660, 140, 50)

    pygame.draw.rect(screen, (200, 200, 200), restart_rect)
    pygame.draw.rect(screen, (200, 200, 200), reset_rect)
    pygame.draw.rect(screen, (200, 200, 200), exit_rect)
    pygame.draw.rect(screen, (0, 0, 0), restart_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), reset_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), exit_rect, 2)

    restart_txt = SMALL.render("Restart", True, (0, 0, 0))
    reset_txt = SMALL.render("Reset", True, (0, 0, 0))
    exit_txt = SMALL.render("Exit", True, (0, 0, 0))

    screen.blit(restart_txt, (restart_rect.centerx - restart_txt.get_width() // 2,
                              restart_rect.centery - restart_txt.get_height() // 2))
    screen.blit(reset_txt, (reset_rect.centerx - reset_txt.get_width() // 2,
                            reset_rect.centery - reset_txt.get_height() // 2))
    screen.blit(exit_txt, (exit_rect.centerx - exit_txt.get_width() // 2,
                           exit_rect.centery - exit_txt.get_height() // 2))

    return {"restart": restart_rect, "reset": reset_rect, "exit": exit_rect}


def draw_end_screen(text):
    screen.fill((255, 255, 255))
    msg = FONT.render(text, True, (0, 0, 0))
    screen.blit(msg, (screen.get_width() // 2 - msg.get_width() // 2, 140))

    restart_rect = pygame.Rect(screen.get_width() // 2 - 170, 320, 160, 50)
    exit_rect = pygame.Rect(screen.get_width() // 2 + 10, 320, 160, 50)

    pygame.draw.rect(screen, (200, 200, 200), restart_rect)
    pygame.draw.rect(screen, (200, 200, 200), exit_rect)
    pygame.draw.rect(screen, (0, 0, 0), restart_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), exit_rect, 2)

    rtxt = SMALL.render("Restart", True, (0, 0, 0))
    etxt = SMALL.render("Exit", True, (0, 0, 0))
    screen.blit(rtxt, (restart_rect.centerx - rtxt.get_width() // 2,
                       restart_rect.centery - rtxt.get_height() // 2))
    screen.blit(etxt, (exit_rect.centerx - etxt.get_width() // 2,
                       exit_rect.centery - etxt.get_height() // 2))

    return {"restart": restart_rect, "exit": exit_rect}


def start_new_game(removed_count):
    # Generate solution
    sol_gen = SudokuGenerator(9, 0)
    sol_gen.fill_values()
    solution = [row[:] for row in sol_gen.get_board()]

    # Generate puzzle
    puzzle_gen = SudokuGenerator(9, removed_count)
    puzzle_gen.fill_values()
    puzzle_gen.remove_cells()
    puzzle = [row[:] for row in puzzle_gen.get_board()]

    return puzzle, solution


running = True
click_pos = None
click_pressed = False
button_rects = {}

while running:
    click_pos = None
    click_pressed = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = pygame.mouse.get_pos()
            click_pressed = True

        elif event.type == pygame.KEYDOWN and board is not None and board.selected and game_state == STATE_PLAYING:
            r, c = board.selected
            if event.key == pygame.K_UP and r > 0:
                board.select(r - 1, c)
            elif event.key == pygame.K_DOWN and r < 8:
                board.select(r + 1, c)
            elif event.key == pygame.K_LEFT and c > 0:
                board.select(r, c - 1)
            elif event.key == pygame.K_RIGHT and c < 8:
                board.select(r, c + 1)
            elif pygame.K_1 <= event.key <= pygame.K_9:
                board.sketch(event.key - pygame.K_0)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                sk = board.cells[r][c].sketched_value
                if sk != 0:
                    board.place_number(sk)
                    full = board.update_board()
                    if full:
                        correct = board.check_board()
                        game_state = STATE_WIN if correct else STATE_LOSE
            elif event.key == pygame.K_BACKSPACE:
                board.clear()

    # DRAW
    if game_state == STATE_MENU:
        button_rects = draw_menu()
        if click_pressed and click_pos:
            x, y = click_pos
            if button_rects["easy"].collidepoint(x, y):
                difficulty = 30
            elif button_rects["medium"].collidepoint(x, y):
                difficulty = 40
            elif button_rects["hard"].collidepoint(x, y):
                difficulty = 50
            else:
                difficulty = None

            if difficulty:
                puzzle, solution = start_new_game(difficulty)
                board = Board(screen, puzzle, solution)
                game_state = STATE_PLAYING

    elif game_state == STATE_PLAYING:
        screen.fill((255, 255, 255))
        if board:
            board.draw()

        # Draw gameplay buttons
        button_rects = draw_game_buttons()

        # Handle clicks
        if click_pressed and click_pos and board:
            x, y = click_pos
            # Check if clicking buttons
            if button_rects["restart"].collidepoint(x, y):
                game_state = STATE_MENU
                board = None
                solution = None
            elif button_rects["reset"].collidepoint(x, y):
                # Reset the current puzzle
                board.reset_to_original()
            elif button_rects["exit"].collidepoint(x, y):
                running = False
            else:
                # Click on board
                pos = board.click(x, y)
                if pos:
                    board.select(*pos)

    elif game_state == STATE_WIN:
        button_rects = draw_end_screen("You Win!")
        if click_pressed and click_pos:
            x, y = click_pos
            if button_rects["restart"].collidepoint(x, y):
                game_state = STATE_MENU
                board = None
                solution = None
            elif button_rects["exit"].collidepoint(x, y):
                running = False

    elif game_state == STATE_LOSE:
        button_rects = draw_end_screen("Game Over")
        if click_pressed and click_pos:
            x, y = click_pos
            if button_rects["restart"].collidepoint(x, y):
                game_state = STATE_MENU
                board = None
                solution = None
            elif button_rects["exit"].collidepoint(x, y):
                running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()