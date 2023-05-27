import numpy as np

from src.building.Building import Building
from src.building.BuildingController import BuildingController
from src.building.BuildingModel import BuildingModel
from src.config.app_config import PATH_GEO_COORDINATES, MAX_ITERATION


class KMeans:
    def __init__(self, buildings, centroids, k):
        self.building_lst = buildings
        self.datasize = len(self.building_lst)
        self.centroids = centroids
        self.k = k
        self.groups = [[] for _ in range(self.k)]

    def grouping(self):
        self.clear_group()
        for building in self.building_lst:
            min_dist = building.get_distance(self.centroids[0])
            nearest_center_index = 0
            for j in range(self.k):
                dist = building.get_distance(self.centroids[j])
                if dist <= min_dist:
                    min_dist = dist
                    nearest_center_index = j
            self.groups[nearest_center_index].append(building)
        self.formatting()

    def formatting(self):
        for i in range(len(self.groups)):
            if len(self.groups[i]) == 0:
                self.centroids[i] = None
                self.k -= 1
        self.groups = [group for group in self.groups if len(group) != 0]
        self.centroids = [center for center in self.centroids if not None]

    def clear_group(self):
        self.groups = [[] for _ in range(self.k)]

    def get_centers_mean(self):
        centers_mean = []
        for i in range(self.k):
            sum = Building(id=None, x=0, y=0, longitude=0, latitude=0)
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
                min_dist = centers_mean[i].get_distance(self.groups[i][0])
                nearest_building = self.groups[i][0]
                for item in self.groups[i]:
                    dist = centers_mean[i].get_distance(item)
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


class KMeansModel:
    def __init__(self, buildings, k, iteration):
        self.buildings = buildings
        self.k = k
        self.iteration = iteration

        self.cluster = self.k_means()

    def k_means(self):
        centers = KMeans.init_centers(self.buildings, self.k)
        cluster = KMeans(self.buildings, centers, self.k)

        for it in range(self.iteration):
            cluster.grouping()
            centers_mean = cluster.get_centers_mean()
            center_new = cluster.find_nearest_centers(centers_mean)

            if center_new == cluster.centroids:
                cluster.centroids = center_new
                cluster.grouping()
                break
            cluster.centroids = center_new

        return cluster


if __name__ == "__main__":
    building_model = BuildingModel(PATH_GEO_COORDINATES, 'Arctic_Bay.xls')
    building_controller = BuildingController(building_model)
    buildings = building_controller.get_buildings_by_category('valid')

    kmeans_model = KMeansModel(buildings, 5, MAX_ITERATION)
    k_means = kmeans_model.k_means()
    print(k_means.centroids)
