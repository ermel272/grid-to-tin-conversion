from random import randint

import numpy as np


def flip_unfair_coin(n):
    assert n >= 2
    return True if randint(1, n) == 1 else False


def estimate_point_in_triangle(p, t1, t2, t3):
    """
    Compute the barycentric coordinate-based weightings of the triangle
    defined by t1, t2, and t3 in order to interpolate the value of the
    point p lying inside the triangle.
    """
    a = area_of_triangle(t1, t2, t3)
    a1 = area_of_triangle(p, t1, t2) / a
    a2 = area_of_triangle(p, t2, t3) / a
    a3 = area_of_triangle(p, t3, t1) / a
    return (a2 * t1.value) + (a1 * t3.value) + (a3 * t2.value)


def area_of_triangle(p1, p2, p3):
    """
    Computes the area of the triangle defined by p1, p2, and p3.
    """
    matrix = np.array([
        [p1.x, p2.x, p3.x],
        [p1.y, p2.y, p3.y],
        [1.0, 1.0, 1.0]
    ])
    return np.linalg.det(matrix) * 0.5