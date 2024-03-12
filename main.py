import pygame
import json
pygame.init()


class Player(object):
    def __init__(self, x, y, width, height, world):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("game_arrow_cut.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x_vel = 0
        self.y_vel = 0
        self.sprite = self.image.subsurface(self.image.get_rect())
        self.world = world

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        pygame.draw.rect(
            screen,
            pygame.Color('red'),
            pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()),
            2
        )

    def key_handling(self, starting_vel, acceleration):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.__init__(10, 10, 30, 30, self.world)

        if keys[pygame.K_a]:
            if self.x_vel <= -starting_vel+1:
                self.x_vel -= acceleration
            elif self.x_vel > 0:
                self.x_vel -= acceleration
            else:
                self.x_vel = -starting_vel

        if keys[pygame.K_d]:
            if self.x_vel >= starting_vel-1:
                self.x_vel += acceleration
            elif self.x_vel < 0:
                self.x_vel += acceleration
            else:
                self.x_vel = starting_vel

        if keys[pygame.K_w]:
            if self.y_vel <= -starting_vel+1:
                self.y_vel -= acceleration
            elif self.y_vel > 0:
                self.y_vel -= acceleration
            else:
                self.y_vel = -starting_vel

        if keys[pygame.K_s]:
            if self.y_vel >= starting_vel-1:
                self.y_vel += acceleration
            elif self.y_vel < 0:
                self.y_vel += acceleration
            else:
                self.y_vel = starting_vel

    def friction_handler(self, friction):
        if self.x_vel > 0:
            if self.x_vel - friction < 0:
                self.x_vel = 0
            else:
                self.x_vel -= friction
        elif self.x_vel < 0:
            if self.x_vel + friction > 0:
                self.x_vel = 0
            else:
                self.x_vel += friction

        if self.y_vel > 0:
            if self.y_vel - friction < 0:
                self.y_vel = 0
            else:
                self.y_vel -= friction
        elif self.y_vel < 0:
            if self.y_vel + friction > 0:
                self.y_vel = 0
            else:
                self.y_vel += friction

        print(f'Y velocity: {self.y_vel}   X velocity: {self.x_vel}')

    def border_collision(self, HEIGHT, WIDTH):
        # TOP
        if self.y < 0:
            self.y_vel = 0
            self.y = 0

        # BOTTOM
        if self.y + self.image.get_height() > HEIGHT:
            self.y_vel = 0
            self.y = HEIGHT - self.image.get_height()

        # LEFT
        if self.x < 0:
            self.x_vel = 0
            self.x = 0

        # RIGHT
        if self.x + self.image.get_width() > WIDTH:
            self.x_vel = 0
            self.x = WIDTH - self.image.get_width()

    def objects_collision(self):
        for world_object in self.world.objects_list:
            # New Collision
            image_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            if image_rect.colliderect(world_object.rectangle):
                self.x_vel *= -1.2
                self.y_vel *= -1.2


            # Old Collision

            # collision = [False, False]
            # obj_left = world_object.rectangle.left
            # obj_right = world_object.rectangle.right
            # obj_top = world_object.rectangle.top
            # obj_bottom = world_object.rectangle.bottom
            #
            # player_collision_points = {}
            # player_collision_points['x'] = [self.x, self.x+self.image.get_width()]
            # player_collision_points['y'] = [self.y, self.y+self.image.get_height()]
            # # print(f'Player: {player_collision_points["x"]}')
            # # print(f'Object: {[obj_left, obj_right]}')
            #
            # for point_x in player_collision_points['x']:
            #     if obj_left < point_x < obj_right:
            #         collision[0] = True
            # for point_y in player_collision_points['y']:
            #     if obj_top < point_y < obj_bottom:
            #         collision[1] = True
            # # print(collision)
            # if collision[0] and collision[1]:
            #     self.x_vel *= -1.2
            #     self.y_vel *= -1.2
            #
            #     # self.x = 400
            #     # self.y = 400
            #     print("collision")


    def movement(self, HEIGHT, WIDTH):
        starting_vel = 3
        acceleration = 0.8
        friction = 0.4

        self.key_handling(starting_vel, acceleration)
        self.friction_handler(friction)

        self.x += self.x_vel
        self.y += self.y_vel

        self.border_collision(HEIGHT, WIDTH)
        self.objects_collision()

class World(object):
    def __init__(self):
        self.objects_list = []

    def construct(self):
        self.add_object(World_object(400, 100, 100, 100))
        self.add_object(World_object(400, 300, 100, 100))
        self.add_object(World_object(400, 500, 100, 100))

    def add_object(self, object):
        self.objects_list.append(object)

    def draw(self, screen):
        for world_object in self.objects_list:
            world_object.draw(screen)

    def load_objects_from_json(self, track_name):
        with open(f'tracks/{track_name}.json', 'r') as track:
            configuration = json.load(track)['objects']
            for world_object_label, world_objects in configuration.items():
                for properties in world_objects:
                    self.add_object(World_object(
                            properties['x'],
                            properties['y'],
                            properties['width'],
                            properties['height']
                        )
                    )


class World_object(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('black'), self.rectangle)


class MainRun(object):
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 800
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.world = World()
        # self.world.construct()
        self.world.load_objects_from_json('track1')

        self.player = Player(0, 0, 30, 30, world=self.world)
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.player.draw(self.screen)
            self.player.movement(self.HEIGHT, self.WIDTH)
            self.world.draw(self.screen)
            self.show_fps()

            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()


a = MainRun()
a.main_loop()

# world = World()
# world.load_objects_from_json('track1')