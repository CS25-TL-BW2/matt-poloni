# import requests
import sys
import json

from endpoints import adv_move
from room import Room
from player import Player
from world import World
import file_io

player = Player()
player.cache_player()

# Current actions
# world = player.current_world
# coords = player.current_room.get_coords()

# target = player.shop_room
# target = player.pirate_room
# target = player.mining_room
# target = player.well_room

# path = world.bfs_to_targets(coords, {target})
# player.travel_route(path)
# print("DONE")

# world.print_rooms()
# player.treasure_hunt()
# path = world.bfs_to_targets({})

# BLOCKCHAIN
# while True:
#     pass