import json
import random
import os
# import matplotlib as plT
# import ttkbootstrap as ttkbs

'''
    GUI utils
'''


def get_all_points(data: json.load) -> dict:
    result = dict()
    for item in data:
        result[item.get('POINT_ID')] = item.get('POINT_NAME')
    return result


def get_relatives(data: json.load, id: int) -> list[int]:    
    result = []   
    for item in data:       
        if item.get('id') == id:        
            print(item.get('id'))       
            relative = item.get("relative", {})         
            result.extend([int(key) for key in relative.keys()])    
            return result
    return result


def update_weight(data: list, id1: int, id2: int, new_weight: int) -> None:  
    for item in data:   
        if item.get('POINT_ID') == str(id1):    
            relative = item.get("RELATIVE", {})   
            if str(id2) in relative:         
                relative[str(id2)] = new_weight     
        if item.get('POINT_ID') == str(id2):        
            relative = item.get("RELATIVE", {})      
            if str(id1) in relative:        
                relative[str(id1)] = new_weight   
    with open('data.json', 'w') as f:      
        json.dump(data, f, indent=4)

def open_new_map(link: str) -> json.load:
    return json.load(link)
#
# def after_cbbox_selected(cbbox: ttkbs.Combobox, cbbox2: ttkbs.Combobox, start_point) -> None:
#     start_point = cbbox.get()
#     cbbox2.configure(values=[x for x in cbbox["values"] if x != start_point])
#
# def change_end_point(cbbox: ttkbs.Combobox, end_point) -> None:
#     end_point = cbbox.get()
#
# def click_find_way(data : json.load, combobox):
#     name = combobox.get()
#     id = find_point_by_name(data, name)["id"]
#     realtives = get_relatives(data, id)
#     print(realtives)

'''
    Data utils
'''
def generate_data(total : int, limit : int) -> list[dict]:
    # khoi tao mang chua cac diem
    points : list[dict] = [{} for i in range(total)]
    # cai dat cac thong so co ban cho cac diem
    for point in points:
        point["id"] : str = str(points.index(point) + 1001)
        point["name"] : str = "point " + str(point["id"])
        point["point_limit"] : int = random.randint(1, limit)
        point["count"] : int = 0
        point["relative"] : dict = dict()
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


def convert_dict_grap(data: json.load) ->dict:
    grap = {}
    for point in data:
        point_id = point.get("id")
        relative_data =point.get("relative",{})
        if point_id is not None :
            grap[point_id]= [(key,value) for key,value in relative_data.items()]
    return grap




def find_point_by_id(data: json.load, id: int) -> dict:  
    for point in data :   
        if point[ "id"]== str(id) :      
            return point

def find_point_by_name(data: json.load, name: str) -> dict:  
    for point in data :   
        if point[ "name"]== name :      
            return point

if __name__ == "__main__":
    # data = generate_data(6, 3)
    # make_new_json(data)
    # #
    with open('data/16.json','r') as f:
        data= json.load(f)
    print( convert_dict_grap(data))