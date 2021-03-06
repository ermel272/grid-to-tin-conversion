import numpy as np

from gis.data_structures.tin import Point


class Grid(object):
    def __init__(self, grid):
        self.grid, self.points = self.__initialize_grid(grid)
        self.width = len(grid)
        self.height = len(grid[0])

    def get(self, x, y):
        assert x <= self.width - 1 and y <= self.height - 1
        return self.grid[int(x)][int(y)]

    def get_corner_set(self):
        return {
            self.get(0, 0),
            self.get(self.width - 1, 0),
            self.get(0, self.height - 1),
            self.get(self.width - 1, self.height - 1)
        }

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

        return np.array(new_grid), points

    def average_error(self):
        total_error = 0
        for row in self.grid:
            for point in row:
                total_error += point.error

        return total_error / (self.width * self.height)

    def convert_to_raster(self):
        raster = list()
        for i in range(0, self.width):
            raster.append(list())
            for j in range(0, self.height):
                pt = self.grid[i][j]
                value = pt.estimate if pt.error > 0 else pt.value
                raster[i].append(value)

        return np.array(raster)
