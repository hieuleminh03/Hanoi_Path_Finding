class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def printPathDetails(self, src, dest, dist, pred):
        path = self.reconstructPath(pred, dest)
        total_weight = dist[dest]
        print(f"Shortest Path from {src} to {dest}: {path}")
        print(f"Total Weight: {total_weight}")

    def reconstructPath(self, pred, target):
        path = []
        current = target
        while current is not None:
            path.insert(0, current)
            current = pred[current]
        return path

    def BellmanFord(self, src, dest):
        if src < 0 or src >= self.V or dest < 0 or dest >= self.V:
            print("Invalid vertex inputs. Please provide valid vertices.")
            return

        dist = [float("Inf")] * self.V
        pred = [None] * self.V
        dist[src] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u

        self.printPathDetails(src, dest, dist, pred)


# Example usage:
g = Graph(5)
g.addEdge(0, 1, 4)
g.addEdge(0, 2, 2)
g.addEdge(1, 3, 1)
g.addEdge(2, 1, 1)
g.addEdge(2, 3, 3)
g.addEdge(3, 4, 5)

source_vertex = 0
destination_vertex = 4
g.BellmanFord(source_vertex, destination_vertex)
