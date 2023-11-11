import heapq

def algorithm_ucs(grap, start_point, end_point):
    visited = ()
    queue = [(0, [start_point])]
    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]
        if node not in visited:
            visited = visited + (node,)
            if node == end_point:
                return cost, path
            for neighbor, weight in grap.get(node, ()):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_cost = cost + weight
                    heapq.heappush(queue, (new_cost, new_path))
    return 0, []
def ucs(graph :dict, start_point: dict, end_point: dict) -> list:
    start_node = start_point.get('id')
    goal_node = end_point.get('id')
    total_cost,path = algorithm_ucs(graph, start_node, goal_node)
    return [path, total_cost]

