import pygame


class PowerUp:

    powerups = []

    def __init__(self, name, desc, image, cooldown):
        self.name = name
        self.desc = desc
        self.image = image
        self.cooldown = cooldown

    @classmethod
    def random(cls):
        import random
        return random.choice(cls.powerups)


class Health(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/heart.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 30
        PowerUp.__init__(self, 'Health', '', image, cooldown)


class Damage(PowerUp):

    def __init__(self):
        image = pygame.image.load(
            'assets/powerups/explosion.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 30
        PowerUp.__init__(self, 'Damage', '', image, cooldown)


class BulletSpeed(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/bullet.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 60 * 15
        PowerUp.__init__(self, 'Bullet Speed', '', image, cooldown)


class PlayerSpeed(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/speed.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 60 * 15
        PowerUp.__init__(self, 'Player Speed', '', image, cooldown)


class Ammo(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/ammo.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 60 * 30
        PowerUp.__init__(self, 'Ammo', '', image, cooldown)


class Shield(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/shield.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 30
        PowerUp.__init__(self, 'Shield', '', image, cooldown)


class TwoGuns(PowerUp):

    def __init__(self):
        image = pygame.image.load('assets/powerups/dual.png').convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        cooldown = 60 * 15
        PowerUp.__init__(self, 'Two Guns', '', image, cooldown)
