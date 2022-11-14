import pygame
import random
import project.constants as constants


class Room:

    def __init__(self, display, size):
        self.display = display
        self.field = pygame.Rect(0, 0, size, size)

        self.chest = pygame.image.load('assets/chests.png').convert_alpha()

        chest_nums = [0, 1, 2]
        weight = [45, 35, 20]
        self.chest_num = random.choices(chest_nums, k=1, weights=weight)[0]

        self.chests = []
        for num in range(self.chest_num):
            x, y = random.randint(500, 1500), random.randint(500, 1500)
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
