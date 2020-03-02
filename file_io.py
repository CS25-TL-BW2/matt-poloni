from ast import literal_eval
import json


def read(target):
    with open(target, 'r') as file:
        result = file.read()
        
    return literal_eval(result)


def write(target, data):
    with open(target, 'w') as file:
        file.write(str(data))

# with open('kos.txt','w') as f:
#    f.write(str({1,3,(3,5)}))  # set of numbers & a tuple
# then read it back again using ast.literal_eval

# import ast
# with open('kos.txt','r') as f:
#    my_set = ast.literal_eval(f.read())
