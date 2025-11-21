import pygame
from sudoku_generator import generate_sudoku
from board import Board

pygame.init()
screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption('Sudoku')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
