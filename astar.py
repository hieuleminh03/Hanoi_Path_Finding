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
    def heuristic(state, goal):
        return 0

    open_list = []  # Danh sách các nút chưa xử lý
    closed_list = set()  # Danh sách các nút đã xử lý

    start_node = Node(state=start, cost=0, heuristic=heuristic(start, goal))
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
                            heuristic=heuristic(neighbor, goal))

            if new_node not in open_list:
                heapq.heappush(open_list, new_node)

    return None, 0

# Đồ thị có trọng số
graph = {'1001': [('1002', 1)], '1002': [('1003', 5), ('1004', 2), ('1006', 7)], '1003': [('1006', 1), ('1005', 2)], '1004': [('1003', 1), ('1005', 4), ('1001', 2)], '1005': [('1004', 3)], '1006': []}


start_node = '1001'
goal_node = '1005'
path, total_cost = astar(graph, start_node, goal_node)
map_list=[]
if path:
    print("Đường đi tìm thấy:")
    for node, _ in path:
        map_list.append(node)
        print(node)

    print("Tổng trọng số:", total_cost)
else:
    print("Không tìm thấy đường đi")
