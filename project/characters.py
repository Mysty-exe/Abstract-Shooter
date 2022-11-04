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
        self.rotated_rect = self.surf.get_rect()
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

    def __init__(self, gun):
        Character.__init__(self, 1000, 1000, 64, 64)
        self.gun = gun
        self.direction = [None, None, None, None]

        self.dashvel = 0
        self.dash_velgoal = 20

        self.velx = 0
        self.vely = 0
        self.velgoalx = 0
        self.velgoaly = 0

        self.dash_color = [255, 255, 255]
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
        if events[pygame.
                  K_w] and not events[pygame.K_s] and not self.isdashing():
            self.direction[0] = 'Up'
            self.velgoaly = -6

        if events[pygame.
                  K_s] and not events[pygame.K_w] and not self.isdashing():
            self.direction[0] = 'Down'
            self.velgoaly = 6

        if events[pygame.
                  K_a] and not events[pygame.K_d] and not self.isdashing():
            self.direction[1] = 'Left'
            self.velgoalx = -6

        if events[pygame.
                  K_d] and not events[pygame.K_a] and not self.isdashing():
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

    def move(self, mouse, dt, scroll):
        self.direction[3] = (mouse - self.realVector)

        self.dash(mouse, dt)
        self.bounce(scroll, dt)
        self.velx = self.approach(self.velgoalx, self.velx, dt / 3)
        self.vely = self.approach(self.velgoaly, self.vely, dt / 3)
        self.vector.x += self.velx * dt
        self.vector.y += self.vely * dt

    def dash(self, mouse, dt):
        if self.isdashing() and self.dash_time < self.max_dash:
            self.dash_time += 1

            self.dash_color[0] -= 8.5
            self.dash_color[1] -= 8.5
            self.dash_color[2] -= 8.5
            self.surf.fill(self.dash_color)

            self.dashvel = self.approach(self.dash_velgoal, self.dashvel, 2)
            self.vector += self.dash_direction * self.dashvel * dt

            if self.dash_time > self.max_dash / 2:
                self.dash_velgoal = 0

            if self.dash_time >= self.max_dash:
                self.surf.fill(constants.COLOURS['black'])
                self.dash_color = [255, 255, 255]
                self.direction[2] = None
                self.dash_velgoal = 20
                self.dash_time = 0
                self.dashvel = 0

    def bounce(self, scroll, dt):
        if (self.rotated_rect.x + scroll[0]) == 0:
            self.vector.x += 100
        if (self.rotated_rect.x + scroll[0] + self.rotated_rect.width) == 2000:
            self.vector.x -= 100

        if (self.rotated_rect.y + scroll[1]) == 0:
            self.vector.y += 100
        if (self.rotated_rect.y + scroll[1] + self.rotated_rect.width) == 2000:
            self.vector.y -= 100

    def shoot(self, mouseInput, mouseCoord):
        self.gun.reload()
        if mouseInput != False and self.gun.trigger_time == 0:
            direction = (mouseCoord - self.realVector)
            self.gun.add_bullet(self.realVector.x, self.realVector.y,
                                direction.normalize())
            self.gun.trigger_time = self.gun.max_trigger

    def isdashing(self):
        if self.direction[2] == 'Dashing':
            return True
        return False

    def isidle(self):
        if self.direction == [None, None]:
            return True
        return False
