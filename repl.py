import requests
import sys
import json

from endpoints import *
from room import Room
from player import Player
from world import World
import file_io

main_map_file = "data/main_world.txt"
main_map = World(main_map_file)
main_map.print_rooms()

# player_data_file = "data/player.txt"
# player_data = file_io.read(player_data_file)
# player = Player(player_data.current_room)

if __name__ == '__main__':
    pass
