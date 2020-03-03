# import requests
import sys
import json

from endpoints import adv_move
from room import Room
from player import Player
from world import World
import file_io

player_data_file = "data/player.txt"
player_data = file_io.read(player_data_file)
player = Player(player_data)
player.cache_player()
player.traverse()

if __name__ == '__main__':
    print(f"ERRORS ({len(player.errors)})")
    for error in player.errors:
        print(error)
    print(f"MESSAGES ({len(player.messages)})")
    for message in player.messages:
        print(message)
