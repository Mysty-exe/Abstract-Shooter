import pygame
from project.math import Vector


class Character:

    def __init__(self, x, y, width, height, image):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.image = image

        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 180)
        self.vector = Vector(self.x, self.y)

    def draw(self, screen, angle):
        self.update_vector()
        char = pygame.transform.rotate(self.image, angle * -1)
        char_rect = char.get_rect(center=self.image.get_rect(
            center=(self.x, self.y)).center)
        screen.blit(char, char_rect)

    def update_vector(self):
        self.vector.x = self.x
        self.vector.y = self.y


class Player(Character):
    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    def __init__(self):
        Character.__init__(self, 0, 0, 64, 64, 'assets/player.png')
        self.direction = [None, None]
        self.velocity = 5

    def move(self, dt, events):
        for event in events:
            if event == pygame.K_w and self.direction[0] != 'Down':
                self.direction[0] = 'Up'
                self.y -= self.velocity * dt
            if event == pygame.K_s and self.direction[0] != 'Up':
                self.direction[0] = 'Down'
                self.y += self.velocity * dt
            if event == pygame.K_a and self.direction[1] != 'Right':
                self.direction[1] = 'Left'
                self.x -= self.velocity * dt
            if event == pygame.K_d and self.direction[1] != 'Left':
                self.direction[1] = 'Right'
                self.x += self.velocity * dt

    def reset_direction(self, events):
        for key in Player.keys:
            if key not in events:
                self.direction[Player.keys[key][1]] = None

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
