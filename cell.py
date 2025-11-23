import pygame

cell_size = 50

class Cell:

    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

        self.main_font = pygame.font.SysFont('comicsans', 30)
        self.sketch_font = pygame.font.SysFont('comicsans', 20)

    def set_cell_value(self, value):
        self.value = value
        self.sketched_value = 0

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * cell_size
        y = self.row * cell_size

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y, cell_size, cell_size))

        if self.value != 0:
            text = self.main_font.render(str(self.value), True, (0,0,0))
            text_rect = text_surface = text.get_rect(center =(x + cell_size//2, y + cell_size//2))
            self.screen.blit(text, text_rect)

        elif self.sketched_value != 0:
            sketch = self.sketch_font.render(str(self.sketched_value), True, (128,128,128))
            self.screen.blit(sketch, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, (255,0,0), (x, y, cell_size, cell_size),3)
        else:
            pygame.draw.rect(self.screen, (0,0,0), (x, y, cell_size, cell_size), 1)
