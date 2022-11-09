import pygame
import random
import project.constants as constants


class Room:

    def __init__(self, display, size):
        self.display = display
        self.field = pygame.Rect(0, 0, size, size)

        self.chest = pygame.image.load('assets/chests.png').convert_alpha()
        poss_values = 1  #[0, 0, 0, 1, 1, 2]
        # self.chest_num = random.choice(poss_values)
        self.chests = []
        for num in range(poss_values):
            x, y = 200, 200  #random.randint(100, 1900), random.randint(100, 1900)
            self.chests.append((x, y))

        self.equippables = []

    def draw_chests(self, scroll):
        for chest in self.chests:
            self.display.blit(self.chest,
                              (chest[0] - scroll[0], chest[1] - scroll[1]))

    def draw_equippables(self, scroll):
        for eq in self.equippables:
            self.display.blit(eq[0].gun,
                              (eq[1][0] - scroll[0], eq[1][0] - scroll[1]))

    def draw_field(self, scroll):
        self.field.x = 0 - scroll[0]
        self.field.y = 0 - scroll[1]
        pygame.draw.rect(self.display, constants.COLOURS['grey'], self.field)
        pygame.draw.rect(self.display, constants.COLOURS['white'],
                         (self.field), 5)
