#!/usr/bin/env python
from __future__ import print_function
from ansible.cli.playbook import PlaybookCLI as CLI
from argparse import ArgumentParser, FileType
from os import path

import ansible.constants as C
import os
import shutil
import sys
import traceback


BASE = path.abspath(path.join(path.dirname(__file__), '..'))


def cinch():
    parser = ArgumentParser(description=
            'A wrapper around Cinch for the most common use case')
    parser.add_argument('inventory')
    args = parser.parse_args()
    if len(args.inventory) > 0:
        if args.inventory[0] == '/':
            inventory = args.inventory
        else:
            inventory = path.join(os.getcwd(), args.inventory)
    else:
        raise Exception("Inventory path needs to be non-empty")
    ansible_args = [
        'ansible-playbook',
        path.join(BASE, 'site.yml'),
        '-i', inventory,
        '-v'
    ]
    print(ansible_args)
    try:
        cli = CLI(ansible_args)
        cli.parse()
        exit_code = cli.run()
    except Exception as ex:
        print("Error detected: {0}".format(str(ex)), sys.stderr)
        print(traceback.format_exc())
        exit_code = 250
    finally:
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
    sys.exit(exit_code)


if __name__ == '__main__':
    print("You should not invoke this file directly.")
    sys.exit(1)
