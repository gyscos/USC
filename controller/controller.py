import sys

sys.path.append("../../python_helper")

import json
import readline
import completer
import network.json_rpc as json_rpc

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
        result = json_rpc.get_answer(self.addr, 'call', params)
        print(result['answer'])
        if (result['refresh']):
            self.load_commands(result['root'])


    def connect(self, host, port):
        self.init = False
        self.addr = (host, port)
        result = json_rpc.get_answer(self.addr, 'list')
        self.load_commands(result)
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
