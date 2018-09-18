from __future__ import print_function
from argparse import ArgumentParser, REMAINDER
from os import getcwd, path
from wrappers import call_ansible

import sys


def cinch_generic(playbook, help_description):
    # Parse the command line arguments
    parser = ArgumentParser(description='A CLI wrapper for ansible-playbook '
                            'to run cinch playbooks.  ' + help_description)
    # The inventory file that the user provides which will get passed along to
    # Ansible for its consumption
    parser.add_argument('inventory', help='Ansible inventory file (required)')
    # All remaining arguments are passed through, untouched, to Ansible
    parser.add_argument('args', nargs=REMAINDER, help='extra args to '
                        'pass to the ansible-playbook command (optional)')
    args = parser.parse_args()
    if len(args.inventory) > 0:
        if args.inventory[0] == '/':
            inventory = args.inventory
        else:
            inventory = path.join(getcwd(), args.inventory)
    else:
        raise Exception('Inventory path needs to be non-empty')
    exit_code = call_ansible(inventory, playbook, args.args)
    sys.exit(exit_code)


def cinch():
    """
    Entry point for the "cinch" CLI that merely wraps the ansible-playbook
    command and pre-fills its path to the site.yml file for Cinch. The cinch
    tool requires a single argument - the Ansible inventory file - and accepts
    an arbitrary number of extra arguments that are passed through to the
    ansible-playbook executable.

    :return: Exit code 0 if the execution is completed successfully, or 255
    if an unknown error occurs. If ansible-playbook exits with an error code,
    this executable will exit with the same code.
    """
    help_description = '''This command runs the 'site.yml' playbook to
                          configure a Jenkins master or slave.'''
    cinch_generic('site.yml', help_description)


def teardown():
    """
    Entry point for the "teardown" CLI that wraps ansible-playbook commands and
    pre-fills its path to the teardown.yml file.

    :return: Exit code 0 if the execution is completed successfully, or 255 if
    an unknown error occurs. If ansible-playbook exits with an error code, this
    executable will exit with the same code.
    """
    help_description = '''This command runs the 'teardown.yml' playbook to
                          disconnect a Jenkins slave.'''
    cinch_generic('teardown.yml', help_description)


if __name__ == '__main__':
    print('You should not invoke this file directly.')
    sys.exit(1)
