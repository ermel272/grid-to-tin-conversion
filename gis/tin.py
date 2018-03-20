import numpy as np


class Tin(object):
    def __init__(self, triangles=None):
        self.triangles = list() if not triangles else triangles

    def add_triangle(self, triangle):
        self.triangles.append(triangle)


class Triangle(object):
    def __init__(self, edges):
        assert len(edges) == 3, "A triangle must be defined by exactly three edges."
        self.edges = edges


class Edge(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = np.array([
            [x],
            [y]
        ])

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False
