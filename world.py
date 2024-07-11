import pygame
import json
from world_object import World_object, Start_line, Finish_line


class World(object):
    def __init__(self):
        self.objects_list = []
        self.start_line_object = None

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
                if world_object_label == "start":
                    start_line = self.create_start_instance(world_objects)
                    self.add_object(start_line)
                    self.start_line_object = start_line

                elif world_object_label == "finish":
                    self.add_object(self.create_finish_instance(world_objects))

                else:
                    for properties in world_objects:
                        self.add_object(self.create_world_object_instance(properties))

    def create_start_instance(self, start_line_properties):
        return Start_line(
            start_line_properties['x'],
            start_line_properties['y'],
            start_line_properties['width'],
            start_line_properties['height']
        )

    def create_finish_instance(self, finish_line_properties):
        return Finish_line(
            finish_line_properties['x'],
            finish_line_properties['y'],
            finish_line_properties['width'],
            finish_line_properties['height']
        )

    def create_world_object_instance(self, world_object_properties):
        return World_object(
            world_object_properties['x'],
            world_object_properties['y'],
            world_object_properties['width'],
            world_object_properties['height']
        )