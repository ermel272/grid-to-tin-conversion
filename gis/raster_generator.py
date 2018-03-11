from __future__ import division
import matplotlib.pyplot as plt
from random import randint

from math import floor


def generate_random_raster(n, maximum):
    return [[randint(0, maximum) for _ in range(0, n)] for _ in range(0, n)]


def generate_correlated_raster(n, maximum):
    correlation_width = int(floor(maximum / 10))
    raster = [list() for _ in range(0, n)]
    raster[0].append(randint(0, maximum))

    # Populate first line of data
    for i in range(1, n):
        if not flip_unfair_coin(n * 8):
            # Correlate raster point to previous point
            new = raster[0][i - 1] + randint(-correlation_width, correlation_width)
            raster[0].append(0 if new < 0 else maximum if new > maximum else new)
        else:
            raster[0].append(randint(0, maximum))

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
                raster[i].append(0 if new < 0 else maximum if new > maximum else new)
            else:
                raster[i].append(randint(0, maximum))

    return raster


def flip_unfair_coin(n):
    assert n >= 2
    return True if randint(1, n) == 1 else False


if __name__ == '__main__':
    # Test out the raster data generation
    n = 100
    max = 500

    data = generate_correlated_raster(n, max)

    plt.imshow(data, interpolation='nearest',
               extent=[0.5, 0.5 + n, 0.5, 0.5 + n],
               cmap='gist_earth')
    plt.show()
