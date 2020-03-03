from time import time
from pprint import pprint
from collections import deque
from ast import literal_eval

from world import World
from endpoints import *
import file_io

class Player:
    def __init__(self, cache="data/player.txt"):
        prop_check = lambda n, v=None, c=cache: v if n not in c else c[n]

        main_world_file = "data/main_world.txt"
        self.main_world = World("main", main_world_file)
        self.unvisited_main = prop_check("unvisited_main")

        dark_world_file = "data/dark_world.txt"
        self.dark_world = World("dark", dark_world_file)
        self.unvisited_dark = prop_check("unvisited_dark")

        self.name = prop_check("name")
        self.cooldown_end = prop_check("cooldown_end")
        self.encumbrance = prop_check("encumbrance")
        self.strength = prop_check("strength")
        self.speed = prop_check("speed")
        self.gold = prop_check("gold")
        self.bodywear = prop_check("bodywear")
        self.footwear = prop_check("footwear")
        self.inventory = prop_check("inventory")
        self.abilities = prop_check("abilities")
        self.status = prop_check("status")
        self.has_mined = prop_check("has_mined")
        self.last_errors = prop_check("last_errors")
        self.last_messages = prop_check("last_messages")

        self.current_world = self.dark_world if prop_check("current_world") == "dark" else self.main_world
        current_coords = prop_check("current_room")
        self.current_room = self.current_world.rooms[current_coords]
        self.current_unvisited = self.unvisited_dark if prop_check("current_world") == "dark" else self.unvisited_main
        self.shop_room = prop_check("shop_room")
        self.mining_room = prop_check("mining_room")
        self.is_renamed = prop_check("is_renamed")
        # -------
        # self.current_room = current_room
        # self.num_rooms = 500
        # self.current_world = {}
        # self.visit_room(current_room)

        # self.cooldown_end = time()
    
    def __repr__(self):
        result = {
          "name": self.name,
          "cooldown_end": self.cooldown_end,
          "encumbrance": self.encumbrance,
          "strength": self.strength,
          "speed": self.speed,
          "gold": self.gold,
          "bodywear": self.bodywear,
          "footwear": self.footwear,
          "inventory": self.inventory,
          "abilities": self.abilities,
          "status": self.status,
          "has_mined": self.has_mined,
          "last_errors": self.last_errors,
          "last_messages": self.last_messages,
          "current_world": self.current_world.name,
          "current_room": self.current_room.get_coords(),
          "shop_room": self.shop_room,
          "mining_room": self.mining_room,
          "is_renamed": self.is_renamed,
          "unvisited_main": self.unvisited_main,
          "unvisited_dark": self.unvisited_dark
        }
        return str(result)

    def cooldown(self):
        print(self.cooldown_end, time())
        seconds_left = lambda: self.cooldown_end - time()
        if seconds_left() > 0:
            print(f"Waiting for cooldown period to end in {int(seconds_left())} seconds.")
        while seconds_left() > 0:
            pass
        return
    
    def cache_player(self):
        player_file = "data/player.txt"
        # print(str(self))
        data = literal_eval(str(self))
        with open(player_file,'w') as f:
            pprint(data, stream=f)

    def visit_room(self, room):
        world = self.current_world

        dirs_math = {
          'n': (0, 1),
          's': (0, -1),
          'e': (1, 0),
          'w': (-1, 0)
        }
        x, y = self.current_room.get_coords()
        dir_coords = lambda d: (x + dirs_math[d][0], y + dirs_math[d][1])

        exits = list(room["exits"])
        room["exits"] = {}

        for direction in exits:
            new_coords = dir_coords(direction)
            if new_coords not in self.current_world.rooms:
                self.current_unvisited.add(new_coords)
                room["exits"][direction] = new_coords
        
        self.current_unvisited.discard(self.current_room)
        world.add_room(room)
        current_room = self.current_world.rooms[(x, y)]
        self.current_room = current_room
    
    def travel(self, direction):
        self.cooldown()
        room_response = adv_move(direction)
        self.cooldown_end = time() + room_response["cooldown"]
        self.cache_player()
        coords = room_response["coordinates"]

        if room_response is not None:
            self.visit_room(room_response)
            next_room = self.current_world.rooms[coords]
            self.current_room = next_room
            self.cache_player()
        else:
            print(f"You cannot move {direction} from room {self.current_room.room_id}.")

    def travel_route(self, route):
        for direction in route:
            self.travel(direction)

    def traverse(self):
        traversal_path = []
        world = self.current_world
        while len(world.rooms) < world.num_rooms:
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
                if dir_coords in self.current_unvisited:
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
            targets = self.current_unvisited
        queue = deque()
        current_coords = self.current_room.get_coords()
        queue.append((current_coords, []))
        visited = set()
        while len(queue) > 0:
            room_coords, path = queue.popleft()
            if room_coords in self.current_world and room_coords not in visited:
                room = self.current_world[room_coords]
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
        print(f"A path could not be found from Room {self.current_room.room_id} to an unvisited room.")
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
            if room_coords in self.current_world.rooms and room_coords not in visited:
                room = self.current_world[room_coords]
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
        print(f"A path could not be found from Room {self.current_room.room_id} to the coordinates {target_coords}.")
        return None
