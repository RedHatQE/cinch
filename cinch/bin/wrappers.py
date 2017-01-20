from __future__ import print_function

from contextlib import contextmanager
from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from traceback import print_exc

import os
import sys
import yaml


BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Link to our docs with configuration examples
DOCS = 'http://redhatqe-cinch.rtfd.io'
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
        '--ssh-common-args=-o StrictHostKeyChecking=no'
    ]
    ansible_args.extend(args)
    ansible = local['ansible-playbook']
    command_handler(ansible, ansible_args)


def call_linchpin(work_dir, arg):
    """
    Wraps a call out to the linchpin executable, and then kicks off a cinch
    Ansible playbook if necessary.

    :param work_dir: The linch-pin working directory that contains a PinFile
    and associated configuration files
    :param arg: A single argument to pass to the linchpin command
    :return: The exit code returned from linchpin, or 255 if errors come from
    elsewhere
    """
    # cinch will only support a subset of linchpin subcommands
    supported_cmds = ['rise', 'drop', 'init']
    if arg not in supported_cmds:
        raise Exception('linchpin command "{0}" not '
                        'supported by cinch'.format(arg))

    # If we are to ask linch-pin to interact with infrastructure we will check
    # for some required configuration items and set up them for later use
    if arg != 'init':
        inventory_file = get_inventory(work_dir)
        inventory_path = os.path.join(work_dir, 'inventory', inventory_file)

    # For drop/teardown, we must run our teardown playbook(s) *before*
    # linchpin terminates the instance(s)
    if arg == 'drop':
        call_ansible(inventory_path, 'teardown.yml')

    # As of right now the linch-pin working directory is not configurable, so
    # we essentially have a 'pushd' here to switch to the linch-pin working
    # directory as needed. This code can be removed if the following issue is
    # resolved:
    # https://github.com/CentOS-PaaS-SIG/linch-pin/issues/119
    @contextmanager
    def pushd(new_dir):
        previous_dir = os.getcwd()
        os.chdir(new_dir)
        yield
        os.chdir(previous_dir)

    # Execute the 'linchpin' command
    with pushd(work_dir):
        linchpin = local['linchpin']
        exit_code = command_handler(linchpin, arg)

    # Set up a linch-pin+cinch configuration skeleton for later use if the
    # 'init' subcommand was executed previously
    if arg == 'init':
        cinchpin_init(work_dir)

    # If linchpin is asked to provision resources, we will then run our
    # cinch provisioning playbook
    if arg == 'rise' and exit_code == 0:
        call_ansible(inventory_path, 'site.yml')


def cinchpin_init(work_dir):
    """
    Set up a linch-pin+cinch configuration skeleton

    :param work_dir: The linch-pin working directory that contains a PinFile
    and associated configuration files
    """
    # Consistent filename to use for various linch-pin YAML configurations
    # for 'cinchpin'
    config_file = 'cinch.yml'
    # Cinch layout and topology paths to be added to linch-pin PinFile
    config_setup = {
        'cinch': {
            'topology': config_file,
            'layout': config_file
        }
    }
    # These are the first-level config paths that linch-pin creates for us
    # in the working directory
    local_paths = ['layouts', 'topologies']

    # Overwrite the PinFile that linch-pin created with our configuration
    pin_file = os.path.join(work_dir, 'PinFile')
    with open(pin_file, 'w') as f:
        yaml.dump(config_setup, f, default_flow_style=False)

    # Write out the skeletons and inform the user that they exist
    for local_path in local_paths:
        path = os.path.join(work_dir, local_path, config_file)
        with open(path, 'w') as f:
            f.write(SKEL_TEXT.format(local_path, DOCS))
        print('Please configure this file to use cinch: ' + path)
    print('Example configurations: ' + DOCS)


def get_inventory(work_dir):
    """
    Basic checks for cinch compatibility in the linch-pin working directory,
    and if successful, we produce a topology file for cinch to use.

    :param work_dir: The linch-pin working directory as created by 'linchpin
    init' or 'cinchpin init'
    :return: The topology file to pass to the 'cinch' command
    """
    # Attempt to open the linch-pin PinFile
    try:
        with open(os.path.join(work_dir, 'PinFile'), 'r') as f:
            pin_file_yaml = yaml.safe_load(f)
    except IOError:
        print('linch-pin PinFile not found in ' + work_dir)
        sys.exit(1)
    # We must find a topology section named 'cinch' to determine where our
    # inventory file will live
    try:
        cinch_topology = 'cinch'
        topology = pin_file_yaml[cinch_topology]['topology']
    except KeyError:
        print('linch-pin PinFile must contain a topology '
              'section named "{0}"'.format(cinch_topology))
        sys.exit(1)
    #  The inventory file generated by linchpin that will be used by cinch for
    #  configuration
    try:
        topology_path = os.path.join(work_dir, 'topologies', topology)
        with open(topology_path) as topology_file:
            topology_yaml = yaml.safe_load(topology_file)
        inventory_file = topology_yaml['topology_name'] + '.inventory'
    except (IOError, TypeError):
        print('linch-pin topology file not found or malformed: ' +
              topology_path)
        sys.exit(1)
    return inventory_file


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
