import pygame
from project.math import Vector
import project.constants as constants
import itertools


class Bullet:
    enemy_bullets = []
    player_bullets = []
    bullets_exploding = []

    def __init__(self, x, y, radius, direction, speed, color, type):
        self.pos = Vector(x, y)
        self.radius = radius
        self.direction = direction
        self.speed = speed
        self.color = color
        self.type = type

        if self.type == 'Player':
            Bullet.player_bullets.append(self)
        elif self.type == 'Enemy':
            Bullet.enemy_bullets.append(self)

        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.fill(constants.COLOURS['white'])
        self.surf.set_colorkey(constants.COLOURS['white'])

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
                'assets/bullet_explosion/11.png').convert_alpha(),
            12: pygame.image.load(
                'assets/bullet_explosion/12.png').convert_alpha(),
            13: pygame.image.load(
                'assets/bullet_explosion/13.png').convert_alpha(),
            14: pygame.image.load(
                'assets/bullet_explosion/14.png').convert_alpha()
        }

    @classmethod
    def draw(cls, screen, dt, scroll, boundary):
        for bullet in itertools.chain(cls.enemy_bullets, cls.player_bullets):
            bullet.pos += bullet.direction * bullet.speed * dt
            # bullet.pos.x = round(bullet.pos.x)
            # bullet.pos.y = round(bullet.pos.y)

            if bullet.pos.x <= 0 or bullet.pos.x >= boundary or bullet.pos.y <= 0 or bullet.pos.y >= boundary:
                cls.bullets_exploding.append([0, bullet])
                if bullet.type == 'Player':
                    cls.player_bullets.remove(bullet)
                elif bullet.type == 'Enemy':
                    cls.enemy_bullets.remove(bullet)
                continue

            pygame.draw.circle(bullet.surf, bullet.color,
                               (bullet.radius, bullet.radius), bullet.radius)

            screen.blit(bullet.surf,
                        (bullet.pos.x - scroll[0], bullet.pos.y - scroll[1]))

    @classmethod
    def explode_bullets(cls, screen, scroll):
        for bullet in cls.bullets_exploding:
            x, y = bullet[1].pos.x, bullet[1].pos.y
            screen.blit(bullet[1].explode[bullet[0] + 1],
                        (x - scroll[0] - 50, y - scroll[1] - 50))
            bullet[0] += 1
            if bullet[0] == 14:
                cls.bullets_exploding.remove(bullet)


class Gun:

    guns = []

    def __init__(self, name, image, radius, speed, cooldown, ammo, color):
        self.name = name
        self.image = image
        self.radius = radius
        self.speed = speed
        self.cooldown = cooldown
        self.ammo = ammo
        self.color = color
        self.double = False
        self.reloading = False

    def add_bullet(self, x, y, mouse, player, color, type, enemy=None):
        x, y = x - self.radius, y - self.radius
        if type != 'Enemy':
            direction = (mouse - player)
        else:
            direction = (player - enemy)

        Bullet(x, y, self.radius, direction.normalize(), self.speed, color,
               type)

        if self.name == 'Shotgun':
            if type != 'Enemy':
                angle2 = mouse.rotate(Vector(player.x, player.y), 25)
                angle3 = mouse.rotate(Vector(player.x, player.y), -25)
                direction2 = (angle2 - player)
                direction3 = (angle3 - player)

            else:
                angle2 = player.rotate(Vector(x, y), 25)
                angle3 = player.rotate(Vector(x, y), -25)
                direction2 = (angle2 - Vector(x, y))
                direction3 = (angle3 - Vector(x, y))

            Bullet(x, y, self.radius, direction2.normalize(), self.speed,
                   color, type)
            Bullet(x, y, self.radius, direction3.normalize(), self.speed,
                   color, type)

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
    def random(cls, difficulty):
        import random

        cls.guns = [
            Pistol(),
            SubMachine(),
            AssaultRifle(),
            MiniGun(),
            Sniper(),
            Shotgun()
        ]

        weight = constants.DIFFICULTY[difficulty][3]
        gun = random.choices(cls.guns, k=1, weights=weight)[0]
        return gun


class Pistol(Gun):

    def __init__(self):
        self.reload_time = 3 * 60
        self.max_trigger = 120
        self.max_ammo = 16
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Pistol'
        image = pygame.image.load('assets/guns/pistol.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 8
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['light grey'])


class SubMachine(Gun):

    def __init__(self):
        self.reload_time = 5 * 60
        self.max_trigger = 30
        self.max_ammo = 48
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'SubMachine Gun'
        image = pygame.image.load('assets/guns/submachine.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 12
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['lime'])


class AssaultRifle(Gun):

    def __init__(self):
        self.reload_time = 5 * 60
        self.max_trigger = 45
        self.max_ammo = 84
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Assault Rifle'
        image = pygame.image.load('assets/guns/rifle.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 10
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['light blue'])


class MiniGun(Gun):

    def __init__(self):
        self.reload_time = 10 * 60
        self.max_trigger = 20
        self.max_ammo = 212
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'MiniGun'
        image = pygame.image.load('assets/guns/minigun.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 12
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['red2'])


class Sniper(Gun):

    def __init__(self):
        self.reload_time = 15 * 60
        self.max_trigger = 180
        self.max_ammo = 12
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Sniper'
        image = pygame.image.load('assets/guns/sniper.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 15
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['purple'])


class Shotgun(Gun):

    def __init__(self):
        self.reload_time = 3 * 60
        self.max_trigger = 30
        self.max_ammo = 6
        self.trigger_time = 0
        cooldown = self.reload_time
        name = 'Shotgun'
        image = pygame.image.load('assets/guns/shotgun.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        ammo = self.max_ammo
        radius = 5
        speed = 6
        Gun.__init__(self, name, image, radius, speed, cooldown, ammo,
                     constants.COLOURS['gold'])
