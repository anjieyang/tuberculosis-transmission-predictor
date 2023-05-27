import math


class Building:
    def __init__(self, id, x, y, prefix=None, suffix=None, from_range=None, range_value=None, category=None, longitude=None, latitude=None):
        self.id = id
        self.x = x
        self.y = y
        self.prefix = prefix
        self.suffix = suffix
        self.from_range = from_range
        self.range_value = range_value
        self.category = category
        self.longitude = longitude
        self.latitude = latitude

    def get_distance(self, building):
        sub = self - building
        return math.sqrt(pow(sub.x, 2) + pow(sub.y, 2))

    def __sub__(self, point):
        return Building(
            id=None,
            x=self.x - point.x,
            y=self.y - point.y,
            longitude=self.longitude - point.longitude,
            latitude=self.latitude - point.latitude,
        )

    def __add__(self, point):
        return Building(
            id=None,
            x=self.x + point.x,
            y=self.y + point.y,
            longitude=self.longitude + point.longitude,
            latitude=self.latitude + point.latitude,
        )

    def __mul__(self, value):
        return Building(
            id=None,
            x=self.x * value,
            y=self.y * value,
            longitude=self.longitude * value,
            latitude=self.latitude * value,
        )