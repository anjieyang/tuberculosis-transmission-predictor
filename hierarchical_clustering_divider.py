from xlwt import Workbook
from math import sqrt
import re
import os
import xml.etree.ElementTree as ET
import math

class Node:

    def __init__(self, type, id, father_index=0, rank=0, x=0.0, y=0.0, real_x=0.0, real_y=0.0, prefix=None, suffix=None):
        self.type = type  # 'group' , 'building' or 'center'
        self.id = id
        self.father_index = father_index
        self.rank = rank
        self.children = []

        self.prefix = prefix
        self.suffix = suffix
        self.x = x
        self.y = y
        self.real_x = real_x
        self.real_y = real_y

    def get_type(self):
        return self.type

    def get_x(self):
        return self.x

    def get_id(self):
        return self.id

    def get_y(self):
        return self.y

    def get_real_x(self):
        return self.real_x

    def get_real_y(self):
        return self.real_y

    def get_father(self):
        return self.father_index

    def get_rank(self):
        return self.rank

    def get_prefix(self):
        return self.prefix

    def get_suffix(self):
        return self.suffix

    @staticmethod
    def find_distance(a, b):
        try:
            return sqrt(((a.get_real_x() - b.get_real_x()) ** 2) + ((a.get_real_y() - b.get_real_y()) ** 2))
        except:
            return None

class Divison_tree:

    def __init__(self, file_dir):

        self.nodes = []
        self.build_tree(file_dir)
        self.group_roots = []
        self.group_nodes = []
        self.centers = []

    def build_tree(self, file_dir):
        file = ET.parse(file_dir)
        root = file.getroot()
        self.nodes.append(Node(
            type='group', id=-1, father_index=-1, rank=0
        ))
        for element in root:
            self.dfs_build(element, rank=1, father_index=0)

    def dfs_build(self, element, rank, father_index):
        # print(rank)
        node_type = element.tag
        id = int(element.attrib['ID'])
        if node_type == 'Building':
            x = float(element.attrib['X'])
            y = float(element.attrib['Y'])
            real_x = float(element.attrib['Longitude'])
            real_y = float(element.attrib['Latitude'])
            prefix = element.attrib['Prefix']
            suffix = element.attrib['Suffix']
            node = Node(type='building', id = id, x=x, y=y, real_x=real_x, real_y=real_y, prefix=prefix,
                        suffix=suffix, father_index=father_index, rank=rank)
            self.nodes.append(node)
        else:
            node = Node(type='group', id=id, father_index=father_index, rank=rank)
            self.nodes.append(node)
            current_index = len(self.nodes)-1
            for child in element:
                self.nodes[current_index].children.append(len(self.nodes))
                self.dfs_build(child, rank=rank+1, father_index=current_index)

    def divide(self, cut_rank):
        self.group_roots = []
        self.group_nodes = []
        self.centers = []
        for node in self.nodes:
            if (node.get_type() == 'building' and node.get_rank() <= cut_rank) or \
                    (node.get_type() == 'group' and node.get_rank() == cut_rank):
                self.group_roots.append(node)
                self.group_nodes.append([])
                self.dfs_find_all_group_nodes(len(self.group_nodes)-1, node)
                self.centers.append(self.find_center(len(self.group_nodes) - 1))

    def find_center(self, group_index):
        x_sum = 0
        y_sum = 0
        real_x_sum = 0
        real_y_sum = 0
        for node in self.group_nodes[group_index]:
            x_sum += node.get_x()
            y_sum += node.get_y()
            real_x_sum += node.get_real_x()
            real_y_sum += node.get_real_y()
        center_x = x_sum / len(self.group_nodes[group_index])
        center_y = y_sum / len(self.group_nodes[group_index])
        real_center_x = real_x_sum / len(self.group_nodes[group_index])
        real_center_y = real_y_sum / len(self.group_nodes[group_index])
        return Node(type='center', id=group_index, x=center_x, y=center_y, real_x=real_center_x, real_y=real_center_y)

    def dfs_find_all_group_nodes(self, group_index, node):
        node_type = node.get_type()
        if node_type == 'building':
            self.group_nodes[group_index].append(node)
        else:
            for child_index in node.children:
                self.dfs_find_all_group_nodes(group_index, self.nodes[child_index])

    def get_num_groups(self):
        return len(self.group_nodes)

    def get_num_nodes_of_group(self, index):
        return len(self.group_nodes[index])

    def find_standard_deviation(self, index):
        sum_std_dev = 0
        for node in self.group_nodes[index]:
            sum_std_dev += Node.find_distance(node, self.centers[index]) ** 2
        return sum_std_dev / self.get_num_nodes_of_group(index)

    def find_closest_three(self, index):
        # find the closest three weights from one weight and calculate the average distance
        distances = list(map(Node.find_distance, [self.centers[index]] * len(self.centers),
                             self.centers))
        return sum(distances[1:3]) / 3



DATA_PATH = 'division_hierarchical_clustering'
RESULT_DIR = 'division_hierarchical_clustering'
RADIUS = 5
CUT_RANK = 30

if __name__ == '__main__':
    hamlets = os.listdir(DATA_PATH)
    for hamlet in hamlets:
        if len(re.findall('_detailed.xml', hamlet)) == 0:
            continue
        print("In {}".format(hamlet.removesuffix('.xls')))

        division_tree = Divison_tree(file_dir=DATA_PATH+'/'+hamlet)
        division_tree.divide(cut_rank=CUT_RANK)

        clustering_xml = ET.Element('root')
        for i in range(len(division_tree.group_nodes)):
            entry = ET.SubElement(clustering_xml, 'Cluster')
            entry.set("ID", str(i))
            for building in division_tree.group_nodes[i]:
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

        xml_path = RESULT_DIR + '/' + hamlet.removesuffix('_detailed.xml') + '_division.xml'
        with open(xml_path, 'w') as f:
            f.write(ET.tostring(clustering_xml).decode('utf-8'))

        matrix_path = RESULT_DIR + '/' + hamlet.removesuffix('_detailed.xml') + '.xls'
        wb = Workbook()
        sheet_num_hamlets = wb.add_sheet('Hamlets')
        sheet_standard_dev = wb.add_sheet("Standard Deviation")
        sheet_distance = wb.add_sheet("Average distances")

        n_divide = division_tree.get_num_groups()
        n_col = sqrt(n_divide)
        for i in range(n_divide):
            sheet_num_hamlets.write(math.floor(i / n_col), int(i % n_col), division_tree.get_num_nodes_of_group(i))
            sheet_standard_dev.write(math.floor(i / n_col), int(i % n_col), division_tree.find_standard_deviation(i))
            sheet_distance.write(math.floor(i / n_col), int(i % n_col), division_tree.find_closest_three(i))

        wb.save(matrix_path)