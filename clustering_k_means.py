import math
import copy
from xlwt import Workbook
from math import sqrt
import re
import os
import random
import xml.etree.ElementTree as ET

from common_modules import Building_Number, read_data_from_xls

class K_means:

    def __init__(self, centers):
        # Param
        # centers : (list of Building_number) centers of each cluster
        self.centers = centers
        self.n_centers = len(centers)

        # self.groups stores buildings belonging to each cluster
        self.groups = None
        self.clear_groups()


    def clear_groups(self):
        self.groups = []
        for i in range(self.n_centers):
            self.groups.append([])
        # self.n_buildings = [0] * self.n_centers

    def get_n_centers(self):
        return self.n_centers

    def get_centers(self):
        return self.centers

    def add_to_group(self, index_of_group, building):
        self.groups[index_of_group].append(building)

    def find_groups(self, buildings):
        # categorize buildings into different groups
        for building in buildings:
            distances = list(map(Building_Number.find_distance, [building] * len(self.centers), self.centers))
            winner_index = distances.index(min(distances))
            print("winner index: {}, building: {}".format(winner_index, building))
            self.add_to_group(winner_index, building)

    def find_closest_three(self, index):
        # find the closest three weights from one weight and calculate the average distance
        distances = list(map(Building_Number.find_distance, [self.centers[index]] * len(self.centers),
                             self.centers))
        return sum(distances[1:3]) / 3

    def find_standard_deviation(self, index):
        # calculate the standard deviation of self.groups[index]
        if len(self.groups[index]) == 0:
            return -1
        sum_std_dev = 0
        for building in self.groups[index]:
            sum_std_dev += Building_Number.find_distance(building, self.centers[index]) ** 2
        return sum_std_dev / len(self.groups[index])

    def update(self):
        # update centers based on self.groups
        for i in range(len(self.groups)):
            if len(self.groups[i]) == 0:
                continue
            x_sum = 0
            y_sum = 0
            real_x_sum = 0
            real_y_sum = 0
            for building in self.groups[ i ]:
                x_sum += building.get_x()
                y_sum += building.get_y()
                real_x_sum += building.get_real_x()
                real_y_sum += building.get_real_y()

            self.centers[i].set_x(x_sum / len(self.groups[ i ]) )
            self.centers[i].set_y(y_sum / len(self.groups[ i ]) )
            self.centers[i].set_real_x(real_x_sum / len(self.groups[ i ]) )
            self.centers[i].set_real_y(real_y_sum / len(self.groups[ i ]) )

from constants import GEO_COORDINATE_PATH
RADIUS = 5
T = 200 # iteration time
RESULT_DIR = 'division_K_means'
####################################################################################
if __name__ == '__main__':
    hamlets = os.listdir(GEO_COORDINATE_PATH)
    for hamlet in hamlets:
        if len(re.findall('.xls', hamlet)) == 0:
            continue
        print("In {}".format(hamlet.removesuffix('.xls')))
        buildings = read_data_from_xls(GEO_COORDINATE_PATH + '/' + hamlet)
        n_divide = int(len(buildings) / 5)
        ob = K_means(copy.deepcopy(random.sample(buildings, min(n_divide, len(buildings)))))

        # k-means algorithm
        print("k-means")
        for i in range(T):
            ob.find_groups(buildings)
            ob.update()
            ob.clear_groups()

        print("end finding")
        ob.find_groups(buildings)
        clustering_xml = ET.Element('root')
        # color the buildings and centers
        for i in range(len(ob.groups)):
            x = ob.centers[i].get_x()
            y = ob.centers[i].get_y()
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
        sheet_num_hamlets = wb.add_sheet('Hamlets')
        sheet_standard_dev = wb.add_sheet("Standard Deviation")
        sheet_distance = wb.add_sheet("Average distances")

        n_col = sqrt(n_divide)
        for i in range(n_divide):
            sheet_num_hamlets.write(math.floor(i / n_col), int(i % n_col), len(ob.groups[i]))
            sheet_standard_dev.write(math.floor(i / n_col), int(i % n_col), ob.find_standard_deviation(i))
            sheet_distance.write(math.floor(i / n_col), int(i % n_col), ob.find_closest_three(i))

        wb.save(matrix_path)

        print("Finished")