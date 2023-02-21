import colors
import hierarchical
import k_means
import math


class Cluster:
    """
    Represents a cluster of buildings in a two-dimensional space.

    Attributes:
        cluster_id (int): The unique identifier for the cluster.
        buildings_lst (list): A list of `Building` objects representing the buildings in the cluster.
        cluster_size (int): The number of buildings in the cluster.
        center (Building): The center `Building` object of the cluster.

    Methods:
        bounds(annotator): Calculates the bounding box of the cluster and returns it as a tuple.
        get_center(): Returns the center `Building` object of the cluster.
        get_cluster_id(): Returns the unique identifier for the cluster.
        get_average_distance(): Calculates the average distance of the buildings in the cluster to its center and returns it as a float.
    """

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

    def get_average_distance(self):
        distance = 0
        for building in self.buildings_lst:
            distance += math.sqrt((building.get_x() - self.get_center().get_x()) ** 2
                                  + (building.get_y() - self.get_center().get_y()) ** 2)
        return distance / len(self.buildings_lst)


def get_clusters_kmeans(read_path, map, k):
    """
    Applies k-means clustering to a map and returns a list of `Cluster` objects.

    Args:
        read_path (str): The file path of the PDF map to be processed.
        map (str): The name of the map as a string.
        k (int): The number of clusters to form.

    Returns:
        List[Cluster]: A list of `Cluster` objects.

    Raises:
        ValueError: If the provided value of `k` is less than 1.

    """
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
    """
    Performs hierarchical clustering on the buildings in the specified map and returns a list of Cluster objects.

    :param read_path: The file path of the map to cluster.
    :param map: The name of the map to cluster, as a string.
    :param k: The number of clusters to create.
    :return: A list of Cluster objects, where each cluster contains buildings that are close to each other.
    """
    clustering = hierarchical.clustering(read_path, map, k)
    clusters_lst = []
    for i in range(k):
        groups = clustering.clusters_lst[i].points
        cluster = Cluster(i, None, groups)
        clusters_lst.append(cluster)
    return clusters_lst


def find_adjacency(clusters, clusters_amount):
    """
    Given a list of Cluster objects and the number of total clusters, returns an adjacency list for the clusters.

    Parameters:
    - clusters: a list of Cluster objects
    - clusters_amount: an integer representing the total number of clusters

    Returns:
    - adjacency_list: a 2D list of integers representing the adjacency list for the clusters
    """
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


def get_cluster_by_id(cluster_id, clusters_lst):
    """
    Search for a cluster in a list of clusters by its ID and return it.

    Args:
        cluster_id (int): The ID of the cluster to be searched for.
        clusters_lst (list): A list of Cluster objects.

    Returns:
        The Cluster object with the given ID, or None if the cluster is not found.
    """
    for cluster in clusters_lst:
        if cluster_id == cluster.cluster_id:
            return cluster
