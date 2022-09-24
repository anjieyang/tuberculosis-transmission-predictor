# from distutils.command.build import build
import numpy as np
import pandas as pd
import math


class Building:
    def __init__(self, building_num, x, y, longitude, latitude, prefix=None, suffix=None, from_range=False, range=None,
                 category='valid'):
        '''
        :param 
        :param 
        :param 
        :return: 
        '''
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

    # rewrite print, +, -, *, / functions
    def __str__(self):
        return "ID = {}| X,Y = ({},{})| Category is {}".format(self.id, self.x, self.y, self.category)

    def __sub__(self, point):
        return Building(building_num=None, x=self.x - point.x, y=self.y - point.y,
                        longitude=self.longitude - point.longitude, latitude=self.latitude - point.latitude)

    def __add__(self, point):
        return Building(building_num=None, x=self.x + point.x, y=self.y + point.y,
                        longitude=self.longitude + point.longitude, latitude=self.latitude + point.latitude)

    def __mul__(self, value):
        return Building(building_num=None, x=self.x * value, y=self.y * value, longitude=self.longitude * value,
                        latitude=self.latitude * value)

    # def __truediv__ (self, value):
    #     return Building(building_num=None, x=self.x/value, y=self.y/value, longitude=self.longitude/value, latitude=self.latitude/value)

    @staticmethod
    def Euclidean_dist(point1, point2):
        # the Euclidean distance between two points
        sub = point1 - point2
        # return math.sqrt(pow(sub.longitude,2) + pow(sub.latitude, 2))
        return math.sqrt(pow(sub.x, 2) + pow(sub.y, 2))

    def xstr(s):
        return '' if s is None or s == 'None' else str(s)

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def get_data(read_path, map_name):
    '''
    read all values of all buildings
    :param read_path: the path of target file
    :param map_name: the name of target file
    :return: a list of buildings, each building belongs to Building class
    '''

    df = pd.read_excel(read_path + '/' + map_name)
    data_size = len(df)
    building_lst = []

    for i in range(data_size):
        if df["Category"][i] == 'valid':
            building_id = df["Building Number"][i]
            x = df["X"][i]
            y = df["Y"][i]
            prefix = df["Prefix"][i]
            suffix = df["Suffix"][i]
            from_range = df["From a Range?"][i]
            range_value = df["Range"][i]
            longitude = df["Longitude"][i]
            latitude = df["Latitude"][i]

            building_lst.append(
                Building(building_num=building_id, x=x, y=y, longitude=longitude, latitude=latitude, prefix=prefix,
                         suffix=suffix, from_range=from_range, range=range_value))

    return building_lst


def dist_matrix(building_lst):
    '''
    read all values of all buildings
    :param building_lst: a list of buildings, each building belongs to Building class
    :return: a numpy matrix, contains the distance of two buildings
    '''
    data_size = len(building_lst)
    dist_matrix = np.zeros([data_size, data_size])
    for i in range(data_size):
        for j in range(data_size):
            dist_matrix[i][j] = Building.Euclidean_dist(building_lst[i], building_lst[j])
    return dist_matrix


# def find_adjacency(cluster_centers):
#     adjacency_list = {}
#     for center in cluster_centers:
#         if center not in adjacency_list:
#             adjacency_list[center] = []
#         for other_center in adjacency_list.keys():
#             if other_center == center:
#                 continue
#             relative_distance = math.sqrt(
#                 (other_center.get_x() - center.get_x()) ** 2 + (other_center.get_y() - center.get_y()) ** 2)
#             if relative_distance < 400:
#                 adjacency_list[center].append(other_center)
#                 adjacency_list[other_center].append(center)
#     return adjacency_list

## testing
READ_PATH = "Geo_coordinates"
MAP = "Arctic_Bay.xls"
if __name__ == "__main__":
    building_lst = get_data(READ_PATH, MAP)
