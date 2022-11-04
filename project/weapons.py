import pygame
from project.math import Vector


class Bullet:
    bullets = []

    def __init__(self, x, y, radius, direction, speed):
        self.pos = Vector(x, y)
        self.radius = radius
        self.direction = direction
        self.speed = speed

    @classmethod
    def draw(cls, screen, dt, scroll):
        for bullet in cls.bullets:
            bullet.pos += bullet.direction * bullet.speed * dt
            bullet.pos.x = round(bullet.pos.x)
            bullet.pos.y = round(bullet.pos.y)

            if bullet.pos.x + scroll[0] <= 0 or bullet.pos.x + scroll[
                    0] >= 2000:
                cls.bullets.remove(bullet)
                continue
            if bullet.pos.y + scroll[1] <= 0 or bullet.pos.y + scroll[
                    1] >= 2000:
                cls.bullets.remove(bullet)
                continue

            pygame.draw.circle(screen, (255, 255, 255),
                               (bullet.pos.x, bullet.pos.y), bullet.radius)


class Gun:

    def __init__(self, radius, speed, trigger_time):
        self.radius = radius
        self.speed = speed
        self.trigger_time = trigger_time

    def add_bullet(self, x, y, direction):
        Bullet.bullets.append(Bullet(x, y, self.radius, direction, self.speed))

    def reload(self):
        if self.trigger_time > 0:
            self.trigger_time -= 1


class Pistol(Gun):

    def __init__(self):
        self.max_trigger = 60
        radius = 5
        speed = 5
        trigger_time = 0
        Gun.__init__(self, radius, speed, trigger_time)


class SubMachine(Gun):

    def __init__(self):
        self.max_trigger = 10
        radius = 5
        speed = 15
        trigger_time = 0
        Gun.__init__(self, radius, speed, trigger_time)


class AssaultRifle(Gun):

    def __init__(self):
        self.max_trigger = 15
        radius = 5
        speed = 10
        trigger_time = 0
        Gun.__init__(self, radius, speed, trigger_time)


class MiniGun(Gun):

    def __init__(self):
        self.max_trigger = 5
        radius = 5
        speed = 15
        trigger_time = 0
        Gun.__init__(self, radius, speed, trigger_time)


class Sniper(Gun):

    def __init__(self):
        self.max_trigger = 180
        radius = 5
        speed = 30
        trigger_time = 0
        Gun.__init__(self, radius, speed, trigger_time)


class Shotgun(Gun):

    def __init__(self):
        pass
