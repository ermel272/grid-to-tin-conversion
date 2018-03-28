from random import randint

import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from gis.fjallstrom import convert_to_tin
from gis.tin import Grid

if __name__ == '__main__':
    im = Image.open('cdem_dem_031G.tif')
    # start = randint(0, 2500)
    # imarray = np.array(im)[start:start + 500, start:start + 500]
    imarray = np.array(im)[1000:1400, 1000:1400]
    grid = Grid(imarray)

    start_time = time.time()
    dt = convert_to_tin(grid, 0.3)
    print("--- %s seconds ---" % (time.time() - start_time))

    plt.figure()
    plt.imshow(imarray, norm=Normalize(vmin=1, vmax=400),
               extent=[0, 0 + imarray.shape[1], 0, 0 + imarray.shape[0]],
               cmap='gist_earth')

    raster = grid.convert_to_raster()
    plt.figure()
    plt.imshow(raster, norm=Normalize(vmin=0, vmax=400),
               extent=[0, 0 + imarray.shape[1], 0, 0 + imarray.shape[0]],
               cmap='gist_earth')
    plt.show()
