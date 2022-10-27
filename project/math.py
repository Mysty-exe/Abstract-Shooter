import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coord(self):
        return (self.x, self.y)

    def __add__(self, num):
        if isinstance(num, Vector):
            self.x += num.x
            self.y += num.y
        else:
            self.x += num
            self.y += num
        return Vector(self.x, self.y)

    def __sub__(self, num):
        if isinstance(num, Vector):
            self.x -= num.x
            self.y -= num.y
        else:
            self.x -= num
            self.y = num
        return Vector(self.x, self.y)

    def __mul__(self, num):
        if isinstance(num, Vector):
            self.x *= num.x
            self.y *= num.y
        else:
            self.x *= num
            self.y *= num
        return Vector(self.x, self.y)

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2))

    def distance(self, vector):
        return math.sqrt(
            math.exp(self.x - vector.x, 2) + math.exp(self.y - vector.y, 2))

    def normalize(self):
        mag = self.magnitude()
        x = self.x / mag
        y = self.y / mag
        return Vector(x, y)

    def degree(self, vector):
        return math.degrees(math.atan2(self.y - vector.y, self.x - vector.x))

    def __str__(self):
        return f'({self.x}, {self.y})'
