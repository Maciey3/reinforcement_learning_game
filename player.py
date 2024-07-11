import pygame
from world_object import Start_line, Finish_line, World_object


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

    def get_direction_info(self):
        # return [self.y_vel < 0, self.x_vel > 0, self.y_vel > 0, self.x_vel < 0]
        return self.y_vel < 0, self.x_vel > 0, self.y_vel > 0, self.x_vel < 0

    def get_finish_info(self):
        for world_object in self.world.objects_list:
            if isinstance(world_object, Finish_line):
                finish_x = world_object.x
                finish_y = world_object.y
                finish_width = world_object.width
                finish_height = world_object.height

        player_x = self.x+(self.width//2)
        player_y = self.y+(self.height//2)
        # print(self.x+(self.width//2))
        # print(self.y+(self.height//2))
        # return [player_y > finish_y+finish_height, player_x < finish_x, player_y < finish_y, player_x > finish_x + finish_width]
        return player_y > finish_y+finish_height, player_x < finish_x, player_y < finish_y, player_x > finish_x + finish_width


    def get_nearby_walls_info(self, WIDTH, HEIGHT):
        max_size = 100
        collision = [[], [], [], []]

        markerT = pygame.Rect(self.x + self.width // 2, self.y - max_size + self.height // 2, 2, max_size)
        markerR = pygame.Rect(self.x + self.width // 2, self.y + self.height // 2, max_size, 2)
        markerB = pygame.Rect(self.x + self.width // 2, self.y + self.height // 2, 2, max_size)
        markerL = pygame.Rect(self.x - max_size + self.width // 2, self.y + self.height // 2, max_size, 2)

        if markerT.top < 0:
            collision[0] = [0, self.y + self.height // 2]
        if markerR.right > WIDTH:
            collision[1] = [self.x + self.width // 2, WIDTH - (self.x + self.width // 2)]
        if markerB.bottom > HEIGHT:
            collision[2] = [self.y + self.height // 2, HEIGHT - (self.y + self.height // 2)]
        if markerL.left < 0:
            collision[3] = [0, self.x + self.width // 2]

        for world_object in self.world.objects_list:
            if isinstance(world_object, World_object):
                if world_object.rectangle.colliderect(markerT):
                    height = (self.y + self.height // 2) - (world_object.y + world_object.height)
                    collision[0] = [world_object.y + world_object.height, height]
                if world_object.rectangle.colliderect(markerR):
                    width = world_object.x - (self.x + self.width // 2)
                    collision[1] = [self.x + self.width // 2, width]
                if world_object.rectangle.colliderect(markerB):
                    height = world_object.y - (self.y + self.height // 2)
                    collision[2] = [self.y + self.height // 2, height]
                if world_object.rectangle.colliderect(markerL):
                    width = (self.x + self.width // 2) - (world_object.x + world_object.width)
                    collision[3] = [world_object.x + world_object.width, width]
        # return [bool(collision[0]), bool(collision[1]), bool(collision[2]), bool(collision[3])]
        return bool(collision[0]), bool(collision[1]), bool(collision[2]), bool(collision[3])

    def get_finish_line_distance(self):
        for world_object in self.world.objects_list:
            if isinstance(world_object, Finish_line):
                finish_x = world_object.x
                finish_y = world_object.y
                finish_width = world_object.width
                finish_height = world_object.height

        return 1037 - pygame.math.Vector2(self.x, self.y).distance_to((finish_x, finish_y))

    def key_handling(self, starting_vel, acceleration, current_time, move_list):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)

        if self.collision_repaired_time:
            # print(current_time, self.collision_repaired_time)
            if current_time <= self.collision_repaired_time:
                return
            self.collision_repaired_time = None

        if keys[pygame.K_a] or move_list[3]:
            if self.x_vel <= -starting_vel+1:
                self.x_vel -= acceleration
            elif self.x_vel > 0:
                self.x_vel -= acceleration
            else:
                self.x_vel = -starting_vel

        if keys[pygame.K_d] or move_list[1]:
            if self.x_vel >= starting_vel-1:
                self.x_vel += acceleration
            elif self.x_vel < 0:
                self.x_vel += acceleration
            else:
                self.x_vel = starting_vel

        if keys[pygame.K_w] or move_list[0]:
            if self.y_vel <= -starting_vel+1:
                self.y_vel -= acceleration
            elif self.y_vel > 0:
                self.y_vel -= acceleration
            else:
                self.y_vel = -starting_vel

        if keys[pygame.K_s] or move_list[2]:
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
            return 3

        # BOTTOM
        if self.y + self.image.get_height() > HEIGHT:
            self.y_vel = 0
            self.y = HEIGHT - self.image.get_height()
            return 3

        # LEFT
        if self.x < 0:
            self.x_vel = 0
            self.x = 0
            return 3

        # RIGHT
        if self.x + self.image.get_width() > WIDTH:
            self.x_vel = 0
            self.x = WIDTH - self.image.get_width()
            return 3

    def objects_collision(self, current_time):
        for world_object in self.world.objects_list:
            image_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            if isinstance(world_object, Start_line):
                continue
            elif isinstance(world_object, Finish_line):
                if image_rect.colliderect(world_object.rectangle):
                    self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)
                    print("Finish")
                    return 1

            # New Collision
            else:
                if image_rect.colliderect(world_object.rectangle):
                    # print(image_rect.colliderect(world_object.rectangle))
                    if not self.collision_repaired_time:
                        self.collision_repaired_time = current_time + self.collision_repair_delay

                    overlap_left = image_rect.right - world_object.rectangle.left
                    overlap_right = world_object.rectangle.right - image_rect.left
                    overlap_top = image_rect.bottom - world_object.rectangle.top
                    overlap_bottom = world_object.rectangle.bottom - image_rect.top

                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    if min_overlap == overlap_left:
                        # print("Collision on left side")
                        self.x = world_object.rectangle.left - self.width
                        self.x_vel *= -0.8
                        return 2
                    elif min_overlap == overlap_right:
                        # print("Collision on right side")
                        self.x = world_object.rectangle.right
                        self.x_vel *= -0.8
                        return 2
                    elif min_overlap == overlap_top:
                        # print("Collision on top side")
                        self.y = world_object.rectangle.top - self.height
                        self.y_vel *= -0.8
                        return 2
                    elif min_overlap == overlap_bottom:
                        # print("Collision on bottom side")
                        self.y = world_object.rectangle.bottom
                        self.y_vel *= -0.8
                        return 2

                    # Have to check where the collision was
                    # and change position +/- 1 or more of the wall
                    # to avoid wall stuck

                    # self.x_vel *= 0
                    # self.y_vel *= 0

    def display_collision_lines(self, screen, WIDTH, HEIGHT):
        max_size = 100
        collision = [[], [], [], []]

        markerT = pygame.Rect(self.x+self.width//2, self.y-max_size+self.height//2, 2, max_size)
        markerR = pygame.Rect(self.x + self.width // 2, self.y + self.height // 2, max_size, 2)
        markerB = pygame.Rect(self.x + self.width // 2, self.y + self.height // 2, 2, max_size)
        markerL = pygame.Rect(self.x - max_size + self.width // 2, self.y + self.height // 2, max_size, 2)

        if markerT.top < 0:
            collision[0] = [0, self.y + self.height // 2]
        if markerR.right > WIDTH:
            collision[1] = [self.x + self.width // 2, WIDTH - (self.x + self.width // 2)]
        if markerB.bottom > HEIGHT:
            collision[2] = [self.y + self.height // 2, HEIGHT - (self.y + self.height // 2)]
        if markerL.left < 0:
            collision[3] = [0, self.x + self.width // 2]


        for world_object in self.world.objects_list:
            if isinstance(world_object, World_object):
                if world_object.rectangle.colliderect(markerT):
                    height = (self.y + self.height // 2) - (world_object.y + world_object.height)
                    collision[0] = [world_object.y + world_object.height, height]
                if world_object.rectangle.colliderect(markerR):
                    width = world_object.x - (self.x + self.width // 2)
                    collision[1] = [self.x + self.width // 2, width]
                if world_object.rectangle.colliderect(markerB):
                    height = world_object.y - (self.y + self.height // 2)
                    collision[2] = [self.y + self.height // 2, height]
                if world_object.rectangle.colliderect(markerL):
                    width = (self.x + self.width // 2) - (world_object.x + world_object.width)
                    collision[3] = [world_object.x + world_object.width, width]



        if collision[0]:
            markerT = pygame.Rect(self.x + self.width // 2, collision[0][0], 2, collision[0][1])
            pygame.draw.rect(screen, pygame.Color('red'), markerT)
        else:
            pygame.draw.rect(screen, pygame.Color('green'), markerT)

        if collision[1]:
            markerR = pygame.Rect(collision[1][0], self.y + self.height // 2, collision[1][1], 2)
            pygame.draw.rect(screen, pygame.Color('red'), markerR)
        else:
            pygame.draw.rect(screen, pygame.Color('green'), markerR)

        if collision[2]:
            markerB = pygame.Rect(self.x + self.width // 2, collision[2][0], 2, collision[2][1])
            pygame.draw.rect(screen, pygame.Color('red'), markerB)
        else:
            pygame.draw.rect(screen, pygame.Color('green'), markerB)

        if collision[3]:
            markerL = pygame.Rect(collision[3][0], self.y + self.height // 2, collision[3][1], 2)
            pygame.draw.rect(screen, pygame.Color('red'), markerL)
        else:
            pygame.draw.rect(screen, pygame.Color('green'), markerL)




    def movement(self, HEIGHT, WIDTH, current_time, move_list=[0, 0, 0, 0]):
        starting_vel = 3
        acceleration = 0.8
        friction = 0.4


        self.key_handling(starting_vel, acceleration, current_time, move_list)

        self.friction_handler(friction)

        border_collision = self.border_collision(HEIGHT, WIDTH)
        object_collision = self.objects_collision(current_time)

        if object_collision == 1:
            return 1

        self.x += self.x_vel
        self.y += self.y_vel

        # if object_collision == 2:
        #     self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)
        #     # print(collision_type)
        #     return 2
        #
        # if border_collision == 3:
        #     self.__init__(self.starting_x, self.starting_y, self.width, self.height, self.world)
        #     # print(collision_type)
        #     return 3

