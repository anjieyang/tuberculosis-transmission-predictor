import os

from tqdm import tqdm

from src.building.BuildingModel import BuildingModel
from src.cluster.ClusterController import ClusterController
from src.cluster.ClusterModel import ClusterModel
from src.config.app_config import PATH_RAW_MAPS, PATH_GEO_COORDINATES, CENTERS_NUM, MAX_ITERATION, K_MEANS
from src.map.Map import Map


class MapModel:
    def __init__(self, path_raw_maps, path_raw_data, cluster_algorithm, cluster_number=CENTERS_NUM):
        self.map_files = os.listdir(path_raw_maps)
        self.data_files = os.listdir(path_raw_data)
        self.maps = []

        for i in tqdm(range(len(self.map_files)), total=len(self.map_files), desc='Clustering'):
            map_file_name = self.map_files[i]
            map_name = map_file_name.split('_Building')[0]
            try:
                building_model = BuildingModel(PATH_GEO_COORDINATES, map_name + '.xls')
                buildings = building_model.get_buildings_by_category('valid')
                cluster_model = ClusterModel(buildings, cluster_number, MAX_ITERATION)
                cluster_controller = ClusterController(cluster_model)
                clusters = cluster_controller.get_clusters_by_algorithm(cluster_algorithm)
                self.maps.append(Map(map_file_name, buildings, clusters))

            except FileNotFoundError:
                print("File not found. Please check the file name and try again.")

    def get_map_by_name(self, map_name):
        for map in self.maps:
            if map.name == map_name:
                return map

    def get_adjacency_by_name(self, map_name):
        map = self.get_map_by_name(map_name)
        return map.adjacency_matrix


if __name__ == '__main__':
    map_model = MapModel(PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS)
    map = map_model.get_map_by_name('Arviat')
    print(map.name)
    print(len(map.buildings))
    print(map.clusters)
    adjacency_matrix = map_model.get_adjacency_by_name('Arviat')
    print(adjacency_matrix)
