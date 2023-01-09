import numpy as np
import math
import io_operations as cm

# hyper-parameters
READ_PATH = "Geo_coordinates"
WRITE_PATH = "output"
MAP = "Arctic_Bay.xls"
CENTERS_NUM = 30
MAX_ITERATION = 10000


class a_cluster:
    def __init__(self, points):
        """
        :param points: a list of buildings which belong to this cluster
        """
        # self.id = id
        self.points = points
        self.size = len(self.points)

    def dist_matrix(self, another_cluster):
        """
        return a numpy matrix, dist[i,j]=the dist between the i-th point in this cluster and the j-th point in another_cluster.
        """
        dist = np.zeros([self.size, another_cluster.size])
        for i in range(self.size):
            for j in range(another_cluster.size):
                dist[i][j] = cm.Building.Euclidean_dist(
                    self.points[i], another_cluster.points[j]
                )
        return dist

    def max_dist(self, another_cluster):
        # the max distance between these two clusters
        dist = self.dist_matrix(another_cluster)
        return np.max(dist)

    def min_dist(self, another_cluster):
        # the min distance between these two clusters
        dist = self.dist_matrix(another_cluster)
        return np.min(dist)

    def avg_dist(self, another_cluster):
        # the average distance between these two clusters
        dist = self.dist_matrix(another_cluster)
        return np.mean(dist)


class hierarchical_cluster:
    def __init__(self, clusters_lst, k):
        """
        :param clusters_lst: a list of clusters(each one is a_cluster type)
        :param k: the target num of centers
        """
        self.clusters_lst = clusters_lst
        self.k = k
        self.q = len(self.clusters_lst)  # the current num of centers
        self.min_dist_matrix = np.zeros([k, k])

    def initialize(self, building_lst):
        self.clusters_lst = []
        for point in building_lst:
            self.clusters_lst.append(a_cluster(points=[point]))
        self.q = len(self.clusters_lst)
        self.min_dist_matrix = np.zeros([self.q, self.q])
        for i in range(self.q):
            for j in range(i + 1, self.q):
                self.min_dist_matrix[i][j] = self.clusters_lst[i].min_dist(
                    self.clusters_lst[j]
                )
        for j in range(self.q):
            for i in range(j + 1, self.q):
                self.min_dist_matrix[i][j] = self.min_dist_matrix[j][i]

    def removing(self, cluster1):
        # removing cluster1 from clusters_lst
        index = self.clusters_lst.index(cluster1)
        self.clusters_lst.remove(cluster1)
        self.min_dist_matrix = np.delete(self.min_dist_matrix, index, axis=0)
        self.min_dist_matrix = np.delete(self.min_dist_matrix, index, axis=1)
        self.q = len(self.clusters_lst)

    def adding(self, cluster1):
        # adding cluster1 into clusters_lst
        self.clusters_lst.append(cluster1)
        vector1 = np.zeros(self.q)
        vector2 = np.zeros(self.q + 1)
        for i in range(self.q):
            vector1[i] = cluster1.min_dist(self.clusters_lst[i])
            vector2[i] = cluster1.min_dist(self.clusters_lst[i])
        self.min_dist_matrix = np.insert(
            self.min_dist_matrix, self.q - 1, vector1, axis=0
        )
        self.min_dist_matrix = np.insert(
            self.min_dist_matrix, self.q - 1, vector2, axis=1
        )
        self.q = len(self.clusters_lst)

    def merging(self, cluster1, cluster2):
        # merge cluster1 and cluster2 into one larger cluster, and update clusters_lst
        points = cluster1.points + cluster2.points
        new_cluster = a_cluster(points=points)
        self.removing(cluster1)
        self.removing(cluster2)
        self.adding(new_cluster)
        self.q = len(self.clusters_lst)

    def clustering(self):
        # starting hierarchical output
        index = np.argmin(self.min_dist_matrix)
        i = math.floor((index + 1) / self.q) - 1
        j = (index + 1) % self.q - 1
        self.merging(self.clusters_lst[i], self.clusters_lst[j])


def clustering(read_path, map, k=CENTERS_NUM, iteration=MAX_ITERATION):
    building_lst = cm.get_data(read_path, map)
    clustering_hierarchical = hierarchical_cluster(clusters_lst=[], k=k)
    clustering_hierarchical.initialize(building_lst)
    while clustering_hierarchical.q > k:
        print("current num of clusters is:", clustering_hierarchical.q)
        clustering_hierarchical.clustering()
    return clustering_hierarchical


if __name__ == "__main__":
    clustering = clustering(READ_PATH, MAP)
    print(clustering.clusters_lst[0].points[0])
