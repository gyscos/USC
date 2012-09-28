import server

class Example(server.Server):
    def __init__(self, host, port):
        super().__init__(host, port)

    def handle(self, conn, addr):
        pass
