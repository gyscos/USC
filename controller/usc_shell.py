import os
import usc_config
import os.path
import json
import readline
import completer
import controller

completer_filename = os.path.expanduser("~/.usc_completer.rc")

def ask():
    cmd = input('> ')
    return cmd

class UscShell:

    def __init__(self):
        readline.read_init_file(completer_filename)

        aliases = usc_config.get_aliases()

        self.comp = completer.Completer({}, "entry")

        self.comp.add_list("entry", {})

        self.comp.add_to_list("entry", "list")
        self.comp.add_to_list("entry", {"drop":["alias"]})

        self.comp.add_to_list("entry", { "save":["alias"] })
        self.comp.add_to_list("entry", { "connect":["alias"], "quit":[] })

        self.comp.add_list("alias", set())
        for alias in aliases:
            self.comp.add_to_list("alias", { alias:[] } )

        self.refresh()

    def refresh(self):
        readline.set_completer(self.comp.complete)

    def handle(self, cmd):
        args = cmd.split(' ')
        if args[0] == 'save':
            if len(args) >= 3:
                alias = args[1]
                (host, port) = usc_config.make_addr(args[2:])
                usc_config.save_alias(alias, host, port)
                self.comp.add_to_list("alias", {alias})
        elif args[0] == 'drop':
            if len(args) == 2:
                usc_config.remove_alias(args[1])
        elif args[0] == 'list':
            aliases = usc_config.get_aliases()
            for alias in aliases:
                print(alias + " : " + repr(aliases[alias]))
        elif args[0] == 'connect':
            print("Connecting...")
            c = controller.UscController()
            (host, port) = usc_config.resolve_addr(args[1:])

            readline.write_history_file('.history')
            readline.clear_history()
            # Long call
            c.connect(host, port)
            print("Disconnected.")

            readline.clear_history()
            readline.read_history_file('.history')
            # Done !
            self.refresh()
        elif args[0] == 'quit':
            return True

        return False


    def start(self):
        # Starts to read shell

        while True:
            try:
                cmd = ask()
                if self.handle(cmd):
                    break
            except KeyboardInterrupt:
                print()
                pass
            except EOFError:
                print()
                break

