from ast import literal_eval
from pprint import pprint
import json


def read(target_file):
    with open(target_file, 'r') as file:
        result = file.read()
        
    return literal_eval(result)


def write(target_file, data):
    with open(target_file, 'w') as file:
        file.write(str(data))

def parse_named():
    read_file = "data/main_world.txt"
    write_file = "data/named_rooms.txt"
    
    with open(read_file, 'r') as file:
        result = file.read()
    result = literal_eval(result)
    graph = result[1]

    pprint(graph.keys())

    named = []
    generics = [
      'A misty room',
      'A Dark Cave'
    ]
    for coords in graph:
        desc = graph[coords]
        if desc["title"] not in generics:
            pprint(desc)
            named.append(desc)

    with open(write_file, 'w') as file:
        file.write(str(named))
