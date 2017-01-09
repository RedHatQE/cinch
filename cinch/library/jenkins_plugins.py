#!/usr/bin/env python

from subprocess import Popen, PIPE
from ansible.module_utils.basic import AnsibleModule
from os import path


# Default values, just to create globals, these values are overridden elsewhere
jar_file = path.expanduser("~/jenkins-cli.jar")
server = "http://localhost:8080"
validate_certs = True


def set_globals(args):
    global jar_file
    global server
    global validate_certs
    jar_file = path.join(path.expanduser(args.working_dir), 'jenkins-cli.jar')
    if args.use_ssl:
        protocol = "https"
    else:
        protocol = "http"
    server = "{0}://{1}{2}".format(protocol, args.server, args.server_path)
    validate_certs = args.validate_certs


def run_jenkins_cli(command, *args):
    """
    Runs an arbitrary Jenkins CLI command

    :returns (out, err) The stdout and stderr of the process
    """
    base_args = ['java', '-jar', jar_file, '-s', server]
    if not validate_certs:
        base_args.append('-noCertificateCheck')
    base_args.append(command)
    base_args.extend(args)
    command = Popen(base_args, stdout=PIPE, stderr=PIPE)
    out, err = command.communicate()
    if command.returncode != 0:
        raise Exception(out + err)
    return out, err


def install_plugin(*plugins):
    """
    Installs the specified plugin
    """
    run_jenkins_cli('install-plugin', *plugins)


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
    module = AnsibleModule(
        argument_spec={
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
        module.fail_json(msg='You must download the jenkins-cli.jar file to '
                             'the specified working_dir path')
    # Default initialized values
    changed = False
    unchanged = set()
    installed = set()
    to_install = set(args.plugins)
    tries = 0
    # Give three tries, because randomly Jenkins only installs some plugins
    while len(to_install) > 0 and tries < 3:
        # Fetch list of current plugins
        current_plugins = set(get_plugin_list())
        # Construct list of plugins not yet installed
        to_install -= current_plugins
        if len(to_install) == 0:
            break
        # If we reach here even once, we're going to be changing system state
        changed = True
        install_plugin(*to_install)
        # Keep a set of plugins that were actually installed
        installed |= to_install
        tries += 1
    unchanged = set(args.plugins) - installed
    module.exit_json(changed=changed,
                     installed=list(installed),
                     unchanged=list(unchanged),
                     tries=tries)


main()
