import time
import json
import pymem
import keys
import keyboard
import mouse
from pymem import Pymem
from math import acos, pi, sin, sqrt, isclose
import utils
KOEF = 1
INDEX = 0


if __name__ == "__main__":
    pm = Pymem("XR_3DA.exe")
    keys = keys.Keys()
    module_offset = get_module_offset("xrGame.dll")
    points = load_file("dataclean")
    five_second_delay()
    keys.directKey("w")
    press_key("x")
    for i in range(0, 90000):
        game_data = data_from_game(pm)
        run_bot(game_data, points)
    keys.directKey("w", keys.key_release)
