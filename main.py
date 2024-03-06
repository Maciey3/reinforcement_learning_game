import pygame
pygame.init()


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("game_arrow.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.x_vel = 0
        self.y_vel = 0
        # self.speed = 1
        self.sprite = self.image.subsurface(self.image.get_rect())
        # self.sprite = (self.image.subsurface(pygame.Rect(0, 0, 20, 20)))
        # print(self.sprite)
        # print(self.image.get_rect())


    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def movement(self, HEIGHT, WIDTH):
        starting_vel = 3
        acceleration = 0.7
        friction = 0.35
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_a]:
            if self.x_vel <= -starting_vel+1:
                self.x_vel -= acceleration
            elif self.x_vel > 0:
                self.x_vel -= acceleration
            else:
                self.x_vel = -starting_vel

        if self.keys[pygame.K_d]:
            if self.x_vel >= starting_vel-1:
                self.x_vel += acceleration
            elif self.x_vel < 0:
                self.x_vel += acceleration
            else:
                self.x_vel = starting_vel

        if self.keys[pygame.K_w]:
            if self.y_vel <= -starting_vel+1:
                self.y_vel -= acceleration
            elif self.y_vel > 0:
                self.y_vel -= acceleration
            else:
                self.y_vel = -starting_vel

        if self.keys[pygame.K_s]:
            if self.y_vel >= starting_vel-1:
                self.y_vel += acceleration
            elif self.y_vel < 0:
                self.y_vel += acceleration
            else:
                self.y_vel = starting_vel

        # BUG with velocity
        if self.x_vel > 0:
            self.x_vel -= friction
        elif self.x_vel < 0:
            self.x_vel += friction

        if self.y_vel > 0:
            self.y_vel -= friction
        elif self.y_vel < 0:
            self.y_vel += friction

        self.x += self.x_vel
        self.y += self.y_vel

        if self.y < 0:
            self.y_vel = 0
            self.y = 0

        if self.y + self.image.get_height() > HEIGHT:
            self.y_vel = 0
            self.y = HEIGHT - self.image.get_height()

        if self.x < 0:
            self.x_vel = 0
            self.x = 0

        if self.x + self.image.get_width() > WIDTH:
            self.x_vel = 0
            self.x = WIDTH - self.image.get_width()

class MainRun(object):
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.player = Player(100, 100, 150, 150)
        self.clock = pygame.time.Clock()

    def show_fps(self):
        font = pygame.font.SysFont("Arial", 18, bold=True)
        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        self.screen.blit(fps_t, (5, 5))

    def main_loop(self):
        run = True
        while run:
            self.screen.fill((255, 255, 255))
            self.show_fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.player.draw(self.screen)
            self.player.movement(self.HEIGHT, self.WIDTH)
            # print(self.player.x)
            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()


a = MainRun()
a.main_loop()
