import random
import math
from pprint import pprint
from copy import deepcopy
from ast import literal_eval
from collections import deque

from room import Room
import file_io

class World:
    def __init__(self, name, map_file, num_rooms=500):
        self.name = name
        self.num_rooms = num_rooms
        self.rooms = {}
        self.unvisited = set()
        self.room_grid = []
        self.grid_size = 0

        self.map_file = map_file
        self.load_graph()
    
    def __repr__(self):
        return str([self.unvisited, self.rooms])

    def cache_graph(self):
        with open(self.map_file,'w') as f:
            pprint([self.unvisited, self.rooms], stream=f)
    
    def load_graph(self):
        unvisited, room_graph = file_io.read(self.map_file)
        self.unvisited = unvisited
        grid_size = 1
        for coords in room_graph:
            x = coords[0]
            y = coords[1]
            print(room_graph[coords])
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
            for direction in room["dirs"]:
                dir_coords = dict_room.exit_coords(direction)
                if dir_coords in self.rooms:
                    dict_room.connect_rooms(direction, self.rooms[dir_coords])

    def add_room(self, room_desc):
        # print(room_desc)
        coords = room_desc["coordinates"]
        self.unvisited.discard(coords)
        self.rooms[coords] = room_desc

        self.cache_graph()
        self.load_graph()

        room = self.rooms[coords]
        for direction in room.dirs:
            dir_coords = room.exit_coords(direction)
            if dir_coords not in self.rooms:
                self.unvisited.add(dir_coords)
        self.cache_graph()
    
    def room_by_coords(self, coords):
        return self.rooms[coords]

    def bfs_to_targets(self, coords, targets=None):
        if targets is None:
            targets = self.unvisited
        queue = deque()
        queue.append((coords, []))
        visited = set()
        while len(queue) > 0:
            room_coords, path = queue.popleft()
            if room_coords in self.rooms and room_coords not in visited:
                room = self.rooms[room_coords]
                visited.add(room_coords)
                dirs = ['n', 's', 'e', 'w']
                for direction in dirs:
                    new_path = list(path)
                    new_path.append(direction)
                    next_coords = room.exit_coords(direction)
                    if next_coords in targets:
                        return new_path
                    else:
                        queue.append((next_coords, new_path))
        print(f"A path could not be found from {coords} to an unvisited room.")
        return None
    
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