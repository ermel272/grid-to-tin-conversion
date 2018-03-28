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

    def convert_to_raster(self):
        raster = list()
        for i in range(0, self.width):
            raster.append(list())
            for j in range(0, self.height):
                pt = self.grid[i][j]
                value = pt.estimate if pt.error > 0 else pt.value
                raster[i].append(value)

        return raster


class Triangle(object):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.points = list()

    def __str__(self):
        return '({}, {}, {})'.format(str(self.p1), str(self.p2), str(self.p3))

    def __hash__(self):
        return hash((str(self.p1), str(self.p2), str(self.p3)))

    def __eq__(self, other):
        return True if self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3 else False


class Point(object):
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.v = np.array([
            [x],
            [y]
        ])
        self.value = value
        self.estimate = 0
        self.error = 0
        self.array = [self.x, self.y]

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return True if (self.x == other.x and self.y == other.y) else False

    def __cmp__(self, other):
        return cmp(self.error, other.error)

    def reset_error(self):
        self.estimate = 0
        self.error = 0
