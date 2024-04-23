import pygame


class World_object(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('black'), self.rectangle)


class Start_line(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load('images/start_line.png'), (self.width, self.height))
        self.rectangle = self.image.get_rect()
        self.rectangle.x = self.x
        self.rectangle.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Finish_line(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load('images/start_line.png'), (self.width, self.height))
        self.rectangle = self.image.get_rect()
        self.rectangle.x = self.x
        self.rectangle.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))