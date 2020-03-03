from time import time
from datetime import datetime
from pprint import pprint
from ast import literal_eval
import random

from world import World
from endpoints import *
import file_io

class Player:
    def __init__(self):
        # Player Cache
        player_file = "data/player.txt"
        player = file_io.read(player_file)
        prop_check = lambda n, v=None, c=player: v if n not in c else c[n]

        self.shop_room = prop_check("shop_room")
        self.mining_room = prop_check("mining_room")
        self.pirate_room = prop_check("pirate_room")
        self.well_room = prop_check("well_room")
        self.cooldown_end = prop_check("cooldown_end")
        self.ideal_name = "matt-poloni"
        
        # Map Caches
        main_world_file = "data/main_world.txt"
        self.main_world = World("main", main_world_file)
        dark_world_file = "data/dark_world.txt"
        self.dark_world = World("dark", dark_world_file)
        self.current_world = self.dark_world if prop_check("current_world") == "dark" else self.main_world

        # Status Endpoint
        status = self.cooldown(adv_status)
        self.cooldown_end = status["cooldown_end"]
        self.name = prop_check("name", c=status)
        self.encumbrance = prop_check("encumbrance", c= status)
        self.strength = prop_check("strength", c=status)
        self.speed = prop_check("speed", c=status)
        self.gold = prop_check("gold", c=status)
        self.bodywear = prop_check("bodywear", c=status)
        self.footwear = prop_check("footwear", c=status)
        self.inventory = prop_check("inventory", c=status)
        self.abilities = prop_check("abilities", c=status)
        self.status = prop_check("status", c=status)
        self.has_mined = prop_check("has_mined", c=status)
        
        # Init Endpoint
        init = self.cooldown(adv_init)
        self.cooldown_end = time() + init["cooldown"]
        current_coords = prop_check("coordinates", c=init)
        self.current_room = self.current_world.rooms[current_coords]
        self.errors = prop_check("errors", c=init)
        self.messages = prop_check("messages", c=init)
    
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
          "errors": self.errors,
          "messages": self.messages,
          "current_world": self.current_world.name,
          "current_room": self.current_room.get_coords(),
          "shop_room": self.shop_room,
          "mining_room": self.mining_room,
          "pirate_room": self.pirate_room,
          "well_room": self.well_room
        }
        return str(result)
    
    def cache_player(self):
        player_file = "data/player.txt"
        data = literal_eval(str(self))
        with open(player_file,'w') as f:
            pprint(data, stream=f)
        
        pprint(data)
        world = self.current_world
        print(f"TRAVERSAL: {len(world.rooms)}/{world.num_rooms}")
        print(f"COORDS: {self.current_room.get_coords()}")
        print(f"ERRORS ({len(self.errors)})")
        for error in self.errors:
            print("- ", error)
        print(f"MESSAGES ({len(self.messages)})")
        for message in self.messages:
            print("- ", message)
        print("--------------------")

    def cooldown(self, fn=None):
        seconds_left = lambda: self.cooldown_end - time()
        if seconds_left() > 0:
            print(f"{datetime.now()} -> Waiting for cooldown period to end in {int(seconds_left())} seconds.")
        while seconds_left() > 0:
            pass
        
        if fn is not None:
            response = fn()
            self.cooldown_end = response["cooldown_end"]
            return response

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
                self.current_world.unvisited.add(new_coords)
                room["exits"][direction] = new_coords
        
        self.current_world.unvisited.discard(self.current_room)
        world.add_room(room)
        current_room = self.current_world.rooms[(x, y)]
        self.current_room = current_room
    
    def travel(self, direction):
        next_coords = self.current_room.exit_coords(direction)
        world = self.current_world
        next_id = None if next_coords not in world.rooms else world.rooms[next_coords].room_id

        room_response = self.cooldown(lambda: adv_move(direction, str(next_id)))
        print('TRAVEL', room_response)
        self.cache_player()
        coords = room_response["coordinates"]
        self.errors = room_response["errors"]
        self.messages = room_response["messages"]
        self.visit_room(room_response)

        if room_response is not None and next_coords == coords:
            next_room = self.current_world.rooms[coords]
            self.current_room = next_room
            self.cache_player()
            return True
        else:
            self.cache_player()
            print(f"You cannot move {direction} from {coords}.")
            return False
        

    def travel_route(self, route):
        for direction in route:
            if not self.travel(direction):
                print(f"Something's wrong with this route: {route}")
                break

    def traverse(self, visit_known=False):
        traversal_path = []
        world = self.current_world
        unvisited = set() if visit_known else self.current_world.unvisited
        visited = {} if visit_known else world.rooms
        while len(visited) < world.num_rooms:
            dirs = self.current_room.dirs
            for direction in dirs:
                dir_coords = self.current_room.exit_coords(direction)
                if dir_coords in unvisited:
                    self.travel(direction)
                    traversal_path.append(direction)
                    break
            else:
                world = self.current_world
                coords = self.current_room.get_coords()
                new_route = world.bfs_to_targets(coords)
                self.travel_route(new_route)
                traversal_path.extend(new_route)
        
        print(f"{datetime.now()} -> All {self.current_world.num_rooms} have been visited.")
        return traversal_path
    
    def take(self, item_name):
        if self.encumbrance < (self.strength * 0.8):
            self.cooldown(lambda: adv_take(item_name))
            
            status_response = self.cooldown(adv_status)
            print(status_response)
            self.inventory = status_response["inventory"]
            self.errors = status_response["errors"]
            self.messages = status_response["messages"]
            self.cache_player()

            init_response = self.cooldown(adv_init)
            responses = {**status_response, **init_response}
            self.current_world.add_room(responses)
            return responses["items"]
        return None

    def treasure_hunt(self):
        while self.encumbrance < (self.strength * 0.8):
            items = self.current_room.items
            while(len(items) > 0):
                for item in items:
                    if "treasure" in item.lower():
                        items = self.take(item)
                        break

            dirs = self.current_room.dirs
            rand_dir = random.choice(dirs)
            self.travel(rand_dir)
        # 
        # If name != ideal name, go get it changed
