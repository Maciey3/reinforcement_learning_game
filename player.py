import pygame
from world_object import Start_line, Finish_line


class Player(object):
    def __init__(self, x, y, width, height, world):
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load("images/game_arrow_cut.png"), (width, height))
        self.sprite = self.image.subsurface(self.image.get_rect())
        self.x_vel = 0
        self.y_vel = 0
        self.collision_repair_delay = 300
        self.collision_repaired_time = None
        self.world = world

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        pygame.draw.rect(
            screen,
            pygame.Color('red'),
            pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()),
            2
        )

    def key_handling(self, starting_vel, acceleration, current_time):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)

        if self.collision_repaired_time:
            print(current_time, self.collision_repaired_time)
            if current_time <= self.collision_repaired_time:
                return
            self.collision_repaired_time = None

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

        # print(f'Y velocity: {self.y_vel}   X velocity: {self.x_vel}')

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

    def objects_collision(self, current_time):
        for world_object in self.world.objects_list:
            image_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            if isinstance(world_object, Start_line):
                continue
            elif isinstance(world_object, Finish_line):
                if image_rect.colliderect(world_object.rectangle):
                    self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)
                    print("Finish")

            # New Collision
            else:
                if image_rect.colliderect(world_object.rectangle):
                    print(image_rect.colliderect(world_object.rectangle))
                    if self.collision_repaired_time:
                        self.collision_repaired_time = current_time + self.collision_repair_delay

                    # Have to check where the collision was
                    # and change position +/- 1 or more of the wall
                    # to avoid wall stuck

                    self.x_vel *= 0
                    self.y_vel *= -1.1


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


    def movement(self, HEIGHT, WIDTH, current_time):
        starting_vel = 3
        acceleration = 0.8
        friction = 0.4



        self.key_handling(starting_vel, acceleration, current_time)
        self.friction_handler(friction)

        self.border_collision(HEIGHT, WIDTH)
        self.objects_collision(current_time)

        self.x += self.x_vel
        self.y += self.y_vel


