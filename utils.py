import json
import random
import os
import heapq
'''
    File manipulation utils
'''


def generate_data(total: int, limit: int) -> list[dict]:
    # khoi tao mang chua cac diem
    points: list[dict] = [{} for i in range(total)]
    # cai dat cac thong so co ban cho cac diem
    for point in points:
        point["id"]: str = str(points.index(point) + 1001)
        point["name"]: str = "point " + str(point["id"])
        point["point_limit"]: int = random.randint(1, limit)
        point["count"]: int = 0
        point["relative"]: dict = dict()
    # duyet xu ly tung point
    for point in points:
        # con thieu bao nhieu relative thi lap bay nhieu lan
        while point["point_limit"] > point["count"]:
            suitable_relatives = [x for x in points
                                  if x["id"] != point["id"]
                                  and x["count"] < x["point_limit"]
                                  and x["id"] not in point["relative"].keys()]
            if len(suitable_relatives) > 0:
                relative = random.choice(suitable_relatives)
                point["relative"][relative["id"]] = random.randint(1, 10)
                relative["count"] += 1
                point["count"] += 1
            else:
                point["point_limit"] = point["count"]
                break
    return points

def make_new_json(data: list[dict]) -> None:
    # read how many data file is in \data
    file_count = len([name for name in os.listdir("data/")])
    # makke new file with name is file_count + 1.json with proper format
    with open("data/" + str(file_count + 1) + ".json", "w") as file:
        json.dump(data, file, indent=2)

def algorithm_ucs(grap: dict, start_point: str, end_point: str) -> list:
    # visited cac dinh da duoc visited
    visited = ()
    # queue chi phi 0 va path la diem dau tien
    queue = [( 0,[start_point])]
    # lap den khi nao queue rong
    while queue:
        # lay ra chi phi va path
        # heappop lay ra phan tu queue co chi phi nho nhat
        (cost,path) = heapq.heappop(queue)
        # lay ra dinh cuoi cung cua path
        node = path[-1]
        # neu dinh chua duoc visited
        if node not in visited:
            # them dinh vao visited
            visited = visited + (node,)
            # neu dinh la dinh cuoi cung
            if node == end_point:
                return  path,cost
            # duyet qua cac dinh ke cua node
            for neighbor, weight in grap.get(node, ()):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_cost = cost + weight
                    heapq.heappush(queue, (new_cost,new_path))
    return  [],path



if __name__ == "__main__":
    pass

