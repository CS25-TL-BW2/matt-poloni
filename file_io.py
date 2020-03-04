from ast import literal_eval
from pprint import pprint
import json


def read(target_file):
    with open(target_file, 'r') as file:
        result = file.read()
        
    return literal_eval(result)


def write(target_file, data):
    with open(target_file, 'w') as file:
        pprint(data, stream=file)

def parse_named():
    read_file = "data/main_world.txt"
    write_file = "data/named_rooms.txt"

    result = read(read_file)
    graph = result[1]

    named = []
    generics = [
      'A misty room',
      'A Dark Cave'
    ]
    for coords in graph:
        desc = graph[coords]
        if desc["title"] not in generics:
            named.append(desc)

    write(write_file, named)
