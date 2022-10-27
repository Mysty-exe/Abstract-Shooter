import pygame
import project.events as events
import project.constants as constants
import project.view as view
import sys


class GameInstance:

    def __init__(self):
        pygame.init()

        self.title = constants.GAME_TITLE
        self.icon = pygame.image.load('assets/icon.png')

        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)

        self.game_state = 'Game'
        self.game = view.GameView()

        self.fps = constants.GAME_FPS
        self.dt = self.fps
        self.clock = pygame.time.Clock()

    def run(self):
        while self.game_state != 'Quit':
            self.game_state = events.MouseInput.check_quit(
                pygame.event.get(), self.game_state)

            if self.game_state == 'Game':
                self.game_state = self.game.run(self.dt, self.game_state)

            pygame.display.update()
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
