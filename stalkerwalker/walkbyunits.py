
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
USING_WEAPON = False


def perform_additional_actions(game_data: dict, key):
    global USING_WEAPON
    global INDEX
    if(not USING_WEAPON and utils.is_wpn_allowed(game_data)):
        utils.press_key("6", key)
        USING_WEAPON = True


if __name__ == "__main__":
    pm = Pymem("XR_3DA.exe")
    key = keys.Keys()
    module_offset = utils.get_module_offset("xrGame.dll", pm)
    points = utils.load_file("dataclean")
    utils.five_second_delay()
    # key.directKey("w")
    #utils.press_key("x", key)
    for i in range(0, 1000):
        game_data = utils.data_from_game(pm, module_offset)
        perform_additional_actions(game_data=game_data, key=key)
        print(utils.calculate_angle_my(points[0], [
              game_data["x"], game_data["z"]], [game_data["cos"], game_data["sin"]]))
        utils.run_bot(game_data, points, INDEX, key)
        # if(utils.on_point(game_data=game_data, points=points, index=INDEX)):
        #    INDEX += 1
        time.sleep(1)
    #key.directKey("w", key.key_release)
