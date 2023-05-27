from src.building.BuildingRepository import BuildingRepository
from src.config.app_config import PATH_GEO_COORDINATES


class BuildingModel:
    def __init__(self, read_path, map_name):
        self.building_repository = BuildingRepository(read_path, map_name)

    def get_all_buildings(self):
        return [building for building in self.building_repository.find_all()]

    def get_buildings_by_category(self, category):
        return [building for building in self.building_repository.find_all_by_category(category)]


if __name__ == '__main__':
    building_model = BuildingModel(PATH_GEO_COORDINATES, 'Arctic_Bay.xls')
    buildings = building_model.get_buildings_by_category('valid')
    print(buildings[4].longitude)
