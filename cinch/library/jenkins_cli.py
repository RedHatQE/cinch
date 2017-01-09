#!/bin/bash

from shlex import split
from subprocess import Popen, PIPE
from ansible.module_utils.basic import AnsibleModule
from os import path


def main():
    module = AnsibleModule(
        argument_spec={
            'command': {'required': True},
            'arguments': {'default': ''},
            'working_dir': {'default': '~/'},
            'use_ssl': {'type': 'bool', 'default': True},
            'validate_certs': {'type': 'bool', 'default': True},
            'server': {'default': 'localhost'},
            'server_path': {'default': '/'}
        }
    )
    params = type('Params', (object,), module.params)
    jar = path.join(path.expanduser(module.params['working_dir']),
                    'jenkins-cli.jar')
    # Check JAR exists before proceeding
    if not path.exists(jar):
        module.fail_json(msg='jenkins-cli.jar not found in specified '
                         'working_dir: {0}'.format(params.working_dir))
    # Construct arguments
    arguments = ['java', '-jar', jar]
    # Constrcut server URL to hit
    if params.use_ssl:
        protocol = 'https'
    else:
        protocol = 'http'
    server = '{0}://{1}{2}'.format(protocol, params.server, params.server_path)
    arguments.extend(['-s', server])
    # validate SSL certificates, if necessary
    if not module.params['validate_certs']:
        arguments.append('-noCertificateCheck')
    # add user arguments
    arguments.append(params.command)
    arguments.extend(split(params.arguments))
    # Execute command
    command = Popen(arguments, stdout=PIPE, stderr=PIPE)
    out, err = command.communicate()
    if command.returncode != 0:
        message = 'Command failed. Return code was ' + \
                  '{0}'.format(command.returncode)
        module.fail_json(msg=message,
                         returncode=command.returncode,
                         stdout=out,
                         stderr=err)
    else:
        module.exit_json(changed=True, stdout=out, stderr=err)


main()
