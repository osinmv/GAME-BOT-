from __future__ import with_statement
from PIL import Image, ImageDraw
import numpy as np
import json

X_OFFSET = 513
Y_OFFSET = 489
X_COEF = 1.54
Y_COEF = -1.50

if __name__ == "__main__":
    im = Image.open("map_garbage.png")
    with open("data", mode="r") as file:
        points = json.loads(file.read())
        drawing = ImageDraw.Draw(im)
        for i in range(1, len(points)):
            drawing.line((points[i-1][0]*X_COEF+X_OFFSET, points[i-1][1]
                          * Y_COEF+Y_OFFSET)+(points[i][0]*X_COEF+X_OFFSET, points[i][1]
                                              * Y_COEF+Y_OFFSET), fill=(255, 255, 255, 255))
        im.save("map_garbage_new.png", "PNG")
