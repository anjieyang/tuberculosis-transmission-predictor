import pandas as pd

from src.building.Building import Building
from src.config.app_config import PATH_GEO_COORDINATES


class BuildingRepository:
    def __init__(self, read_path, map_name):
        self.buildings = []

        df = pd.read_excel(read_path + map_name)
        data_size = len(df)

        for i in range(data_size):
            building_id = df["Building Number"][i]
            x = df["X"][i]
            y = df["Y"][i]
            prefix = df["Prefix"][i]
            suffix = df["Suffix"][i]
            from_range = df["From a Range?"][i]
            range_value = df["Range"][i]
            category = df["Category"][i]
            longitude = df["Longitude"][i]
            latitude = df["Latitude"][i]

            building = Building(id=building_id, x=x, y=y, prefix=prefix, suffix=suffix, from_range=from_range, range_value=range_value, category=category, longitude=longitude, latitude=latitude)
            self.buildings.append(building)

    def find_all(self):
        return self.buildings

    def find_all_by_category(self, category):
        return [building for building in self.buildings if building.category == category]


if __name__ == '__main__':
    building_repository = BuildingRepository(PATH_GEO_COORDINATES, 'Arctic_Bay.xlsx')

    print(building_repository.find_all())
