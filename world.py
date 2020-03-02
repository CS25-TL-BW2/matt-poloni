import random
import math
from pprint import pprint
from copy import deepcopy

from room import Room
import file_io

class World:
    def __init__(self, name, map_file, num_rooms=500):
        self.name = name
        self.num_rooms = num_rooms
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0

        dict_map = file_io.read(map_file)
        self.load_graph(dict_map)
    
    def __repr__(self):
        return str(self.rooms)
    
    def load_graph(self, room_graph):
        grid_size = 1
        for coords in room_graph:
            x = coords[0]
            y = coords[1]
            self.rooms[coords] = Room(x, y, room_graph[coords])
            grid_size = max(grid_size, x, y)
        
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for _ in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        
        for coords in room_graph:
            x = coords[0]
            y = coords[1]
            dict_room = self.rooms[coords]
            self.room_grid[x][y] = dict_room
            room = room_graph[coords]
            # print(room["exits"])
            for direction in room["exits"]:
                dir_exit = room["exits"][direction]
                if dir_exit in self.rooms:
                    dict_room.connect_rooms(direction, self.rooms[dir_exit])

    def add_room(self, room_desc):
        print(room_desc)
        # coords = room_desc["coordinates"]
        # self.rooms[coords] = 
        # rooms_copy = deepcopy(self.rooms)
        # self.load_graph(rooms_copy)
        # self.cache_graph(rooms_copy)

    def cache_graph(self):
        map_file = "data/main_world.txt"
        with open(map_file,'w') as f:
            pprint(self.rooms, stream=f)

    
    def print_rooms(self):
        rotated_room_grid = []
        for i in range(0, len(self.room_grid)):
            rotated_room_grid.append([None] * len(self.room_grid))
        for i in range(len(self.room_grid)):
            for j in range(len(self.room_grid[0])):
                rotated_room_grid[len(self.room_grid[0]) - j - 1][i] = self.room_grid[i][j]
        print("#####")
        str = ""
        for row in rotated_room_grid:
            all_null = True
            for room in row:
                if room is not None:
                    all_null = False
                    break
            if all_null:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.room_id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")