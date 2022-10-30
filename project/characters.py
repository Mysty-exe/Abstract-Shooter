import pygame
from project.math import Vector
# https://www.youtube.com/watch?v=qJq7I2DLGzI


class Character:

    def __init__(self, x, y, width, height, image):
        self.vector = Vector(x, y)
        self.width, self.height = width, height

        self.image = image
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 180)

    def draw(self, screen, angle):
        char = pygame.transform.rotate(self.image, angle * -1)
        char_rect = char.get_rect(center=(self.image.get_rect(
            center=(self.vector.x, self.vector.y)).center))
        screen.blit(char, char_rect)


class Player(Character):
    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    def __init__(self, gun):
        Character.__init__(self, 100, 100, 64, 64, 'assets/player.png')
        self.gun = gun
        self.direction = [None, None]
        self.velx = 0
        self.vely = 0

    def approach(self):
        pass

    def process_keys(self, events):
        if events[pygame.K_w] and self.direction[0] != 'Down':
            self.direction[0] = 'Up'
            self.vely = -5

        if events[pygame.K_s] and self.direction[0] != 'Up':
            self.direction[0] = 'Down'
            self.vely = 5

        if events[pygame.K_a] and self.direction[1] != 'Right':
            self.direction[1] = 'Left'
            self.velx = -5

        if events[pygame.K_d] and self.direction[1] != 'Left':
            self.direction[1] = 'Right'
            self.velx = 5

        if not events[pygame.K_w] and not events[pygame.K_s]:
            self.direction[0] = None
            self.vely = 0

        if not events[pygame.K_d] and not events[pygame.K_a]:
            self.direction[1] = None
            self.velx = 0

    def move(self, dt):
        self.vector.x += self.velx * dt
        self.vector.y += self.vely * dt
        print(self.velx, self.vely, self.direction)

    def shoot(self, mouseInput, mouseCoord, angle):
        self.gun.reload()
        if mouseInput != False and self.gun.reload_time == 0:
            direction = (mouseCoord - self.vector)
            self.gun.add_bullet(self.vector.x, self.vector.y,
                                direction.normalize(), angle)
            self.gun.reload_time = self.gun.max_reload

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
