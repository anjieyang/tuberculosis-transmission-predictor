from src.utils.Utils import Utils


class Map:
    def __init__(self, file_name, buildings, clusters):
        self.file_name = file_name
        self.name = file_name.split('_Building')[0]
        self.buildings = buildings
        self.clusters = clusters
        self.adjacency_matrix = []

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
            self.adjacency_matrix.append(adjacency_list)
