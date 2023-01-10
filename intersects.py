from random import randint
from border import graham_scan
from matplotlib import pyplot as plt
from shapely.geometry import Polygon


def is_intersects(poly1, poly2):
    if len(poly1) < 4 or len(poly2) < 4:
        return False
    poly1 = Polygon(poly1)
    poly2 = Polygon(poly2)
    return poly1.intersects(poly2)


if __name__ == "__main__":
    x = [randint(10, 100) for _ in range(10)]
    y = [randint(60, 100) for _ in range(10)]
    poly1 = list(zip(x, y))

    x = [randint(1, 50) for _ in range(10)]
    y = [randint(1, 100) for _ in range(10)]
    poly2 = list(zip(x, y))

    hull1 = graham_scan(poly1)
    hull2 = graham_scan(poly2)

    hull1_x, hull1_y = zip(*hull1)
    plt.plot(hull1_x, hull1_y, "-o", color="blue")

    hull2_x, hull2_y = zip(*hull2)
    plt.plot(hull2_x, hull2_y, "-o", color="green")

    print(is_intersects(hull1, hull2))

    plt.show()
