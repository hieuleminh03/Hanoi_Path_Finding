# this is an implementation of bellman ford algorithm

import utils
import algorithms


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def getPathDetails(self, dest, dist, pred) -> list[int, list]:
        path = self.reconstructPath(pred, dest)
        total_weight = dist[dest]
        return [total_weight, path]

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
                print(f"Checking edge ({u}, {v}) with weight {w}")
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u

        # self.printPathDetails(src, dest, dist, pred)
        return self.getPathDetails(dest, dist, pred)


'''
    call bellman with prepared data
'''


def call_bellman(graph: dict, start: int, dest: int) -> list[int, list]:
    vertices_count = len(graph)
    print("Vertices count: ", vertices_count)
    g = Graph(vertices_count)
    for node in graph:
        for neighbor, weight in graph[node]:
            g.addEdge(int(node), int(neighbor), int(weight))
    print("Graph: ", g.graph)
    data = g.BellmanFord(start, dest)
    print("Weight: ", data[0])  # Access total_weight from the list
    print("Path: ", data[1])    # Access path from the list


if __name__ == "__main__":
    graph: dict = algorithms.convert_dict_grap(utils.read_data('data.json'))
    call_bellman(graph, 0, 4)
