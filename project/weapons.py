class Weapon:
    pass

class Bullet:
    bullets = []

    def __init__(self, x, y):
        self.x self.y = x, y

    def draw(self, screen):
        for bullet in bullets:
            pygame.draw.rect(screen, color, pygame.Rect(40, 10, self.x, self.y))
