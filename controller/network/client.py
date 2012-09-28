import socket
import threading
import network.agent

class Client(network.agent.Agent):

    def __init__(self, handler):
        super().__init__(handler)

    def connect(self, host, port):
        self.running = True
        self.addr = (host, port)
        thread = threading.Thread(target = self.prepare)
        thread.start()

    def prepare(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client connecting...")
        s.connect(self.addr)
        self.setup(s)
        self.run()
