import time
import json
import pymem
import keys
import keyboard
import mouse
from pymem import Pymem
from math import acos, pi, sin, sqrt, isclose

"""попытка сделать идеальный лифт"""

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
    index = 0
    for i in range(2):
        print(i)
        time.sleep(1)
    keys.directKey("lctrl")
    time.sleep(0.016)
    keys.directKey("lshift")
    time.sleep(0.016)

    keys.directKey("w")
    time.sleep(0.016)
    keys.directKey("w", keys.key_release)
    time.sleep(0.016)

    keys.directKey("s")
    time.sleep(0.016)
    keys.directKey("s", keys.key_release)
    time.sleep(0.1)

    keys.directKey("space")
    time.sleep(0.016)
    keys.directKey("space", keys.key_release)
    time.sleep(0.3)

    for i in range(0, 4):
        if(keyboard.is_pressed('F4')):
            break
        keys.directKey("w")
        time.sleep(0.05)
        keys.directKey("w", keys.key_release)
        time.sleep(0.05)

    keys.directKey("w")
    time.sleep(1)

    for i in range(0, 10):
        if(keyboard.is_pressed('F4')):
            break
        keys.directKey("w")
        time.sleep(0.1)
        keys.directKey("w", keys.key_release)
        time.sleep(0.1)
    keys.directKey("w")
    print(str(keyboard.is_pressed('F4')))
    for i in range(0, 100000):
        if(keyboard.is_pressed('F4')):
            keys.directKey("lctrl", keys.key_release)
            keys.directKey("lshift", keys.key_release)
            keys.directKey("w", keys.key_release)
            break
        time.sleep(0.016)
