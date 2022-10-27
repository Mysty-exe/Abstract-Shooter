import pygame
import project.characters as characters
from project.math import Vector


class KeyboardInput:

    def __init__(self):
        self.events_queue = []

    def process_events(self, events):
        for event in characters.Player.keys:
            if events[event]:
                self.events_queue.append(event)

        return self.events_queue

    def empty_queue(self):
        self.events_queue.clear()


class MouseInput:

    def __init__(self):
        self.coords = []
        self.button_pressed = False

    @classmethod
    def check_quit(cls, events, state):
        for event in events:
            if event.type == pygame.QUIT:
                state = 'Quit'
        return state

    def process_events(self, pressed, coords):
        mouse_Vector = Vector(coords[0], coords[1])
        self.coords.append(mouse_Vector)
        if pressed:
            self.button_pressed = mouse_Vector
        else:
            self.button_pressed = False

        return mouse_Vector
