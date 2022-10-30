import pygame
import project.constants as constants
import project.events as events
from project.characters import Player
import project.weapons as weapons


class View:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.cursor = pygame.image.load('assets/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (16, 16))
        pygame.mouse.set_visible(False)


class GameView(View):

    def __init__(self):
        View.__init__(self)
        self.player = Player(weapons.MiniGun())
        self.k_input = events.KeyboardInput()
        self.m_input = events.MouseInput()

    def run(self, dt, state):
        self.screen.fill(constants.COLOURS['white'])  #Clear Screen

        #Mouse Input and Cursor / Keyboard Input
        pos = pygame.mouse.get_pos()
        mouseVector = self.m_input.process_events(
            pygame.mouse.get_pressed()[0], pos)

        m_input = self.m_input.button_pressed
        angle = self.player.vector.degree(mouseVector)  #Get Angle

        #Draw Player
        weapons.Bullet.draw(self.screen, dt)
        self.screen.blit(self.cursor, (pos[0] - 8, pos[1] - 8))
        self.player.draw(self.screen, angle)
        self.player.process_keys(pygame.key.get_pressed())
        self.player.move(dt)
        self.player.shoot(m_input, mouseVector, angle)
        self.k_input.empty_queue()
        pygame.draw.line(self.screen, constants.COLOURS['red'],
                         (self.player.vector.coord()), mouseVector.coord())

        return state
