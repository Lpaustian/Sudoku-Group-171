import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketch_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketch_value = value

    def get_sketched_value(self):
        return self.sketch_value

    def draw(self):
        x = self.col * 60
        y = self.row * 60
        rect = pygame.Rect(self.col * 60, self.row * 60, 60, 60)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        #rect = pygame.Rect(x, y, 60, 60)
        #pygame.draw.rect(self.screen, (255, 255, 255), rect)
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
        if self.value != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 20))
        elif self.sketch_value != 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.sketch_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))