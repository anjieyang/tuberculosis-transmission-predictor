#
# by Yue Zhang
import math
import copy
from xlwt import Workbook
from math import sqrt
import re
import os
import random
import xml.etree.ElementTree as ET

from common_modules import Building_Number, read_data_from_xls

class SOM:
    # SOM class
    def __init__(self, weights, learning_rate):
        # Param
        # weights: (list of Building_number) initial weights
        # learning_rate: (float) initial learning rate
        self.weights = weights
        self.learning_rate = learning_rate
        self.groups = []
        for i in range(len(weights)):
            self.groups.append([])

    def find_winner_index(self, sample):
        # find the closest weight to sample and return its index
        distances = list(map(Building_Number.find_distance, [sample] * len(self.weights), self.weights ))
        winner_index = distances.index(min(distances))
        return winner_index

    def add_count(self, index, building):
        self.groups[index].append(building)

    def find_winner_and_update(self, sample, r):
        # find the winner
        winner_index = self.find_winner_index(sample)
        # update
        # r = 0
        self.weights[winner_index] += (sample - self.weights[winner_index]) * self.learning_rate * (1-r)

    def find_closest_three(self, index):
        # find the closest three weights from one weight and calculate the average distance
        distances = list(map(Building_Number.find_distance, [self.weights[index]] * len(self.weights), self.weights))
        return sum(distances[1:3]) / 3

    def clear_groups(self):
        self.groups = []
        for i in range(len(self.weights)):
            self.groups.append([])

    def find_groups(self, buildings):
        self.clear_groups()
        for building in buildings:
            winner_index = self.find_winner_index(building)
            self.groups[winner_index].append(building)

    def get_num_groups(self, index):
        return len(self.groups[index])

    def find_standard_deviation(self, index):
        # calculate the standard deviation of self.groups[index]
        if len(self.groups[index]) == 0:
            return -1
        sum_std_dev = 0
        for building in self.groups[index]:
            sum_std_dev += Building_Number.find_distance(building, self.weights[index]) ** 2
        return sum_std_dev / len(self.groups[index])

from constants import GEO_COORDINATE_PATH
N_DIVIDE = 25
LEARNING_RATE = 0.03
RADIUS = 5
T = 5 # times of iteration
RESULT_DIR = 'division_SOM'
####################################################################################

if __name__ == '__main__':
    hamlets = os.listdir(GEO_COORDINATE_PATH)
    for hamlet in hamlets:
        if len(re.findall('.xls', hamlet)) == 0:
            continue
        print("In {}".format(hamlet.removesuffix('.xls')))
        buildings = read_data_from_xls(GEO_COORDINATE_PATH + '/' + hamlet)
        ob = SOM(copy.deepcopy(random.sample(buildings, min(N_DIVIDE, len(buildings)))),
                 LEARNING_RATE)

        # SOM
        for i in range(T):
            for building in buildings:
                ob.find_winner_and_update(building, i / T)
        ob.find_groups(buildings)

        # color the buildings
        clustering_xml = ET.Element('root')
        # color the buildings and centers
        for i in range(len(ob.groups)):
            # x = ob.weights[i].get_x()
            # y = ob.weights[i].get_y()
            entry = ET.SubElement(clustering_xml, 'Cluster')
            entry.set("ID", str(i))
            for building in ob.groups[i]:
                id = building.get_id()
                x = building.get_x()
                y = building.get_y()
                real_x = building.get_real_x()
                real_y = building.get_real_y()
                prefix = building.get_prefix()
                suffix = building.get_suffix()
                entry_building = ET.SubElement(entry, 'Building')
                entry_building.set('ID', str(id))
                entry_building.set('X', str(x))
                entry_building.set('Y', str(y))
                entry_building.set('Longitude', str(real_x))
                entry_building.set('Latitude', str(real_y))
                entry_building.set('Prefix', prefix)
                entry_building.set('Suffix', suffix)

        # save data
        xml_path = RESULT_DIR + '/' + hamlet.removesuffix('.xls') + '_division.xml'
        with open(xml_path, 'w') as f:
            f.write(ET.tostring(clustering_xml).decode('utf-8'))

        matrix_path = RESULT_DIR + '/' + hamlet
        wb = Workbook()
        sheet_num_buildings = wb.add_sheet('Number of buildings')
        sheet_standard_dev = wb.add_sheet("Standard Deviation")
        sheet_distance = wb.add_sheet("Average distances")
        n_col = sqrt(N_DIVIDE)

        for i in range(N_DIVIDE):
            sheet_num_buildings.write(math.floor(i / n_col), int(i % n_col), ob.get_num_groups(i))
            sheet_standard_dev.write(math.floor(i / n_col), int(i % n_col), ob.find_standard_deviation(i))
            sheet_distance.write(math.floor(i / n_col), int(i % n_col), ob.find_closest_three(i))

        wb.save(matrix_path)