from yeelight import Bulb
from mss import mss
from PIL import Image
import threading
import cv2
import numpy
import math

bulb = Bulb('192.168.0.160')
sct = mss()
w, h = 1920, 1080
monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}


def screenToRGB():
    img = Image.frombytes('RGB', (w, h), sct.grab(monitor).rgb)
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)

    colors = []

    for item in avg_color:
        colors.append(math.floor(item))

    if numpy.sum(colors) > 25:
        bulb.set_rgb(colors[0], colors[1], colors[2])
    print(colors)
    main()


def main():
    threading.Timer(1.5, screenToRGB).start()


if __name__ == '__main__':
    main()
