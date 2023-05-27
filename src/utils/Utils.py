import os
import shutil
from math import atan2, sqrt

import xlsxwriter
from shapely import Polygon

from src.config.app_config import DIRECTIONS
from src.old_version.border import polar_angle, dist, is_counter_clockwise


class Utils:
    @staticmethod
    def get_border(points):
        p0 = min(points, key=lambda p: (p[1], p[0]))
        points.sort(key=lambda p: (polar_angle(p, p0), dist(p, p0)))
        border = []
        for i in range(len(points)):
            while len(border) >= 2 and not is_counter_clockwise(
                    border[-2], border[-1], points[i]
            ):
                border.pop()
            border.append(points[i])
        border.append(p0)
        return border

    @staticmethod
    def get_cluster_border(cluster):
        points = [(building.x, 3370 - building.y) for building in cluster.buildings]
        return Utils.get_border(points)

    @staticmethod
    def polar_angle(p, p0):
        return atan2((p[1] - p0[1]), (p[0] - p0[0]))

    @staticmethod
    def dist(p, p0):
        distance_x = p[0] - p0[0]
        distance_y = p[1] - p0[1]
        return sqrt(distance_x ** 2 + distance_y ** 2)

    @staticmethod
    def is_counter_clockwise(p1, p2, p3):
        return (p3[1] - p2[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p2[0])

    @staticmethod
    def is_adjacency(base_cluster, move_cluster):
        base_border = base_cluster.border
        move_border = move_cluster.border

        is_adjacency = False
        for direction in DIRECTIONS:
            distance = 0
            while distance <= 300 and not is_adjacency:
                distance += 15
                moved_border = Utils.get_moved_border(move_border, direction, distance)
                is_adjacency = Utils.is_intersects(base_border, moved_border)

        return is_adjacency

    @staticmethod
    def is_intersects(border1, border2):
        try:
            border1 = Polygon(border1)
            border2 = Polygon(border2)
            return border1.intersects(border2)

        except:
            return False

    @staticmethod
    def get_moved_border(border, direction, distance):
        moved = []
        for point in border:
            point = list(point)
            if direction == 'left':
                point[0] -= distance
            elif direction == 'right':
                point[0] += distance
            elif direction == 'up':
                point[1] += distance
            elif direction == 'down':
                point[1] -= distance
            elif direction == 'left_up':
                point[0] -= distance
                point[1] += distance
            elif direction == 'left_down':
                point[0] -= distance
                point[1] -= distance
            elif direction == 'right_up':
                point[0] += distance
                point[1] += distance
            elif direction == 'right_down':
                point[0] += distance
                point[1] -= distance
            moved.append(tuple(point))
        return moved

    @staticmethod
    def save_map(map, original_path, to_path):
        file_name = map.file_name
        map_name = map.name
        k = len(map.clusters)

        new_path = f'{to_path}{map_name}/{k}/'
        try:
            shutil.copy(original_path + file_name, new_path + file_name)
        except:
            os.makedirs(f'{to_path}{map_name}/{k}/')
            shutil.copy(original_path + file_name, new_path + file_name)
        return new_path

    @staticmethod
    def save_data(map, to_path):
        file_name = 'cluster_data.xlsx'
        try:
            os.remove(to_path + file_name)
        except:
            pass

        workbook = xlsxwriter.Workbook(to_path + file_name)
        Utils.save_map_data(map, workbook)
        workbook.close()

    @staticmethod
    def save_map_data(map, workbook):
        # save cluster data
        worksheet = workbook.add_worksheet("Clusters Data")
        worksheet.write(0, 0, "Cluster ID")
        for i in range(len(map.clusters)):
            cluster = map.clusters[i]
            cluster_format = workbook.add_format({"bold": True})
            worksheet.write(i + 1, 0, i, cluster_format)
            for j in range(len(cluster.buildings)):
                worksheet.write(i + 1, j + 1, cluster.buildings[j].id)

        # save adjacency data
        worksheet = workbook.add_worksheet("Adjacency Data")
        worksheet.write(0, 0, "Cluster ID")
        for i in range(len(map.adjacency_matrix)):
            adjacency_list = map.adjacency_matrix[i]
            cluster_format = workbook.add_format({"bold": True})
            worksheet.write(i + 1, 0, i, cluster_format)
            for j in range(len(adjacency_list)):
                worksheet.write(i + 1, j + 1, adjacency_list[j])
