import pygame
from project.math import Vector
import project.constants as constants


class Character:

    def __init__(self, x, y, width, height):
        self.vector = Vector(x, y)
        self.realVector = Vector(x, y)
        self.width, self.height = width, height

        self.surf = pygame.Surface((width, height))
        self.surf.set_colorkey(constants.COLOURS['blue'])
        self.surf.fill(constants.COLOURS['black'])

        self.rotated = pygame.transform.rotate(self.surf, 0)
        self.rotated_rect = self.rotated.get_rect()
        self.border = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, screen, angle, scroll):
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


class Player(Character):

    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    def __init__(self, room, gun):
        Character.__init__(self, 100, 100, 64, 64)
        self.room = room
        self.gun = gun
        self.direction = [None, None, None, None]

        self.bounce_direction = 0
        self.bouncevel = 7

        self.velx = 0
        self.vely = 0
        self.velgoalx = 0
        self.velgoaly = 0

        self.dashvel = 0
        self.dash_velgoal = 20
        self.dash_color = [255, 255, 255]
        self.dash_direction = 0
        self.max_dash = 30
        self.dash_time = 0

        self.collecting = False

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
            self.velgoaly = -6

        if keys[pygame.K_s] and not keys[pygame.K_w] and not self.isdashing():
            self.direction[0] = 'Down'
            self.velgoaly = 6

        if keys[pygame.K_a] and not keys[pygame.K_d] and not self.isdashing():
            self.direction[1] = 'Left'
            self.velgoalx = -6

        if keys[pygame.K_d] and not keys[pygame.K_a] and not self.isdashing():
            self.direction[1] = 'Right'
            self.velgoalx = 6

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction[0] = None
            self.velgoaly = 0

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction[1] = None
            self.velgoalx = 0

        if keys[pygame.K_SPACE] and self.direction[2] != 'Dashing':
            self.direction[2] = 'Dashing'
            self.dash_direction = (self.direction[3]).normalize()

        if keys[pygame.K_e] and not self.collecting and (
                self.unlock_chest() or self.collect_equippables()):
            self.collecting = True

        if not keys[pygame.K_e]:
            self.collecting = False

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
        if self.isdashing() and self.dash_time < self.max_dash:
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
                self.dash_color = [255, 255, 255]
                self.direction[2] = None
                self.dash_velgoal = 20
                self.dash_time = 0
                self.dashvel = 0

    def hit_border(self, scroll):
        if (self.rotated_rect.x + scroll[0]) == 0:
            self.vector.x += 0.5
            return True
        if (self.rotated_rect.x + scroll[0] + self.rotated_rect.width) == 2000:
            self.vector.x -= 0.5
            return True

        if (self.rotated_rect.y + scroll[1]) == 0:
            self.vector.y += 0.5
            return True
        if (self.rotated_rect.y + scroll[1] + self.rotated_rect.width) == 2000:
            self.vector.y -= 0.5
            return True

        return False

    def shoot(self, mouseInput, mouseCoord):
        self.gun.reload()
        if mouseInput != False and self.gun.trigger_time == 0:
            direction = (mouseCoord - self.realVector).normalize()
            self.gun.add_bullet(self.vector.x, self.vector.y, direction)
            self.gun.trigger_time = self.gun.max_trigger

    def unlock_chest(self):
        for chest in self.room.chests:
            chestVector = Vector(chest[0] + 64, chest[1] + 64)
            if self.vector.distance(chestVector) <= 150:
                self.room.equippables.append((self.gun.random(), chest))
                self.room.chests.remove(chest)
                return True
        return False

    def collect_equippables(self):
        for eq in self.room.equippables:
            equipVector = Vector(eq[1][0] + 64, eq[1][1] + 64)
            if self.vector.distance(equipVector) <= 100:
                self.gun = eq[0]
                self.room.equippables.remove(eq)
                return True
        return False

    def isdashing(self):
        if self.direction[2] == 'Dashing':
            return True
        return False

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
