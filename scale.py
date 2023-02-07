import math
from math import sqrt
from random import randint
from matplotlib import pyplot as plt
from border import graham_scan


def get_centroid(points):
    x_list = [point[0] for point in points]
    y_list = [point[1] for point in points]
    return sum(x_list) / len(points), sum(y_list) / len(points)


def get_centriod_by_cluster(cluster):
    buildings = []
    for building in cluster.buildings_lst:
        buildings.append((building.x, 3370 - building.y))
    return get_centroid(buildings)


def get_average_distance(centroid, points):
    total_distance = 0
    for point in points:
        total_distance += sqrt((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2)
    return total_distance / len(points)


def get_scale_points(points, scale_number):
    centroid = get_centroid(points)
    r = get_average_distance(centroid, points) * scale_number
    scaled_points = [(math.cos(2 * math.pi / 100 * x) * r + centroid[0], math.sin(2 * math.pi / 100 * x) * r + centroid[1]) for x in range(0, 100 + 1)]
    return scaled_points


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

    # Scaled polygon
    scaled_points = get_scale_points(hull, 2)
    print(f"Scaled: {scaled_points}")
    scaled_x, scaled_y = zip(*scaled_points)
    plt.plot(scaled_x, scaled_y, "-o", color="red")

    plt.show()
