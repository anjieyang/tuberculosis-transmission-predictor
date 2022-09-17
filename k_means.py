import numpy as np
import random
import common_modules as cm
import matplotlib.pyplot as plt

# hyper-parameters
READ_PATH = "geo coordinates"
WRITE_PATH = "Clustering"
# MAPS = os.listdir(READ_PATH)
MAP = "Arctic_Bay.xls"
CENTERS_NUM = 30
MAX_ITERATION = 100


class k_means:
    def __init__(self, building_lst, center_lst, k):
        self.building_lst = building_lst
        self.datasize = len(self.building_lst)
        # self.dist_matrix = dist_matrix
        self.center_lst = center_lst
        self.k = k
        self.groups = [[] for i in range(self.k)]

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

    def clear_group(self):
        self.groups = [[] for i in range(self.k)]

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
        # center_lst = [building_lst[i] for i in centers_index]

        center_lst = {}
        for i in centers_index:
            center = building_lst[i]
            center_lst[center] = center.get_longitude() + center.get_latitude()

        # Sort the center list by geo position
        center_lst = sorted(center_lst.items(), key=lambda kv: (kv[1], kv[0]))
        # center_lst = dict(sorted(center_lst.items(), key=lambda item: item[1]))
        # center_lst = [i[0] for i in center_lst]
        print(center_lst)

        return list(i[0] for i in center_lst)
        # return list(center_lst.keys())


def clustering(read_path, map, k=CENTERS_NUM, iteration=MAX_ITERATION):
    building_lst = cm.get_data(read_path, map)
    centers_new = k_means.init_centers(building_lst, k)
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
        print("iteration = ", iter)
        clustering_kmeans.grouping()
        centers_mean = clustering_kmeans.centers_mean()
        center_new = clustering_kmeans.find_nearest_centers(centers_mean)

        if center_new == clustering_kmeans.center_lst:
            print("converge at {}-th iteration".format(iter))
            clustering_kmeans.center_lst = center_new
            clustering_kmeans.grouping()
            break
        clustering_kmeans.center_lst = center_new

    return clustering_kmeans


if __name__ == "__main__":
    clustering = clustering(READ_PATH, MAP)
    groups = clustering.groups
    centers = clustering.center_lst

    for center in centers:
        print(center)
