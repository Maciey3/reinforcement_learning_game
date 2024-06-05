import pygame
from player import Player
from world import World
from button import Button
pygame.init()
pygame.font.init()


class Game(object):
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 800
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.world = World()
        # self.world.construct()
        self.world.load_objects_from_json('track1')

        self.player = Player(
            (self.world.start_line_object.x + self.world.start_line_object.width - 30) // 2,
            (self.world.start_line_object.y + self.world.start_line_object.height - 30) // 2,
            30,
            30,
            world=self.world
        )
        self.clock = pygame.time.Clock()

    def show_fps(self):
        font = pygame.font.SysFont("Arial", 18, bold=True)
        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        self.screen.blit(fps_t, (5, 5))

    def run(self):
        run = True
        timer = 0
        while run:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                else:
                    keys = None

                if keys:
                    if keys[pygame.K_ESCAPE]:
                        print('asd')
                        self.menu()

                if event.type == pygame.QUIT:
                    run = False
                    break

            self.world.render(self.screen)
            self.player.render(self.screen)
            self.player.movement(self.HEIGHT, self.WIDTH, timer)
            self.show_fps()
            # print(self.player.collision_repaired_time)

            pygame.display.update()
            timer += self.clock.tick(self.FPS)
            print(f"{timer//1000} s")
        pygame.quit()

    def menu(self):
        run = True
        click = False
        header_font = pygame.font.SysFont('Arial', 50, bold=True)

        while run:
            self.screen.fill((255, 255, 255))

            header_surface = header_font.render('Menu', False, (0, 0, 0))
            text_rect = header_surface.get_rect(center=(self.WIDTH/2, 100))
            self.screen.blit(header_surface, text_rect)

            mx, my = pygame.mouse.get_pos()

            button_play = Button(self.WIDTH, 300, 250, 70, self.screen, center=True)
            button_play.add_text('Play')
            button_play.render()

            button_options = Button(self.WIDTH, 400, 250, 70, self.screen, center=True)
            button_options.add_text('Options')
            button_options.render()

            if button_play.button.collidepoint((mx, my)):
                if click:
                    self.__init__()
                    self.run()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pygame.QUIT:
                    run = False
                    break

            pygame.display.update()
        pygame.quit()

game = Game()
# game.run()
game.menu()