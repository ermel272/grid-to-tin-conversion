import numpy as np


class Tin(object):
    def __init__(self, triangles=None):
        self.triangles = list() if not triangles else triangles

    def add_triangle(self, triangle):
        self.triangles.append(triangle)


class Grid(object):
    def __init__(self, grid):
        self.grid, self.points = self.__initialize_grid(grid)
        self.width = len(grid)
        self.height = len(grid[0])

    def get(self, x, y):
        assert x <= self.width - 1 and y <= self.height - 1
        return self.grid[x][y]

    @staticmethod
    def __initialize_grid(grid):
        new_grid = list()
        points = set()
        for i in range(0, len(grid)):
            new_grid.append(list())
            for j in range(0, len(grid[i])):
                new_pt = Point(i, j, value=grid[i][j])
                new_grid[i].append(new_pt)
                points.add(new_pt)

        return new_grid, points


class Triangle(object):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.e1 = Edge(p1, p2)
        self.e2 = Edge(p2, p3)
        self.e3 = Edge(p3, p1)

    def __str__(self):
        return '({}, {}, {})'.format(str(self.p1), str(self.p2), str(self.p3))

    def __hash__(self):
        return hash((str(self.p1), str(self.p2), str(self.p3)))

    def __eq__(self, other):
        return True if self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3 else False

    def contains(self, p):
        # Ugly test, since we don't know the orientation of the points
        if (right_turn(self.p1, self.p2, p) and
                right_turn(self.p2, self.p3, p) and
                right_turn(self.p3, self.p1, p)) \
                or (right_turn(self.p1, self.p3, p) and
                        right_turn(self.p3, self.p2, p) and
                        right_turn(self.p2, self.p1, p)):
            return True

        return False

    def is_on_edge(self, p):
        if p.is_on_edge(self.e1):
            return self.e1
        elif p.is_on_edge(self.e2):
            return self.e2
        elif p.is_on_edge(self.e3):
            return self.e3
        return None


class Edge(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
        self.y_int = self.p1.y - (self.slope * self.p1.x)
        self.d = np.linalg.norm(self.p1.v - self.p2.v)


class Point(object):
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.v = np.array([
            [x],
            [y]
        ])
        self.value = value
        self.array = [self.x, self.y]

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False

    def is_on_edge(self, edge):
        if self.y == (edge.slope * self.x) + edge.y_int:
            if edge.p1.x < edge.p2.x:
                return edge.p1.x <= self.x <= edge.p2.x
            elif edge.p2.x < edge.p1.x:
                return edge.p2.c <= self.x <= edge.p1.x
            elif edge.p1.y < edge.p2.y:
                return edge.p1.y <= self.y <= edge.p2.y
            elif edge.p2.y < edge.p1.y:
                return edge.p2.y <= self.y <= edge.p1.y

        return False


def right_turn(p1, p2, p3):
    """
    Determines if p1 -> p2 -> p3 is a right turn.

    Note: Counts three points on the same line as a right turn.
    """
    det = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return det >= 0
