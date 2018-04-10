import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import Normalize

from gis.algorithms.combined import combined_convert
from gis.algorithms.fjallstrom import fjallstrom_convert
from gis.algorithms.lee import lee_convert

if __name__ == '__main__':
    im = Image.open('cdem_dem_031G.tif')
    # start = randint(0, 2500)
    # imarray = np.array(im)[start:start + 500, start:start + 500]
    raster = np.array(im)[2000:2030, 2000:2030]

    start_time = time.time()
    dt, grid = fjallstrom_convert(raster, 0.1)
    print 'Fjallstrom:'
    print("--- %s seconds ---" % (time.time() - start_time))
    print 'Avg error: ', grid.average_error()
    print

    plt.imshow(grid.convert_to_raster(), norm=Normalize(vmin=1, vmax=400),
               extent=[0, 0 + raster.shape[1], 0, 0 + raster.shape[0]],
               cmap='gist_earth')
    plt.show()

    start_time = time.time()
    dt, grid = lee_convert(raster, 0.01)
    print 'Lee:'
    print("--- %s seconds ---" % (time.time() - start_time))
    print 'Avg error: ', grid.average_error()
    print

    plt.imshow(grid.convert_to_raster(), norm=Normalize(vmin=1, vmax=400),
               extent=[0, 0 + raster.shape[1], 0, 0 + raster.shape[0]],
               cmap='gist_earth')
    plt.show()

    start_time = time.time()
    dt, grid = combined_convert(raster, 0.01)
    print 'Combined:'
    print("--- %s seconds ---" % (time.time() - start_time))
    print 'Avg error: ', grid.average_error()
    print

    plt.imshow(grid.convert_to_raster(), norm=Normalize(vmin=1, vmax=400),
               extent=[0, 0 + raster.shape[1], 0, 0 + raster.shape[0]],
               cmap='gist_earth')
    plt.show()
