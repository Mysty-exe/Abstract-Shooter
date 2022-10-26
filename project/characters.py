import pygame
import project.constants as constants
from project.math import Vector

class Character:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.vector = Vector(self.x + (self.width / 2), self.y + (self.height / 2))

    def draw(self, screen):
        self.update_vector()
        pygame.draw.rect(screen, constants.COLOURS['black'], (self.x, self.y, self.width, self.height))

    def update_vector(self):
        self.vector.x = self.x + (self.width / 2)
        self.vector.y = self.y + (self.height / 2)

class Player( Character ):
    keys = {pygame.K_w: ('Up', 0), pygame.K_s: ('Down', 0), pygame.K_a: ('Left', 1), pygame.K_d: ('Right', 1)}

    def __init__(self):
        Character.__init__(self, 0, 0, 50, 50)
        self.direction = [None, None]
        self.velocity = 5

    def move(self, events):
        for event in events:
            if event == pygame.K_w and self.direction[0] != 'Down':
                self.direction[0] = 'Up'
                self.y -= self.velocity
            if event == pygame.K_s and self.direction[0] != 'Up':
                self.direction[0] = 'Down'
                self.y += self.velocity
            if event == pygame.K_a and self.direction[1] != 'Right':
                self.direction[1] = 'Left'
                self.x -= self.velocity
            if event == pygame.K_d and self.direction[1] != 'Left':
                self.direction[1] = 'Right'
                self.x += self.velocity

    def reset_direction(self, events):
        for key in Player.keys:
            if key not in events:
                self.direction[Player.keys[key][1]] = None

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
