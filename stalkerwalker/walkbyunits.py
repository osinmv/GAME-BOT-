
import time
import threading
# import json
import pymem
import keys
# import keyboard
# import mouse
from pymem import Pymem
# from math import acos, pi, sin, sqrt, isclose
import utils
KOEF = 1
INDEX = 0
USING_WEAPON = False
#                   x, y, cos, sin
CURRENT_POSITION = (1, 1, 0.5, 0.5,)
CURRENT_POINT = (1, 1,)


def perform_additional_actions(game_data: dict, key):
    global USING_WEAPON
    global INDEX
    if(not USING_WEAPON and utils.is_wpn_allowed(game_data)):
        utils.press_key("6", key)
        USING_WEAPON = True


def position_tracker(points):
    global INDEX
    global CURRENT_POSITION
    global CURRENT_POINT
    INDEX = 0
    pm = Pymem("XR_3DA.exe")
    module_offset = utils.get_module_offset("xrGame.dll", pm)
    CURRENT_POSITION = utils.data_from_game(pm, module_offset)
    while INDEX < len(points):
        CURRENT_POINT = tuple(points[INDEX])
        CURRENT_POSITION = utils.data_from_game(pm, module_offset)
        if(utils.on_point(game_data=CURRENT_POSITION, point=CURRENT_POINT)):
            INDEX += 1


def perform_actions():
    key = keys.Keys()
    key.directKey("w")
    utils.press_key("x", key)
    while INDEX < len(points):
        utils.run_bot(CURRENT_POSITION, CURRENT_POINT, key)
        perform_additional_actions(game_data=CURRENT_POSITION, key=key)
        time.sleep(0.016)
    key.directKey("w", key.key_release)


if __name__ == "__main__":
    # casting to tuple to avoid any modification
    points = tuple(utils.load_file("dataclean"))
    CURRENT_POINT = tuple(points[0])
    utils.five_second_delay()
    position_thread = threading.Thread(target=position_tracker, args=(points,))
    position_thread.start()
    actions_thread = threading.Thread(target=perform_actions)
    actions_thread.start()
