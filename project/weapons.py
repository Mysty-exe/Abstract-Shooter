import pygame
from project.math import Vector


class Bullet:
    bullets = []

    def __init__(self, x, y, width, height, direction, angle, speed):
        self.x, self.y = x, y
        self.pos = Vector(self.x, self.y)
        self.width, self.height = width, height
        self.direction = direction
        self.speed = speed
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, angle * -1)

    @classmethod
    def draw(cls, screen, dt):
        for bullet in cls.bullets:
            bullet.pos += bullet.direction * bullet.speed * dt
            bullet.x = round(bullet.pos.x)
            bullet.y = round(bullet.pos.y)
            b = bullet.image.get_rect(center=bullet.image.get_rect(
                center=(bullet.x, bullet.y)).center)
            screen.blit(bullet.image, b)


class Gun:

    def __init__(self,
                 bullet_width,
                 bullet_height,
                 speed,
                 trigger_time,
                 guns=1):
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.speed = speed
        self.trigger_time = trigger_time
        self.guns = guns

    def add_bullet(self, x, y, direction, angle):
        Bullet.bullets.append(
            Bullet(x, y, self.bullet_width, self.bullet_height, direction,
                   angle, self.speed))

    def reload(self):
        if self.trigger_time > 0:
            self.trigger_time -= 1


class Pistol(Gun):

    def __init__(self):
        self.max_trigger = 60
        width = 15
        height = 10
        speed = 15
        trigger_time = 0
        Gun.__init__(self, width, height, speed, trigger_time)


class SubMachine(Gun):

    def __init__(self):
        self.max_trigger = 10
        width = 15
        height = 5
        speed = 15
        trigger_time = 0
        Gun.__init__(self, width, height, speed, trigger_time)


class AssaultRifle(Gun):

    def __init__(self):
        self.max_trigger = 15
        width = 20
        height = 10
        speed = 10
        trigger_time = 0
        Gun.__init__(self, width, height, speed, trigger_time)


class MiniGun(Gun):

    def __init__(self):
        self.max_trigger = 5
        width = 15
        height = 10
        speed = 15
        trigger_time = 0
        Gun.__init__(self, width, height, speed, trigger_time)


class Sniper(Gun):

    def __init__(self):
        self.max_trigger = 180
        width = 30
        height = 10
        speed = 30
        trigger_time = 0
        Gun.__init__(self, width, height, speed, trigger_time)


class Shotgun(Gun):

    def __init__(self):
        pass
