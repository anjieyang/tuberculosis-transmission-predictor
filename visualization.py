import math
import shutil

import xlsxwriter as xlsxwriter
from pdf_annotate import PdfAnnotator, Appearance, Location
import matplotlib.pyplot as plt
import numpy as np
import colors, k_means, hierarchical
import random
import os
from queue import *

READ_PATH = "geo coordinates"
PDF_PATH = "Clustering"
PDF_NAME = "Arviat_Building_No_2021_Wall.pdf"
WRITE_PATH = "Clustering"
# MAPS = os.listdir(READ_PATH)
MAP = "Arviat.xls"


# CENTERS_NUM = 30


class Cluster:
    def __init__(self, cluster_id, center, buildings_lst):
        self.cluster_id = cluster_id
        self.buildings_lst = buildings_lst
        self.cluster_size = len(buildings_lst)
        self.center = center

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


def get_clusters_kmeans(read_path, map, k):
    clustering = k_means.clustering(read_path, map, k)
    clusters_lst = []
    print(str(len(clustering.center_lst)))
    k = len(clustering.center_lst) if k >= len(clustering.center_lst) else k
    for i in range(k):
        center = clustering.center_lst[i]
        groups = clustering.groups[i]
        cluster = Cluster(i, center, groups)
        clusters_lst.append(cluster)
    return clusters_lst


def get_clusters_hierarchical(read_path, map, k):
    clustering = hierarchical.clustering(read_path, map, k)
    clusters_lst = []
    for i in range(k):
        groups = clustering.clusters_lst[i].points
        cluster = Cluster(i, None, groups)
        clusters_lst.append(cluster)
    return clusters_lst


def save_data(cluster_lst, workbook):
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Cluster Number')
    for i in range(len(clusters_lst)):
        cluster = cluster_lst[i]
        # worksheet.write(i + 1, 0, cluster.get_cluster_id() + 1)
        cluster_format = workbook.add_format({'bold': True})
        worksheet.write(i + 1, 0, i + 1, cluster_format)
        cluster_buildings = cluster.buildings_lst
        for j in range(len(cluster_buildings)):
            worksheet.write(i + 1, j + 1, cluster_buildings[j].get_building_num())


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


def find_adjancency(clusters, clusters_amount):
    print('Adjacency Cluster Number: ' + str(int(math.ceil(clusters_amount / 4.5))))
    adjancency_list = [[0 for _ in range(len(clusters))] for _ in range(len(clusters))]
    for i in range(len(clusters)):
        distances = {}
        for j in range(len(clusters)):
            if clusters[j] == clusters[i]:
                continue
            relative_distance = math.sqrt((clusters[j].get_center().get_x() - clusters[i].get_center().get_x()) ** 2 + (
                    clusters[j].get_center().get_y() - clusters[i].get_center().get_y()) ** 2)
            distances[relative_distance] = j
        # print(sorted(distances))
        for k in range(int(math.ceil(clusters_amount / 4.5))):
            # print(distances[sorted(distances)[k]])
            index = distances[sorted(distances)[k]]
            adjancency_list[i][index] = 1

    return adjancency_list


def dfs_coloring(currently_coloring, adjancencies_number):
    if currently_coloring >= len(clusters_lst):
        return
    for color in range(1, adjancencies_number + 1):
        if can_use(color, currently_coloring):
            picked_color[currently_coloring] = color
            break
    dfs_coloring(currently_coloring + 1, adjancencies_number)


def can_use(color, currently_coloring):
    for colored in range(currently_coloring):
        if adjancencies[colored][currently_coloring] == 1 or adjancencies[currently_coloring][colored] == 1:
            if picked_color[colored] == color:
                return False
    return True


if __name__ == "__main__":
    cluster_number = k_means.get_cluster_number(READ_PATH, MAP)
    print(cluster_number)

    # Create different directories to store the data of different granularity
    for k in cluster_number:
        try:
            shutil.copy(PDF_PATH + '/' + PDF_NAME, PDF_PATH + '/' + PDF_NAME.split('.')[0] + f'/k_{k}/')
        except:
            os.makedirs(PDF_PATH + '/' + PDF_NAME.split('.')[0] + '/' + f'k_{k}/')
            shutil.copy(PDF_PATH + '/' + PDF_NAME, PDF_PATH + '/' + PDF_NAME.split('.')[0] + f'/k_{k}/')

        clusters_lst = get_clusters_kmeans(READ_PATH, MAP, k=k)
        adjancencies = find_adjancency(clusters_lst, k)

        try:
            os.remove(PDF_PATH + '/' + PDF_NAME.split('.')[0] + f'/k_{k}/cluster_data.xlsx')
        except:
            pass

        workbook = xlsxwriter.Workbook(PDF_PATH + '/' + PDF_NAME.split('.')[0] + f'/k_{k}/cluster_data.xlsx')
        save_data(clusters_lst, workbook)
        workbook.close()

        print("Adjacency Matrix: ")
        for i in range(len(adjancencies)):
            print(adjancencies[i])

        picked_color = [-1 for _ in range(len(clusters_lst))]
        picked_color[0] = 1
        dfs_coloring(1, len(adjancencies))

        print("\nPicked Color:")
        print(picked_color)

        # annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME)
        annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME.split('.')[0] + f'/k_{k}/{PDF_NAME}')
        for i in range(len(picked_color)):
            color = colors.COLORS[picked_color[i] % 7]
            r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
            clusters_lst[i].coloring(annotator, (r, g, b, 1),
                                     size=10)
            print("Coloring cluster {} using color(r, g, b): {} {} {}".format(str(i), str(r), str(g), str(b)))
            annotator.write(WRITE_PATH + "/" + PDF_NAME.split('.')[0] + f"/k_{k}/{PDF_NAME}")
