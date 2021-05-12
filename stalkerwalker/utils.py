import time
import json
import pymem
import keys
import keyboard
import mouse
from pymem import Pymem
from math import acos, pi, sin, sqrt, isclose
KOEF = 1
INDEX = 0

#ТЫКАЕТ НАЧАТЬ НОВУЮ ИГРУ 
def start_new_game():
    #keys = keys.Keys()
    #ставим мышку в 0
    keys.directMouse(-5000,-5000)
    time.sleep(0.016)
    #начинаем новую игру
    keys.directMouse(800,440)
    time.sleep(0.016)
    mouse.click(button='left')
    time.sleep(0.016)
    mouse.release(button='left')
    time.sleep(0.5) #тут пауза побольше, игра почему-то тупит
    mouse.click(button='left')
    time.sleep(0.016)
    mouse.release(button='left')
    time.sleep(0.016)

#ЖДЕТ ПОКА КОНЧИТСЯ ЗАГРУЗКА
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

    #само ожидание
    for i in range(0,10000):
        loading = pm.read_bool(module_offset_xrnetserver+0xFAC4)
        sync = pm.read_float(pm.base_address+0x104928)
        plahka = pm.read_bool(module_offset_xrgame+0x54C2F9)
        if(not loading or (sync > 0.09 and sync < 0.11) or plahka):
            time.sleep(0.016)
        else:
            break
  

#двойной сейвлод + ожидание конца загрузки
def double_saveload():
    #сейвлоды и ожидание
    keys.directKey("F6")
    time.sleep(0.016)
    keys.directKey("F6", keys.key_release)
    time.sleep(0.016)
    keys.directKey("F7")
    time.sleep(0.016)
    keys.directKey("F7", keys.key_release)
    time.sleep(0.016)
    load_waiter()




def calculate_angle_my(target: list, current: list, view: list):
    """Return turning angle in grad"""
    # getting vectors
    vector = [target[0]-current[0], target[1]-current[1]]
    dot = vector[0]*view[0] + vector[1]*view[1]
    lengths = sqrt(vector[0]*vector[0]+vector[1]*vector[1])
    lenv = sqrt(view[0]*view[0]+view[1]*view[1])
    angle = 0
    # angle calculation
    if(lengths != 0):
        angle = acos(dot/(lengths*lenv))
    else:
        angle = 0
    vector2 = [vector[0]/lengths-view[0]/lenv, vector[1]/lengths-view[1]/lenv]
    # angle correction based on sin and cos as view[0] and view[1]
    if(view[0] > 0 and view[1] > 0):
        if(vector2[0] < 0):
            angle = -1*angle
    elif(view[0] > 0 and view[1] < 0):
        if(vector2[1] > 0):
            angle = -1*angle
    elif(view[0] < 0 and view[1] < 0):
        if(vector2[0] > 0):
            angle = -1*angle
    elif(view[0] < 0 and view[1] > 0):
        if(vector2[1] < 0):
            angle = -1*angle
    return int(KOEF*angle*180/pi)


def data_from_game(pm: Pymem):
    """Return x,z,confirmation, sin and cos values read from game memory"""
    plahka = pm.read_bool(module_offset+0x54C2F9)
    x = pm.read_float(pm.base_address+0x10493C)
    z = pm.read_float(pm.base_address+0x104944)
    view_sin = pm.read_float(pm.base_address+0x104950)
    view_cos = pm.read_float(pm.base_address+0x104948)
    return {"x": x, "z": z, "sin": view_sin, "cos": view_cos, "plashka": plahka}


def load_file(name: str):
    """Return list of data from file"""
    points = None
    with open("dataclean", mode="r") as file:
        points = json.load(file)
    return points


def get_module_offset(module: str):
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


def press_key(key: str):
    """Presses a key"""
    keys.directKey(key)
    keys.directKey(key, keys.key_release)


def press_mouse_key(key: str):
    """Presses key on mouse"""
    mouse.click(button=key)
    mouse.release(button=key)


def turn_camera(pixels: int):
    """Turns camera"""
    keys.directMouse(pixels, 0)


def run_bot(game_data: dict, points: list):
    """Runs bot"""
    wpn_allowed = True
    global INDEX
    if(wpn_allowed and game_data["x"] > -245.0 and game_data["z"] > -125.0):
        press_key("6")
        wpn_allowed = False
    if(sqrt((points[INDEX][0]-game_data["x"])*(points[INDEX][0]-game_data["x"]) + (points[INDEX][1]-game_data["z"])*(points[INDEX][1]-game_data["z"])) < 0.5):
        INDEX += 1
    angle1 = calculate_angle_my(
        points[INDEX], [game_data["x"], game_data["z"]], [game_data["cos"], game_data["sin"]])
    turn_camera(angle1)
    if(points[INDEX][2]):
        press_key("SPACE")
    if(points[INDEX][3]):
        press_mouse_key("right")

