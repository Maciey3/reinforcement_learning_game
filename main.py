import pygame
import json
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython import display
from player import Player
from world import World
from elements.button import Button
from elements.checkbox import Checkbox
from elements.optionbox import OptionBox
from agent import Agent
pygame.init()
pygame.font.init()


class Game(object):
    def __init__(self):
        self.FPS = 60
        self.WIDTH = 800
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.timer = 0

        self.track_name = 1

        self.ai_clicked = 0
        self.ai_train = 0

        self.player_size = 30
        self.clock = pygame.time.Clock()

        self.agent = Agent()
        self.walls_distance_score = 0
        self.finish_line_distance_reward = 0
        self.score = 0
        self.record = 0

    def show_timer(self, time):
        font = pygame.font.SysFont("Arial", 25, bold=True)
        rectangle = pygame.Rect((self.WIDTH-150)//2, self.HEIGHT-50, 150, 50)
        surf = pygame.Surface(rectangle.size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 255, 0, 127), surf.get_rect())
        text_surface = font.render(f'{str(format(round(time/1000, 2), ".2f"))} sec', False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rectangle.center)

        self.screen.blit(surf, rectangle)
        self.screen.blit(text_surface, text_rect)

    def show_fps(self):
        font = pygame.font.SysFont("Arial", 18, bold=True)
        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps, True, pygame.Color("RED"))
        self.screen.blit(fps_t, (5, 5))

    def get_records(self, track_name):
        with open(f'records/records.json', 'r+') as records:
            records_json = json.load(records)
            if track_name in records_json:
                return sorted(records_json[track_name], key=lambda x:float(x))

        with open(f'records/records.json', 'w') as records:
            records_json[track_name] = []
            records.write(json.dumps(records_json, indent=2))
        return sorted(records_json[track_name], key=lambda x:float(x))

    def save_record(self, track_name, time):
        time = str(format(round(time/1000, 2), ".2f"))
        with open(f'records/records.json', 'r+') as records:
            records_json = json.load(records)
            if track_name not in records_json:
                records_json[track_name] = [time]

        with open(f'records/records.json', 'w') as records:
            records_json[track_name].append(time)
            records.write(json.dumps(records_json, indent=2))
        return records_json[track_name]

    def display_records(self, track_name, font):
        for i, record in enumerate(self.get_records(track_name)):
            if i > 9:
                break
            time_surface = font.render(f'{i + 1}. {record}', False, (0, 0, 0))
            time_rect = time_surface.get_rect(center=(self.WIDTH / 2, 400 + i * 40))
            self.screen.blit(time_surface, time_rect)

    def get_game_info(self):
        return np.array([
            self.player.get_nearby_walls_info(self.WIDTH, self.HEIGHT),
            self.player.get_direction_info(),
            self.player.get_finish_info()], dtype=int).flatten()

    def get_tracks_name(self):
        path = './tracks'
        return [x.split('.')[0] for x in next(os.walk(path), (None, None, []))[2]]

    def run(self):
        run = True
        self.world = World()
        self.world.load_objects_from_json(self.track_name)
        self.timer = 0
        self.clock = pygame.time.Clock()
        self.player = Player(
                (self.world.start_line_object.x + self.world.start_line_object.width - self.player_size) // 2,
                (self.world.start_line_object.y + self.world.start_line_object.height - self.player_size) // 2,
                self.player_size,
                self.player_size,
                world=self.world
            )

        if self.ai_train or self.ai_clicked:
            self.FPS = 500


        done = 0
        while run:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                else:
                    keys = None

                if keys:
                    if keys[pygame.K_ESCAPE]:
                        print('Going to menu')
                        self.timer = 0
                        self.FPS = 60
                        self.menu()

                    if keys[pygame.K_r]:
                        print('Reset')
                        self.timer = 0

                if event.type == pygame.QUIT:
                    run = False
                    break

            if self.ai_clicked:
                state_old = self.get_game_info()
                final_move = self.agent.get_action(state_old, load_from_model=not self.ai_train)
                finish_line_distance_reward = self.player.get_finish_line_distance()

            self.world.render(self.screen)
            self.player.render(self.screen)

            if self.ai_clicked:
                self.player.display_collision_lines(self.screen, self.WIDTH, self.HEIGHT)
                collision_type = self.player.movement(self.HEIGHT, self.WIDTH, self.timer, move_list=final_move)
            else:
                collision_type = self.player.movement(self.HEIGHT, self.WIDTH, self.timer)

            if collision_type in [1, 2, 3]:
                # if collision_type == 2 or collision_type == 3:
                #     self.score = finish_line_distance_reward
                # else:
                self.score = 1000 - float(format(round(self.timer/1000, 2), ".2f")) * 2
                    # self.score = finish_line_distance_reward
                done = 1
                if self.ai_clicked:
                    self.agent.n_games += 1

                    self.agent.train_long_memory()
                    print(f'Game: {self.agent.n_games}, score: {self.score}')
                    # if self.ai_train:
                    #     self.agent.plot_scores.append(self.score)
                    #     self.agent.total_score += self.score
                    #     self.agent.plot_mean_scores.append(self.agent.total_score / self.agent.n_games)
                    #     plt.ion()
                    #     self.agent.plot(self.agent.plot_scores, self.agent.plot_mean_scores)



                    if self.score > self.record:
                        self.record = self.score
                        if self.ai_train:
                            self.agent.model.save()

                # self.__init__()
                if self.ai_clicked:
                    self.timer = 0
                    self.run()
                else:
                    self.save_record(self.track_name, self.timer)
                    self.finish(self.timer)

            self.show_timer(self.timer)
            self.show_fps()

            pygame.display.update()
            self.timer += self.clock.tick(self.FPS)

            if self.ai_clicked:
                state_new = self.get_game_info()
                self.agent.train_short_memory(state_old, final_move, finish_line_distance_reward, state_new, done)
                self.agent.remember(state_old, final_move, finish_line_distance_reward, state_new, done)

        pygame.quit()

    def menu(self):
        self.ai_clicked = 0
        self.ai_train = 0

        run = True
        click = False
        header_font = pygame.font.SysFont('Arial', 50, bold=True)
        button_play = Button(self.WIDTH, 300, 250, 70, self.screen, 'Play', center=True)
        # button_options = Button(self.WIDTH, 400, 250, 70, self.screen, 'Options', center=True)
        checkbox_ai = Checkbox(self.screen, 375, 400, 1, caption='AI')
        checkbox_train = Checkbox(self.screen, 375, 440, 1, caption='Train')

        button_optionbox = OptionBox(30, 80, 160, 40, self.screen, (255, 255, 255), (222, 222, 222), self.get_tracks_name(), selected=self.track_name)

        while run:
            self.screen.fill((255, 255, 255))

            header_surface = header_font.render('Menu', False, (0, 0, 0))
            text_rect = header_surface.get_rect(center=(self.WIDTH/2, 100))
            self.screen.blit(header_surface, text_rect)

            self.track_name = button_optionbox.update(click)

            mx, my = pygame.mouse.get_pos()

            button_play.render()
            # button_options.render()
            button_optionbox.render()
            checkbox_ai.render()
            checkbox_train.render()

            if button_play.button.collidepoint((mx, my)):
                if click:
                    # self.__init__()
                    self.run()

            if checkbox_ai.checkbox_obj.collidepoint((mx, my)):
                if click:
                    self.ai_clicked = checkbox_ai.update_checkbox()

            if checkbox_train.checkbox_obj.collidepoint((mx, my)):
                if click:
                    self.ai_train = checkbox_train.update_checkbox()

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

    def finish(self, time):
        run = True
        click = False
        header_font = pygame.font.SysFont('Arial', 50, bold=True)
        time_font = pygame.font.SysFont('Arial', 30, bold=False)

        button_play = Button(130, 250, 250, 70, self.screen, 'Play again', center=False)
        button_menu = Button(430, 250, 250, 70, self.screen, 'Menu', center=False)
        while run:
            self.screen.fill((255, 255, 255))

            header_surface = header_font.render('Your Time', False, (0, 0, 0))
            text_rect = header_surface.get_rect(center=(self.WIDTH/2, 100))
            self.screen.blit(header_surface, text_rect)

            time_surface = time_font.render(f'{round(time/1000, 2)} seconds', False, (0, 0, 0))
            time_rect = time_surface.get_rect(center=(self.WIDTH / 2, 180))
            self.screen.blit(time_surface, time_rect)

            self.display_records(self.track_name ,time_font)

            mx, my = pygame.mouse.get_pos()

            button_play.render()
            button_menu.render()

            if button_play.button.collidepoint((mx, my)):
                if click:
                    # self.__init__()
                    self.run()

            if button_menu.button.collidepoint((mx, my)):
                if click:
                    # self.__init__()
                    self.menu()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                else:
                    keys = None

                if keys:
                    if keys[pygame.K_ESCAPE]:
                        self.menu()

                    if keys[pygame.K_r]:
                        self.timer = 0
                        self.run(self.track_name)

                if event.type == pygame.QUIT:
                    run = False
                    break

            self.clock.tick(self.FPS)
            pygame.display.update()
        pygame.quit()

game = Game()
game.menu()
# game.menu()