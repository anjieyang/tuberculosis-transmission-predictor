import math
import os
import pandas as pd



def get_data(read_path, map_name):
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


def save_clusters_data(cluster_lst, workbook):
    """
    Saves the building numbers of each cluster into an Excel workbook.

    Args:
    - cluster_lst (list of Cluster objects): A list of clusters.
    - workbook (XlsxWriter Workbook object): The workbook object to write the clusters data.

    Returns: None
    """
    worksheet = workbook.add_worksheet("Clusters Data")
    worksheet.write(0, 0, "Cluster ID")
    for i in range(len(cluster_lst)):
        cluster = cluster_lst[i]
        cluster_format = workbook.add_format({"bold": True})
        worksheet.write(i + 1, 0, i, cluster_format)
        cluster_buildings = cluster.buildings
        for j in range(len(cluster_buildings)):
            worksheet.write(i + 1, j + 1, cluster_buildings[j].get_building_num())


def save_adjacencies_data(adjacency_data, workbook):
    """
    Writes adjacency data to a worksheet in a given workbook.

    Args:
        adjacency_data (dict): A dictionary containing adjacency data for each cluster.
            The keys of the dictionary are cluster IDs, and the values are dictionaries
            representing the cluster's adjacency list. The adjacency list is also a
            dictionary, where the keys are the IDs of adjacent clusters and the values
            are the weights of the edges between them.
        workbook (Workbook): An instance of the openpyxl Workbook class where the
            adjacency data will be written.

    Returns:
        None
    """
    worksheet = workbook.add_worksheet("Adjacencies Data")
    worksheet.write(0, 0, "Cluster ID")
    i = 0
    for cluster_id, adjacencies in adjacency_data.items():
        cluster_format = workbook.add_format({"bold": True})
        worksheet.write(i + 1, 0, cluster_id, cluster_format)
        adjacencies = list(adjacencies.keys())
        for j in range(len(adjacencies)):
            worksheet.write(i + 1, j + 1, adjacencies[j])
        i += 1


def get_files(path):
    files = os.listdir(path)
    return files


# Testing
READ_PATH = "../../data/geo_coordinates"
MAP = "Arctic_Bay.xls"
if __name__ == "__main__":
    building_list = get_data(READ_PATH, MAP)
    print(building_list)
