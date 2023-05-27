from src.building.BuildingController import BuildingController
from src.building.BuildingModel import BuildingModel
from src.cluster.ClusterModel import ClusterModel
from src.config.app_config import CENTERS_NUM, MAX_ITERATION, PATH_GEO_COORDINATES, COLORS, K_MEANS
from src.utils.Utils import Utils


class ClusterController:
    def __init__(self, model):
        self.model = model
        self.clusters = []

    def get_clusters_by_algorithm(self, algorithm):
        if algorithm == K_MEANS:
            self.clusters = self.model.get_clusters_by_k_means()
        self.assign_colors()
        return self.clusters

    def assign_colors(self):
        clusters = self.clusters
        for cluster in clusters:
            cluster.nearby_clusters = self.get_nearby_clusters(cluster)

        clusters.sort(key=lambda cluster: len(cluster.nearby_clusters), reverse=True)

        for cluster in clusters:
            used_colors = {nearby_cluster.color for nearby_cluster in cluster.nearby_clusters if
                           hasattr(nearby_cluster, 'color')}
            for color in COLORS:
                if color not in used_colors:
                    cluster.color = color
                    r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
                    break

    def get_nearby_clusters(self, cluster):
        distances = []
        for other_cluster in self.clusters:
            if other_cluster == cluster:
                continue
            distance = self.get_distance_between_clusters(cluster, other_cluster)
            distances.append((distance, other_cluster))
        distances.sort()

        return [cluster for distance, cluster in distances[:4]]

    def get_adjacency_matrix(self):
        # include self-connection
        for current in range(len(self.clusters)):
            current_cluster = self.clusters[current]
            for another in range(current, len(self.clusters)):
                another_cluster = self.clusters[another]
                if Utils.is_adjacency(current_cluster, another_cluster):
                    current_cluster.adjacency_clusters.append(another_cluster.id)
                    another_cluster.adjacency_clusters.append(current_cluster.id)

        for cluster in self.clusters:
            adjacency_list = []
            for i in range(len(self.clusters)):
                if i in cluster.adjacency_clusters:
                    adjacency_list.append(1)
                else:
                    adjacency_list.append(0)
            self.model.adjacency_matrix.append(adjacency_list)

        return self.model.adjacency_matrix

    def get_cluster_by_id(self, cluster_id):
        for cluster in self.clusters:
            if cluster_id == cluster.id:
                return cluster

    @staticmethod
    def get_distance_between_clusters(cluster, other_cluster):
        return cluster.centroid.get_distance(other_cluster.centroid)


if __name__ == '__main__':
    building_model = BuildingModel(PATH_GEO_COORDINATES, 'Arctic_Bay.xls')
    building_controller = BuildingController(building_model)
    buildings = building_controller.get_buildings_by_category('valid')

    cluster_model = ClusterModel(buildings, CENTERS_NUM, MAX_ITERATION)
    cluster_controller = ClusterController(cluster_model)
    k_means_clusters = cluster_controller.get_clusters_by_algorithm(K_MEANS)

    for cluster in k_means_clusters:
        print(cluster.color)

    print(cluster_controller.get_adjacency_matrix())
