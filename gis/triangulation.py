from gis.graph import DirectedAcyclicGraph
from gis.tin import Point, Triangle


def delaunay_triangulation(p):
    """
    Computes the Delaunay Triangulation of the input point set p.

    Implements that algorithm described in page 200 of Computational
    Geometry - Algorithms and Applications by Mark de Berg et. al.
    (Third Edition).

    Note: Operates under the assumption that the input points are
    arranged on a grid (in a square or rectangular-like shape).

    :param p: A set of points in the two-dimensional plane.
    :return: A sequence of triangle objects, corresponding to a Delaunay
    Triangulation.
    """
    p_0 = __find_highest_point(p)
    p_minus1, p_minus2 = __find_binding_points(p_0)

    # Construct initial triangulation and point location DAG
    t = [Triangle(p_0, p_minus1, p_minus2)]
    dag = DirectedAcyclicGraph()
    dag.add_vertex(t[0])

    random_perm = p.difference({p_0})
    for point in random_perm:
        t = insert_point(t, point, dag)

    # TODO: Remove binding points, p_minus1 and p_minus2
    return t


def insert_point(t, p, dag):
    """
    Given a Delaunay Triangulation t, inserts the new point p
    and readjusts the Delaunay Triangulation.

    Note: Assumes that the point p is contained within a triangle of t.

    :param dag: The DAG representing the history of the triangulation.
    :param t: The list of triangles representing the DT.
    :param p: The point being added to the DT.
    :return: A new list of triangles.
    """
    def __find_triangle(p, dag):
        curr = dag.root

        # Traverse graph until the end
        while curr.num_edges() != 0:
            for triangle in curr.points:
                if triangle.contains(p):
                    curr = dag.graph.get(str(triangle))
                    break

        return curr.from_pt


def __find_highest_point(p):
    """
    Find the point in p with the highest x coordinate among all points with
    the highest y coordinate.

    :param p: The point set.
    :return: The lexicographically highest point.
    """
    highest = p[0]

    for point in p:
        if point.y > highest.y:
            highest = point
        elif point.y == highest.y and point.x > highest.x:
            highest = point

    return highest


def __find_binding_points(point):
    """
    Computes a large triangle defined by the input point.

    Note: Since we assumed that the input point set to the Delaunay triangulation
    is a grid, we know this point will be the highest and rightmost point on the grid.
    Since the grid has a rectangular or square shape, we can define the binding points
    by x & y coordinates the point given as a parameter here.

    :param point: The lexicographically highest point in the point set.
    :return: Two points that create a triangle with the input point around the
        entire pointset.
    """
    return Point(point.x, point.y - (2 * point.y)), \
           Point(point.x - (2 * point.x), point.y - (2 * point.y))
