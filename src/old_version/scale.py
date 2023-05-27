import math
from math import sqrt
from random import randint
from matplotlib import pyplot as plt
from border import graham_scan


def get_centroid(points):
    """
    Calculate the centroid of the given points.

    Args:
        points (list): a list of 2-dimensional points represented as tuples

    Returns:
        tuple: a tuple that represents the centroid of the given points as (x,y) coordinate
    """
    x_list = [point[0] for point in points]
    y_list = [point[1] for point in points]
    return sum(x_list) / len(points), sum(y_list) / len(points)


def get_centriod_by_cluster(cluster):
    """
    Calculate the centroid of a given cluster.

    Args:
        cluster (Cluster): a Cluster object that contains a list of buildings

    Returns:
        tuple: a tuple that represents the centroid of the given cluster as (x,y) coordinate
    """
    buildings = []
    for building in cluster.buildings:
        buildings.append((building.x, 3370 - building.y))
    return get_centroid(buildings)


def get_average_distance(centroid, points):
    """
    Calculate the average distance between the centroid and the points.

    Args:
        centroid (tuple): a tuple that represents the centroid of a group of points as (x,y) coordinate
        points (list): a list of 2-dimensional points represented as tuples

    Returns:
        float: the average distance between the centroid and the given points
    """
    total_distance = 0
    for point in points:
        total_distance += sqrt((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2)
    return total_distance / len(points)


def get_circled_points(points, scale_number):
    """
    Scale the given points from their centroid and return them as a circle.

    Args:
        points (list): a list of 2-dimensional points represented as tuples
        scale_number (float): a number that represents the scale factor

    Returns:
        list: a list of 2-dimensional points that represents the circle created by the scaled points
    """
    centroid = get_centroid(points)
    r = get_average_distance(centroid, points) * scale_number
    scaled_points = [(math.cos(2 * math.pi / 100 * x) * r + centroid[0], math.sin(2 * math.pi / 100 * x) * r + centroid[1]) for x in range(0, 100 + 1)]
    return scaled_points


def get_moved_border(points, direction, distance):
    """
    Move the given points in a certain direction and distance.

    Args:
        points (list): a list of 2-dimensional points represented as tuples
        direction (str): a string that represents the direction to move the points ('left', 'right', 'up', 'down', 'left_up', 'left_down', 'right_up', 'right_down')
        distance (float): a number that represents the distance to move the points

    Returns:
        list: a list of 2-dimensional points that represents the new location of the given points after being moved in the given direction
    """
    moved = []
    for point in points:
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


if __name__ == "__main__":
    x = [randint(1, 30) for _ in range(10)]
    y = [randint(1, 30) for _ in range(10)]
    points = list(zip(x, y))
    print(f"Points: {points}")
    hull = graham_scan(points)
    print(f"Hull: {hull}")

    centroid = get_centroid(hull)
    print(centroid)
    plt.scatter(centroid[0], centroid[1], marker="o", color="black")

    # Original polygon
    hull_x, hull_y = zip(*hull)
    plt.plot(hull_x, hull_y, "-o", color="blue")

    # # Scaled polygon
    # scaled_points = get_scale_points(hull, 2)
    # print(f"Scaled: {scaled_points}")
    # scaled_x, scaled_y = zip(*scaled_points)
    # plt.plot(scaled_x, scaled_y, "-o", color="red")

    # move boundary
    moved = get_moved_border(points=hull, direction='left', distance=10)
    print(f"Scaled: {moved}")
    scaled_x, scaled_y = zip(*moved)
    plt.plot(scaled_x, scaled_y, "-o", color="red")

    plt.show()
