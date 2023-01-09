import math
import numpy as np


class Building:
    def __init__(
        self,
        building_num,
        x,
        y,
        longitude,
        latitude,
        prefix=None,
        suffix=None,
        from_range=False,
        range=None,
        category="valid",
    ):
        self.building_num = building_num
        self.x = x
        self.y = y
        self.prefix = prefix
        self.suffix = suffix
        self.category = category
        self.longitude = longitude
        self.latitude = latitude
        self.from_range = from_range
        self.range = range
        self.category = category
        self.id = Building.xstr(prefix) + str(building_num) + Building.xstr(suffix)

    # Rewrite print, +, -, *, / functions
    def __str__(self):
        return "ID = {}| X,Y = ({},{})| Category is {}".format(
            self.id, self.x, self.y, self.category
        )

    def __sub__(self, point):
        return Building(
            building_num=None,
            x=self.x - point.x,
            y=self.y - point.y,
            longitude=self.longitude - point.longitude,
            latitude=self.latitude - point.latitude,
        )

    def __add__(self, point):
        return Building(
            building_num=None,
            x=self.x + point.x,
            y=self.y + point.y,
            longitude=self.longitude + point.longitude,
            latitude=self.latitude + point.latitude,
        )

    def __mul__(self, value):
        return Building(
            building_num=None,
            x=self.x * value,
            y=self.y * value,
            longitude=self.longitude * value,
            latitude=self.latitude * value,
        )

    def get_building_num(self):
        return self.building_num

    @staticmethod
    def get_euclidean_distance(point1, point2):
        # The Euclidean distance between two points
        sub = point1 - point2
        # Return math.sqrt(pow(sub.longitude,2) + pow(sub.latitude, 2))
        return math.sqrt(pow(sub.x, 2) + pow(sub.y, 2))

    def xstr(s):
        return "" if s is None or s == "None" else str(s)

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def get_building_distance_matrix(building_list):
    '''
    Returns a matrix containing the distance of two buildings
    :param building_list: A list of buildings, each building belongs to the Building class
    :return: A numpy matrix which contains the distance of two buildings
    '''
    data_size = len(building_list)
    building_distance_matrix = np.zeros([data_size, data_size])
    for i in range(data_size):
        for j in range(data_size):
            building_distance_matrix[i][j] = Building.get_euclidean_distance(
                building_list[i], building_list[j]
            )
    return building_distance_matrix
