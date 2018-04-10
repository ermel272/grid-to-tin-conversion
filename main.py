import matplotlib.pyplot as plt

from gis.algorithms.fjallstrom import fjallstrom_convert
from gis.algorithms.lee import lee_convert
from gis.utils.raster_generator import generate_correlated_raster


def convert(sidelength=30, algorithm='fjallstrom', error=0.3):
    """
    Performs a demo of the Grid to TIN conversion algorithms using pyplot.

    :param sidelength: Controls the sidelength of the randomly generated raster image.
    :param algorithm: Controls the algorithm used to perform the conversion. Acceptable
                        values are 'fjallstrom' or 'lee'.
    :param error: A float value between zero and one controlling the error rate at which
                    the generated TIN will have.
    """
    raster = generate_correlated_raster(sidelength, 500)

    if algorithm == 'fjallstrom':
        dt, grid = fjallstrom_convert(raster, error)
    elif algorithm == 'lee':
        dt, grid = lee_convert(raster, error)
    else:
        return

    plt.figure()
    plt.title('Original Raster')
    plt.imshow(raster, extent=[0, sidelength, 0, sidelength], cmap='gist_earth')
    plt.xticks([])
    plt.yticks([])

    raster = grid.convert_to_raster()
    plt.figure()
    plt.title('Converted raster at {}% Error'.format(error * 100))
    plt.imshow(raster, extent=[0, sidelength, 0, sidelength], cmap='gist_earth')
    plt.xticks([])
    plt.yticks([])

    plt.show()
