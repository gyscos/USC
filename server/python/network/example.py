import server

class ExampleHandler:
    def handle_message(self, msg):
        print("Message : " + msg)
        self.agent.send(msg)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass


class Example(server.Server):
    def __init__(self):
        super().__init__()

    def get_handler(self):
        return ExampleHandler()

ex = Example()
ex.start("localhost", 1115)

print("Passed !")

