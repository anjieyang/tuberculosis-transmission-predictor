from src.building.BuildingController import BuildingController
from src.building.BuildingModel import BuildingModel
from src.cluster.Cluster import Cluster
from src.cluster.KMeansModel import KMeansModel

from src.config.app_config import PATH_GEO_COORDINATES, MAX_ITERATION


class ClusterModel:
    def __init__(self, buildings, k, iteration):
        self.buildings = buildings
        self.k = k
        self.iteration = iteration
        self.clusters = []
        self.adjacency_matrix = []

    def get_clusters_by_k_means(self):
        self.clusters = []

        # anomaly detection
        self.k = self.k if self.k <= len(self.buildings) else len(self.buildings)

        k_means_model = KMeansModel(self.buildings, self.k, self.iteration)
        k_means = k_means_model.k_means()

        for i in range(self.k):
            try:
                center = k_means.centroids[i]
                groups = k_means.groups[i]
                self.clusters.append(Cluster(i, center, groups))
            except IndexError:
                # print("Warning: Cannot get enough centroids.")
                pass

        return self.clusters









if __name__ == '__main__':
    building_model = BuildingModel(PATH_GEO_COORDINATES, 'Arctic_Bay.xls')
    building_controller = BuildingController(building_model)
    buildings = building_controller.get_buildings_by_category('valid')

    cluster_model = ClusterModel(buildings, 10, MAX_ITERATION)
    k_means = cluster_model.get_clusters_by_k_means()
    print(cluster_model.clusters[0].border)
    print(cluster_model.adjacency_matrix)
    # adjacency_matrix = cluster_model.get_adjacency_matrix()
    # print(adjacency_matrix)
