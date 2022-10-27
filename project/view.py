import pygame
import project.constants as constants
import project.events as events
from project.characters import Player


class View:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.cursor = pygame.image.load('assets/icon.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (16, 16))
        pygame.mouse.set_visible(False)


class GameView(View):

    def __init__(self):
        View.__init__(self)
        self.player = Player()
        self.k_input = events.KeyboardInput()
        self.m_input = events.MouseInput()

    def run(self, dt, state):
        self.screen.fill(constants.COLOURS['white'])  #Clear Screen

        #Mouse Input and Cursor
        pos = pygame.mouse.get_pos()
        mouseVector = self.m_input.process_events(
            pygame.mouse.get_pressed()[0], pos)
        self.screen.blit(self.cursor, (pos[0] - 8, pos[1] - 8))
        print(self.m_input.button_pressed)

        #Keyboard Input
        k_events = self.k_input.process_events(pygame.key.get_pressed())
        angle = self.player.vector.degree(mouseVector)  #Get Angle

        #Draw Player
        self.player.draw(self.screen, angle)
        self.player.move(dt, k_events)
        self.player.reset_direction(k_events)
        self.k_input.empty_queue()

        return state
