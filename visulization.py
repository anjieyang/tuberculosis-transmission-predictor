import os
import shutil

import xlsxwriter
from pdf_annotate import Appearance
from pdf_annotate import PdfAnnotator
from pdf_annotate import Location

import colors
import io_operations
import k_means
from cluster import get_clusters_kmeans, get_cluster_by_id
from cluster import find_adjacency
from border import graham_scan
from scale import get_moved_border, get_centriod_by_cluster
from scale import get_centroid
from intersects import is_intersects

from statistics import draw_degree_distribution

GEO_PATH = "data/geo_coordinates"
MAP_PATH = "data/raw_maps"
OUTPUT_PATH = "output"


def coloring(cluster, annotator, color, size):
    """
    Adds color and square annotations to the PDF file for the given cluster and annotator.

    Parameters:
        cluster (Cluster): The cluster object to be annotated.
        annotator (PdfAnnotator): The annotator object for the PDF file.
        color (tuple): The color tuple to be used for the annotations.
        size (int): The size of the square annotations to be added.

    Returns:
        None
    """
    for building in cluster.buildings_lst:
        x = building.x
        y = building.y
        id = building.id
        x1 = x - size
        x2 = x + size
        y1 = 3370 - y - size
        y2 = 3370 - y + size
        annotator.add_annotation(
            annotation_type="square",
            location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
            appearance=Appearance(fill=color, stroke_width=0),
        )
        annotator.add_annotation(
            annotation_type="text",
            location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
            appearance=Appearance(content=str(cluster.cluster_id), fill=(1, 1, 1), font_size=5),
        )  # black text


def dfs_coloring(currently_coloring, adjacencies_number):
    """
    Helper function to assign colors to the clusters using the DFS algorithm.

    Parameters:
        currently_coloring (int): The cluster number currently being colored.
        adjacencies_number (int): The number of adjacencies between the clusters.

    Returns:
        None
    """
    if currently_coloring >= len(clusters_lst):
        return
    for color in range(adjacencies_number + 1):
        if can_use(color, currently_coloring):
            picked_color[currently_coloring] = color
            break
    dfs_coloring(currently_coloring + 1, adjacencies_number)


def can_use(color, currently_coloring):
    """
    Helper function to check if a color can be used for the current cluster.

    Parameters:
        color (int): The color to be checked.
        currently_coloring (int): The cluster number currently being colored.

    Returns:
        True if the color can be used for the current cluster, False otherwise.
    """
    for colored in range(currently_coloring):
        if (
                adjacencies[colored][currently_coloring] == 1
                or adjacencies[currently_coloring][colored] == 1
        ):
            if picked_color[colored] == color:
                return False
    return True


def draw_border(cluster, annotator, color):
    """
    Draws the border for the given cluster and annotator, and adds the border annotations to the PDF file.

    Parameters:
        cluster (Cluster): The cluster object for which the border is to be drawn.
        annotator (PdfAnnotator): The annotator object for the PDF file.
        color (tuple): The color tuple to be used for the border annotations.

    Returns:
        The list of points that form the border.
    """
    buildings = []
    for building in cluster.buildings_lst:
        buildings.append((building.x, 3370 - building.y))
    hull = graham_scan(buildings)
    centroid = get_centroid(buildings)

    annotator.add_annotation(
        annotation_type="polyline",
        location=Location(points=hull, page=0),
        appearance=Appearance(fill=color, stroke_width=5),
    )

    annotator.add_annotation(
        annotation_type="square",
        location=Location(x1=centroid[0] - 10, y1=centroid[1] - 10, x2=centroid[0] + 10, y2=centroid[1] + 10, page=0),
        appearance=Appearance(fill=(0, 0, 0), stroke_width=1),
    )

    return hull


if __name__ == "__main__":
    files = io_operations.get_files(MAP_PATH)
    for file in files:
        # to check if file is a .pdf file
        if ".pdf" not in file:
            continue

        map_name = file.split("_Building")[0]
        map = map_name + ".xls"

        cluster_number = k_means.get_cluster_number(GEO_PATH, map)

        # Create different directories to store the data of different granularity
        for k_value in cluster_number:
            try:
                shutil.copy(
                    MAP_PATH + "/" + file, OUTPUT_PATH + "/" + map_name + f"/k_{k_value}/"
                )
            except:
                os.makedirs(OUTPUT_PATH + "/" + map_name + "/" + f"k_{k_value}/")
                shutil.copy(
                    MAP_PATH + "/" + file, OUTPUT_PATH + "/" + map_name + f"/k_{k_value}/"
                )

            clusters_lst = get_clusters_kmeans(GEO_PATH, map, k=k_value)
            adjacencies = find_adjacency(clusters_lst, k_value)

            picked_color = [-1 for _ in range(len(clusters_lst))]
            picked_color[0] = 1
            dfs_coloring(1, len(adjacencies))

            annotator = PdfAnnotator(f"{OUTPUT_PATH}/{map_name}/k_{k_value}/{file}")
            clusters = {}
            after_moved_adjacencies = {}
            for i in range(len(picked_color)):
                current_cluster_id = clusters_lst[i].get_cluster_id()
                after_moved_adjacencies[clusters_lst[i].get_cluster_id()] = {}
                color = colors.COLORS[picked_color[i] % 7]
                r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
                coloring(clusters_lst[i], annotator, (r, g, b, 1), size=10)

                current_hull = draw_border(clusters_lst[i], annotator, (r, g, b, 1))
                clusters[clusters_lst[i].get_cluster_id()] = current_hull

            for original_id, original_border in clusters.items():
                for current_id, current_border in clusters.items():
                    if current_id == original_id:
                        continue

                    directions = ['left', 'right', 'up', 'down', 'left_up', 'left_down', 'right_up', 'right_down']
                    for direction in directions:
                        distance = 0
                        intersects = False
                        while not intersects:
                            distance += 15
                            moved_border = get_moved_border(current_border, direction, distance)
                            intersects = is_intersects(original_border, moved_border)

                            if distance >= 150:
                                break

                        if intersects:
                            average_distance_within_original = get_cluster_by_id(original_id,
                                                                                 clusters_lst).get_average_distance()
                            average_distance_within_current = get_cluster_by_id(current_id,
                                                                                clusters_lst).get_average_distance()

                            print(f"distance: {distance} ({direction})\naverage of {original_id}: {average_distance_within_original}\naverage of {current_id}: {average_distance_within_current}")

                            if distance <= (average_distance_within_original + average_distance_within_current) / 2:
                                after_moved_adjacencies[original_id][current_id] = distance
                                after_moved_adjacencies[current_id][original_id] = distance

                                centroid1 = get_centriod_by_cluster(get_cluster_by_id(original_id, clusters_lst))
                                centroid2 = get_centriod_by_cluster(get_cluster_by_id(current_id, clusters_lst))
                                annotator.add_annotation(
                                    annotation_type="line",
                                    location=Location(points=(centroid1, centroid2), page=0),
                                    appearance=Appearance(fill=(0, 0, 0), stroke_width=3),
                                )

            print(after_moved_adjacencies)
            annotator.write(f"{OUTPUT_PATH}/{map_name}/k_{k_value}/{file}")

            save_path = f"{OUTPUT_PATH}/{map_name}/k_{k_value}/"
            degree_distribution = draw_degree_distribution(after_moved_adjacencies, save_path)

            try:
                os.remove(f"{OUTPUT_PATH}/{map_name}/k_{k_value}/clusters_data.xlsx")
            except:
                pass

            workbook = xlsxwriter.Workbook(
                f"{OUTPUT_PATH}/{map_name}/k_{k_value}/clusters_data.xlsx"
            )
            io_operations.save_clusters_data(clusters_lst, workbook)
            io_operations.save_adjacencies_data(after_moved_adjacencies, workbook)
            workbook.close()
