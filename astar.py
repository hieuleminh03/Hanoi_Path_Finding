import heapq

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state  # Trạng thái tại nút này
        self.parent = parent  # Nút cha
        self.action = action  # Hành động dẫn đến nút này từ nút cha
        self.cost = cost  # Tổng chi phí từ nút gốc đến nút này
        self.heuristic = heuristic  # Ước tính chi phí từ nút này đến đích

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def astar(graph, start, goal):
    def heuristic(grap, start_point, end_point):
        visited = ()
        queue = [( 0,[start_point])]
        while queue:
            (cost,path) = heapq.heappop(queue)
            node = path[-1]
            if node not in visited:
                visited = visited + (node,)
                if node == end_point:
                    return  cost
                for neighbor, weight in grap.get(node, ()):
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        new_cost = cost + weight
                        heapq.heappush(queue, (new_cost,new_path))
        if(path[-1] != end_point):
            return float('inf')
        else:
            return cost

    open_list = []  # Danh sách các nút chưa xử lý
    closed_list = set()  # Danh sách các nút đã xử lý

    start_node = Node(state=start, cost=0, heuristic=heuristic(graph,start, goal))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.state == goal:
            path = []
            total_cost = current_node.cost
            while current_node:
                path.append((current_node.state, current_node.action))
                current_node = current_node.parent
            return list(reversed(path)), total_cost

        closed_list.add(current_node.state)

        for neighbor, edge_cost in graph[current_node.state]:
            if neighbor in closed_list:
                continue

            new_cost = current_node.cost + edge_cost
            new_node = Node(state=neighbor, parent=current_node,
                            action=None, cost=new_cost,
                            heuristic=heuristic(graph,neighbor, goal))

            if new_node not in open_list:
                heapq.heappush(open_list, new_node)

    return None, 0


def a_star(graph :dict, start_point: dict, end_point: dict) -> list:
    start_node = start_point.get('id')
    goal_node = end_point.get('id')
    path, total_cost = astar(graph, start_node, goal_node)
    points = []
    for node, _ in path:
        points.append(node)
    return [points, total_cost]
    