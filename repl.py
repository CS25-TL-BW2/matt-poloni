import requests
import sys
import json

from endpoints import *
from room import Room
from player import Player
from world import World
import file_io

world = World()
main_map_file = "data/main_world.txt"
main_map = file_io.read(main_map_file)
world.load_graph(main_map)
# print(world)
# world.cache_graph()
world.print_rooms()

# player_data_file = "data/player.txt"
# player_data = file_io.read(player_data_file)
# player = Player(player_data.current_room)

if __name__ == '__main__':
    pass
