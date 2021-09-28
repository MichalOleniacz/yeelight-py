import threading
import time
from random import randrange
from models.rgb_strip import RGB_Strip
from models.sock import MySock
import numpy
from mss import mss
from PIL import Image
import math

# Definitions
SOURCE_IP = "192.168.0.111"
SOURCE_PORT = 55443
LIGHT_IP = "192.168.0.160"
LIGHT_PORT = 55443
sct = mss()
w, h = 1920, 1080
monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}

sock = MySock()
music_sock = MySock(bind_addr="192.168.0.111",
                    bind_port=53332, listening=True)
sock.connect(host=LIGHT_IP, port=LIGHT_PORT)
strip = RGB_Strip(sock=sock, ip=LIGHT_IP, port=LIGHT_PORT)
strip.start_music()


def rgb_to_hex(rgb):
    red, green, blue = rgb
    return (red << 16) + (green << 8) + blue


def start_on_thread():
    # i = 0
    while True:
        img = Image.frombytes('RGB', (w, h), sct.grab(monitor).rgb)
        # myimg = cv2.imread('image.jpg')
        avg_color_per_row = numpy.average(img, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)

        colors = []

        for item in avg_color:
            colors.append(math.floor(item))

        if numpy.sum(colors) > 25:
            print("Update: ", rgb_to_hex((colors[0], colors[1], colors[2])))
            strip.set_rgb_int(
                int(rgb_to_hex((colors[0], colors[1], colors[2]))))


if __name__ == "__main__":
    threading.Timer(0.4, start_on_thread).start()
    # val = randrange(16777214)
    # print("setting light to:", hex(val))
    # strip.set_rgb_int(val)
    # i += 1
    # sock.send(msg=MESSAGE)
