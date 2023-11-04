import json
import heapq
import astar
'''
    Call algorithms from other files
'''

def call_algorithm(data: json.load, start_point: dict, end_point: dict, algorithm: str) -> list:
    if algorithm == "UCS":
        return UCS(data, start_point, end_point)
    elif algorithm == "A*":
        return a_star(data, start_point, end_point)
    
'''
    Algorithms
'''
    
def UCS(data: json.load, start_point: dict, end_point: dict) -> list:
    return [],0

def a_star(data: json.load, start_point: dict, end_point: dict) -> list:
    grap_list = convert_dict_grap(data)

    return [],0

'''
    Data tranform utils
'''

def find_point_by_name(data: json.load, name: str) -> dict:
    for item in data:
        if item.get('name') == name:
            return item
    return None

def find_point_by_id(data: json.load, id: int) -> dict:
    for item in data:
        if item.get('id') == str(id):
            return item
    return None

def get_all_points(data: json.load) -> dict:
    result = dict()
    for item in data:
        result[item.get('id')] = item.get('name')
    return result

def get_relatives(data: json.load, id: int) -> list[int]:
    result = []
    for item in data:
        if item.get('id') == id:
            relative = item.get("relative", {})
            result.extend([int(key) for key in relative.keys()])
            return result
    return result

def convert_dict_grap(data: json.load) -> dict:
    grap = {}
    for point in data:
        point_id = point.get("id")
        relative_data = point.get("relative", {})
        if point_id is not None:
            grap[point_id] = [(key, value) for key, value in relative_data.items()]
    return grap