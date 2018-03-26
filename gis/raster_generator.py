from __future__ import division
import matplotlib.pyplot as plt
from random import randint

from math import floor


def generate_random_raster(n, maximum):
    """
    Generates a raster of dimension (n x n) with grid value at most param maximum.
    All raster values are random.

    :param n: The grid height of the raster.
    :param maximum: The maximum value of a particular raster cell.
    :return: A (n x n) raster in list format.
    """
    return [[randint(1, maximum) for _ in range(0, n)] for _ in range(0, n)]


def generate_correlated_raster(n, maximum):
    """
    Generates a raster of dimension (n x n) with grid value at most param maximum.
    The algorithm attempts to correlate previous cell values to new ones.

    :param n: The grid height of the raster.
    :param maximum: The maximum value of a particular raster cell.
    :return: A (n x n) raster in list format.
    """
    correlation_width = int(floor(maximum / 10))
    raster = [list() for _ in range(0, n)]
    raster[0].append(randint(1, maximum))

    # Populate first line of data
    for i in range(1, n):
        if not flip_unfair_coin(n * 8):
            # Correlate raster point to previous point
            new = raster[0][i - 1] + randint(-correlation_width, correlation_width)
            raster[0].append(1 if new <= 0 else maximum if new > maximum else new)
        else:
            raster[0].append(randint(1, maximum))

    # Generate the rest of the raster
    for i in range(1, n):
        for j in range(0, n):
            if not flip_unfair_coin(n * 8):
                # Correlate raster pt to nearby points
                if j == 0:
                    prev = raster[i - 1][0]
                else:
                    prev = int(floor((raster[i][j - 1] + raster[i - 1][j]) / 2))

                new = prev + randint(-correlation_width, correlation_width)
                raster[i].append(1 if new <= 0 else maximum if new > maximum else new)
            else:
                raster[i].append(randint(1, maximum))

    return raster


def flip_unfair_coin(n):
    assert n >= 2
    return True if randint(1, n) == 1 else False


if __name__ == '__main__':
    # Test out the raster data generation
    n = 1000
    max = 500

    raster = generate_correlated_raster(n, max)

    plt.imshow(raster, interpolation='nearest',
               extent=[0.5, 0.5 + n, 0.5, 0.5 + n],
               cmap='gist_earth')
    plt.show()
