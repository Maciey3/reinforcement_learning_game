import pygame


class Button:
    def __init__(self, left, top, width, height, screen, text, center=True, color=(0, 0, 0)):
        if center:
            self.button = pygame.Rect((left-width)/2, top, width, height)
        else:
            self.button = pygame.Rect(left, top, width, height)
        self.color = color
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 30)

        self.text_surface = self.font.render(text, False, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.button.center)

    # def add_text(self, text):


    def render(self):
        pygame.draw.rect(self.screen, self.color, self.button, 3)
        self.screen.blit(self.text_surface, self.text_rect)