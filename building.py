import math
import numpy as np


class Building:
    """
    A class to represent a building.

    Attributes:
        building_num (int): The building number.
        x (float): The x coordinate of the building.
        y (float): The y coordinate of the building.
        longitude (float): The longitude of the building.
        latitude (float): The latitude of the building.
        prefix (str, optional): The prefix of the building ID.
        suffix (str, optional): The suffix of the building ID.
        from_range (bool, optional): Whether the building is from a range.
        range (str, optional): The range of the building.
        category (str, optional): The category of the building.

    Methods:
        __str__(): Returns a string representation of the building.
        __sub__(point): Returns a new building with the x and y coordinates subtracted by the given point.
        __add__(point): Returns a new building with the x and y coordinates added by the given point.
        __mul__(value): Returns a new building with the x and y coordinates multiplied by the given value.
        get_building_num(): Returns the building number.
        get_euclidean_distance(point1, point2): Returns the Euclidean distance between two points.
        xstr(s): Returns an empty string if s is None or "None", otherwise returns s.
        get_longitude(): Returns the longitude of the building.
        get_latitude(): Returns the latitude of the building.
        get_x(): Returns the x coordinate of the building.
        get_y(): Returns the y coordinate of the building.
    """
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
    """
    Calculates the Euclidean distance between all pairs of buildings in a given list of buildings.

    Parameters:
        building_list (list): A list of Building objects representing buildings on a map.

    Returns:
        numpy.ndarray: A 2D numpy array of shape (n, n) where n is the number of buildings in building_list.
                       The value at the i-th row and j-th column represents the Euclidean distance between the
                       i-th and j-th buildings in the list.
    """
    data_size = len(building_list)
    building_distance_matrix = np.zeros([data_size, data_size])
    for i in range(data_size):
        for j in range(data_size):
            building_distance_matrix[i][j] = Building.get_euclidean_distance(
                building_list[i], building_list[j]
            )
    return building_distance_matrix
