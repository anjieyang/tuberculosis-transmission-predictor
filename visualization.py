import math

from pdf_annotate import PdfAnnotator, Appearance, Location
import matplotlib.pyplot as plt
import numpy as np
import colors, k_means, hierarchical
import random
import os
from queue import *

READ_PATH = "geo coordinates"
PDF_PATH = "Clustering"
PDF_NAME = "Arctic_Bay_Building_No_2021_Wall.pdf"
WRITE_PATH = "Clustering"
# MAPS = os.listdir(READ_PATH)
MAP = "Arctic_Bay.xls"
CENTERS_NUM = 30


class Cluster:
    def __init__(self, cluster_id, center, buildings_lst):
        self.cluster_id = cluster_id
        self.buildings_lst = buildings_lst
        self.cluster_size = len(buildings_lst)
        self.center = center

    # TODO:
    def coloring(self, annotator, color, size):
        for building in self.buildings_lst:
            x = building.x
            y = building.y
            id = building.id
            x1 = x - size
            x2 = x + size
            y1 = 3370 - y - size
            y2 = 3370 - y + size
            annotator.add_annotation(annotation_type='square', location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                                     appearance=Appearance(fill=color, stroke_width=0))
            annotator.add_annotation(annotation_type='text', location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                                     appearance=Appearance(content=id, fill=(1, 1, 1), font_size=5))  # black text
            # annotator.add_annotation(annotation_type='text', location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
            #                          appearance=Appearance(content=str(self.cluster_id), fill=(1, 1, 1),
            #                                                font_size=5))  # black text
            # print(x1,y1)

    def bounds(self, annotator):
        pass

    def get_center(self):
        return self.center

    def get_cluster_id(self):
        '''
        this functiion returns the cluster id of the current building
        :param building:
        :return:
        '''
        return self.cluster_id


def get_Clusters_kmean(read_path, map, k=CENTERS_NUM):
    clustering = k_means.clustering(read_path, map, k)
    clusters_lst = []
    for i in range(k):
        center = clustering.center_lst[i]
        groups = clustering.groups[i]
        cluster = Cluster(i, center, groups)
        clusters_lst.append(cluster)
    return clusters_lst


def get_Clusters_hierarchical(read_path, map, k=CENTERS_NUM):
    clustering = hierarchical.clustering(read_path, map, k=CENTERS_NUM)
    clusters_lst = []
    for i in range(k):
        groups = clustering.clusters_lst[i].points
        cluster = Cluster(i, None, groups)
        clusters_lst.append(cluster)
    return clusters_lst


def is_similar(color, recent_colors):
    """
    This function is used to check if there are similar colors in the last 5 used colors.
    :param color: New color in the list of RGB value.
    :param recent_colors: The list of last 5 used colors.
    :return: There are similar colors or not.
    """

    # To avoid picking too bright color
    if color[0] > 0.99 or color[1] > 0.99 or color[2] > 0.99:
        return True

    # To avoid picking too dark color
    if color[0] < 0.01 or color[1] < 0.01 or color[2] < 0.01:
        return True

    for recent_color in recent_colors:
        diff = math.sqrt(
            (recent_color[0] - color[0]) ** 2 + (recent_color[1] - color[1]) ** 2 + (recent_color[2] - color[2]) ** 2)
        if diff < 0.7:
            return True
    return False


# def find_adjancency(clusters):
#     adjacency_list = {}
#     for cluster in clusters:
#         if cluster not in adjacency_list:
#             adjacency_list[cluster] = []
#         for other_cluster in adjacency_list.keys():
#             if other_cluster == cluster:
#                 continue
#             relative_distance = math.sqrt(
#                 (other_cluster.get_center().get_x() - cluster.get_center().get_x()) ** 2 + (
#                             other_cluster.get_center().get_y() - cluster.get_center().get_y()) ** 2)
#             if relative_distance < 400:
#                 adjacency_list[cluster].append(other_cluster)
#                 adjacency_list[other_cluster].append(cluster)
#     return adjacency_list


def find_adjancency(clusters):
    adjancency_list = [[0 for i in range(len(clusters))] for j in range(len(clusters))]
    for i in range(len(clusters)):
        distances = {}
        for j in range(len(clusters)):
            if clusters[j] == clusters[i]:
                continue
            relative_distance = math.sqrt((clusters[j].get_center().get_x() - clusters[i].get_center().get_x()) ** 2 + (
                    clusters[j].get_center().get_y() - clusters[i].get_center().get_y()) ** 2)
            # if relative_distance < 400:
            #     adjancency_list[i][j] = 1
            distances[relative_distance] = j
        # print(sorted(distances))
        for k in range(7):
            # print(distances[sorted(distances)[k]])
            index = distances[sorted(distances)[k]]
            adjancency_list[i][index] = 1

    return adjancency_list


def dfs_coloring(currently_coloring):
    if currently_coloring >= len(clusters_lst):
        return
    for color in range(1, 8):
        if can_use(color, currently_coloring):
            picked_color[currently_coloring] = color
            break
    dfs_coloring(currently_coloring + 1)
    # dfs_coloring(currently_coloring - 1)
    # picked_color[currently_coloring] = color
    # dfs_coloring(currently_coloring + 1)


def can_use(color, currently_coloring):
    for colored in range(currently_coloring):
        if adjancencies[colored][currently_coloring] == 1 and picked_color[colored] == color:
            return False
    return True


if __name__ == "__main__":
    # COLORS = colors.COLORS
    # cluster_colors = colors._get_colors(10)
    # clusters_lst, adjacency_dict = get_Clusters_kmean(READ_PATH, MAP, k=CENTERS_NUM)
    clusters_lst = get_Clusters_kmean(READ_PATH, MAP, k=CENTERS_NUM)
    adjancencies = find_adjancency(clusters_lst)
    # for adjancency in adjancencies.keys():
    #     print(str(adjancency.cluster_id) + ": " + str([cluster.cluster_id for cluster in adjancencies[adjancency]]))

    for i in range(len(adjancencies)):
        print(adjancencies[i])

    # red yellow blue green
    picked_color = [-1 for i in range(len(clusters_lst))]
    picked_color[0] = 1
    dfs_coloring(1)

    print("\nPicked Color:")
    print(picked_color)

    annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME)
    for i in range(len(picked_color)):
        color = colors.COLORS[picked_color[i] % 7]
        r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
        clusters_lst[i].coloring(annotator, (r, g, b, 1),
                                       size=10)
        print("Coloring cluster {} using color(r, g, b): {} {} {}".format(str(i), str(r), str(g), str(b)))
        annotator.write(WRITE_PATH + "/" + PDF_NAME)


    # for cluster in picked_color:
    #     print("painting")
    #     if picked_color[cluster] == 1:
    #         clusters_lst[cluster].coloring(annotator, (0.9019607843137255, 0.09803921568627451, 0.29411764705882354, 1),
    #                                        size=10)
    #     if picked_color[cluster] == 2:
    #         clusters_lst[cluster].coloring(annotator, (0.5686274509803921, 0.11764705882352941, 0.7058823529411765, 1),
    #                                        size=10)
    #     if picked_color[cluster] == 3:
    #         clusters_lst[cluster].coloring(annotator, (0.27450980392156865, 0.6, 0.5647058823529412, 1), size=10)
    #     if picked_color[cluster] == 4:
    #         # clusters_lst[cluster].coloring(annotator, (0.6666666666666666, 1.0, 0.7647058823529411, 1), size=10)
    #         clusters_lst[cluster].coloring(annotator, (1, 1, 1, 1), size=10)
    #     annotator.write(WRITE_PATH + "/" + PDF_NAME)

    # colors_index = np.random.choice(22, CENTERS_NUM, replace=False)
    # colors_lst = [COLORS[i] for i in colors_index]
    # colors_lst = colors.COLORS
    # recent_colors = []

    # i = 0
    # annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME)
    # coloring_queue = [clusters_lst[0]]
    # colored = set()
    # while coloring_queue:
    #     if i == len(colors_lst) - 1:
    #         i = 0
    #     else:
    #         i += 1
    #     curr_coloring = coloring_queue.pop()
    #     color = [rgb / 255 for rgb in colors_lst[i]]
    #     r = color[0]
    #     g = color[1]
    #     b = color[2]
    #     curr_coloring.coloring(annotator, (r, g, b, 1), size=10)
    #     print(r, g, b)
    #     annotator.write(WRITE_PATH + "/" + PDF_NAME)
    #     if curr_coloring not in colored:
    #         # yield curr_coloring
    #         colored.add(curr_coloring)
    #         if adjancencies[curr_coloring]:
    #             for cluster in adjancencies[curr_coloring]:
    #                 coloring_queue.append(cluster)

    # for i in range(CENTERS_NUM):
    #     annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME)
    #     cluster = clusters_lst[i]
    #     print(CENTERS_NUM == len(clusters_lst))
    #     adjacencies = list(adjacency_list.get(cluster.get_center()))
    #     # color = [rgb/255 for rgb in colors_lst[i]]
    #     # r = color[0]
    #     # g = color[1]
    #     # b = color[2]
    #     # r = random.random()
    #     # g = random.random()
    #     # b = random.random()
    #     # color = [random.random(), random.random(), random.random()]
    #     # if len(recent_colors) == 5:
    #     #     recent_colors.pop(0)
    #     # while is_similar(color, recent_colors):
    #     #     color = [random.random(), random.random(), random.random()]
    #     # recent_colors.append(color)
    #     # r, g, b = color[0], color[1], color[2]
    #     # print(color)
    #     # cluster.coloring(annotator, (r, g, b, 1), size=10)
    #
    #     coloring_queue = []
    #     # coloring_queue.append(clus)
    #
    #     for color in colors_lst:
    #         cluster.coloring(annotator, (color, 1), size=10)
    #     annotator.write(WRITE_PATH + "/" + PDF_NAME)
    # #     # cluster.bounds(annotator)
    # #     # annotator.write(WRITE_PATH+ "/" + PDF_NAME)
