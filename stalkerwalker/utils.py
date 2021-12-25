import time
import json
import pymem
import keys
import keyboard
import mouse
from pymem import Pymem
from math import acos, pi, sin, sqrt, isclose, cos
KOEF = 0.1

# ТЫКАЕТ НАЧАТЬ НОВУЮ ИГРУ

"""
def start_new_game():
    # keys = keys.Keys()
    # ставим мышку в 0
    keys.directMouse(-5000, -5000)
    time.sleep(0.016)
    # начинаем новую игру
    keys.directMouse(800, 440)
    time.sleep(0.016)
    mouse.click(button='left')
    time.sleep(0.016)
    mouse.release(button='left')
    time.sleep(0.5)  # тут пауза побольше, игра почему-то тупит
    mouse.click(button='left')
    time.sleep(0.016)
    mouse.release(button='left')
    time.sleep(0.016)

# ЖДЕТ ПОКА КОНЧИТСЯ ЗАГРУЗКА


def load_waiter():
    pm = Pymem("XR_3DA.exe")
    keys = keys.Keys()
    module_offset = None
    for i in list(pm.list_modules()):
        if(i.name == "xrGame.dll"):
            module_offset_xrgame = i.lpBaseOfDll
    for i in list(pm.list_modules()):
        if(i.name == "xrNetServer.dll"):
            module_offset_xrnetserver = i.lpBaseOfDll
    # само ожидание
    for i in range(0, 10000):
        loading = pm.read_bool(module_offset_xrnetserver+0xFAC4)
        sync = pm.read_float(pm.base_address+0x104928)
        plahka = pm.read_bool(module_offset_xrgame+0x54C2F9)
        if(not loading or (sync > 0.09 and sync < 0.11) or plahka):
            time.sleep(0.016)
        else:
            break


# двойной сейвлод + ожидание конца загрузки
def double_saveload():
    # сейвлоды и ожидание
    keys.directKey("F6")
    time.sleep(0.016)
    keys.directKey("F6", keys.key_release)
    time.sleep(0.016)
    keys.directKey("F7")
    time.sleep(0.016)
    keys.directKey("F7", keys.key_release)
    time.sleep(0.016)
    load_waiter()
"""


def angle_from_cos_sin(vector: list):
    """Return angle from cos and sin"""
    angle = acos(vector[0])
    if(vector[1] < 0):
        angle = -angle
    return angle/pi*180


def normalize_vector(vector: list):
    """Normalize vector"""
    length = sqrt(vector[0]*vector[0]+vector[1]*vector[1])
    return [vector[0]/length, vector[1]/length]


def turn_vector(vector: list, angle: float):
    """Return turned vector"""
    angle = angle/180*pi
    return [vector[0]*cos(angle)-vector[1]*sin(angle),
            vector[0]*sin(angle)+vector[1]*cos(angle)]


def calculate_rotation(target: list, current: list, view: list):
    """Return turning angle in grad"""
    # getting vectors
    vector = [current[0]-target[0], target[1]-current[1]]
    direction = angle_from_cos_sin(normalize_vector(vector))
    view_angle = angle_from_cos_sin(normalize_vector(view))
    # calculating turning angle
    # print("View: "+str(view_angle)+" Direction: "+str(direction))
    angle = direction - view_angle
    if abs(angle) > 100:
        return get_sign_of_float(angle)*200
    elif abs(angle) > 10:
        return get_sign_of_float(angle)*150
    elif abs(angle) > 7:
        return get_sign_of_float(angle)*50
    elif abs(angle) > 1:
        return get_sign_of_float(angle)*5
    else:
        return 0


def get_sign_of_float(number: float):
    """Return sign of float"""
    if(number > 0):
        return 1
    else:
        return -1


def data_from_game(pm: Pymem, module_offset: int):
    """Return x,z,confirmation, sin and cos values read from game memory"""
    plahka = pm.read_bool(module_offset+0x54C2F9)
    x = pm.read_float(pm.base_address+0x10493C)
    z = pm.read_float(pm.base_address+0x104944)
    view_sin = pm.read_float(pm.base_address+0x104950)
    view_cos = pm.read_float(pm.base_address+0x104968)
    return (x, z, view_cos, view_sin, plahka)


def load_file(name: str):
    """Return list of data from file"""
    points = None
    with open("dataclean", mode="r") as file:
        points = json.load(file)
    return points


def get_module_offset(module: str, pm: Pymem):
    """Return module offset
    """
    module_offset = None
    for i in list(pm.list_modules()):
        if(i.name == module):
            module_offset = i.lpBaseOfDll
    return module_offset


def five_second_delay():
    """Waits 5 seconds"""
    for i in range(5):
        print(i)
        time.sleep(1)


def press_key(key: str, keys):
    """Presses a key"""
    keys.directKey(key)
    keys.directKey(key, keys.key_release)


def press_mouse_key(key: str):
    """Presses key on mouse"""
    mouse.click(button=key)
    mouse.release(button=key)


def turn_camera(pixels: int, keys: keys.Keys):
    """Turns camera"""
    keys.directMouse(pixels, 0)


def is_wpn_allowed(game_data: tuple):
    """Return True if player is outside of no weapon area
        Used only on Cordon"""
    return game_data[0] > -245.0 and game_data[1] > -125.0


def on_point(game_data: tuple, point: tuple):
    if(sqrt((point[0]-game_data[0])*(point[0]-game_data[0])
            + (point[1]-game_data[1])*(point[1]-game_data[1])) < 1):
        return True
    return False


def run_bot(game_data: tuple, point: tuple, keys):
    """Moves camer and does actions like throw bolt or jump"""
    angle = calculate_rotation(
        point, (game_data[0], game_data[1]),
        (game_data[2], game_data[3]))
    turn_camera(angle, keys)
    if(point[2]):
        press_key("SPACE", keys=keys)
    if(point[3]):
        press_mouse_key("right")
