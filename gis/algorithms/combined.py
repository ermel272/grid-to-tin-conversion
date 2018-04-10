import matplotlib.pyplot as plt
import sys
from multiprocessing import Process, Manager

from gis.algorithms.fjallstrom import fjallstrom_convert
from gis.algorithms.lee import lee_convert
from gis.utils.raster_generator import generate_correlated_raster


def run_lee(queue, raster, max_error):
    sys.setrecursionlimit(4000)
    tin, grid = lee_convert(raster, max_error)
    queue.put([tin, grid])


def run_fjallstrom(queue, raster, max_error):
    sys.setrecursionlimit(4000)
    tin, grid = fjallstrom_convert(raster, max_error)
    queue.put([tin, grid])


def combined_convert(raster, max_error):
    """
    Parallelizes both the Fjallstrom and Lee grid to tin conversion methods
    in order to optimize between both of the speeds.

    The theory behind this is that the Lee method performs much faster on lower max_error values,
    while the Fjallstrom method performs much faster on high max_error values.

    :param max_error: The maximum error allowed in the converted TIN.
    :param raster: A two dimensional array of numbers
    :return: An initialized TIN object.
    """
    q = Manager().Queue()
    p1 = Process(target=run_lee, args=(q, raster, max_error,))
    p2 = Process(target=run_fjallstrom, args=(q, raster, max_error,))

    # Start the race
    p1.start()
    p2.start()

    result = q.get()

    # Join both processes - terminating both
    p1.terminate()
    p2.terminate()
    p1.join()
    p2.join()

    # Return both the tin and grid from the winning algorithm
    return result[0], result[1]
