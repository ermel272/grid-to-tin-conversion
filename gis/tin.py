import numpy as np


class Tin(object):
    def __init__(self, triangles=None):
        self.triangles = list() if not triangles else triangles

    def add_triangle(self, triangle):
        self.triangles.append(triangle)


class Triangle(object):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        return '({}, {}, {})'.format(str(self.p1), str(self.p2), str(self.p3))

    def __hash__(self):
        return hash((str(self.p1), str(self.p2), str(self.p3)))

    def __eq__(self, other):
        return True if self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3 else False

    def contains(self, p):
        # TODO: implement
        return True


class Edge(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Point(object):
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.v = np.array([
            [x],
            [y]
        ])
        self.value = value

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False


def right_turn(p1, p2, p3):
    """
    Determines if p1 -> p2 -> p3 is a right turn.

    Note: Counts three points on the same line as a right turn.
    """
    det = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return det >= 0
