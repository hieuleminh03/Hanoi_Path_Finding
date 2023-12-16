import heapq
import algorithms
import utils

class FloydWarshall:
    def floyd_warshall(graph):
        nodes = list(graph.keys())
        n = len(nodes)

        # Initialize distance matrix with infinity for unconnected nodes
        distance_matrix = {i: {j: float('inf') for j in nodes} for i in nodes}
        next_node_matrix = {i: {j: None for j in nodes} for i in nodes}

        # Update distance matrix with actual edge weights
        for node in nodes:
            for neighbor, weight in graph.get(node, []):
                distance_matrix[node][neighbor] = weight
                next_node_matrix[node][neighbor] = neighbor

        # Floyd-Warshall algorithm
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if distance_matrix[i][k] + distance_matrix[k][j] < distance_matrix[i][j]:
                        distance_matrix[i][j] = distance_matrix[i][k] + distance_matrix[k][j]
                        next_node_matrix[i][j] = next_node_matrix[i][k]

        return distance_matrix, next_node_matrix


    def get_shortest_distance(result_matrix, node1, node2):
        return result_matrix[node1][node2]


    def get_shortest_path(next_node_matrix, node1, node2):
        path = [node1]
        while node1 != node2:
            node1 = next_node_matrix[node1][node2]
            path.append(node1)
        return path

if __name__ == "__main__":
    graph = algorithms.convert_dict_grap(utils.read_data('data.json'))
    result_matrix, next_node_matrix = FloydWarshall.floyd_warshall(graph)
    node1 = '1'
    node2 = '5'
    shortest_distance = FloydWarshall.get_shortest_distance(result_matrix, node1, node2)
    shortest_path = FloydWarshall.get_shortest_path(next_node_matrix, node1, node2)
    print(f"Shortest distance between node {node1} and node {node2}: {shortest_distance}")
    print(f"Shortest path: {' -> '.join(map(str, shortest_path))}")
