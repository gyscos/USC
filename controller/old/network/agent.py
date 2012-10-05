import socket

class Agent:
    def __init__(self, handler):
        self.handler = handler
        self.running = False
        self.closed = False

        self.handler.agent = self

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def handle_message(self, message):
        self.handler.handle_message(message)

    def on_connect(self):
        self.handler.on_connect()

    def on_disconnect(self):
        self.handler.on_disconnect()

    def read_line(self):
        msg = ''
        while self.running:
            chunk = self.s.recv(2048)
            if len(chunk) == 0:
                #Error !!!
                return ''
            chunk = str(chunk, encoding='utf-8')
            msg += chunk
            if chunk[-1] == '\n':
                break
        return msg

    def send(self, msg):
        msg += '\n'
        msg = bytes(msg, encoding='utf-8')
        length = len(msg)
        total_sent = 0

        while total_sent < length:
            sent = self.s.send(msg[total_sent:])
            if sent == 0:
                # Error !
                break
            total_sent += sent

    def setup(self, s):
        self.s = s
        self.running = True

    def run(self):
        self.on_connect()

        while self.running:
            message = self.read_line()
            if message == '':
                self.running = False
            else:
                self.handle_message(message)

        self.close()

        self.on_disconnect()

