from world import World
from time import time
from collections import deque
from endpoints import *

class Player:
    def __init__(self, current_room, cache=None, main_world=None, dark_world=None):
        self.name = name
        self.cooldown_end = cooldown_end
        self.encumbrance = encumberance
        self.strength = strength
        self.speed = speed
        self.gold = gold
        self.bodywear = bodywear
        self.footwear = footwear
        self.inventory = inventory
        self.abilities = abilities
        self.status = status
        self.has_mined = has_mined
        self.last_errors = last_errors
        self.last_messages = last_messages
        
        self.current_room = current_room
        self.shop_room = shop_room
        self.mining_room = mining_room
        self.is_renamed = is_renamed
        # -------




        self.current_room = current_room
        self.num_rooms = 500
        self.unvisited_coords = set()
        self.visited_rooms = {}
        self.add_room_to_visited(current_room)

        self.cooldown_end = time()
    
    def __repr__(self):
        return {
            "name": self.name,
            "cooldown_end": self.cooldown_end,
            "last_errors": self.last_errors,
            "last_messages": self.last_messages,
            "encumberance": self.encumbrance,
            "strength": self.strength,
        }
    def cooldown(self):
        seconds_left = lambda: self.cooldown_end - time()
        if seconds_left() < 0:
            print(f"Waiting for cooldown period to end in {int(seconds_left)} seconds.")
        while seconds_left() < 0:
            pass
        return
    
    def cache_player(self):
        player_file = "data/player.txt"
        # file_io.write(player_file, self.rooms)
    def add_room_to_visited(self, room):
        room_coords = room.get_coords()
        self.visited_rooms[room_coords] = {
          "id": room.id
        }
        dirs = ['n', 's', 'e', 'w']
        for direction in dirs:
            dir_room = getattr(room, f"{direction}_to")
            dir_coords = None if dir_room is None else dir_room.get_coords()
            self.visited_rooms[room_coords][direction] = dir_coords
            if dir_room is not None and dir_coords not in self.visited_rooms:
                self.unvisited_coords.add(dir_coords)
        self.unvisited_coords.discard(room_coords)
        # print("UNVISITED", self.unvisited_coords)
        # print("VISITED", self.visited_rooms.keys())
    
    def travel(self, direction):
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
            if self.current_room.get_coords() not in self.visited_rooms:
                self.add_room_to_visited(self.current_room)
        else:
            print(f"You cannot move {direction} from room {self.current_room.id}.")

    def travel_route(self, route):
        for direction in route:
            self.travel(direction)

    def traverse(self):
        traversal_path = []
        while len(self.visited_rooms) < self.num_rooms:
            x, y = self.current_room.get_coords()
            exits = self.current_room.get_exits()

            # Grab exits
            # Grab four nearest unvisited
            # Compare each exit's shortest distance to unvisited
            
            def min_dist(direction):
                vx, vy = getattr(self.current_room, f"{direction}_to").get_coords()
                return abs(x-vx) + abs(y-vy)
            
            exits = sorted(exits, key=min_dist)
            # print(exits)
            unvisited_neighbor = False
            for direction in exits:
                dir_coords = getattr(self.current_room, f"{direction}_to").get_coords()
                if dir_coords in self.unvisited_coords:
                    self.travel(direction)
                    traversal_path.append(direction)
                    unvisited_neighbor = True
                    break
            
            if unvisited_neighbor: continue
            
            new_route = self.bfs_to_targets()
            self.travel_route(new_route)
            traversal_path.extend(new_route)
        
        return traversal_path
                    

    
    def bfs_to_targets(self, targets=None):
        if targets is None:
            targets = self.unvisited_coords
        queue = deque()
        current_coords = self.current_room.get_coords()
        queue.append((current_coords, []))
        visited = set()
        while len(queue) > 0:
            room_coords, path = queue.popleft()
            if room_coords in self.visited_rooms and room_coords not in visited:
                room = self.visited_rooms[room_coords]
                visited.add(room_coords)
                dirs = ['n', 's', 'e', 'w']
                for direction in dirs:
                    new_path = list(path)
                    new_path.append(direction)
                    next_coords = room[direction]
                    if next_coords in targets:
                        return new_path
                    else:
                        queue.append((next_coords, new_path))
        print(f"A path could not be found from Room {self.current_room.id} to an unvisited room.")
        return None
    
    def bfs_to_coords(self, target_coords):
        current_coords = self.current_room.get_coords()
        if target_coords == current_coords:
            print("You are already at those coordinates.")
            return
        
        queue = deque()
        queue.append((current_coords, []))
        visited = set()
        while len(queue) > 0:
            room_coords, path = queue.popleft()
            if room_coords in self.visited_rooms and room_coords not in visited:
                room = self.visited_rooms[room_coords]
                visited.add(room_coords)
                dirs = ['n', 's', 'e', 'w']
                for direction in dirs:
                    new_path = list(path)
                    new_path.append(direction)
                    next_coords = room[direction]
                    if next_coords == target_coords:
                        return new_path
                    else:
                        queue.append((next_coords, new_path))
        print(f"A path could not be found from Room {self.current_room.id} to the coordinates {target_coords}.")
        return None
