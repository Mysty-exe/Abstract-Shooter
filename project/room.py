import pygame
import random
import project.constants as constants
from project.characters import Enemy
import project.weapons as weapons


class Room:

    def __init__(self, display, size, difficulty):
        self.display = display
        self.size = size
        self.difficulty = difficulty
        self.field = pygame.Rect(0, 0, self.size, self.size)
        self.num = constants.DIFFICULTY[self.difficulty][0]
        self.spawn_interval = constants.DIFFICULTY[self.difficulty][1] * 60
        self.spawn_cooldown = 0

        self.chest = pygame.image.load('assets/chests.png').convert_alpha()
        self.chest = pygame.transform.scale(self.chest, (64, 64))

        chest_nums = [0, 1, 2]
        weight = constants.DIFFICULTY[self.difficulty][2]
        self.chest_num = random.choices(chest_nums, k=1, weights=weight)[0]

        self.chests = []
        for num in range(self.chest_num):
            x, y = random.randint(150, self.size - 150), random.randint(
                150, self.size - 150)
            self.chests.append((x, y))

        obstacles_num = [0, 1, 2, 3]
        weight = [10, 25, 40, 25]
        self.obstacles_num = random.choices(obstacles_num, k=1, weights=weight)[0]
        self.obstacles = []

        for num in range(self.obstacles_num):
            self.add_obstacle()

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

    def add_obstacle(self):
        orientation = random.choice(['h', 'v'])
        while True:
            if orientation == 'h':
                x = random.randint(200, 1200)
                y = random.randint(200, 1700)
                w = random.randint(100, 600)
                h = 50
            else:
                x = random.randint(200, 1700)
                y = random.randint(200, 1200)
                w = 50
                h = random.randint(100, 600)

            if not pygame.Rect(x, y, w, h).colliderect(pygame.Rect(1000, 1000, 48, 48)):
                break

        self.obstacles.append(pygame.Rect(x, y, w, h))

    def draw_obstacles(self, scroll):
        for obstacle in self.obstacles:
            obstacle.x -= scroll[0]
            obstacle.y -= scroll[1]
            pygame.draw.rect(self.display, constants.COLOURS['white'], obstacle)
            obstacle.x += scroll[0]
            obstacle.y += scroll[1]

    def spawn(self):
        if len(Enemy.enemies) < self.num:
            Enemy.enemies.append(Enemy(self, weapons.Gun.random(self.difficulty), self.difficulty))

    def draw_enemies(self, player, scroll, dt, no=False):
        for enemy in Enemy.enemies:
            angle = enemy.vector.degree(player.vector)
            if no == False:
                enemy.shoot(player, scroll)
            enemy.move(player, dt, scroll)
            enemy.draw(self.display, angle, scroll)
        Enemy.explode_enemies(self.display, scroll)

    def collision(self, player):
        for enemy in Enemy.enemies:
            for bullet in weapons.Bullet.player_bullets:
                enemy_mask = pygame.mask.from_surface(enemy.surf)
                bullet_mask = pygame.mask.from_surface(bullet.surf)
                offset = (bullet.pos.x - (enemy.vector.x - 24),
                          bullet.pos.y - (enemy.vector.y - 24))
                if enemy_mask.overlap(bullet_mask, offset):
                    Enemy.enemy_exploding.append([0, enemy])
                    Enemy.enemies.remove(enemy)
                    weapons.Bullet.player_bullets.remove(bullet)
                    player.kills += 1

        for obstacle in self.obstacles:
            for bullet in weapons.Bullet.player_bullets + weapons.Bullet.enemy_bullets:
                bullet_mask = pygame.mask.from_surface(bullet.surf)
                obstacle_mask = pygame.mask.Mask((obstacle.width, obstacle.height))
                obstacle_mask.fill()
                offset = (bullet.pos.x - (obstacle.x),
                          bullet.pos.y - (obstacle.y))
                if obstacle_mask.overlap(bullet_mask, offset):
                    weapons.Bullet.bullets_exploding.append([0, bullet])
                    if bullet.type == 'Player':
                        weapons.Bullet.player_bullets.remove(bullet)
                    else:
                        weapons.Bullet.enemy_bullets.remove(bullet)