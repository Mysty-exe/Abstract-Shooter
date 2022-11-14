import pygame
from project.math import Vector
import project.constants as constants


class Character:

    def __init__(self, x, y, width, height, color):
        self.vector = Vector(x, y)
        self.realVector = Vector(x, y)
        self.width, self.height = width, height

        self.surf = pygame.Surface((width, height))
        self.surf.set_colorkey(constants.COLOURS['blue'])
        self.surf.fill(color)

        self.rotated = pygame.transform.rotate(self.surf, 0)
        self.rotated_rect = self.rotated.get_rect()
        self.border = pygame.Rect(0, 0, self.width, self.height)


class Player(Character):

    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    guns = []
    powerups = []

    def __init__(self, room, gun, powerup):
        Character.__init__(self, 100, 100, 64, 64, constants.COLOURS['black'])
        self.room = room
        self.gun = gun
        self.twoguns = [
            Vector(self.vector.x - 32, self.vector.y + 32),
            Vector(self.vector.x - 32, self.vector.y - 32)
        ]
        self.powerup = powerup
        self.direction = [None, None, None, None]

        self.speed = 6
        self.velx = 0
        self.vely = 0
        self.velgoalx = 0
        self.velgoaly = 0

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

    def draw(self, screen, angle, scroll):

        self.twoguns = [
            Vector(self.vector.x - 32, self.vector.y + 32),
            Vector(self.vector.x - 32, self.vector.y - 32)
        ]

        for i, v in enumerate(self.twoguns):
            self.twoguns[i] = v.rotate(self.vector, angle)

        self.rotated = pygame.transform.rotate(self.surf, angle * -1)
        self.rotated_rect = self.rotated.get_rect(
            center=(self.vector.x,
                    self.vector.y)).clamp(pygame.Rect(0, 0, 2000, 2000))

        self.rotated_rect.x -= scroll[0]
        self.rotated_rect.y -= scroll[1]
        self.realVector = self.vector - Vector(scroll[0], scroll[1])

        pygame.draw.rect(self.surf, constants.COLOURS['white'], self.border, 3)
        screen.blit(self.rotated, self.rotated_rect)

    def draw_line(self, screen, mouseCoord, scroll):
        pygame.draw.line(screen, constants.COLOURS['red'],
                         self.realVector.coord(), mouseCoord.coord())

    def approach(self, goal, current, dt):
        difference = goal - current
        if difference > dt:
            return current + dt
        if difference < -dt:
            return current - dt

        return goal

    def process_keys(self, screen, keys, scroll):
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
                self.unlock_chest() or self.collect_equippables()):
            self.collecting = True

        if not keys[pygame.K_e]:
            self.collecting = False

        if keys[pygame.K_r]:
            if not self.gun.reloading:
                self.gun.reloading = True

    def move(self, mouse, dt, scroll):
        self.direction[3] = (mouse - self.realVector)

        self.hit_border(scroll)
        self.dash(mouse, dt, scroll)
        self.velx = self.approach(self.velgoalx, self.velx, dt / 5)
        self.vely = self.approach(self.velgoaly, self.vely, dt / 5)
        if not self.hit_border(scroll):
            self.vector.x += self.velx * dt
            self.vector.y += self.vely * dt

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

    def hit_border(self, scroll):
        x, y = self.rotated_rect.x, self.rotated_rect.y
        width = self.rotated_rect.width
        if (x + scroll[0]) == 0:
            self.vector.x += 0.5
            return True
        if (x + scroll[0] + width) == 2000:
            self.vector.x -= 0.5
            return True

        if (y + scroll[1]) == 0:
            self.vector.y += 0.5
            return True
        if (y + scroll[1] + width) == 2000:
            self.vector.y -= 0.5
            return True

        return False

    def shoot(self, mouseInput, mouseCoord, scroll):
        self.gun.trigger_time = self.gun.reload(self.gun.reload_time,
                                                self.gun.trigger_time,
                                                self.gun.max_ammo)

        if mouseInput != False and self.gun.trigger_time == 0 and not self.gun.reloading:
            self.gun.ammo -= 1
            if self.gun.double:
                for gun in self.twoguns:
                    point = gun.midpoint(self.vector)
                    self.gun.add_bullet(point.x, point.y, mouseCoord,
                                        self.realVector)
            else:
                self.gun.add_bullet(self.vector.x, self.vector.y, mouseCoord,
                                    self.realVector)
            self.gun.trigger_time = self.gun.max_trigger

    def unlock_chest(self):
        for chest in self.room.chests:
            chestVector = Vector(chest[0] + 64, chest[1] + 64)
            if self.vector.distance(chestVector) <= 150:
                import random
                equippables = [self.gun.random()] * 6 + [self.powerups[6]] * 4
                equippable = random.choice(equippables)

                self.room.equippables.append(
                    ((equippable.name, equippable), chest))
                self.room.chests.remove(chest)

                return True
        return False

    def collect_equippables(self):
        for eq in self.room.equippables:
            equipVector = Vector(eq[1][0] + 64, eq[1][1] + 64)
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
            powerup[0].cooldown -= 1
            name = powerup[1]
            status = powerup[3]
            cooldown = powerup[0].cooldown

            if status == 'Started' or cooldown <= 0:
                if status == 'Started':
                    powerup[3] = 'Active'

                if name == 'Health':
                    pass

                elif name == 'Damage':
                    pass

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
                    pass

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
        if self.direction == [None, None]:
            return True
        return False
