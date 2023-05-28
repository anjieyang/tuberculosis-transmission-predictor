from tqdm import tqdm

from src.config.app_config import PATH_RAW_MAPS, PATH_OUTPUT
from src.utils.Utils import Utils


class MapController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_all_maps(self):
        return self.model.maps

    def get_map_by_name(self, map_name):
        return self.model.get_map_by_name(map_name)

    def coloring_map_by_name(self, map_name):
        map = self.model.get_map_by_name(map_name)
        path = Utils.save_map(map, PATH_RAW_MAPS, PATH_OUTPUT)

        self.view.coloring(map, path)
        Utils.save_data(map, path)

    def coloring_all_maps(self):
        maps = self.get_all_maps()
        for i in tqdm(range(len(maps)), total=len(maps), desc='Coloring'):
            map = maps[i]
            self.coloring_map_by_name(map.name)

