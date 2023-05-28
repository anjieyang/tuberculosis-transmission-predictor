from src.config.app_config import PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS
from src.map.MapController import MapController
from src.map.MapModel import MapModel
from src.map.MapView import MapView
from src.sir.SIRController import SIRController
from src.sir.SIRModel import SIRModel
from src.sir.SIRView import SIRView

if __name__ == '__main__':
    map_model = MapModel(PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS, 10)
    map_view = MapView()
    map_controller = MapController(map_model, map_view)
    map = map_controller.get_map_by_name('Arctic_Bay')

    sir_model = SIRModel(map, 100)
    sir_view = SIRView()

    sir_controller = SIRController(sir_model, sir_view)
    sir_controller.simulate()