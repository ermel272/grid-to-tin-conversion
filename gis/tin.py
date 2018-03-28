import numpy as np
from scipy.spatial.qhull import Delaunay

from gis.utils import estimate_point_in_triangle


class Tin(object):
    def __init__(self, triangulation_pts, grid):
        self.grid = grid
        self.triangulation_pts = triangulation_pts
        self.dt = Delaunay(triangulation_pts)
        self.triangles = self.__init_triangles(triangulation_pts[self.dt.simplices])

    def get_keys(self):
        return self.triangles.keys()

    def get_triangle(self, key):
        return self.triangles.get(key)

    def replace_triangle(self, key, new_triangle):
        """
        Replaces a triangle by param new_triangle given their key.
        """
        if self.triangles.get(key):
            del self.triangles[key]
            self.triangles[key] = new_triangle
            return True

        return False

    def distribute_points(self, points):
        """
        Distributes some points into the Triangles to which they belong.
        """
        for point in points:
            simplex = self.dt.find_simplex(np.array([(point.x, point.y)]))
            triangle_pts = self.triangulation_pts[self.dt.simplices[simplex]]
            triangle = self.triangles[Triangle.get_triangle_key(triangle_pts[0])]
            triangle.points.append(point)

            # Get the points defining the triangle from the grid
            p1 = self.grid.get(triangle_pts[0][0][0], triangle_pts[0][0][1])
            p2 = self.grid.get(triangle_pts[0][1][0], triangle_pts[0][1][1])
            p3 = self.grid.get(triangle_pts[0][2][0], triangle_pts[0][2][1])

            # Edit the points estimation and error values
            estimation = estimate_point_in_triangle(point, p1, p2, p3)
            point.error = abs((estimation - point.value) / point.value)
            point.estimate = estimation

    @staticmethod
    def __init_triangles(tri_coords):
        """
        Creates a dictionary of triangles given their coordinates.
        """
        triangles = dict()
        for coord in tri_coords:
            p1 = Point(coord[0][0], coord[0][1])
            p2 = Point(coord[1][0], coord[1][1])
            p3 = Point(coord[2][0], coord[2][1])
            triangles[Triangle.get_triangle_key(coord)] = Triangle(p1, p2, p3)

        return triangles


class Grid(object):
    def __init__(self, grid):
        self.grid, self.points = self.__initialize_grid(grid)
        self.width = len(grid)
        self.height = len(grid[0])

    def get(self, x, y):
        assert x <= self.width - 1 and y <= self.height - 1
        return self.grid[x][y]

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

    @staticmethod
    def get_triangle_key(coord):
        """
        Given a list of triangle x and y coordinates, generates a string key.
        """
        return "({}, {}), ({}, {}), ({}, {})".format(
            coord[0][0], coord[0][1],
            coord[1][0], coord[1][1],
            coord[2][0], coord[2][1]
        )


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
