class Weapon:
    pass

class Bullet:
    def __init__(self, x, y):
        self.x self.y = x, y

    def draw(self, screen):
        pygame.draw.rect(screen, color, pygame.Rect(40, 10, self.x, self.y))
