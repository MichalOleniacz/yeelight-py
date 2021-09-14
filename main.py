import time
from random import randrange
from models.rgb_strip import RGB_Strip
from models.sock import MySock

# Definitions
SOURCE_IP = "192.168.0.111"
SOURCE_PORT = 55443
LIGHT_IP = "192.168.0.160"
LIGHT_PORT = 55443

if __name__ == "__main__":
    sock = MySock()
    music_sock = MySock(bind_addr="192.168.0.111", bind_port=53332, listening=True)
    sock.connect(host=LIGHT_IP, port=LIGHT_PORT)
    strip = RGB_Strip(sock=sock, ip=LIGHT_IP, port=LIGHT_PORT)
    strip.start_music()
    i = 0
    while True:
        time.sleep(0.2)
        val = randrange(16777214)
        print("setting light to:", hex(val))
        strip.set_rgb_int(val)
        i += 1
    # sock.send(msg=MESSAGE)
