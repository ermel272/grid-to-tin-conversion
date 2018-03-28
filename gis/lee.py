import numpy as np

from gis.tin import Tin


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
    triangulation_points = grid.points.difference(non_removable_points)

    # Create initial Tin on all points of the grid
    tin = Tin(np.array(triangulation_points), grid)
