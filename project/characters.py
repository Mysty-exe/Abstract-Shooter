import pygame
from project.math import Vector
import project.constants as constants
import random


class Entity:

    def __init__(self, room, x, y, width, height, color):
        self.room = room
        self.vector = Vector(x, y)
        self.realVector = Vector(x, y)
        self.width, self.height = width, height
        self.color = color

        self.surf = pygame.Surface((width, height))
        self.surf.fill(self.color)
        self.surf.set_colorkey(constants.COLOURS['blue'])

        self.rotated = pygame.transform.rotate(self.surf, 0)
        self.rotated_rect = self.rotated.get_rect()
        self.border = pygame.Rect(0, 0, self.width, self.height)

        self.explode = {
            1:
            pygame.image.load('assets/enemy_explosion/1.png').convert_alpha(),
            2:
            pygame.image.load('assets/enemy_explosion/2.png').convert_alpha(),
            3:
            pygame.image.load('assets/enemy_explosion/3.png').convert_alpha(),
            4:
            pygame.image.load('assets/enemy_explosion/4.png').convert_alpha(),
            5:
            pygame.image.load('assets/enemy_explosion/5.png').convert_alpha(),
            6:
            pygame.image.load('assets/enemy_explosion/6.png').convert_alpha(),
            7:
            pygame.image.load('assets/enemy_explosion/7.png').convert_alpha(),
            8:
            pygame.image.load('assets/enemy_explosion/8.png').convert_alpha(),
            9:
            pygame.image.load('assets/enemy_explosion/9.png').convert_alpha(),
            10:
            pygame.image.load('assets/enemy_explosion/10.png').convert_alpha(),
            11:
            pygame.image.load('assets/enemy_explosion/11.png').convert_alpha(),
            12:
            pygame.image.load('assets/enemy_explosion/12.png').convert_alpha(),
            13:
            pygame.image.load('assets/enemy_explosion/13.png').convert_alpha(),
            14:
            pygame.image.load('assets/enemy_explosion/14.png').convert_alpha(),
            15:
            pygame.image.load('assets/enemy_explosion/15.png').convert_alpha(),
            16:
            pygame.image.load('assets/enemy_explosion/16.png').convert_alpha(),
            17:
            pygame.image.load('assets/enemy_explosion/17.png').convert_alpha(),
            18:
            pygame.image.load('assets/enemy_explosion/18.png').convert_alpha(),
            19:
            pygame.image.load('assets/enemy_explosion/19.png').convert_alpha(),
            20:
            pygame.image.load('assets/enemy_explosion/20.png').convert_alpha(),
            21:
            pygame.image.load('assets/enemy_explosion/21.png').convert_alpha(),
            22:
            pygame.image.load('assets/enemy_explosion/22.png').convert_alpha(),
            23:
            pygame.image.load('assets/enemy_explosion/23.png').convert_alpha(),
            24:
            pygame.image.load('assets/enemy_explosion/24.png').convert_alpha(),
            25:
            pygame.image.load('assets/enemy_explosion/25.png').convert_alpha(),
            26:
            pygame.image.load('assets/enemy_explosion/26.png').convert_alpha(),
            27:
            pygame.image.load('assets/enemy_explosion/27.png').convert_alpha(),
            28:
            pygame.image.load('assets/enemy_explosion/28.png').convert_alpha(),
            29:
            pygame.image.load('assets/enemy_explosion/29.png').convert_alpha(),
            30:
            pygame.image.load('assets/enemy_explosion/30.png').convert_alpha(),
            31:
            pygame.image.load('assets/enemy_explosion/31.png').convert_alpha(),
            32:
            pygame.image.load('assets/enemy_explosion/32.png').convert_alpha(),
        }

        for x in range(1, len(self.explode) + 1):
          self.explode[x] = pygame.transform.scale(self.explode[x], (160, 120))
          self.explode[x].set_colorkey(constants.COLOURS['black'])
        
    def approach(self, goal, current, dt):
        difference = goal - current
        if difference > dt:
            return current + dt
        if difference < -dt:
            return current - dt

        return goal


class Player(Entity):

    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    guns = []
    powerups = []

    def __init__(self, room, gun, powerup):
        self.size = 48
        Entity.__init__(self, room, room.size / 2, room.size / 2, self.size,
                        self.size, constants.COLOURS['black'])
        self.room = room
        self.gun = gun
        self.twoguns = [
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y + (self.width / 2)),
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y - (self.width / 2))
        ]
        self.powerup = powerup
        self.direction = [None, None, None, None]
        self.speed = 7
        self.vel = Vector(0, 0)
        self.velgoalx = 0
        self.velgoaly = 0
        self.angle = 0

        self.dashvel = 0
        self.dash_velgoal = 20
        self.dash_color = list(constants.COLOURS['white'])
        self.dash_direction = 0
        self.max_dash = 30
        self.dash_time = 0
        self.dash_cooldown = 15 * 60
        self.can_dash = True

        self.collecting = False
        self.active_powerups = []
        self.lives = 5
        self.explode_timer = 1
        self.shield = False
        self.kills = 0

    def draw(self, screen, angle, obstacles, scroll):
        self.twoguns = [
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y + (self.width / 2)),
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y - (self.width / 2))
        ]

        self.rotated = pygame.transform.rotate(self.surf, angle * -1)
        if self.hit_obstacle(obstacles):
            self.rotated = pygame.transform.rotate(self.surf, self.angle * -1)
        else:
            for i, v in enumerate(self.twoguns):
                self.twoguns[i] = v.rotate(self.vector, angle)
            self.angle = angle
        
        self.rotated_rect = self.rotated.get_rect(
            center=(self.vector.x, self.vector.y)).clamp(
                pygame.Rect(0, 0, self.room.size, self.room.size))

        self.rotated_rect.x -= scroll[0]
        self.rotated_rect.y -= scroll[1]
        self.realVector = self.vector - Vector(scroll[0], scroll[1])

        pygame.draw.rect(self.surf, constants.COLOURS['white'], self.border, 3)
        screen.blit(self.rotated, self.rotated_rect)

    def draw_line(self, screen, mouseCoord, scroll):
        pygame.draw.line(screen, constants.COLOURS['red'],
                         self.realVector.coord(), mouseCoord.coord())

    def process_keys(self, screen, keys, difficulty, scroll):
        if keys[pygame.K_w] and not keys[pygame.K_s] and not self.isdashing():
            self.direction[0] = 'Up'
            self.velgoaly = self.speed * -1

        if keys[pygame.K_s] and not keys[pygame.K_w] and not self.isdashing():
            self.direction[0] = 'Down'
            self.velgoaly = self.speed

        if keys[pygame.K_a] and not keys[pygame.K_d] and not self.isdashing():
            self.direction[1] = 'Left'
            self.velgoalx = self.speed * -1

        if keys[pygame.K_d] and not keys[pygame.K_a] and not self.isdashing():
            self.direction[1] = 'Right'
            self.velgoalx = self.speed

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction[0] = None
            self.velgoaly = 0

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction[1] = None
            self.velgoalx = 0

        if keys[pygame.
                K_SPACE] and self.direction[2] != 'Dashing' and self.can_dash:
            self.direction[2] = 'Dashing'
            self.dash_direction = (self.direction[3]).normalize()

        if keys[pygame.K_e] and not self.collecting and (
                self.unlock_chest(difficulty) or self.collect_equippables()):
            self.collecting = True

        if not keys[pygame.K_e]:
            self.collecting = False

        if keys[pygame.K_r]:
            if not self.gun.reloading:
                self.gun.reloading = True

    def move(self, mouse, obstacles, dt, scroll):
        self.direction[3] = (mouse - self.realVector)

        self.hit_border(scroll)
        self.update_speed()
        self.dash(mouse, dt, scroll)
        self.vel.x = self.approach(self.velgoalx, self.vel.x, dt / 5)
        self.vel.y = self.approach(self.velgoaly, self.vel.y, dt / 5)
        if not self.hit_border(scroll):
            self.vector += self.vel * dt
            self.vector.round()
            if self.hit_obstacle(obstacles):
                self.vector -= self.vel * dt
                self.vector.round()

    def update_speed(self):
        powerup = False
        if self.speed == 14:
            powerup = True

        if self.gun.name == 'Pistol':
            self.speed = 7
        elif self.gun.name == 'SubMachine Gun':
            self.speed = 6
        elif self.gun.name == 'Assault Rifle':
            self.speed = 5
        elif self.gun.name == 'MiniGun':
            self.speed = 4
        elif self.gun.name == 'Sniper':
            self.speed = 4
        elif self.gun.name == 'Shotgun':
            self.speed = 5

        if powerup:
            self.speed *= 2

    def dash(self, mouse, dt, scroll):
        if self.isdashing(
        ) and self.dash_time < self.max_dash and self.can_dash:
            self.dash_time += 1

            self.dash_color[0] -= 8.5
            self.dash_color[1] -= 8.5
            self.dash_color[2] -= 8.5
            self.surf.fill(self.dash_color)

            self.dashvel = self.approach(self.dash_velgoal, self.dashvel, dt)
            self.vector += self.dash_direction * self.dashvel * dt

            if self.dash_time > self.max_dash / 2:
                self.dash_velgoal = 0

            if self.dash_time >= self.max_dash or self.hit_border(scroll):
                self.surf.fill(constants.COLOURS['black'])
                self.dash_color = list(constants.COLOURS['white'])
                self.direction[2] = None
                self.dash_velgoal = 20
                self.dash_time = 0
                self.dashvel = 0
                self.can_dash = False
        self.reset_dash()

    def reset_dash(self):
        if not self.can_dash:
            self.dash_cooldown -= 1

        if self.dash_cooldown <= 0:
            self.dash_cooldown = 60 * 15
            self.can_dash = True

    def hit_obstacle(self, obstacles):
        player_mask = pygame.mask.from_surface(self.surf)
        for obstacle in obstacles:
            obstacle_mask = pygame.mask.Mask((obstacle.width, obstacle.height))
            obstacle_mask.fill()
            offset = (obstacle.x - (self.vector.x - 24), obstacle.y - (self.vector.y - 24))
            if player_mask.overlap(obstacle_mask, offset):
                return True
        else:
            return False

    def hit_border(self, scroll):
        x, y = self.rotated_rect.x, self.rotated_rect.y
        width = self.rotated_rect.width
        if (x + scroll[0]) == 0:
            self.vector.x += 1
            return True
        if (x + scroll[0] + width) == self.room.size:
            self.vector.x -= 1
            return True

        if (y + scroll[1]) == 0:
            self.vector.y += 1
            return True
        if (y + scroll[1] + width) == self.room.size:
            self.vector.y -= 1
            return True

        return False


    def shot(self, bullets, shake):
        if not shake:
            shake = 0
        for bullet in bullets:
            player_mask = pygame.mask.from_surface(self.surf)
            bullet_mask = pygame.mask.from_surface(bullet.surf)
            offset = (bullet.pos.x - (self.vector.x - 24), bullet.pos.y - (self.vector.y - 24))
            if player_mask.overlap(bullet_mask, offset) and not self.shield:
                shake = 30
                bullets.remove(bullet)
                if self.lives > 0:
                	self.lives -= 1
        return bullets, shake


    def shoot(self, mouseInput, mouseCoord, scroll):
        self.gun.trigger_time = self.gun.reload(self.gun.reload_time,
                                                self.gun.trigger_time,
                                                self.gun.max_ammo)

        if mouseInput != False and self.gun.trigger_time == 0 and not self.gun.reloading:
            self.gun.ammo -= 1
            if self.gun.double and self.gun.name != 'Shotgun':
                for gun in self.twoguns:
                    point = gun.midpoint(self.vector)
                    self.gun.add_bullet(point.x, point.y, mouseCoord,
                                        self.realVector, self.color, 'Player')
            else:
                self.gun.add_bullet(self.vector.x, self.vector.y, mouseCoord,
                                    self.realVector, self.color, 'Player')
            self.gun.trigger_time = self.gun.max_trigger

    def unlock_chest(self, difficulty):
        for chest in self.room.chests:
            chestVector = Vector(chest[0] + (self.width),
                                 chest[1] + (self.width))
            if self.vector.distance(chestVector) <= 150:
                equippables = [self.gun.random(difficulty)] * 6 + [self.powerup.random()] * 6
                equippable = random.choice(equippables)

                self.room.equippables.append(
                    ((equippable.name, equippable), chest))
                self.room.chests.remove(chest)

                return True
        return False

    def collect_equippables(self):
        for eq in self.room.equippables:
            equipVector = Vector(eq[1][0] + (self.width),
                                 eq[1][1] + (self.width))
            if self.vector.distance(equipVector) <= 100:
                self.room.equippables.remove(eq)
                if eq[0][0] in [gun.name for gun in self.guns]:
                    self.room.equippables.append(
                        ((self.gun.name, self.gun), eq[1]))
                    self.gun = eq[0][1]
                else:
                    self.active_powerups.append(
                        [eq[0][1], eq[0][0], 0, 'Started'])

                return True
        return False

    def listen_powerups(self):
        for powerup in self.active_powerups:
            if powerup[0].cooldown != None:
                powerup[0].cooldown -= 1
            name = powerup[1]
            status = powerup[3]
            cooldown = powerup[0].cooldown

            if status == 'Started' or cooldown <= 0:
                if status == 'Started':
                    powerup[3] = 'Active'

                if name == 'Heart':
                    if self.lives != 0 and self.lives != 5:
                        self.lives += 1
                    self.active_powerups.remove(powerup)

                elif name == 'Bullet Speed':
                    if not cooldown <= 0:
                        self.gun.speed *= 2
                    else:
                        self.gun.speed /= 2
                        self.active_powerups.remove(powerup)

                elif name == 'Player Speed':
                    if not cooldown <= 0:
                        self.speed *= 2
                    else:
                        self.speed /= 2
                        self.active_powerups.remove(powerup)

                elif name == 'Ammo':
                    if not cooldown <= 0:
                        self.gun.max_ammo *= 2
                    else:
                        self.gun.max_ammo /= 2
                        self.active_powerups.remove(powerup)

                elif name == 'Shield':
                    if not cooldown <= 0:
                        self.shield = True
                    else:
                        self.shield = False
                        self.active_powerups.remove(powerup)

                elif name == 'Two Guns':
                    if not cooldown <= 0:
                        self.gun.double = True
                    else:
                        self.gun.double = False
                        self.active_powerups.remove(powerup)

    def isdashing(self):
        if self.direction[2] == 'Dashing':
            return True
        return False

    def isidle(self):
        if self.direction[0] == None and self.direction[1] == None:
            return True
        return False

    def self_explode(self, screen, scroll):
        x, y = self.vector.x, self.vector.y
        if self.explode_timer < 33:
            screen.blit(self.explode[self.explode_timer], (x - scroll[0] - 80, y - scroll[1] - 60))
            self.explode_timer += 1

class Enemy(Entity):
    enemies = []
    enemy_exploding = []
    distance_between_entities = 100

    def __init__(self, room, gun, difficulty):
        self.x, self.y = random.choice(constants.POSS_LOCATIONS)
        self.size = 48
        Entity.__init__(self, room, self.x, self.y, self.size, self.size,
                        gun.color)

        self.vector = Vector(self.x, self.y)
        self.realVector = Vector(self.x, self.y)
        self.gun = gun
        self.gun.speed /= 2
        self.difficulty = difficulty
        if random.random() < constants.DIFFICULTY[self.difficulty][4]:
            self.gun.double = True

        self.twoguns = [
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y + (self.width / 2)),
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y - (self.width / 2))
        ]

        self.speed = 5.0
        self.acceleration = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.max_force = 5
        self.mass = 1.0

        self.distance = 300

    def draw(self, screen, angle, scroll):

        self.twoguns = [
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y + (self.width / 2)),
            Vector(self.vector.x - (self.width / 2),
                   self.vector.y - (self.width / 2))
        ]

        for i, v in enumerate(self.twoguns):
            self.twoguns[i] = v.rotate(self.vector, angle)

        self.rotated = pygame.transform.rotate(self.surf, angle * -1)
        self.rotated_rect = self.rotated.get_rect(
            center=(self.vector.x, self.vector.y)).clamp(
                pygame.Rect(0, 0, self.room.size, self.room.size))

        self.rotated_rect.x -= scroll[0]
        self.rotated_rect.y -= scroll[1]
        self.realVector = self.vector - Vector(scroll[0], scroll[1])

        pygame.draw.rect(self.surf, constants.COLOURS['white'], self.border, 3)
        screen.blit(self.rotated, self.rotated_rect)
        print(self.acceleration)

    def hit_border(self, scroll):
        x, y = self.rotated_rect.x, self.rotated_rect.y
        width = self.rotated_rect.width
        if (x + scroll[0]) == 0:
            self.vector.x += 1
            return True
        if (x + scroll[0] + width) == self.room.size:
            self.vector.x -= 1
            return True

        if (y + scroll[1]) == 0:
            self.vector.y += 1
            return True
        if (y + scroll[1] + width) == self.room.size:
            self.vector.y -= 1
            return True

        return False

    def update_speed(self):
        if self.gun.name == 'Pistol':
            self.speed = 5
        elif self.gun.name == 'SubMachine Gun':
            self.speed = 4
        elif self.gun.name == 'Assault Rifle':
            self.speed = 3
        elif self.gun.name == 'MiniGun':
            self.speed = 2
        elif self.gun.name == 'Sniper':
            self.speed = 2
        elif self.gun.name == 'Shotgun':
            self.speed = 3

    def separate(self):
        separation = Vector(0, 0)
        radius = 100
        count = 0
        for neighbor in Enemy.enemies:
            distance = self.vector.distance(neighbor.vector)
            if distance > 0 and distance < radius:
                diff = self.vector - neighbor.vector
                diff = diff.scale_to_length(1 / distance)
                separation += diff
                count += 1

        if count > 0:
            separation /= count
        if separation.scale_to_length(1).magnitude() > 0:
            separation = seperation.scale_to_length(1)
    
        return separation

    def calc_velocity(self, enemy, player):
        distance = player - enemy
        distance = distance.normalize()
        velocity = distance * self.speed
        return velocity

    def move(self, player, dt, scroll):
        distance = self.vector.distance(player.vector)
        if distance > self.distance:
            desired_vel = self.calc_velocity(self.vector, player.vector) 
            steering = (desired_vel - self.vel).truncate(self.max_force)
            self.acceleration = steering / self.mass
            self.vel += self.acceleration
        else:
            self.vel = Vector(0, 0)

        if not self.hit_border(scroll):
            self.vector += self.vel
            self.vector.round()

        self.update_speed() 

    def shoot(self, player, scroll):

        self.gun.trigger_time = self.gun.reload(self.gun.reload_time,
                                                self.gun.trigger_time,
                                                self.gun.max_ammo)

        if self.gun.trigger_time == 0 and not self.gun.reloading:
            self.gun.ammo -= 1
            if self.gun.double and self.gun.name != 'Shotgun':
                for gun in self.twoguns:
                    point = gun.midpoint(self.vector)
                    self.gun.add_bullet(point.x,
                                        point.y,
                                        player.vector,
                                        player.vector,
                                        self.color,
                                        'Enemy',
                                        enemy=self.vector)
            else:
                self.gun.add_bullet(self.vector.x,
                                    self.vector.y,
                                    player.vector,
                                    player.vector,
                                    self.color,
                                    'Enemy',
                                    enemy=self.vector)
            self.gun.trigger_time = self.gun.max_trigger

    @classmethod
    def explode_enemies(cls, screen, scroll):
        for enemy in cls.enemy_exploding:
            x, y = enemy[1].vector.x, enemy[1].vector.y
            screen.blit(enemy[1].explode[enemy[0] + 1],
                        (x - scroll[0] - 80, y - scroll[1] - 60))
            enemy[0] += 1
            if enemy[0] == 32:
                cls.enemy_exploding.remove(enemy)
