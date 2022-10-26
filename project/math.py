import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coord(self):
        return (self.x, self.y)

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2))

    def distance(self, vector):
        return math.sqrt(
            math.exp(self.x - vector.x, 2) + math.exp(self.y - vector.y, 2))

    def add(self, vector):
        vectorx = self.x + vector.x
        vectory = self.y + vector.y
        return Vector(vectorx, vectory)

    def sub(self, vector):
        vectorx = self.x - vector.x
        vectory = self.y - vector.y
        return Vector(vectorx, vectory)

    def multiply(self, vector):
        vectorx = self.x * vector.x
        vectory = self.y * vector.y
        return Vector(vectorx, vectory)

    def normalize(self):
        mag = self.magnitude()
        x = self.x / mag
        y = self.y / mag
        return Vector(x, y)

    def __str__(self):
        return f'({self.x}, {self.y})'
