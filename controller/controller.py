import json
import readline
import completer
import network.client

def ask():
    cmd = input('> ')
    return cmd

class UscController:

    def load_commands(self, commands):
        self.commands = commands
        self.comp = completer.Completer({}, "entry")
        for name in commands:
            self.comp.add_list(name)
            args = commands[name]
            for cmd in args:
                (cmdId, childs) = args[cmd]
                self.comp.add_to_list(name, {cmd:childs})

        readline.set_completer(self.comp.complete)

    def parse(self, args, expected):
        if len(args) == 0:
            return []
        arg = args[0]
        if len(expected) == 0:
            return [(arg, -1)] + self.parse(args[1:], expected)
        pos = expected[0]
        if pos in self.commands:
            if arg in self.commands[pos]:
                (cmdId, childs) = self.commands[pos][arg]
                return [(arg, cmdId)] + self.parse(args[1:], childs + expected[1:])
        return [(arg, -1)] + self.parse(args[1:], expected[1:])

    def get_param_list(self, command):
        args = command.split()
        return self.parse(args, ["entry"])

    def handle_command(self, command):
        # Get param list corresponding to command
        params = self.get_param_list(command)
        self.client.send(json.dumps(params))

    def handle_message(self, msg):
        content = json.loads(msg)
        if not self.init:
            self.init = True
            self.load_commands(content)
        else:
            print(content['answer'])
            if content['refresh']:
                self.load_commands(content['root'])


    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def connect(self, host, port):
        self.init = False
        self.client = network.client.Client(self)
        self.client.connect(host, port)
        self.run()

    def run(self):

        while True:
            try:
                cmd = ask()
                self.handle_command(cmd)
            except KeyboardInterrupt:
                print()
                pass
            except EOFError:
                print()
                break
        self.client.close()
