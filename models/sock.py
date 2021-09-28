import socket
import json


class MySock:
    def __init__(self, sock=None, bind_addr="localhost", bind_port=54321, listening=False):
        self.ingore_listening = listening
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if listening:
                self.sock.bind((bind_addr, bind_port))
                self.sock.listen(3)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def send(self, msg):
        try:
            self.sock.send((json.dumps(msg) + "\r\n").encode("utf8"))
            if not self.ingore_listening:
                response = self.sock.recv(1024)
                return response
        finally:
            print("updated")
