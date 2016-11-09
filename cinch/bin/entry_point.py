#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser, REMAINDER
from os import path
from wrappers import call_ansible

import os
import sys


def cinch():
    """
    Entry point for the "cinch" CLI that merely wrapps the ansible-playbook
    command and pre-fills its path to the site.yml file for Cinch. The cinch
    tool requires a single argument - the Ansible inventory file - and accepts
    an arbitrary number of extra arguments that are passed through to the
    ansible-playbook executable.

    :return: Exit code 0 if the execution is completed successfully, or 255
    if an unknown error occurs. If ansible-playbook exits with an error code,
    this executable will exit with the same code.
    """
    # Parse the command line arguments
    parser = ArgumentParser(description=
            'A wrapper around Cinch for the most common use case')
    # The inventory file that the user provides which will get passed along to
    # Ansible for its consumption
    parser.add_argument('inventory')
    # All remaining arguments are passed through, untouched, to Ansible
    parser.add_argument('args', nargs=REMAINDER)
    args = parser.parse_args()
    if len(args.inventory) > 0:
        if args.inventory[0] == '/':
            inventory = args.inventory
        else:
            inventory = path.join(os.getcwd(), args.inventory)
    else:
        raise Exception("Inventory path needs to be non-empty")
    exit_code = call_ansible(inventory, args.args)
    sys.exit(exit_code)


if __name__ == '__main__':
    print("You should not invoke this file directly.")
    sys.exit(1)
