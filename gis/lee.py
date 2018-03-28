import numpy as np
from scipy.spatial.qhull import Delaunay


def lee_convert(grid, max_error):
    """
    Converts the input grid into a TIN object with maximum error specified by param error.

    The algorithm implemented can be seen in "Coverage and Visibility Problems on Topographic Surfaces"
    by Jay Lee.

    :param max_error: The maximum error allowed in the converted TIN.
    :param grid: A grid object.
    :return: An initialized TIN object.
    """
    # Create initial triangulation and distribute points to triangles
    point_array = np.array([pt.array for pt in grid.points])
    dt = Delaunay(point_array)
