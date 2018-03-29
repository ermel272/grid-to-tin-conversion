import matplotlib.pyplot as plt
import numpy as np

from gis.data_structures.grid import Grid
from gis.data_structures.tin import Tin
from gis.utils.raster_generator import generate_correlated_raster


def lee_convert(grid, max_error):
    """
    Converts the input grid into a TIN object with maximum error specified by param error.

    The algorithm implemented can be seen in "Coverage and Visibility Problems on Topographic Surfaces"
    by Jay Lee.

    :param max_error: The maximum error allowed in the converted TIN.
    :param grid: A grid object.
    :return: An initialized TIN object.
    """
    assert 0 <= max_error <= 1, "Maximum error must be between 0 and 1."

    # Ensure algorithm does not remove corners so that triangles will always be able to interpolate
    non_removable_points = grid.get_corner_set()
    triangulation_points = np.array([pt.array for pt in grid.points])
    error_array = np.array([pt for pt in grid.points.difference(non_removable_points)])

    # Create initial Tin on all points of the grid
    tin = Tin(triangulation_points, grid)

    # Compute errors of points if they were to be removed from the triangulation
    tin.compute_hypothetical_errors(range(0, triangulation_points.shape[0]))
    error_array = np.sort(error_array)

    while error_array.size > 0:
        # Take point with smallest error off the front
        best = error_array[0]
        error_array = error_array[1:]
        triangulation_points = np.append([pt.array for pt in error_array],
                                         [pt.array for pt in non_removable_points], axis=0)

        if best.error >= max_error:
            break

        # Retriangulate & find indeces of the points neighbors in new tin
        tin = Tin(triangulation_points, grid)

        i = 0
        indices = list()
        for pt in tin.dt.points:
            pt = grid.get(pt[0], pt[1])
            if pt in best.neighbors:
                indices.append(i)
            i += 1

        # Recompute error values & sort
        tin.compute_hypothetical_errors(indices)
        error_array = np.sort(error_array)

    return tin


if __name__ == '__main__':
    # Test out the raster conversion
    n = 30
    max = 500

    raster = generate_correlated_raster(n, max)
    grid = Grid(raster)
    dt = lee_convert(grid, 0.05)

    plt.figure()
    plt.imshow(raster, interpolation='nearest',
               extent=[0, 0 + n, 0, 0. + n],
               cmap='gist_earth')

    raster = grid.convert_to_raster()
    plt.figure()
    plt.imshow(raster, interpolation='nearest',
               extent=[0, 0 + n, 0, 0 + n],
               cmap='gist_earth')
    plt.show()
