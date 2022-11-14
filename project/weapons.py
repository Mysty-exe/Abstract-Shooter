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
            # bullet.pos.x = round(bullet.pos.x)
            # bullet.pos.y = round(bullet.pos.y)

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
            x, y = bullet[1].pos.x, bullet[1].pos.y
            screen.blit(bullet[1].explode[bullet[0] + 1], (x - scroll[0] - 50, y - scroll[1] - 50))
            bullet[0] += 1
            if bullet[0] == 14:
                cls.bullets_exploding.remove(bullet)


class Gun:

    guns = []

    def __init__(self, name, image, radius, speed, cooldown, ammo):
        self.name = name
        self.image = image
        self.radius = radius
        self.speed = speed
        self.cooldown = cooldown
        self.ammo = ammo
        self.double = False
        self.reloading = False

    def add_bullet(self, x, y, mouse, player):
        angle = mouse
        angle2 = mouse.rotate(Vector(player.x, player.y), 25)
        angle3 = mouse.rotate(Vector(player.x, player.y), -25)

        direction = (angle - player)
        Bullet.bullets.append(
            Bullet(x, y, self.radius, direction.normalize(), self.speed))

        if self.name == 'Shotgun':

            direction2 = (angle2 - player)
            direction3 = (angle3 - player)
            Bullet.bullets.append(
                Bullet(x, y, self.radius, direction2.normalize(), self.speed))
            Bullet.bullets.append(
                Bullet(x, y, self.radius, direction3.normalize(), self.speed))

    def reload(self, reload, trigger, ammo):
        if trigger > 0:
            trigger -= 1

        if self.cooldown == 0:
            self.cooldown = reload
            self.ammo = ammo
            self.reloading = False

        if self.reloading:
            self.cooldown -= 1

        if self.ammo == 0:
            self.reloading = True

        return trigger

    @classmethod
    def random(cls):
        import random
        weight = [30, 20, 15, 5, 10, 20]
        return random.choices(cls.guns, k=1, weights=weight)[0]


class Pistol(Gun):

    def __init__(self):
        self.reload_time = 3 * 60
        self.max_trigger = 60
        self.max_ammo = 16
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Pistol'
        image = pygame.image.load('assets/guns/pistol.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 5
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)


class SubMachine(Gun):

    def __init__(self):
        self.reload_time = 5 * 60
        self.max_trigger = 10
        self.max_ammo = 48
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'SubMachine Gun'
        image = pygame.image.load('assets/guns/submachine.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 15
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)


class AssaultRifle(Gun):

    def __init__(self):
        self.reload_time = 5 * 60
        self.max_trigger = 15
        self.max_ammo = 84
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Assault Rifle'
        image = pygame.image.load('assets/guns/rifle.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 10
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)


class MiniGun(Gun):

    def __init__(self):
        self.reload_time = 10 * 60
        self.max_trigger = 5
        self.max_ammo = 212
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'MiniGun'
        image = pygame.image.load('assets/guns/minigun.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 15
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)


class Sniper(Gun):

    def __init__(self):
        self.reload_time = 15 * 60
        self.max_trigger = 180
        self.max_ammo = 12
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Sniper'
        image = pygame.image.load('assets/guns/sniper.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 30
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)


class Shotgun(Gun):

    def __init__(self):
        self.reload_time = 3 * 60
        self.max_trigger = 20
        self.max_ammo = 6
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Shotgun'
        image = pygame.image.load('assets/guns/shotgun.png').convert_alpha()
        image = pygame.transform.scale(image, (128, 128))
        ammo = self.max_ammo
        radius = 5
        speed = 5
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo)
