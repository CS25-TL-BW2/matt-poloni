# import requests
import sys
import json

from endpoints import adv_move
from room import Room
from player import Player
from world import World
import file_io

# main_map_file = "data/main_world.txt"
# main_map = World("main", main_map_file)
# main_map.print_rooms()

player_data_file = "data/player.txt"
player_data = file_io.read(player_data_file)
player = Player(player_data)
player.cache_player()
# data4 = {
#   "room_id": 2,
#   "title": "A misty room",
#   "description": "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.",
#   "coordinates": "(60,59)",
#   "elevation": 0,
#   "terrain": "NORMAL",
#   "exits": {
#     "n": (60, 60),
#     "s": (60, 58),
#     "e": (61, 59)
#   }
# }
# player.visit_room(data4)
# player.current_world.print_rooms()
player.travel('n')

if __name__ == '__main__':
    pass
    # print(f"ERRORS ({len(player.last_errors())})")
    # for error in player.last_errors:
    #     print(error)
    # print(f"MESSAGES ({len(player.last_messages())})")
    # for message in player.last_messages:
    #     print(message)
