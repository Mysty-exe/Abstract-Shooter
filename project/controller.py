import pygame
from project.characters import Player
import project.events as events
import project.constants as constants
import project.images as images
import project.view as view
import sys

class GameInstance:
    def __init__(self):
        pygame.init()

        self.title = constants.GAME_TITLE
        self.icon = images.icon

        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)
        self.fps = constants.GAME_FPS
        self.clock = pygame.time.Clock()

        self.game_state = 'Game'
        self.game = view.GameView()


    def run(self):
        while self.game_state != 'Quit':
            self.game_state = events.MouseInput.check_quit(pygame.event.get(), self.game_state)

            if self.game_state == 'Game':
                self.game_state = self.game.run(self.game_state)

            self.clock.tick(self.fps)
            pygame.display.update()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
