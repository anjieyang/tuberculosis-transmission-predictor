from src.building.BuildingModel import BuildingModel
from src.config.app_config import PATH_GEO_COORDINATES


class BuildingController:
    def __init__(self, model):
        self.model = model

    def get_all_buildings(self):
        return self.model.get_all_buildings()

    def get_buildings_by_category(self, category):
        return self.model.get_buildings_by_category(category)


if __name__ == '__main__':
    building_model = BuildingModel(PATH_GEO_COORDINATES, 'Arctic_Bay.xls')
    building_controller = BuildingController(building_model)
    buildings = building_controller.get_buildings_by_category('valid')
    print(buildings[0].category)
