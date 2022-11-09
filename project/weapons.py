import pygame
from project.math import Vector


class Bullet:
    bullets = []
    bullets_exploding = []

    def __init__(self, x, y, radius, direction, speed):
        self.pos = Vector(x, y)
        self.radius = radius
        self.direction = direction
        self.speed = speed

        self.explode = {
            1:
            pygame.image.load('assets/bullet_explosion/1.png').convert_alpha(),
            2:
            pygame.image.load('assets/bullet_explosion/2.png').convert_alpha(),
            3:
            pygame.image.load('assets/bullet_explosion/3.png').convert_alpha(),
            4:
            pygame.image.load('assets/bullet_explosion/4.png').convert_alpha(),
            5:
            pygame.image.load('assets/bullet_explosion/5.png').convert_alpha(),
            6:
            pygame.image.load('assets/bullet_explosion/6.png').convert_alpha(),
            7:
            pygame.image.load('assets/bullet_explosion/7.png').convert_alpha(),
            8:
            pygame.image.load('assets/bullet_explosion/8.png').convert_alpha(),
            9:
            pygame.image.load('assets/bullet_explosion/9.png').convert_alpha(),
            10: pygame.image.load(
                'assets/bullet_explosion/10.png').convert_alpha(),
            11: pygame.image.load(
                'assets/bullet_explosion/10.png').convert_alpha(),
            12: pygame.image.load(
                'assets/bullet_explosion/10.png').convert_alpha(),
            13: pygame.image.load(
                'assets/bullet_explosion/10.png').convert_alpha(),
            14: pygame.image.load(
                'assets/bullet_explosion/10.png').convert_alpha()
        }

    @classmethod
    def draw(cls, screen, dt, scroll):
        for bullet in cls.bullets:
            bullet.pos += bullet.direction * bullet.speed * dt
            bullet.pos.x = round(bullet.pos.x)
            bullet.pos.y = round(bullet.pos.y)

            if bullet.pos.x <= 0 or bullet.pos.x >= 2000:
                cls.bullets_exploding.append([0, bullet])
                cls.bullets.remove(bullet)
                continue

            if bullet.pos.y <= 0 or bullet.pos.y >= 2000:
                cls.bullets_exploding.append([0, bullet])
                cls.bullets.remove(bullet)
                continue

            pygame.draw.circle(
                screen, (255, 255, 255),
                (bullet.pos.x - scroll[0], bullet.pos.y - scroll[1]),
                bullet.radius)

    @classmethod
    def explode_bullets(cls, screen, scroll):
        for bullet in cls.bullets_exploding:
            screen.blit(bullet[1].explode[bullet[0] + 1],
                        (bullet[1].pos.x - scroll[0] - 50,
                         bullet[1].pos.y - scroll[1] - 50))
            bullet[0] += 1
            if bullet[0] == 14:
                cls.bullets_exploding.remove(bullet)


class Gun:

    guns = []

    def __init__(self, gun, radius, speed, trigger_time):
        self.gun = gun
        self.radius = radius
        self.speed = speed
        self.trigger_time = trigger_time

    def add_bullet(self, x, y, direction):
        Bullet.bullets.append(Bullet(x, y, self.radius, direction, self.speed))

    def reload(self):
        if self.trigger_time > 0:
            self.trigger_time -= 1

    @classmethod
    def random(cls):
        import random
        return random.choice(cls.guns)


class Pistol(Gun):

    def __init__(self):
        self.max_trigger = 60
        gun = pygame.image.load('assets/guns/pistol.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        radius = 5
        speed = 5
        trigger_time = 0
        Gun.__init__(self, gun, radius, speed, trigger_time)


class SubMachine(Gun):

    def __init__(self):
        self.max_trigger = 10
        gun = pygame.image.load('assets/guns/submachine.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        radius = 5
        speed = 15
        trigger_time = 0
        Gun.__init__(self, gun, radius, speed, trigger_time)


class AssaultRifle(Gun):

    def __init__(self):
        self.max_trigger = 15
        gun = pygame.image.load('assets/guns/ak47.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        radius = 5
        speed = 10
        trigger_time = 0
        Gun.__init__(self, gun, radius, speed, trigger_time)


class MiniGun(Gun):

    def __init__(self):
        self.max_trigger = 5
        gun = pygame.image.load('assets/guns/minigun.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        radius = 5
        speed = 15
        trigger_time = 0
        Gun.__init__(self, gun, radius, speed, trigger_time)


class Sniper(Gun):

    def __init__(self):
        self.max_trigger = 180
        gun = pygame.image.load('assets/guns/sniper.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        radius = 5
        speed = 30
        trigger_time = 0
        Gun.__init__(self, gun, radius, speed, trigger_time)


class Shotgun(Gun):

    def __init__(self):
        gun = pygame.image.load('assets/guns/pistol.png').convert_alpha()
        gun = pygame.transform.scale(gun, (128, 128))
        print(gun)
