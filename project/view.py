import pygame
import project.constants as constants
import project.events as events
import project.weapons as weapons
import project.powerups as powerups
from project.characters import Player
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

        weapons.Gun.guns = [
            weapons.Pistol(),
            weapons.SubMachine(),
            weapons.AssaultRifle(),
            weapons.MiniGun(),
            weapons.Sniper(),
            weapons.Shotgun()
        ]

        powerups.PowerUp.powerups = [
            powerups.Health(),
            powerups.Damage(),
            powerups.BulletSpeed(),
            powerups.PlayerSpeed(),
            powerups.Ammo(),
            powerups.Shield(),
            powerups.TwoGuns()
        ]

        self.display = pygame.Surface((self.width, self.height))

        self.m_input = events.MouseInput()

        cursor1, cursor2 = 'assets/idle_cursor.png', 'assets/target_cursor.png'
        self.cursor_state = 'Idle'

        self.idle_cursor = pygame.image.load(cursor1).convert_alpha()
        self.target_cursor = pygame.image.load(cursor2).convert_alpha()

        self.true_scroll = [0, 0]
        self.scroll = self.true_scroll.copy()

        self.room = Room(self.display, 2000)

        self.player = Player(self.room, weapons.Shotgun(), powerups.PowerUp)
        Player.powerups = powerups.PowerUp.powerups
        Player.guns = weapons.Gun.guns

    def run(self, dt, state):
        self.update_camera()

        self.screen.blit(self.display, (0, 0))
        self.display.fill(constants.COLOURS['black'])

        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouseVector = self.m_input.process_events(mouse_pressed, pos)
        angle = self.player.realVector.degree(mouseVector)

        if self.cursor_state == 'Idle':
            self.draw_cursor(self.idle_cursor, pos)
        else:
            self.draw_cursor(self.target_cursor, pos)

        self.room.draw_field(self.scroll)
        self.room.draw_chests(self.scroll)
        self.room.draw_equippables(self.scroll)

        weapons.Bullet.draw(self.display, dt, self.scroll)
        weapons.Bullet.explode_bullets(self.display, self.scroll)

        mouse = self.m_input.button_pressed
        key_pressed = pygame.key.get_pressed()
        self.player.process_keys(self.display, key_pressed, self.scroll)

        self.player.draw(self.display, angle, self.scroll)
        self.player.draw_line(self.display, mouseVector, self.scroll)

        self.player.move(mouseVector, dt, self.scroll)
        self.player.shoot(mouse, mouseVector, self.scroll)

        self.player.listen_powerups()

        return state

    def update_camera(self):
        x, y = self.player.vector.x, self.player.vector.y
        width, height = self.width / 2, self.height / 2
        self.true_scroll[0] += (x - self.scroll[0] - width) / 15
        self.true_scroll[1] += (y - self.scroll[1] - height) / 15
        self.scroll[0] = int(self.true_scroll[0])
        self.scroll[1] = int(self.true_scroll[1])
