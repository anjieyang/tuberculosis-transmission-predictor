from pdf_annotate import PdfAnnotator, Appearance, Location
import matplotlib.pyplot as plt
import numpy as np
import colors, k_means, hierarchical
import random
import os

# hyper-parameters
READ_PATH = "Geo_coordinates"
PDF_PATH = "Clustering"
PDF_NAME = "Arctic_Bay_Building_No_2021_Wall.pdf"
WRITE_PATH = "Clustering"
# MAPS = os.listdir(READ_PATH)
MAP = "Arctic_Bay.xls"
CENTERS_NUM = 20


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
                                     appearance=Appearance(content=id, fill=(0, 0, 0), font_size=5))  # black text
            # print(x1,y1)

    def bounds(self, annotator):
        pass


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


if __name__ == "__main__":
    COLORS = colors.COLORS
    clusters_lst = get_Clusters_hierarchical(READ_PATH, MAP, k=CENTERS_NUM)

    # colors_index = np.random.choice(22, CENTERS_NUM, replace=False)
    # colors_lst = [COLORS[i] for i in colors_index]
    for i in range(CENTERS_NUM):
        annotator = PdfAnnotator(PDF_PATH + '/' + PDF_NAME)
        cluster = clusters_lst[i]
        # color = [rgb/255 for rgb in colors_lst[i]]
        # r = color[0]
        # g = color[1]
        # b = color[2]
        r = random.random()
        g = random.random()
        b = random.random()
        cluster.coloring(annotator, (r, g, b, 0.8), size=10)
        annotator.write(WRITE_PATH + "/" + PDF_NAME)
    #     # cluster.bounds(annotator)
    #     # annotator.write(WRITE_PATH+ "/" + PDF_NAME)
