import keys
import time


if __name__ == "__main__":
    for i in range(0, 5):
        time.sleep(1)
    keys = keys.Keys()
    keys.directMouse(2128, 0)

    # koef = 11.82