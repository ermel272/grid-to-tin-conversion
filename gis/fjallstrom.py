from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

from gis.raster_generator import generate_correlated_raster
from gis.tin import Grid, Point, Triangle


def convert_to_tin(grid, max_error):
    """
    Converts the input grid into a TIN object with maximum error specified by param error.

    :param max_error: The maximum error allowed in the converted TIN.
    :param grid: A grid object.
    :return: An initialized TIN object.
    """
    assert 0 <= max_error <= 1, "Maximum error must be between 0 and 1."

    # Compute set S of boundary point_array
    s = {
        grid.get(0, 0),
        grid.get(grid.width - 1, 0),
        grid.get(0, grid.height - 1),
        grid.get(grid.width - 1, grid.height - 1)
    }
    point_set = grid.points.difference(s)

    def distribute_points(changed_points, triangles):
        """
        Distributes the set of change_points of Point objects into the dictionary triangles
        of newly instantiated Triangle objects.
        """
        for point in changed_points:
            simplex = dt.find_simplex(np.array([(point.x, point.y)]))
            triangle_pts = point_array[dt.simplices[simplex]]
            triangle = triangles[get_triangle_key(triangle_pts[0])]
            triangle.points.append(point)

            # Get the points defining the triangle from the grid
            p1 = grid.get(triangle_pts[0][0][0], triangle_pts[0][0][1])
            p2 = grid.get(triangle_pts[0][1][0], triangle_pts[0][1][1])
            p3 = grid.get(triangle_pts[0][2][0], triangle_pts[0][2][1])

            estimation = estimate_point_in_triangle(point, p1, p2, p3)
            point.error = abs((estimation - point.value) / point.value)
            point.estimate = estimation

    # Create initial triangulation and distribute points to triangles
    point_array = np.array([pt.array for pt in s])
    dt = Delaunay(point_array)
    tri_coords = point_array[dt.simplices]
    triangles = create_triangles(tri_coords)
    distribute_points(point_set, triangles)

    # Create initially sorted list of point error values
    error_array = [pt for pt in point_set]
    error_array.sort(key=lambda elem: elem.error)

    while True:
        # Find point of P with biggest error
        worst = error_array.pop()
        if worst.error <= max_error or len(point_set) == 0:
            break

        # Remove worst point from P and retriangulate
        point_set = point_set.difference({worst})
        worst.reset_estimates()
        s.add(worst)
        point_array = np.array([pt.array for pt in s])
        dt = Delaunay(np.array(point_array))
        tri_coords = point_array[dt.simplices]
        old_triangles = triangles
        triangles = create_triangles(tri_coords)

        # Figure out which triangles are new and which have been deleted
        deleted_keys = {key for key in old_triangles.keys() if key not in triangles.keys()}
        removable_keys = {key for key in triangles.keys() if key in old_triangles.keys() and key not in deleted_keys}

        # Replace triangles that have not been modified
        for key in removable_keys:
            del triangles[key]
            triangles[key] = old_triangles[key]

        # Find all the points from the deleted triangles
        changed_points = list()
        for key in deleted_keys:
            triangle = old_triangles[key]
            changed_points += triangle.points

        # Distribute the changed_points into the triangles
        distribute_points(changed_points, triangles)
        error_array.sort(key=lambda elem: elem.error)

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


def create_triangles(tri_coords):
    """
    Creates a dictionary of triangles given their coordinates.
    """
    triangles = dict()
    for coord in tri_coords:
        p1 = Point(coord[0][0], coord[0][1])
        p2 = Point(coord[1][0], coord[1][1])
        p3 = Point(coord[2][0], coord[2][1])
        triangles[get_triangle_key(coord)] = Triangle(p1, p2, p3)

    return triangles


def get_triangle_key(coord):
    """
    Turns a triangles point coordinates into a one-dimensional string key.
    """
    return "({}, {}), ({}, {}), ({}, {})".format(
        coord[0][0], coord[0][1],
        coord[1][0], coord[1][1],
        coord[2][0], coord[2][1]
    )


if __name__ == '__main__':
    # Test out the raster data generation
    n = 100
    max = 500

    raster = generate_correlated_raster(n, max)
    grid = Grid(raster)
    dt = convert_to_tin(grid, 0.3)

    plt.imshow(raster, interpolation='nearest',
               extent=[0.5, 0.5 + n, 0.5, 0.5 + n],
               cmap='gist_earth')
    plt.show()

    raster = grid.convert_to_raster()
    plt.imshow(raster, interpolation='nearest',
               extent=[0, 0 + n, 0, 0 + n],
               cmap='gist_earth')
    plt.show()
