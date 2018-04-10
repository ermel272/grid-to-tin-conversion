import matplotlib.pyplot as plt
import time

from gis.algorithms.fjallstrom import fjallstrom_convert
from gis.algorithms.lee import lee_convert
from gis.utils.raster_generator import generate_correlated_raster

if __name__ == '__main__':
    n = 40
    max = 500
    error = 0.05
    f_times = list()
    f_errors = list()
    l_times = list()
    l_errors = list()

    for i in range(0, 10):
        raster = generate_correlated_raster(n, max)

        start_time = time.time()
        dt, grid = fjallstrom_convert(raster, error)
        f_times.append(time.time() - start_time)
        f_errors.append(grid.average_error())

        start_time = time.time()
        dt, grid = lee_convert(raster, error)
        l_times.append(time.time() - start_time)
        l_errors.append(grid.average_error())

    print "Number of pixels: ", n ** 2

    print

    print "Fjallstrom"
    print "Average time: ", sum(f_times) / len(f_times)
    print "Average error: ", sum(f_errors) / len(f_errors)

    print

    print "Lee"
    print "Average time: ", sum(l_times) / len(l_times)
    print "Average error: ", sum(l_errors) / len(l_errors)
