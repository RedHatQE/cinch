#!/usr/bin/env python

from subprocess import Popen, PIPE
from ansible.module_utils.basic import *
from os import path


# Default values, just to create globals, these values are overridden elsewhere
jar_file = path.expanduser("~/jenkins-cli.jar")
server = "http://localhost:8080"


def set_globals(args):
    global jar_file
    global server
    jar_file = path.join(path.expanduser(args.working_dir), 'jenkins-cli.jar') 
    if args.use_ssl:
        protocol = "https"
    else:
        protocol = "http"
    server = "{0}://{1}{2}".format(protocol, args.server, args.server_path)


def run_jenkins_cli(command, *args):
    """
    Runs an arbitrary Jenkins CLI command

    :returns (out, err) The stdout and stderr of the process
    """
    base_args = ['java', '-jar', jar_file, '-s', server]
    base_args.append(command)
    base_args.extend(args)
    command = Popen(base_args, stdout=PIPE, stderr=PIPE)
    out, err = command.communicate()
    return out, err


def install_plugin(plugin):
    """
    Installs the specified plugin
    """
    run_jenkins_cli('install-plugin', plugin)


def get_plugin_list():
    """
    Checks the selected server to determine if this plugin is already installed
    """
    out, err = run_jenkins_cli('list-plugins')
    lines = out.split('\n')
    plugins = []
    for line in lines:
        parts = line.split(' ')
        plugins.append(parts[0])
    return plugins


def main():
    global jar_file
    global server
    module = AnsibleModule(
        argument_spec = {
            'plugins': {'type': 'list'},
            'working_dir': {'default': '~/'},
            'use_ssl': {'type': 'bool', 'default': True},
            'validate_certs': {'type': 'bool', 'default': True},
            'server': {'default': 'localhost'},
            'server_path': {'default': '/'}
        }
    )
    args = type('Args', (object,), module.params)
    set_globals(args)
    # Basic sanity, to ensure the jar file is present
    if not path.exists(jar_file):
        module.fail_json(msg='You must download the jenkins-cli.jar file to the specified working_dir path')
    changed = False
    plugins = get_plugin_list()
    unchanged = []
    installed = []
    for plugin in args.plugins:
        if plugin not in plugins:
            install_plugin(plugin)
            changed = True
            installed.append(plugin)
        else:
            unchanged.append(plugin)
    module.exit_json(changed=changed, installed=installed, unchanged=unchanged)


main()
