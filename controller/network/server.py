import socket
import agent
import threading

class ServerAgent:
    def __init__(self, handler):
        self.agent = agent.Agent(handler)

    def run(self):
        print("Server Agent running...")
        self.agent.setup(self.s)
        self.agent.run()

    def start(self, s):
        self.s = s
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.agent.close()
        self.thread.join()



class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle(self):
        pass

    def start(self, host, port):
        self.addr = (host, port)
        thread = threading.Thread(target=self.run)
        thread.start()

    def get_handler(self):
        def handle(msg):
            pass
        return handle

    def run(self):
        self.s.bind(self.addr)
        self.s.listen(5)

        self.running = True
        while self.running:
            conn, addr = self.s.accept()
            print(addr)

            handler = self.get_handler()
            agent = ServerAgent(handler)
            agent.start(conn)


