from random import randint
from matplotlib import pyplot as plt
from border import graham_scan


def get_centroid(points):
    x_list = [point[0] for point in points]
    y_list = [point[1] for point in points]
    return sum(x_list) / len(points), sum(y_list) / len(points)


def get_scale_points(points, scale_number):
    centroid = get_centroid(points)
    scaled_points = []
    for point in points:
        scaled_x = centroid[0] + (point[0] - centroid[0]) * scale_number
        scaled_y = centroid[1] + (point[1] - centroid[1]) * scale_number
        scaled_points.append((scaled_x, scaled_y))
    return scaled_points


if __name__ == '__main__':
    x = [randint(1, 30) for _ in range(10)]
    y = [randint(1, 30) for _ in range(10)]
    points = list(zip(x, y))
    print(f'Points: {points}')
    hull = graham_scan(points)
    print(f'Hull: {hull}')

    # centroid_x, centroid_y = get_centroid(hull)
    # print(centroid_x, centroid_y)
    centroid = get_centroid(hull)
    print(centroid)
    plt.scatter(centroid[0], centroid[1], marker="o", color="black")

    # Original polygon
    hull_x, hull_y = zip(*hull)
    plt.plot(hull_x, hull_y, "-o", color="blue")

    # Scaled polygon
    scaled_points = get_scale_points(hull, 2)
    print(f'Scaled: {scaled_points}')
    scaled_x, scaled_y = zip(*scaled_points)
    plt.plot(scaled_x, scaled_y, "-o", color="red")

    plt.show()
