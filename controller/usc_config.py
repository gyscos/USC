import json
import os.path

rc_filename = os.path.expanduser("~/.usc.rc")

default_port = 2222


def get_aliases():
    try:
        f = open(rc_filename, 'r')
        aliases = json.load(f)
        f.close()
    except IOError:
        aliases = {}

    return aliases

def write_aliases(aliases):
    try:
        content = json.dumps(aliases)
        f = open(rc_filename, 'w')
        f.write(content)
        f.close()
    except IOError:
        pass

def make_addr(args):
    if len(args) == 2 and args[1] != '':
        return (args[0], int(args[1]))
    else:
        return (args[0], default_port)

def resolve_alias(alias):
    aliases = get_aliases()
    if alias in aliases:
        return aliases[alias]
    else:
        return (alias, default_port)

def resolve_addr(args):
    if len(args) == 2 and args[1] != '':
        return make_addr(args)
    else:
        return resolve_alias(args[0])


def save_alias(alias, host, port):
    aliases = get_aliases()
    aliases[alias] = (host, port)
    write_aliases(aliases)

def remove_alias(alias):
    aliases = get_aliases()
    aliases.pop(alias)
    write_aliases(aliases)
