import time
import json
import pymem
import keys
import keyboard
import mouse
from pymem import Pymem
from math import acos, pi, sin, sqrt, isclose


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




def calculate_angle_my(target: list, current: list, view: list):
    """Return turning angle in grad"""
    vector = [target[0]-current[0], target[1]-current[1]]
    dot = vector[0]*view[0] + vector[1]*view[1]
    lengths = sqrt(vector[0]*vector[0]+vector[1]*vector[1])
    lenv = sqrt(view[0]*view[0]+view[1]*view[1])
    angle = 0
    if(lengths != 0):
        angle = acos(dot/(lengths*lenv))
    else:
        angle = 0
    vector2 = [vector[0]/lengths-view[0]/lenv, vector[1]/lengths-view[1]/lenv]

    if(view[0] > 0):
        a = "1"
    else:
        a = "0"

    if(view[1] > 0):
        b = "1"
    else:
        b = "0"

    if(vector2[0] > 0):
        c = "1"
    else:
        c = "0"

    if(vector2[1] > 0):
        d = "1"
    else:
        d = "0"

    #print(a + b + c + d)

    if(view[0] > 0 and view[1] > 0): 
        if(vector2[1] < 0):
            pass
        if(vector2[0] < 0):
            angle = -1*angle

    if(view[0] > 0 and view[1] < 0):
        if(vector2[0] < 0):
            pass
        if(vector2[1] > 0):
            angle = -1*angle

    if(view[0] < 0 and view[1] < 0):
        if(vector2[1] > 0):
            pass
        if(vector2[0] > 0):
            angle = -1*angle
    
    if(view[0] < 0 and view[1] > 0):
        if(vector2[0] > 0):
            pass
        if(vector2[1] < 0):
            angle = -1*angle
    if(abs(angle*180/pi) > 0):
        return angle*180/pi#angle/abs(angle)
    else:
        return 0



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
    for i in range(5):
        print(i)
        time.sleep(1)
    keys.directKey("w")
    keys.directKey("x")
    keys.directKey("x", keys.key_release)
    wpn_allowed = 'false'
    for i in range(0, 100000):
        plahka = pm.read_bool(module_offset+0x54C2F9)
        x = pm.read_float(pm.base_address+0x10493C)
        z = pm.read_float(pm.base_address+0x104944)
        view_sin = pm.read_float(pm.base_address+0x104950)
        view_cos = pm.read_float(pm.base_address+0x104948)
        if(wpn_allowed == 'false' and x > -245 and z > -125):
            keys.directKey("6")
            keys.directKey("6", keys.key_release)
            wpn_allowed = 'true'
        #print("x: " + str(x) + " y: " + str(z))
        #print("view_x: " + str(view_cos) + ", view_y: " + str(view_sin))
        if(sqrt((points[index][0]-x)*(points[index][0]-x) + (points[index][1]-z)*(points[index][1]-z)) < 0.5):
            print("reached:" + str(points[index]))
            index += 1
        angle1 = calculate_angle_my(
            points[index], [x, z], [view_cos, view_sin])
        angle_pix = angle1*7.29378
        print(str(angle1))
        if(float(points[index][2]) > 0.1):
            keys.directKey("SPACE")
        else:
            keys.directKey("SPACE", keys.key_release)
        if(float(points[index][3]) > 0.1):
            mouse.click(button='right')
        else:
            mouse.release(button='right')
        keys.directMouse(int(angle_pix), 0)
        #print("dir to get: "+ str(angle_pix/11.82) + ", in grad: " + str(int(angle_pix)))
        if(keyboard.is_pressed('F4')):
            break
        time.sleep(0.01)
    keys.directKey("w", keys.key_release)
