from ast import literal_eval
import json


def file_write(target, data):
    with open(target, 'w') as file:
        file.write(json.dumps(data))


def file_read(target):
    with open(target, 'r') as file:
        result = file.read()
        
    return literal_eval(result)