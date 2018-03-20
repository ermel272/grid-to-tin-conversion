class Graph(object):
    def __init__(self):
        self.graph = dict()
        self.root = None

    def add_vertex(self, point):
        if not self.graph.get(str(point)):
            self.graph[str(point)] = self._AdjacencyContainer(point)
            return True

        if not self.root:
            self.root = self.graph[str(point)]

        return False

    def add_edge(self, p1, p2, weight=None):
        self.add_vertex(p1)
        return self.graph[str(p1)].add(p2, weight)

    class _AdjacencyContainer(object):
        def __init__(self, point):
            self.from_pt = point
            self.points = list()
            self.point_set = set()
            self.weights = dict()

        def add(self, point, weight=None):
            if point not in self.point_set:
                self.points.append(point)
                self.point_set.add(point)
                self.weights[str(point)] = weight
                return True

            return False

        def is_in(self, point):
            return point in self.point_set

        def num_edges(self):
            return len(self.points)


class DirectedAcyclicGraph(Graph):
    def __init__(self):
        super(DirectedAcyclicGraph).__init__()

    def add_edge(self, p1, p2, weight=None):
        self.add_vertex(p1)
        other = self.graph.get(str(p2))

        # Ensure acyclic property of the graph
        if not other or not other.is_in(p1):
            return self.graph[str(p1)].add(p2, weight)

        return False
