import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt((x ^ 2) + (y ^ 2))

    def distance(self, vector):
        return math.sqrt(math.exp(self.x - vector.x, 2) + math.exp(self.y - vector.y, 2))

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y

    def normalize(self):
        mag = self.magnitude()
        x = self.x / mag
        y = self.y / mag
        return  Vector2D(x,y)

    def __str__(self):
        return f'({self.x}, {self.y})'
