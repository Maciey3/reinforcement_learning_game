import pygame
from player import Player
from world import World
pygame.init()


class Game(object):
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 800
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.world = World()
        # self.world.construct()
        self.world.load_objects_from_json('track1')
        # return

        self.player = Player(0, 0, 30, 30, world=self.world)
        self.clock = pygame.time.Clock()

    def show_fps(self):
        font = pygame.font.SysFont("Arial", 18, bold=True)
        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        self.screen.blit(fps_t, (5, 5))

    def run(self):
        run = True
        while run:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.world.render(self.screen)
            self.player.render(self.screen)
            self.player.movement(self.HEIGHT, self.WIDTH)
            self.show_fps()

            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()


a = Game()
a.run()

# world = World()
# world.load_objects_from_json('track1')