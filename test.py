import matplotlib as plT
import networkx as nx
import matplotlib.pyplot as plt
import json
import ttkbootstrap as ttkbs

def make_graph_frame(data : json.load) -> ttkbs.Frame:
    frame = ttkbs.Frame()
    graph = nx.Graph()
    for item in data:
        graph.add_node(item.get('POINT_ID'))
        for key in item.get('RELATIVE').keys():
            graph.add_edge(item.get('POINT_ID'), key)
    nx.draw(graph)
    
    return frame

def make_graph(data : json.load) -> None:
    graph = nx.Graph()
    for item in data:
        graph.add_node(item.get('POINT_ID'))
        for key in item.get('RELATIVE').keys():
            graph.add_edge(item.get('POINT_ID'), key)
    nx.draw(graph)
    plt.show()
    return None

def make_graph_with_weight(data : json.load) -> None:
    graph = nx.Graph()
    for item in data:
        graph.add_node(item.get('POINT_ID'))
        for key in item.get('RELATIVE').keys():
            graph.add_edge(item.get('POINT_ID'), key, weight=item.get('RELATIVE').get(key))
    nx.draw(graph)
    plt.show()
    return None

def make_graph_with_weight_and_name(data : json.load) -> None:
    graph = nx.Graph()
    for item in data:
        graph.add_node(item.get('id'), name=item.get('name'))
        for key in item.get('relative').keys():
            graph.add_edge(item.get('id'), key, weight=item.get('relative').get(key))
    nx.draw(graph, with_labels=True, node_color='darkgrey', font_weight='bold')
    plt.show()
    return None

if __name__ == "__main__":
    with open('data/4.json', 'r') as f:
        data = json.load(f)
    make_graph_with_weight_and_name(data)