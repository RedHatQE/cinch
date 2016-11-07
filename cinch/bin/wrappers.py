from __future__ import print_function

from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from os import path
from traceback import print_exc

import sys


BASE = path.abspath(path.join(path.dirname(__file__), '..'))


def call_ansible(inventory, *args):
    """
    Wraps a call out to the ansible-playbook executable, passing it the cinch site.yml
    file that kicks off this playbook.

    :param inventory: The Ansible inventory file to pass through
    :param args: An array of other command-line arguments to ansible-playbook to pass
    :return: The exit code returned from ansible-playbook, or 255 if errors come from elsewhere
    """
    # Construct the arguments to pass to Ansible by munging the arguments
    # provided to this method
    ansible_args = [
        path.join(BASE, 'site.yml'),
        '-i', inventory,
        '-v'
    ]
    ansible_args.extend(args)
    ansible = local['ansible-playbook']
    try:
        ansible.run(ansible_args, stdout=sys.stdout, stderr=sys.stderr)
        exit_code = 0
    except ProcessExecutionError as ex:
        print("Error encountered while executing ansible-playbook.", file=sys.stderr)
        exit_code = ex.retcode
    except Exception as ex:
        print("Unknown error occurred: {0}".format(ex), file=sys.stderr)
        print_exc()
        exit_code = 255
    return exit_code