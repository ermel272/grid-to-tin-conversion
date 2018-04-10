from __future__ import division

import matplotlib.pyplot as plt
import numpy as np

from gis.data_structures.grid import Grid
from gis.data_structures.tin import Tin
from gis.utils.raster_generator import generate_correlated_raster


def fjallstrom_convert(raster, max_error):
    """
    Converts the input raster into a TIN object with maximum error specified by param error.

    The algorithm implemented can be seen in "Algorithms for the All-nearest Neighbors Problem"
    by Per-Olof Fjallstrom.

    :param max_error: The maximum error allowed in the converted TIN.
    :param raster: A two-dimensional array of numbers.
    :return: An initialized TIN object.
    """
    assert 0 <= max_error <= 1, "Maximum error must be between 0 and 1."

    grid = Grid(raster)

    # Take the boundary points as the initial triangulation point set
    initial_tri_set = grid.get_corner_set()
    estimated_points = grid.points.difference(initial_tri_set)

    # Create initial triangulation and distribute points within
    triangulation_points = np.array([pt.array for pt in initial_tri_set])
    tin = Tin(triangulation_points, grid)
    tin.distribute_points(estimated_points)

    # Create list of points sorted by error value in ascending order
    error_array = np.sort(np.array([pt for pt in estimated_points]))

    while error_array.size > 0:
        # Pop point with highest error off of the top
        worst = error_array[-1]
        error_array = error_array[:-1]

        if worst.error <= max_error:
            break

        # Move the worst point from the estimated set to the set of points forming the triangulation
        triangulation_points = np.append(triangulation_points, [worst.array], axis=0)
        worst.reset_error()

        # Retriangulate the new points
        old_tin = tin
        tin = Tin(triangulation_points, grid)

        # Figure out which triangles are new and which have been deleted
        deleted_keys = {key for key in old_tin.get_keys() if key not in tin.get_keys()}
        removable_keys = {key for key in tin.get_keys() if key in old_tin.get_keys() and key not in deleted_keys}

        # Replace triangles in new Tin that have not been modified from old Tin
        for key in removable_keys:
            tin.replace_triangle(key, old_tin.get_triangle(key))

        # Find all the points with changed error values from the deleted triangles
        changed_points = np.array([])
        for key in deleted_keys:
            triangle = old_tin.get_triangle(key)
            changed_points = np.append(changed_points, triangle.points)

        # Distribute the changed points into the triangles & resort the error array
        tin.distribute_points(changed_points, remove=worst)
        error_array = np.sort(error_array)

    return tin, grid
