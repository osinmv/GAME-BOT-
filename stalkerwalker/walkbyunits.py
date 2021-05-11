import time
import json
import pymem
import keys
from pymem import Pymem
from math import acos, sin, sqrt, isclose


def calculate_angle(target: list, current: list, view: list):
    """Return turning angle in pixels"""
    vector = [target[0]-current[0], target[1]-current[1]]
    lengths = sqrt(vector[0]*vector[0]+vector[1]*vector[1])
    vector2 = [view[1] - vector[0]/lengths, view[0] - vector[1]/lengths]
    l2 = sqrt(vector2[0]*vector2[0]+vector2[1]*vector2[1])
    vector2 = [vector2[0]/l2, vector2[1]/l2]
    print(str(vector2[0]))
    angle = acos(vector2[0])
    return int(-1*angle*11.82)


if __name__ == "__main__":
    pm = Pymem("XR_3DA.exe")
    keys = keys.Keys()
    module_offset = None
    for i in list(pm.list_modules()):
        if(i.name == "xrGame.dll"):
            module_offset = i.lpBaseOfDll
    plahka = False
    points = None
    with open("dataclean", mode="r") as file:
        points = json.loads(file.read())
    index = 2
    for i in range(5):
        print(i)
        time.sleep(1)
    keys.directKey("w")
    keys.directKey("x")
    keys.directKey("x", keys.key_release)
    for i in range(0, 100000):
        plahka = pm.read_bool(module_offset+0x54C2F9)
        x = pm.read_float(pm.base_address+0x10493C)
        z = pm.read_float(pm.base_address+0x104944)
        view_sin = pm.read_float(pm.base_address+0x104950)
        view_cos = pm.read_float(pm.base_address+0x104948)
        if(-0.5 < points[index-1][0]-x < 0.5 and -0.5 < points[index-1][1] - z < 0.5):
            index += 1
        angle = calculate_angle(
            points[index], [x, z], [view_sin, view_cos])
        keys.directMouse(angle, 0)
        print("Desired position" + str(points[index]))
        time.sleep(0.16)

    keys.directKey("w", keys.key_release)
