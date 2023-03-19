import pygame
import project.events as e
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

        self.game_state = 'Menu'
        self.game = view.GameView()

        self.fps = constants.GAME_FPS
        self.dt = self.fps
        self.clock = pygame.time.Clock()

    def run(self):
        while self.game_state != 'Quit':
            events = pygame.event.get()
            self.game_state = e.MouseInput.check(
                events, self.game_state)

            if self.game_state in ['Transition - Game', 'Transition - Menu']:
                self.game_state = self.game.transition(self.game_state)

            if self.game_state == 'Menu':
                self.game_state = self.game.main_menu(self.game_state, events)

            if self.game_state == 'Game':
                self.game_state = self.game.run(self.dt, self.game_state, events)

            elif self.game_state == 'Paused':
                self.game_state = self.game.pause(self.game_state, events)

            elif self.game_state == 'Game Over':
                self.game_state = self.game.game_over(self.dt, self.game_state, events)

            pygame.display.update()
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
