import random
from math import atan2
from math import sqrt

from matplotlib import pyplot as plt


def graham_scan(points):
    """
    Compute the convex hull of a set of points using the Graham scan algorithm.

    Args:
        points (list): A list of (x, y) tuples representing the points.

    Returns:
        list: A list of (x, y) tuples representing the vertices of the convex hull.
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
    """
    Compute the polar angle of a point with respect to a reference point.

    Args:
        p (tuple): A tuple representing the (x, y) coordinates of the point.
        p0 (tuple): A tuple representing the (x, y) coordinates of the reference point.

    Returns:
        float: The polar angle of the point with respect to the reference point, in radians.
    """
    return atan2((p[1] - p0[1]), (p[0] - p0[0]))


def dist(p, p0):
    """
    Compute the Euclidean distance between two points.

    Args:
        p (tuple): A tuple representing the (x, y) coordinates of the first point.
        p0 (tuple): A tuple representing the (x, y) coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    distance_x = p[0] - p0[0]
    distance_y = p[1] - p0[1]
    return sqrt(distance_x ** 2 + distance_y ** 2)


def is_counter_clockwise(p1, p2, p3):
    """
    Determine whether three points are in counter-clockwise order.

    Args:
        p1 (tuple): A tuple representing the (x, y) coordinates of the first point.
        p2 (tuple): A tuple representing the (x, y) coordinates of the second point.
        p3 (tuple): A tuple representing the (x, y) coordinates of the third point.

    Returns:
        bool: True if the three points are in counter-clockwise order, False otherwise.
    """
    return (p3[1] - p2[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p2[0])


def draw_lines(points):
    """
    Plot a set of points as a line.

    Args:
        points (list): A list of tuples representing the (x, y) coordinates of the points.

    Returns:
        None
    """
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
