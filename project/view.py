import pygame
import project.constants as constants
import project.events as events
from project.characters import Player

class View:
    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))

class GameView( View ):
    def __init__(self):
        View.__init__(self)
        self.player = Player()
        self.k_input = events.KeyboardInput()
        self.m_input = events.MouseInput()

    def run(self, state):
        self.screen.fill(constants.COLOURS['white'])
        self.player.draw(self.screen)

        k_events = self.k_input.process_events(pygame.key.get_pressed())
        self.player.move(k_events)
        self.player.reset_direction(k_events)
        self.k_input.empty_queue()

        return state
