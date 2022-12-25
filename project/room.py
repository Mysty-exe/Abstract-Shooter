import pygame
import random
import project.constants as constants
from project.characters import Enemy
import project.weapons as weapons


class Room:

    def __init__(self, display, size, num):
        self.display = display
        self.size = size
        self.field = pygame.Rect(0, 0, self.size, self.size)

        for n, enemy in enumerate(range(num)):
            Enemy.enemies.append(Enemy(self, n + 1, weapons.Gun.random()))

        self.chest = pygame.image.load('assets/chests.png').convert_alpha()
        self.chest = pygame.transform.scale(self.chest, (64, 64))

        chest_nums = [0, 1, 2]
        weight = [45, 35, 20]
        self.chest_num = random.choices(chest_nums, k=1, weights=weight)[0]

        self.chests = []
        for num in range(self.chest_num):
            x, y = random.randint(150, self.size - 150), random.randint(
                150, self.size - 150)
            self.chests.append((x, y))

        self.equippables = []

    def draw_chests(self, scroll):
        for chest in self.chests:
            self.display.blit(self.chest,
                              (chest[0] - scroll[0], chest[1] - scroll[1]))

    def draw_equippables(self, scroll):
        for eq in self.equippables:
            self.display.blit(eq[0][1].image,
                              (eq[1][0] - scroll[0], eq[1][1] - scroll[1]))

    def draw_field(self, scroll):
        self.field.x = 0 - scroll[0]
        self.field.y = 0 - scroll[1]
        pygame.draw.rect(self.display, constants.COLOURS['grey'], self.field)
        pygame.draw.rect(self.display, constants.COLOURS['white'],
                         (self.field), 5)

    def draw_enemies(self, player, scroll, dt):
        for enemy in Enemy.enemies:
            angle = enemy.vector.degree(player.vector)
            enemy.shoot(player, scroll)
            enemy.move(player, dt, scroll)
            enemy.draw(self.display, angle, scroll)
        Enemy.explode_enemies(self.display, scroll)

    def collision(self):
        for enemy in Enemy.enemies:
            for bullet in weapons.Bullet.player_bullets:
                enemy_mask = pygame.mask.from_surface(enemy.surf)
                bullet_mask = pygame.mask.from_surface(bullet.surf)
                offset = (bullet.pos.x - enemy.vector.x,
                          bullet.pos.y - enemy.vector.y)
                if enemy_mask.overlap(bullet_mask, offset):
                    Enemy.enemy_exploding.append([0, enemy])
                    Enemy.enemies.remove(enemy)
                    weapons.Bullet.player_bullets.remove(bullet)
