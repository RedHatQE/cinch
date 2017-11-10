from __future__ import print_function

from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from traceback import print_exc

import os
import sys


BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Link to our docs with configuration examples
DOCS = 'https://redhatqe-cinch.readthedocs.io/en/latest/users.html'
# Skeleton text to insert in YAML config files
SKEL_TEXT = '''---
# Add your cinch {0} configuration here
# Examples: {1}
'''


def call_ansible(inventory, playbook, *args):
    """
    Wraps a call out to the ansible-playbook executable, passing it the cinch
    site.yml file that kicks off this playbook.

    :param inventory: The Ansible inventory file to pass through
    :param args: An array of other command-line arguments to ansible-playbook
    to pass
    :return: The exit code returned from ansible-playbook, or 255 if errors
    come from elsewhere
    """
    # Construct the arguments to pass to Ansible by munging the arguments
    # provided to this method
    ansible_args = [
        os.path.join(BASE, playbook),
        '-i', inventory,
        '-v',
        '--ssh-common-args=-o StrictHostKeyChecking=no ' +
        '-o UserKnownHostsFile=/dev/null'
    ]
    ansible_args.extend(args)
    ansible = local['ansible-playbook']
    exit_code = command_handler(ansible, ansible_args)
    return exit_code


def command_handler(command, args):
    """
    Generic function to run external programs.
    :param command: Exectuable to run
    :param args: arguments to be given to the external executable
    :return: The exit code of the external command, or exit code 255 if we are
    unable to determine the exit code
    """
    try:
        command.run(args, stdout=sys.stdout, stderr=sys.stderr)
        exit_code = 0
    except ProcessExecutionError as ex:
        print('Error encountered while executing command.',
              file=sys.stderr)
        exit_code = ex.retcode
    except Exception as ex:
        print('Unknown error occurred: {0}'.format(ex), file=sys.stderr)
        print_exc()
        exit_code = 255
    return exit_code
