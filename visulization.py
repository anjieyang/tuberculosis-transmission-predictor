import os
import shutil

import xlsxwriter
from pdf_annotate import Appearance
from pdf_annotate import PdfAnnotator
from pdf_annotate import Location

import colors
import io_operations
import k_means
from cluster import get_clusters_kmeans
from cluster import find_adjacency

READ_PATH = "geo_coordinates"
WRITE_PATH = "output"
PDF_PATH = "output"


def coloring(cluster, annotator, color, size):
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
            appearance=Appearance(content=id, fill=(1, 1, 1), font_size=5),
        )  # black text


def dfs_coloring(currently_coloring, adjancencies_number):
    if currently_coloring >= len(clusters_lst):
        return
    for color in range(adjancencies_number + 1):
        if can_use(color, currently_coloring):
            picked_color[currently_coloring] = color
            break
    dfs_coloring(currently_coloring + 1, adjancencies_number)


def can_use(color, currently_coloring):
    for colored in range(currently_coloring):
        if (
            adjancencies[colored][currently_coloring] == 1
            or adjancencies[currently_coloring][colored] == 1
        ):
            if picked_color[colored] == color:
                return False
    return True


if __name__ == "__main__":
    files = io_operations.get_files(PDF_PATH)
    print(f"Total File: {len(files)}")
    print(f"Files List: {files}")
    for file in files:
        # to check if file is a .pdf file
        if ".pdf" not in file:
            continue

        print(f"\nCurrent File: {file}")
        map_name = file.split("_Building")[0]
        map = map_name + ".xls"

        cluster_number = k_means.get_cluster_number(READ_PATH, map)
        print(cluster_number)

        # Create different directories to store the data of different granularity
        for k_value in cluster_number:
            print(PDF_PATH + "/" + file)
            try:
                shutil.copy(
                    PDF_PATH + "/" + file, PDF_PATH + "/" + map_name + f"/k_{k_value}/"
                )
            except:
                os.makedirs(PDF_PATH + "/" + map_name + "/" + f"k_{k_value}/")
                shutil.copy(
                    PDF_PATH + "/" + file, PDF_PATH + "/" + map_name + f"/k_{k_value}/"
                )

            clusters_lst = get_clusters_kmeans(READ_PATH, map, k=k_value)
            adjancencies = find_adjacency(clusters_lst, k_value)

            try:
                os.remove(f"{PDF_PATH}/{map_name}/k_{k_value}/cluster_data.xlsx")
            except:
                pass

            workbook = xlsxwriter.Workbook(
                f"{PDF_PATH}/{map_name}/k_{k_value}/cluster_data.xlsx"
            )
            io_operations.save_data(clusters_lst, workbook)
            workbook.close()

            print("Adjacency Matrix: ")
            for i in range(len(adjancencies)):
                print(adjancencies[i])

            picked_color = [-1 for _ in range(len(clusters_lst))]
            picked_color[0] = 1
            dfs_coloring(1, len(adjancencies))

            print("\nPicked Color:")
            print(picked_color)

            annotator = PdfAnnotator(f"{PDF_PATH}/{map_name}/k_{k_value}/{file}")
            for i in range(len(picked_color)):
                color = colors.COLORS[picked_color[i] % 7]
                r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
                coloring(clusters_lst[i], annotator, (r, g, b, 1), size=10)
                print(
                    "Coloring cluster {} using color(r, g, b): {} {} {}".format(
                        str(i), str(r), str(g), str(b)
                    )
                )
                annotator.write(f"{WRITE_PATH}/{map_name}/k_{k_value}/{file}")
