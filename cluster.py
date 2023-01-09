import colors
import hierarchical
import k_means
import math


class Cluster:
    def __init__(self, cluster_id, center, buildings_lst):
        self.cluster_id = cluster_id
        self.buildings_lst = buildings_lst
        self.cluster_size = len(buildings_lst)
        self.center = center

    def bounds(self, annotator):
        pass

    def get_center(self):
        return self.center

    def get_cluster_id(self):
        return self.cluster_id


def get_clusters_kmeans(read_path, map, k):
    clustering = k_means.get_clusters(read_path, map, k)
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


def find_adjacency(clusters, clusters_amount):
    print(
        "Adjacency Cluster Number: "
        + str(min(int(math.ceil(clusters_amount / 4.5)), len(colors.COLORS)))
    )
    adjacency_list = [[0 for _ in range(len(clusters))] for _ in range(len(clusters))]
    for i in range(len(clusters)):
        distances = {}
        for j in range(len(clusters)):
            if clusters[j] == clusters[i]:
                continue
            relative_distance = math.sqrt(
                (clusters[j].get_center().get_x() - clusters[i].get_center().get_x())
                ** 2
                + (clusters[j].get_center().get_y() - clusters[i].get_center().get_y())
                ** 2
            )
            distances[relative_distance] = j
        # print(sorted(distances))
        for k in range(min(int(math.ceil(clusters_amount / 4.5)), len(colors.COLORS))):
            # print(distances[sorted(distances)[k]])
            if not distances:
                break
            index = distances[sorted(distances)[k]]
            adjacency_list[i][index] = 1

    return adjacency_list
