import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coord(self):
        return (self.x, self.y)

    def __add__(self, num):
        if isinstance(num, Vector):
            x = self.x + num.x
            y = self.y + num.y
        else:
            x = self.x + num
            y = self.y + num
        return Vector(x, y)

    def __sub__(self, num):
        if isinstance(num, Vector):
            x = self.x - num.x
            y = self.y - num.y
        else:
            x = self.x - num
            y = self.y - num
        return Vector(x, y)

    def __mul__(self, num):
        if isinstance(num, Vector):
            x = self.x * num.x
            y = self.y * num.y
        else:
            x = self.x * num
            y = self.y * num
        return Vector(x, y)

    def __truediv__(self, num):
        if isinstance(num, Vector):
            x = self.x / num.x
            y = self.y / num.y
        else:
            x = self.x / num
            y = self.y / num
        return Vector(x, y)

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2))

    def distance(self, vector):
        return math.sqrt(((self.x - vector.x) ** 2) + ((self.y - vector.y) ** 2))

    def normalize(self):
        mag = self.magnitude()
        normalized = self / mag
        return normalized

    def degree(self, vector):
        return math.degrees(math.atan2(self.y - vector.y, self.x - vector.x))

    def rotate(self, origin, angle):
        angle = math.radians(angle)
        origin = origin
        originPoint = self - origin

        rotatedX = originPoint.x * math.cos(angle) - originPoint.y * math.sin(
            angle)
        rotatedY = originPoint.x * math.sin(angle) + originPoint.y * math.cos(
            angle)

        return round(rotatedX + origin.x), round(rotatedY + origin.y)

    def __str__(self):
        return f'({self.x}, {self.y})'
