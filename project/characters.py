import pygame
from project.math import Vector
import project.constants as constants


class Character:

    def __init__(self, x, y, width, height):
        self.vector = Vector(x, y)
        self.width, self.height = width, height

        self.surf = pygame.Surface((width, height))
        self.surf.set_colorkey(constants.COLOURS['black'])
        self.surf.fill(constants.COLOURS['blue'])

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surf, constants.COLOURS['white'], self.rect, 3)

    def draw(self, screen, angle):
        rotated = pygame.transform.rotate(self.surf, angle * -1)
        rotated_rect = rotated.get_rect(center=self.surf.get_rect(
            center=(self.vector.x, self.vector.y)).center)
        screen.blit(rotated, rotated_rect)


class Player(Character):

    keys = {
        pygame.K_w: ('Up', 0),
        pygame.K_s: ('Down', 0),
        pygame.K_a: ('Left', 1),
        pygame.K_d: ('Right', 1)
    }

    def __init__(self, gun):
        Character.__init__(self, 100, 100, 64, 64)
        self.gun = gun
        self.direction = [None, None, None, None]

        self.dashvel = 0
        self.dash_velgoal = 20

        self.velx = 0
        self.vely = 0
        self.velgoalx = 0
        self.velgoaly = 0

        self.dash_direction = 0
        self.max_dash = 30
        self.dash_time = 0

    def approach(self, goal, current, dt):
        difference = goal - current
        if difference > dt:
            return current + dt
        if difference < -dt:
            return current - dt

        return goal

    def process_keys(self, events):
        if events[pygame.K_w] and not events[pygame.K_s] and not self.isdashing():
            self.direction[0] = 'Up'
            self.velgoaly = -6

        if events[pygame.K_s] and not events[pygame.K_w] and not self.isdashing():
            self.direction[0] = 'Down'
            self.velgoaly = 6

        if events[pygame.K_a] and not events[pygame.K_d] and not self.isdashing():
            self.direction[1] = 'Left'
            self.velgoalx = -6

        if events[pygame.K_d] and not events[pygame.K_a] and not self.isdashing():
            self.direction[1] = 'Right'
            self.velgoalx = 6

        if not events[pygame.K_w] and not events[pygame.K_s]:
            self.direction[0] = None
            self.velgoaly = 0

        if not events[pygame.K_d] and not events[pygame.K_a]:
            self.direction[1] = None
            self.velgoalx = 0

        if events[pygame.K_SPACE] and self.direction[2] != 'Dashing':
            self.direction[2] = 'Dashing'
            self.dash_direction = (self.direction[3]).normalize()

    def move(self, mouse, dt):
        self.direction[3] = (mouse - self.vector)

        self.dash(mouse, dt)
        print(self.dashvel)
        self.velx = self.approach(self.velgoalx, self.velx, dt / 3)
        self.vely = self.approach(self.velgoaly, self.vely, dt / 3)
        self.vector.x += self.velx * dt
        self.vector.y += self.vely * dt

    def dash(self, mouse, dt):
        if self.isdashing() and self.dash_time < self.max_dash:
            self.dash_time += 1
            self.dashvel = self.approach(self.dash_velgoal, self.dashvel, dt * 2)
            self.vector += self.dash_direction * self.dashvel * dt

            if self.dash_time > self.max_dash / 2:
                self.dash_velgoal = 0

            if self.dash_time >= self.max_dash:
                self.direction[2] = None
                self.dash_velgoal = 20
                self.dash_time = 0
                self.dashvel = 0

    def shoot(self, mouseInput, mouseCoord, angle):
        self.gun.reload()
        if mouseInput != False and self.gun.trigger_time == 0:
            direction = (mouseCoord - self.vector)
            self.gun.add_bullet(self.vector.x, self.vector.y,
                                direction.normalize(), angle)
            self.gun.trigger_time = self.gun.max_trigger

    def isdashing(self):
        if self.direction[2] == 'Dashing':
            return True
        return False

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
