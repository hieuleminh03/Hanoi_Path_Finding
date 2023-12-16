import json
import heapq
import astar
import ucs
'''
    Call algorithms from other files
'''

def call_algorithm(data: json.load, start_point: dict, end_point: dict, algorithm: str) -> list:
    graph = convert_dict_grap(data)
    if algorithm == "UCS":
        return UCS(graph, start_point, end_point)
    elif algorithm == "A*":
        return a_star(graph, start_point, end_point)
    
'''
    Algorithms
'''
    
def UCS(graph: dict, start_point: dict, end_point: dict) -> list:
    answer = ucs.ucs(graph, start_point, end_point)
    return answer

def a_star(graph: dict, start_point: dict, end_point: dict) -> list:
    answer = astar.a_star(graph, start_point, end_point)
    return answer

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
            result.extend([key for key in relative.keys()])
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

def convert_dict_grap_with_name(data: list) -> dict:
    grap = {}
    # get name, id , relative to other name
    for point in data:
        point_id = point.get("id")
        point_name = point.get("name")
        relative_data = point.get("relative", {})
        if point_id is not None:
            grap[point_name] = [(item.get("name"), value) for item in data for key, value in relative_data.items() if item.get("id") == key]
    return grap