from gis.tin import Point
from gis.triangulation import delaunay_triangulation


def convert_to_tin(grid, error):
    """
    Converts the input grid into a TIN object with maximum error specified by param error.

    :param error: The maximum error allowed in the converted TIN.
    :param grid: A two-dimensional array of of numbers, representing a raster.
    :return: An initialized TIN object.
    """
    assert 0 <= error <= 1, "Maximum error must be between 0 and 1."
    width = len(grid)
    height = len(grid[0])

    # Compute set S of boundary points
    s = {
        Point(0, 0, grid[0][0]),
        Point(width - 1, 0, grid[width - 1][0]),
        Point(0, height - 1, grid[0][height - 1]),
        Point(width - 1, height - 1, grid[width - 1][height - 1])
    }

    # Create initial triangulation of the set S of points
    dt = delaunay_triangulation(s)
