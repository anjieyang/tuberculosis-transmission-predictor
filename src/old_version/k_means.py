import math
import numpy as np
from src.old_version import io_operations
from building_out import Building

# hyper-parameters
READ_PATH = "../../data/geo_coordinates"
WRITE_PATH = "../../output"
MAP = "Grise_Fiord.xls"
CENTERS_NUM = 5
MAX_ITERATION = 100


class KMeansCluster:
    def __init__(self, building_lst, center_lst, k):
        self.building_lst = building_lst
        self.datasize = len(self.building_lst)
        self.center_lst = center_lst
        self.k = k
        self.groups = [[] for _ in range(self.k)]

    def grouping(self):
        self.clear_group()
        for building in self.building_lst:
            min_dist = io_operations.Building.get_euclidean_distance(
                building, self.center_lst[0]
            )
            nearest_center_index = 0
            for j in range(self.k):
                dist = io_operations.Building.get_euclidean_distance(
                    building, self.center_lst[j]
                )
                if dist <= min_dist:
                    min_dist = dist
                    nearest_center_index = j
            self.groups[nearest_center_index].append(building)
        self.formatting()

    def formatting(self):
        for i in range(len(self.groups)):
            if len(self.groups[i]) == 0:
                self.center_lst[i] = None
                print("Remove: " + str(i))
                self.k -= 1
        self.groups = [group for group in self.groups if len(group) != 0]
        self.center_lst = [center for center in self.center_lst if not None]

    def clear_group(self):
        self.groups = [[] for _ in range(self.k)]

    def get_centers_mean(self):
        centers_mean = []
        for i in range(self.k):
            sum = Building(building_num=None, x=0, y=0, longitude=0, latitude=0)
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
                min_dist = Building.get_euclidean_distance(
                    centers_mean[i], self.groups[i][0]
                )
                nearest_building = self.groups[i][0]
                for item in self.groups[i]:
                    dist = Building.get_euclidean_distance(centers_mean[i], item)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_building = item
                center_lst_new.append(nearest_building)
        return center_lst_new

    @staticmethod
    def init_centers(building_list, k):
        centers_index = np.random.choice(len(building_list), k, replace=False)
        center_lst = [building_list[i] for i in centers_index]
        return center_lst


def get_clusters(read_path, picked_map, k=CENTERS_NUM, iteration=MAX_ITERATION):
    building_lst = io_operations.get_data(read_path, picked_map)
    centers_new = KMeansCluster.init_centers(building_lst, k)
    clustering_kmeans = KMeansCluster(building_lst=building_lst, center_lst=centers_new, k=k)

    for it in range(iteration):
        clustering_kmeans.grouping()
        centers_mean = clustering_kmeans.get_centers_mean()
        center_new = clustering_kmeans.find_nearest_centers(centers_mean)

        if center_new == clustering_kmeans.center_lst:
            clustering_kmeans.center_lst = center_new
            clustering_kmeans.grouping()
            break
        clustering_kmeans.center_lst = center_new

    return clustering_kmeans



def get_cluster_number(read_path, map):
    building_lst = io_operations.get_data(read_path, map)
    return [
        int(math.ceil(len(building_lst) / 6)),
        int(math.ceil(len(building_lst) / 25)),
        int(math.ceil(len(building_lst) / 80)),
    ]


if __name__ == "__main__":
    cluster = get_clusters(READ_PATH, MAP, CENTERS_NUM, MAX_ITERATION)
    cluster_list = cluster.groups
    for cluster_centers in cluster_list:
        print(cluster_centers)
