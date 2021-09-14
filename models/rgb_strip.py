import json
import enum
import socket
from models.sock import MySock

class Methods(enum.Enum):
    set_rgb = "set_rgb"


class RGB_Strip:
    def __init__(self, ip, sock, port=55443):
        self._ip = ip
        self._sock = sock
        self._port = port
        self.req = {"id": 1, "method": None, "params": [None, None, None]}
        self._music_sock = None
        self._music_mode = False

    def ensure_on(self):
        power_res = self._sock.send({"id": 1, "method": "get_prop", "params": ["power"]})
        json_res = json.loads(power_res)
        if json_res["result"][0] == "on":
            return
        else:
            self._sock.send({"id": 1, "method": "toggle", "params": []})
            return

    def send_request(self, request):
        if self._music_mode:
            self._music_sock.send(request)
        else:
            self.ensure_on()
            response = self._sock.send(request)
            return json.loads(response)

    def toggle(self):
        self.req["method"] = "toggle"
        self.req["params"] = []
        return self.send_request(self.req)

    def get_prop(self, *args):
        self.req["method"] = "get_prop"
        self.req["params"] = args
        return self.send_request(self.req)

    def set_rgb(self, hex_color):
        self.req["method"] = "set_rgb"
        self.req["params"] = [int(hex_color), "smooth", 300]
        return self.send_request(self.req)

    def set_rgb_int(self, color):
        self.req["method"] = "set_rgb"
        self.req["params"] = [color, "smooth", 300]
        return self.send_request(self.req)

    def toggle_led(self):
        self.req["method"] = "toggle"
        self.req["params"] = []
        return self.send_request(self.req)

    def start_color_flow(self, flow, count=0, action=0, flow_expression=None):
        self.req["method"] = "start_cf"
        self.req["params"] = [count, action, flow]
        return self.send_request(self.req)

    def start_music(self):
        self.req["method"] = "set_music"
        self.req["params"] = [1, "192.168.0.111", 53322]

        # New sock for Yeelight to connect to
        listening_sock = MySock(listening=True, bind_addr="192.168.0.111", bind_port=53322)
        listening_sock.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_sock.sock.settimeout(5)

        # Send request to yeelight
        self.send_request(self.req)

        # Establish new TCP connection
        conn, _ = listening_sock.sock.accept()
        music_sock = MySock(sock=conn, listening=True)

        # Close old sock and remap self
        listening_sock.close()
        self._music_sock = music_sock
        self._music_mode = True
