import os
import pandas as pd

from building import Building


def get_data(read_path, map_name):
    """
    Read all values of all buildings
    :param read_path: The path of target file
    :param map_name: The name of target file
    :return: A list of buildings, each building belongs to Building class
    """

    df = pd.read_excel(read_path + "/" + map_name)
    data_size = len(df)
    building_lst = []

    for i in range(data_size):
        if df["Category"][i] == "valid":
            building_id = df["Building Number"][i]
            x = df["X"][i]
            y = df["Y"][i]
            prefix = df["Prefix"][i]
            suffix = df["Suffix"][i]
            from_range = df["From a Range?"][i]
            range_value = df["Range"][i]
            longitude = df["Longitude"][i]
            latitude = df["Latitude"][i]

            new_building = Building(
                building_num=building_id,
                x=x,
                y=y,
                longitude=longitude,
                latitude=latitude,
                prefix=prefix,
                suffix=suffix,
                from_range=from_range,
                range=range_value,
            )
            building_lst.append(new_building)

    return building_lst


def save_data(cluster_lst, workbook):
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Cluster Number")
    for i in range(len(cluster_lst)):
        cluster = cluster_lst[i]
        cluster_format = workbook.add_format({"bold": True})
        worksheet.write(i + 1, 0, i + 1, cluster_format)
        cluster_buildings = cluster.buildings_lst
        for j in range(len(cluster_buildings)):
            worksheet.write(i + 1, j + 1, cluster_buildings[j].get_building_num())


def get_files(path):
    files = os.listdir(path)
    return files


# Testing
READ_PATH = "geo_coordinates"
MAP = "Arctic_Bay.xls"
if __name__ == "__main__":
    building_list = get_data(READ_PATH, MAP)
    print(building_list)
