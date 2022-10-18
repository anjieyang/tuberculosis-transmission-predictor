import math

import numpy as np
import random
import common_modules as cm
import matplotlib.pyplot as plt
from math import sqrt
from kneed import KneeLocator
import matplotlib.pyplot as plt

# hyper-parameters
READ_PATH = "geo coordinates"
WRITE_PATH = "Clustering"
# MAPS = os.listdir(READ_PATH)
MAP = "Grise_Fiord.xls"
CENTERS_NUM = 5
MAX_ITERATION = 100


class k_means:
    def __init__(self, building_lst, center_lst, k):
        self.building_lst = building_lst
        self.datasize = len(self.building_lst)
        # self.dist_matrix = dist_matrix
        self.center_lst = center_lst
        self.k = k
        self.groups = [[] for _ in range(self.k)]

    def grouping(self):
        self.clear_group()
        for building in self.building_lst:
            min_dist = cm.Building.Euclidean_dist(building, self.center_lst[0])
            nearest_center_index = 0
            for j in range(self.k):
                dist = cm.Building.Euclidean_dist(building, self.center_lst[j])
                if dist <= min_dist:
                    min_dist = dist
                    nearest_center_index = j
            self.groups[nearest_center_index].append(building)
        self.format_groups()

    def format_groups(self):
        for i in range(len(self.groups)):
            if len(self.groups[i]) == 0:
                self.center_lst[i] = None
                print("Remove: " + str(i))
                self.k -= 1
        self.groups = [group for group in self.groups if len(group) != 0]
        self.center_lst = [center for center in self.center_lst if not None]

    def clear_group(self):
        self.groups = [[] for _ in range(self.k)]

    def centers_mean(self):
        '''
        compute the mean(longitude, latitude) of centers of each group
        :return: a list of the means, len of the list = k
        '''
        centers_mean = []
        for i in range(self.k):
            # print("class ",i," has ", len(self.groups[i])," points")
            sum = cm.Building(building_num=None, x=0, y=0, longitude=0, latitude=0)
            for item in self.groups[i]:
                sum += item
            mean = sum * (1 / len(self.groups[i]))
            centers_mean.append(mean)
        return centers_mean

    def find_nearest_centers(self, centers_mean):
        center_lst_new = []
        for i in range(self.k):
            if len(self.groups[i]) == 0:
                center_lst_new.append(centers_mean[i])
            else:
                min_dist = cm.Building.Euclidean_dist(centers_mean[i], self.groups[i][0])
                nearest_building = self.groups[i][0]
                for item in self.groups[i]:
                    dist = cm.Building.Euclidean_dist(centers_mean[i], item)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_building = item
                center_lst_new.append(nearest_building)
        return center_lst_new

    def init_centers(building_lst, k):
        """
        This function is used to initialize k cluster centers.
        :param k: The number of cluster centers need to be initialized.
        :return: The sorted list of buildings that are selected to be cluster centers.
        """
        centers_index = np.random.choice(len(building_lst), k, replace=False)
        center_lst = [building_lst[i] for i in centers_index]
        return center_lst


def clustering(read_path, map, k=CENTERS_NUM, iteration=MAX_ITERATION):
    building_lst = cm.get_data(read_path, map)
    centers_new = k_means.init_centers(building_lst, k)
    # centers_new = list(centers_dict.keys())
    clustering_kmeans = k_means(building_lst=building_lst, center_lst=centers_new, k=k)
    ## without find_nearest_centers()
    # for iter in range(iteration):
    #     # print("iteration = ", iter)
    #     clustering_kmeans.grouping()
    #     centers_new = clustering_kmeans.centers_mean()        
    #     if clustering_kmeans.find_nearest_centers(centers_new)==clustering_kmeans.find_nearest_centers(clustering_kmeans.center_lst):
    #         # clustering_kmeans.center_lst = centers_new
    #         # clustering_kmeans.grouping()
    #         print("converge at {}-th iteration".format(iter))
    #         break
    #     clustering_kmeans.center_lst = centers_new

    ## with find_nearest_centers()
    for iter in range(iteration):
        # print("iteration = ", iter)
        clustering_kmeans.grouping()
        centers_mean = clustering_kmeans.centers_mean()
        center_new = clustering_kmeans.find_nearest_centers(centers_mean)

        if center_new == clustering_kmeans.center_lst:
            # print("converge at {}-th iteration".format(iter))
            clustering_kmeans.center_lst = center_new
            clustering_kmeans.grouping()
            break
        clustering_kmeans.center_lst = center_new

    return clustering_kmeans


def get_cluster_wss(cluster, sum_squard_distances):
    centers = cluster.center_lst
    # print(centers)
    groups = cluster.groups
    sum_squard_distance = 0
    for i in range(len(groups)):
        center = centers[i]
        for building in groups[i]:
            # wss += sqrt((building.get_latitude() - center.get_latitude()) ** 2 + (building.get_longitude() - center.get_longitude()) ** 2)
            sum_squard_distance += sqrt((building.get_y() - center.get_y()) ** 2 + (
                        building.get_x() - center.get_x()) ** 2)
    print(sum_squard_distance)
    sum_squard_distances.append(sum_squard_distance)


# def optimize_cluster_number():
#     sum_squared_distances = []
#     cluster_amount = range(1, 101)
#     for i in cluster_amount:
#         cluster = clustering(READ_PATH, MAP, i)
#         get_cluster_wss(cluster, sum_squared_distances)
#     print("Sum Squared Distances: ")
#     print(sum_squared_distances)
#
#     kn = KneeLocator(cluster_amount, sum_squared_distances, curve='convex', direction='decreasing', interp_method='polynomial')
#
#     plt.xlabel("Number of Clusters K")
#     plt.ylabel('Sum of Squared Distances')
#     plt.plot(cluster_amount, sum_squared_distances, 'bx-')
#     plt.vlines(kn.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
#     plt.show()
#
#     return kn.knee

def get_cluster_number(read_path, map):
    building_lst = cm.get_data(read_path, map)
    # print(f"Total Building Numbers: {len(building_lst)}")
    return [int(math.ceil(len(building_lst) / 6)), int(math.ceil(len(building_lst) / 25)), int(math.ceil(len(building_lst) / 80))]


if __name__ == "__main__":
    # optimize_cluster_number()
    clustering = clustering(READ_PATH, MAP, CENTERS_NUM, MAX_ITERATION)
    lst = clustering.groups
    for center in lst:
        print(center)




