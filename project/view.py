import pygame
import project.constants as constants
import project.events as events
import project.weapons as weapons
import project.powerups as powerups
import project.characters as entity
from project.room import Room


class View:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.mouse.set_visible(False)

    def draw_cursor(self, cursor, pos):
        self.screen.blit(cursor, (pos[0] - 16, pos[1] - 16))

    def mouse_interaction(self, point, object, vector):
        object_mask = pygame.mask.from_surface(object)
        offset = (point.x - vector.x, point.y - vector.y)
        try:
            if object_mask.get_at(offset):
                return True
        except IndexError:
            return False


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

        self.timer = 0

        self.m_input = events.MouseInput()

        cursor1, cursor2 = 'assets/idle_cursor.png', 'assets/target_cursor.png'
        self.cursor_state = 'Idle'

        self.idle_cursor = pygame.image.load(cursor1).convert_alpha()
        self.target_cursor = pygame.image.load(cursor2).convert_alpha()
        self.idle_cursor = pygame.transform.scale(self.idle_cursor, (32, 32))
        self.target_cursor = pygame.transform.scale(self.target_cursor,
                                                    (32, 32))

        self.true_scroll = [0, 0]
        self.scroll = self.true_scroll.copy()

        self.room = Room(self.display, 2000, 5)

        self.player = entity.Player(self.room, weapons.Pistol(),
                                    powerups.PowerUp)
        entity.Player.powerups = powerups.PowerUp.powerups
        entity.Player.guns = weapons.Gun.guns

    def run(self, dt, state):
        self.update_camera()
        self.timer += 1

        self.screen.blit(self.display, (0, 0))
        self.display.fill(constants.COLOURS['black'])

        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouseVector = self.m_input.process_events(mouse_pressed, pos)
        player_angle = self.player.realVector.degree(mouseVector)

        for enemy in entity.Enemy.enemies:
            if self.mouse_interaction(mouseVector, enemy.surf,
                                      enemy.realVector - enemy.size / 2):
                self.cursor_state = 'Target'
                break
        else:
            self.cursor_state = 'Idle'

        if self.cursor_state == 'Idle':
            self.draw_cursor(self.idle_cursor, pos)
        else:
            self.draw_cursor(self.target_cursor, pos)

        self.room.draw_field(self.scroll)
        self.room.draw_chests(self.scroll)
        self.room.draw_equippables(self.scroll)
        if (self.timer / 60) > 0:
            self.room.draw_enemies(self.player, self.scroll, dt)
            self.room.collision()

        weapons.Bullet.draw(self.display, dt, self.scroll, self.room.size)
        weapons.Bullet.explode_bullets(self.display, self.scroll)

        mouse = self.m_input.button_pressed
        key_pressed = pygame.key.get_pressed()
        self.player.process_keys(self.display, key_pressed, self.scroll)

        self.player.draw(self.display, player_angle, self.scroll)
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
        self.scroll[0] = round(self.true_scroll[0])
        self.scroll[1] = round(self.true_scroll[1])
