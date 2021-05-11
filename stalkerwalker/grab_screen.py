import cv2
import mss
import time
import numpy as np
import keys

debug = True


def grab_screen(selection: dict, screen_graber):
    """Return image based on specified selection
        selectoin is a dict with top,left,width,height keys"""
    return screen_graber.grab(selection)


def find_direction(image):
    """Return direction vector based on gray image"""
    matches = np.argwhere(image > 100)
    mean_y = np.mean(matches[:, 1])
    center = 10
    error = center - mean_y
    if(str(error) == "nan"):
        error = 0
    else:
        error = int(error)
    print(error)
    if(debug):
        keys.directMouse(-5*error, 0)
    cv2.waitKey(10)


if __name__ == "__main__":
    keys = keys.Keys()
    selection = {'top': 50, 'left': 68,
                 'width': 20, 'height': 20}
    screen_graber = mss.mss()
    for i in range(5):
        print(i)
        time.sleep(1)
    if(debug):
        keys.directKey("w")
        keys.directKey("x")
        keys.directKey("x", keys.key_release)
    for i in range(0, 25000):
        image = np.array(grab_screen(selection, screen_graber))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("screen", image)
        direction = find_direction(gray)
        # print(find_direction(gray))
        # angle = int(25*(direction[1]/1))
        # print(angle)
        time.sleep(0.033)
    # cv2.waitKey()
    if(debug):
        keys.directKey("w", keys.key_release)
    cv2.destroyAllWindows()
