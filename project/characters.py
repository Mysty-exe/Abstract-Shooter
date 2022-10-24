import pygame
import project.constants as constants

class Character:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw(self, screen):
        pygame.draw.rect(screen, constants.COLOURS['black'], (self.x, self.y, self.width, self.height))

class Player( Character ):
    keys = {pygame.K_w: ('Up', 0), pygame.K_s: ('Down', 0), pygame.K_a: ('Left', 1), pygame.K_d: ('Right', 1)}

    def __init__(self):
        Character.__init__(self, 150, 150, 50, 50)
        self.direction = [None, None]
        self.speed = 5

    def move(self, events):
        for event in events:
            if event == pygame.K_w and self.direction[0] != 'Down':
                self.direction[0] = 'Up'
                self.y -= self.speed
            if event == pygame.K_s and self.direction[0] != 'Up':
                self.direction[0] = 'Down'
                self.y += self.speed
            if event == pygame.K_a and self.direction[1] != 'Right':
                self.direction[1] = 'Left'
                self.x -= self.speed
            if event == pygame.K_d and self.direction[1] != 'Left':
                self.direction[1] = 'Right'
                self.x += self.speed

    def reset_direction(self, events):
        for key in Player.keys:
            if key not in events:
                self.direction[Player.keys[key][1]] = None
