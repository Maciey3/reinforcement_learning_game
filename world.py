import pygame
import json
from world_object import World_object, Start_line, Finish_line



class World(object):
    def __init__(self):
        self.objects_list = []
    #   We need to take informations about start to place player in a middle of a start line

    def construct(self):
        # Useless in current form
        self.add_object(World_object(400, 100, 100, 100))
        self.add_object(World_object(400, 300, 100, 100))
        self.add_object(World_object(400, 500, 100, 100))

    def add_object(self, object):
        self.objects_list.append(object)

    def render(self, screen):
        for world_object in self.objects_list:
            world_object.draw(screen)

    def load_objects_from_json(self, track_name):
        with open(f'tracks/{track_name}.json', 'r') as track:
            configuration = json.load(track)['objects']
            for world_object_label, world_objects in configuration.items():
                # Change that because that looks awful
                if world_object_label == "start":
                    self.add_object(Start_line(
                            world_objects['x'],
                            world_objects['y'],
                            world_objects['width'],
                            world_objects['height']
                        )
                    )
                elif world_object_label == "finish":
                    self.add_object(Finish_line(
                            world_objects['x'],
                            world_objects['y'],
                            world_objects['width'],
                            world_objects['height']
                        )
                    )
                else:
                    for properties in world_objects:
                        self.add_object(World_object(
                                properties['x'],
                                properties['y'],
                                properties['width'],
                                properties['height']
                            )
                        )
