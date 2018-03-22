from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

from gis.raster_generator import generate_correlated_raster
from gis.tin import Grid


def convert_to_tin(grid, error):
    """
    Converts the input grid into a TIN object with maximum error specified by param error.

    :param error: The maximum error allowed in the converted TIN.
    :param grid: A grid object.
    :return: An initialized TIN object.
    """
    assert 0 <= error <= 1, "Maximum error must be between 0 and 1."

    # Compute set S of boundary points
    s = {
        grid.get(0, 0),
        grid.get(grid.width - 1, 0),
        grid.get(0, grid.height - 1),
        grid.get(grid.width - 1, grid.height - 1)
    }
    p = grid.points.difference(s)

    # Create initial triangulation of the set S of points
    points = np.array([pt.array for pt in s])
    dt = Delaunay(np.array(points))

    def __update_error(point):
        simplex = dt.find_simplex(np.array([(point.x, point.y)]))
        triangle = points[dt.simplices[simplex]]

        # Get the points defining the triangle from the grid
        p1 = grid.get(triangle[0][0][0], triangle[0][0][1])
        p2 = grid.get(triangle[0][1][0], triangle[0][1][1])
        p3 = grid.get(triangle[0][2][0], triangle[0][2][1])

        estimation = estimate_point_in_triangle(point, p1, p2, p3)
        error = estimation / point.value

        return error

    while True:
        worst = None
        worst_error = 0

        # Find point of P with biggest error
        for point in p:
            pt_error = __update_error(point)
            if not worst or pt_error > worst_error:
                worst = point
                worst_error = pt_error

        if worst_error <= error:
            break

        # Remove worst point from P
        p = p.difference({worst})
        s.add(worst)
        points = np.array([pt.array for pt in s])
        dt = Delaunay(np.array(points))

        # Plot the triangulation
        # plt.triplot(points[:, 0], points[:, 1], dt.simplices.copy())
        # plt.plot(points[:, 0], points[:, 1], 'o')
        # plt.show()

    return dt


def estimate_point_in_triangle(p, t1, t2, t3):
    """
    Compute the barycentric coordinate weightings of the triangle
    defined by t1, t2, and t3 in order to interpolate the value of the
    point p lying inside the triangle.
    """
    a = area_of_triangle(t1, t2, t3)
    a1 = area_of_triangle(p, t1, t2) / a
    a2 = area_of_triangle(p, t2, t3) / a
    a3 = area_of_triangle(p, t3, t1) / a
    return (a2 * t1.value) + (a1 * t3.value) + (a3 * t2.value)


def area_of_triangle(p1, p2, p3):
    """
    Computes the area of the triangle defined by p1, p2, and p3.
    """
    matrix = np.array([
        [p1.x, p2.x, p3.x],
        [p1.y, p2.y, p3.y],
        [1.0, 1.0, 1.0]
    ])
    return np.linalg.det(matrix) * 0.5


if __name__ == '__main__':
    # Test out the raster data generation
    n = 10
    max = 500

    raster = generate_correlated_raster(n, max)
    grid = Grid(raster)
    dt = convert_to_tin(grid, 0.1)

    plt.imshow(raster, interpolation='nearest',
               extent=[0.5, 0.5 + n, 0.5, 0.5 + n],
               cmap='gist_earth')
    plt.show()
