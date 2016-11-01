#!/usr/bin/env python
from __future__ import print_function
from ansible.cli.playbook import CLI
from argparse import ArgumentParser, FileType
from os import path

import ansible.constants as C
import shutil
import sys


BASE = path.abspath(path.join(path.dirname(__file__), '..'))


def cinch():
    parser = ArgumentParser(description=
            'A wrapper around Cinch for the most common use case')
    parser.add_argument('inventory', dest='inventory', type=FileType('r'))
    args = parser.parse_args(sys.argv)
    ansible_args = [
        path.join(BASE, 'site.yml'),
        '-i', args.inventory,
        '-v'
    ]
    try:
        cli = CLI(ansible_args)
        cli.parse()
        exit_code = cli.run()
    except:
        exit_code = 250
    finally:
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
    sys.exit(exit_code)


if __name__ == '__main__':
    print("You should not invoke this file directly.")
    sys.exit(1)
