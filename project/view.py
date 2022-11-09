import pygame
import project.constants as constants
import project.events as events
from project.characters import Player
import project.weapons as weapons
from project.room import Room


class View:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.mouse.set_visible(False)

    def draw_cursor(self, cursor, pos):
        self.screen.blit(cursor, (pos[0] - 16, pos[1] - 16))


class GameView(View):

    def __init__(self):
        View.__init__(self)

        self.display = pygame.Surface((self.width, self.height))

        self.k_input = events.KeyboardInput()
        self.m_input = events.MouseInput()
        self.cursor1 = pygame.image.load(
            'assets/idle_cursor.png').convert_alpha()
        self.cursor2 = pygame.image.load(
            'assets/target_cursor.png').convert_alpha()

        self.true_scroll = [0, 0]
        self.scroll = self.true_scroll.copy()

        self.room = Room(self.display, 2000)

        weapons.Gun.guns = [
            weapons.Pistol(),
            weapons.SubMachine(),
            weapons.AssaultRifle(),
            weapons.MiniGun(),
            weapons.Sniper()
        ]

        self.player = Player(self.room, weapons.Pistol())

    def run(self, dt, state):
        self.update_camera()

        self.screen.blit(self.display, (0, 0))
        self.display.fill(constants.COLOURS['black'])

        self.room.draw_field(self.scroll)
        self.room.draw_chests(self.scroll)
        self.room.draw_equippables(self.scroll)

        pos = pygame.mouse.get_pos()
        mouseVector = self.m_input.process_events(
            pygame.mouse.get_pressed()[0], pos)
        angle = self.player.realVector.degree(mouseVector)

        weapons.Bullet.draw(self.display, dt, self.scroll)
        weapons.Bullet.explode_bullets(self.display, self.scroll)

        m_input = self.m_input.button_pressed
        self.player.process_keys(self.display, pygame.key.get_pressed(), self.scroll)
        self.player.draw_line(self.display, mouseVector, self.scroll)
        self.player.draw(self.display, angle, self.scroll)
        self.player.move(mouseVector, dt, self.scroll)
        self.player.shoot(m_input, mouseVector)
        self.k_input.empty_queue()

        self.draw_cursor(self.cursor1, pos)

        return state

    def update_camera(self):
        self.true_scroll[0] += (self.player.vector.x - self.scroll[0] -
                                (self.width / 2)) / 15
        self.true_scroll[1] += (self.player.vector.y - self.scroll[1] -
                                (self.height / 2)) / 15
        self.scroll[0] = int(self.true_scroll[0])
        self.scroll[1] = int(self.true_scroll[1])
