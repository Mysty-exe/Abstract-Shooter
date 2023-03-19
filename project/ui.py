import pygame
import project.constants as constants

pygame.init()

class UI:
    def __init__(self, screen):
        self.screen = screen
        
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        self.largefont = pygame.font.Font('fonts/font.ttf', 80)
        self.font = pygame.font.Font('fonts/font.ttf', 60)
        self.smallfont = pygame.font.Font('fonts/font.ttf', 20)
        self.medfont = pygame.font.Font('fonts/font.ttf', 35)
        

class Button(UI):
    def __init__(self, screen, text):
        UI.__init__(self, screen)

        self.text = text
        self.btn_width, self.btn_height = 300, 100

    def draw(self, pos, mouse, clicked):
        button = pygame.Rect(pos[0], pos[1], self.btn_width, self.btn_height)
        color = constants.COLOURS['white']
        pressed = False
        if button.collidepoint(mouse):
             color = constants.COLOURS['black']
             if clicked:
                 pressed = True
	
        txt = self.font.render(self.text, True, color)      
        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), pos[1]))     
        pygame.draw.rect(self.screen, color, button, 2, 3)
  
        return pressed

class MenuUI(UI):
    def __init__(self, screen):
        UI.__init__(self, screen)

    def draw_title(self):
        txt = self.largefont.render('Dungeon', True, constants.COLOURS['white'])
        txt2 = self.largefont.render('Of Cubes', True, constants.COLOURS['white'])
        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), 50))
        self.screen.blit(txt2, ((self.width / 2) - (txt.get_width() / 2), txt.get_height() + 30))

class GameUI(UI):
    def __init__(self, screen):
        UI.__init__(self, screen)

        self.dead_heart = pygame.image.load('assets/dead_heart.png').convert_alpha()
        self.heart = pygame.image.load('assets/heart.png').convert_alpha()
        self.kill_counter = pygame.image.load('assets/death.png').convert_alpha()

        self.dead_heart = pygame.transform.scale(self.dead_heart, (48, 48))
        self.heart = pygame.transform.scale(self.heart, (48, 48))
        self.kill_counter = pygame.transform.scale(self.kill_counter, (48, 48))

    def display_timer(self, time):
        txt = self.font.render(time, True, constants.COLOURS['white'])
        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), 5))

    def display_difficulty(self, difficulty):
        txt = self.smallfont.render(difficulty, True, constants.COLOURS['white'])
        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), self.font.size('00:00')[1] + 20))

    def display_ammo(self, ammo, max):
        txt = self.medfont.render(f'{int(ammo)}/{int(max)}', True, constants.COLOURS['white'])
        self.screen.blit(txt, (((self.font.size('00:00')[0] / 2) + (self.width / 2)) + 25, 25))

    def display_health(self, health):
        for i, num in enumerate(range(50, 251, 50)):
            if i < health:
                self.screen.blit(self.heart, (num, 30))
            else:
                self.screen.blit(self.dead_heart, (num, 30))

    def display_kills(self, kills):
        self.screen.blit(self.kill_counter, ((self.font.size('00:00')[0] / 2 + (self.width / 2)) + 25 + self.medfont.size('32/32')[0] + 40, 30))
        txt = self.medfont.render(f'{kills}', True, constants.COLOURS['white'])
        self.screen.blit(txt, ((self.font.size('00:00')[0] / 2 + (self.width / 2)) + 25 + self.medfont.size('32/32')[0] + 100, 25))

    def display_powerups(self, powerups):
        nums = [x for x in range(540, 0, -50)]
        for num, powerup in zip(nums, powerups):
            txt = self.medfont.render(f'{round(powerup[0].cooldown / 60)}', True, constants.COLOURS['white'])
            self.screen.blit(pygame.transform.scale(powerup[0].image, (48, 48)), (10, num))
            self.screen.blit(txt, (60, num))

    def draw_paused(self):
        txt = self.largefont.render('PAUSED', True, constants.COLOURS['white'])
        txt2 = self.smallfont.render('PRESS ESC TO UPAUSE THE GAME', True, constants.COLOURS['white'])

        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), (self.height / 2) - 100))
        self.screen.blit(txt2, ((self.width / 2) - (txt2.get_width() / 2), (self.height / 2) + (self.largefont.size('ESC')[1] / 2) + 20))

    def draw_end(self):
        txt = self.largefont.render('GAME OVER', True, constants.COLOURS['white'])
        self.screen.blit(txt, ((self.width / 2) - (txt.get_width() / 2), self.height / 4))