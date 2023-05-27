from src.config.app_config import PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS
from src.map.MapController import MapController
from src.map.MapModel import MapModel
from src.map.MapView import MapView

if __name__ == '__main__':
    map_model = MapModel(PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS, 10)
    map_view = MapView()
    map_controller = MapController(map_model, map_view)

    map_controller.coloring_all_maps()
