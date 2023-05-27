from src.utils.Utils import Utils


class Cluster:
    def __init__(self, cluster_id, centroid, buildings_lst):
        self.id = cluster_id
        self.buildings = buildings_lst
        self.size = len(buildings_lst)
        self.centroid = centroid
        self.color = None
        self.nearby_clusters = []
        self.border = self.get_border()
        self.adjacency_clusters = []

    def get_average_distance(self):
        distance = 0
        for building in self.buildings:
            distance += self.centroid.get_distance(building)
        return distance / len(self.buildings)

    def get_border(self):
        return Utils.get_cluster_border(self)
