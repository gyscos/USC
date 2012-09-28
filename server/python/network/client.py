import socket
import threading
import agent

class Client(agent.Agent):

    def __init__(self, handler):
        super().__init__(handler)

    def connect(self, host, port):
        self.running = True
        self.addr = (host, port)
        thread = threading.Thread(target = self.prepare)

    def prepare(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(s.addr)
        self.setup(s)
        self.run()
