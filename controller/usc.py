#!/usr/bin/python

import usc_shell
import controller
import sys
import json
import usc_config

"""
Use cases :

usc
    Show the usc command prompt

usc host (port)
    Starts usc and tries to connect to host

usc alias
    Starts usc and tries to connect to a known (host[, port]) alias

"""

if __name__ == "__main__":

    aliases = usc_config.get_aliases()


    if len(sys.argv) > 1:
        # Directly connects

        (host, port) = usc_config.resolve_addr(sys.argv[1:])

        usc = controller.UscController()
        usc.connect(host, port)
    else:
        # Starts a usc shell
        shell = usc_shell.UscShell()
        shell.start()

