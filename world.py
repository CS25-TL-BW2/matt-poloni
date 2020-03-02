import random
import math
from copy import deepcopy

from room import Room
import file_io

class World:
    def __init__(self):
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
    
    def __repr__(self):
        return self.rooms
    
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
            print(room["exits"])
            for direction in room["exits"]:
                dict_room.connect_rooms(direction, self.rooms[room["exits"][direction]])

    def add_room(self, room):
        pass
        # Logic specific to adding a room
        # self.load_graph(deepcopy(self.rooms))

    def cache_graph(self):
        map_file = "data/main_world.txt"
        file_io.write(map_file, self.rooms)

    
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
                    str += f"{room.id}".zfill(3)
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