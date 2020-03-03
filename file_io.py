from ast import literal_eval
import json


def read(target):
    with open(target, 'r') as file:
        result = file.read()
        
    return literal_eval(result)


def write(target, data):
    with open(target, 'w') as file:
        file.write(str(data))
