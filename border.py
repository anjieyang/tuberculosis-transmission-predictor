import random
from math import sqrt
from math import atan2
from matplotlib import pyplot as plt


def graham_scan(points):
    """
    Returns list of border points by graham scan algorithm
    :param points: List of points
    :return: List of border points
    """
    p0 = min(points, key=lambda p: (p[1], p[0]))
    points.sort(key=lambda p: (polar_angle(p, p0), dist(p, p0)))
    hull = []
    for i in range(len(points)):
        while len(hull) >= 2 and not is_counter_clockwise(
            hull[-2], hull[-1], points[i]
        ):
            hull.pop()
        hull.append(points[i])
    hull.append(p0)
    return hull


def polar_angle(p, p0):
    return atan2((p[1] - p0[1]), (p[0] - p0[0]))


def dist(p, p0):
    distance_x = p[0] - p0[0]
    distance_y = p[1] - p0[1]
    return sqrt(distance_x**2 + distance_y**2)


def is_counter_clockwise(p1, p2, p3):
    return (p3[1] - p2[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p2[0])


def draw_lines(points):
    x, y = zip(*points)
    plt.plot(x, y, "-o", color="blue")
    plt.show()


if __name__ == "__main__":
    x = []
    y = []
    for _ in range(20):
        x.append(random.randint(0, 50))
        y.append(random.randint(0, 50))

    points = list(zip(x, y))

    print(f"Points: {points}")
    p0 = min(points, key=lambda p: (p[1], p[0]))
    print(f"Original Point: {p0}")

    plt.scatter(x, y)

    hull = graham_scan(points)
    print(hull)

    draw_lines(hull)
