import pygame
import random, math
import project.constants as constants
import project.events as e
import project.weapons as weapons
import project.powerups as powerups
import project.characters as entity
from project.room import Room
from project.ui import GameUI, MenuUI, Button

class View:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)

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
            powerups.Heart(),
            powerups.BulletSpeed(),
            powerups.PlayerSpeed(),
            powerups.Ammo(),
            powerups.Shield(),
            powerups.TwoGuns()
        ]

        pygame.mouse.set_visible(False)
        self.display = pygame.Surface((self.width, self.height))
        self.blanket = pygame.Surface((self.width, self.height))
        self.trans_state = None
        self.blacken_var = 0

        self.timer = 0
        self.difficulty = 'Very Easy'

        self.m_input = e.MouseInput()

        cursor1, cursor2 = 'assets/idle_cursor.png', 'assets/target_cursor.png'
        self.cursor_state = 'Idle'

        self.idle_cursor = pygame.image.load(cursor1).convert_alpha()
        self.target_cursor = pygame.image.load(cursor2).convert_alpha()
        self.idle_cursor = pygame.transform.scale(self.idle_cursor, (32, 32))
        self.target_cursor = pygame.transform.scale(self.target_cursor,
                                                    (32, 32))

        self.true_scroll = [0, 0]
        self.scroll = self.true_scroll.copy()
        self.screenshake = 0

        self.menu_ui = MenuUI(self.display)
        self.game_ui = GameUI(self.display)

        self.play_btn = Button(self.display, 'Play')
        self.main_menu_btn = Button(self.display, 'Main Menu')
        self.quit_btn = Button(self.display, 'Quit')

        self.room = Room(self.display, 2000, self.difficulty)

        self.player = entity.Player(self.room, weapons.Pistol(), powerups.PowerUp)
        entity.Player.powerups = powerups.PowerUp.powerups
        entity.Player.guns = weapons.Gun.guns

    def reset(self):
        self.timer = 0

        self.room = Room(self.display, 2000, self.difficulty)

        self.player = entity.Player(self.room, weapons.Pistol(), powerups.PowerUp)
        entity.Player.powerups = powerups.PowerUp.powerups
        entity.Player.guns = weapons.Gun.guns
        entity.Enemy.enemies.clear()
        entity.Enemy.enemy_exploding.clear()
        weapons.Bullet.enemy_bullets.clear()
        weapons.Bullet.player_bullets.clear()
        weapons.Bullet.bullets_exploding.clear()

    def transition(self, state):

        pygame.mouse.set_visible(True)
        self.screen.blit(self.display, (0, 0))
        self.blacken_var += 5

        self.blanket.set_alpha(self.blacken_var)
        self.display.blit(self.blanket, (0,0))

        if self.blacken_var == 255:
            self.trans_state = 'Lighten'
            state = state.split()[-1]

        return state

    def main_menu(self, state, events):

        pygame.mouse.set_visible(True)

        if self.trans_state == 'Lighten':
            self.blacken_var -= 5

        self.screen.blit(self.display, (0, 0))
        self.display.fill(constants.COLOURS['grey'])

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pressed = True

        self.menu_ui.draw_title()
        play = self.play_btn.draw((self.width / 2 - (self.play_btn.btn_width / 2), (self.height / 2) - 20), pygame.mouse.get_pos(), pressed)
        quit = self.quit_btn.draw((self.width / 2 - (self.play_btn.btn_width / 2), (self.height / 2) + 110), pygame.mouse.get_pos(), pressed)

        self.blanket.set_alpha(self.blacken_var)
        self.display.blit(self.blanket, (0,0))

        if not self.blacken_var and self.trans_state == 'Lighten':
            self.trans_state = None

        if play:
            self.reset()
            state = 'Transition - Game'

        elif quit:
            state = 'Quit'

        return state

    def run(self, dt, state, events):

        pygame.mouse.set_visible(False)
        self.update_camera()
        self.timer += 1
        self.update_difficulty(self.timer)

        render_offset = [0, 0]
        if self.screenshake > 0:
            self.screenshake -= 1
            render_offset[0] = random.randint(0, 16) - 8
            render_offset[1] = random.randint(0, 16) - 8

        if self.trans_state == 'Lighten':
            self.blacken_var -= 5

        self.screen.blit(self.display, render_offset)
        self.display.fill(constants.COLOURS['black'])

        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouseVector = self.m_input.process_events(mouse_pressed, pos)
        player_angle = self.player.realVector.degree(mouseVector)

        for enemy in entity.Enemy.enemies:
            if self.mouse_interaction(mouseVector, enemy.surf, enemy.realVector - enemy.size / 2):
                self.cursor_state = 'Target'
                break
        else:
            self.cursor_state = 'Idle'

        if self.cursor_state == 'Idle':
            self.draw_cursor(self.idle_cursor, pos)
        else:
            self.draw_cursor(self.target_cursor, pos)

        self.room.draw_field(self.scroll)
        self.room.draw_obstacles(self.scroll)
        self.room.draw_chests(self.scroll)
        self.room.draw_equippables(self.scroll)
        self.room.collision(self.player)
        if (self.timer / 60) > 5:
            if not self.room.spawn_cooldown:
                self.room.spawn()
                self.room.spawn_cooldown = self.room.spawn_interval
            self.room.draw_enemies(self.player, self.scroll, dt)
            self.room.spawn_cooldown -= 1

        weapons.Bullet.draw(self.display, dt, self.scroll, self.room.size)
        weapons.Bullet.explode_bullets(self.display, self.scroll)

        mouse = self.m_input.button_pressed
        key_pressed = pygame.key.get_pressed()
        self.player.process_keys(self.display, key_pressed, self.difficulty, self.scroll)

        self.player.draw(self.display, player_angle, self.room.obstacles, self.scroll)
        self.player.draw_line(self.display, mouseVector, self.scroll)

        self.player.move(mouseVector, self.room.obstacles, dt, self.scroll)
        self.player.hit_obstacle(self.room.obstacles)
        self.player.shoot(mouse, mouseVector, self.scroll)
        weapons.Bullet.enemy_bullets, self.screenshake = self.player.shot(weapons.Bullet.enemy_bullets, self.screenshake)

        self.player.listen_powerups()

        self.game_ui.display_timer(self.get_time(self.timer))
        self.game_ui.display_difficulty(self.difficulty)
        self.game_ui.display_ammo(self.player.gun.ammo, self.player.gun.max_ammo)
        self.game_ui.display_health(self.player.lives)
        self.game_ui.display_kills(self.player.kills)
        self.game_ui.display_powerups(self.player.active_powerups)

        self.blanket.set_alpha(self.blacken_var)
        self.display.blit(self.blanket, (0,0))

        if not self.blacken_var and self.trans_state == 'Lighten':
            self.trans_state = None

        if self.player.lives == 0:
            state = 'Game Over'

        return state

    def pause(self, state, events):
        pygame.mouse.set_visible(True)

        self.screen.blit(self.display, [0, 0])
        self.game_ui.draw_paused()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('yes') 
                    self.paused = False
                    state = 'Game'

        return state

    def game_over(self, dt, state, events):
        pygame.mouse.set_visible(True)

        render_offset = [0, 0]
        if self.screenshake > 0:
            self.screenshake -= 1
            render_offset[0] = random.randint(0, 16) - 8
            render_offset[1] = random.randint(0, 16) - 8

        self.screen.blit(self.display, render_offset)
        self.display.fill(constants.COLOURS['black'])

        self.room.draw_field(self.scroll)
        self.room.draw_chests(self.scroll)
        self.room.draw_equippables(self.scroll)

        self.room.draw_enemies(self.player, self.scroll, dt, no=True)
        self.room.collision(self.player)

        weapons.Bullet.draw(self.display, dt, self.scroll, self.room.size)
        weapons.Bullet.explode_bullets(self.display, self.scroll)

        self.player.self_explode(self.display, self.scroll)

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pressed = True

        self.game_ui.draw_end()
        main_menu = self.main_menu_btn.draw((self.width / 2 - (self.main_menu_btn.btn_width / 2), self.height / 2), pygame.mouse.get_pos(), pressed)

        if main_menu:
            state = 'Transition - Menu'

        return state

    def update_camera(self):
        x, y = self.player.vector.x, self.player.vector.y
        width, height = self.width / 2, self.height / 2
        self.true_scroll[0] += (x - self.scroll[0] - width) / 15
        self.true_scroll[1] += (y - self.scroll[1] - height) / 15
        self.scroll[0] = round(self.true_scroll[0])
        self.scroll[1] = round(self.true_scroll[1])

    
    def update_difficulty(self, ms):
        min = math.floor(ms / 3600)
        if min < 2:
            return 'Very Easy'
        elif 2 > min > 4:
            return 'Lightwork'
        elif 4 > min > 6:
            return 'Moderate'
        elif 6 > min > 8:
            return 'Hard'
        elif 8 > min > 10:
            return 'Challenging'
        elif 10 > min > 15:
            return 'Near Impossible'
        elif 15 > min > 20:
            return 'Impossible'

    def get_time(self, ms):
        min = math.floor(ms / 3600)
        min_secs = min * 3600
        ms_left = ms - min_secs
        secs = math.floor(ms_left / 60)
        return f'{min:02}:{secs:02}'        
