# hierarchical clustering using single linkage method
import xlrd
from math import sqrt
import re
import os
import xml.etree.ElementTree as ET

from constants import GEO_COORDINATE_PATH

from common_modules import Building_Number, read_data_from_xls

class point_pair:
    # class of point pairs for sorting
    def __init__(self, u, u_id, v, v_id):
        self.u = u
        self.v = v
        self.u_id = u_id
        self.v_id = v_id
        self.distance = Building_Number.find_distance(u, v)

    def __lt__(self, other):
        return self.distance < other.distance

class Single_linkage:

    def __init__(self, buildings):

        self.buildings = buildings
        self.n_clusters = len(buildings)
        self.direct_fathers = []
        self.fathers = [] # used in disjoint-set
        self.children = [] # children of each group
        for i in range(2 * len(buildings)):
            self.direct_fathers.append(-1)
            self.fathers.append(-1)
            self.children.append([])

        self.pairs = []
        for i in range(len(buildings)):
            for j in range(i+1, len(buildings)):
                self.pairs.append(point_pair(buildings[i], i, buildings[j], j))
        self.pairs.sort()
        self.top = None

    def find_father(self, index):
        if self.direct_fathers[index] == -1:
            return index
        else:
            self.fathers[index] = self.find_father(self.fathers[index])
            return self.fathers[index]

    def merge(self, a, b):
        b_father = self.find_father(b)
        a_father = self.find_father(a)
        # create a new node
        new_index = 2 * len(self.buildings) - self.n_clusters
        # merge node a and b into the new node
        self.direct_fathers[b_father] = new_index
        self.direct_fathers[a_father] = new_index
        self.fathers[b_father] = new_index
        self.fathers[a_father] = new_index
        self.children[new_index].append(b_father)
        self.children[new_index].append(a_father)
        self.n_clusters -= 1

    def update(self):
        while(self.n_clusters > 1):
            # choose the shortest point pair
            pair = self.pairs[0]
            self.pairs.pop(0)
            u_id = pair.u_id
            v_id = pair.v_id

            # find if they have already merged
            if self.find_father(u_id) == self.find_father(v_id):
                continue
            else:
                self.merge(u_id,v_id)
                if self.n_clusters == 1:
                    self.top = self.find_father(u_id)

    def generate_xml_tree(self):
        root = ET.Element('root')
        self.dfs_xml_tree(self.top, root)
        return ET.tostring(root)

    def dfs_xml_tree(self, node_id, father):
        if node_id < len(self.buildings): # if the node is a building
            node = self.buildings[node_id]
            entry = ET.SubElement(father, 'Building')
            entry.set('ID', str(node.get_id()))
            entry.set('X', str(node.get_x()))
            entry.set('Y', str(node.get_y()))
            entry.set('Longitude', str(node.get_real_x()))
            entry.set('Latitude', str(node.get_real_y()))
            entry.set('Prefix', node.get_prefix())
            entry.set('Suffix', node.get_suffix())
        else:
            entry = ET.SubElement(father, "Group")
            entry.set('ID', str(node_id - len(self.buildings)))
            for child in self.children[node_id]:
                self.dfs_xml_tree(child, entry)
        # if len(self.children[node_id]) > 0:
        #     children_entry = ET.SubElement(entry, 'Children')
        #     for child in self.children[node_id]:
        #         self.dfs_xml_tree(child, children_entry)

RESULT_DIR = 'division_hierarchical_clustering'
####################################################################################

if __name__ == '__main__':
    hamlets = os.listdir(GEO_COORDINATE_PATH)
    for hamlet in hamlets:
        if len(re.findall('.xls', hamlet)) == 0:
            continue
        print("In {}".format(hamlet.removesuffix('.xls')))
        buildings = read_data_from_xls(GEO_COORDINATE_PATH + '/' + hamlet)

        # hierarchical clustering
        single_linkage = Single_linkage(buildings)
        single_linkage.update()

        # save as xml tree
        xml_path = RESULT_DIR + '/' + hamlet.removesuffix('.xls') + '_detailed.xml'
        xml_tree = single_linkage.generate_xml_tree()

        with open(xml_path, 'w') as f:
            f.write(xml_tree.decode('utf-8'))
