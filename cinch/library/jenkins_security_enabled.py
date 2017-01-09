#!/usr/bin/env python

import os
from ansible.module_utils.basic import AnsibleModule


def exit_json(module, enabled=False):
    facts = {'jenkins_security_enabled': enabled}
    module.exit_json(changed=False, ansible_facts=facts)


def main():
    module = AnsibleModule(
        argument_spec={
            'jenkins_home': {'required': True}
        }
    )
    jenkins_cfg = os.path.join(module.params['jenkins_home'], 'config.xml')
    # By default, auth will be created. If there is no config.xml, then a new
    # one will be created and will set this to true
    if not os.path.exists(jenkins_cfg):
        exit_json(module)
    # If there is a file, then query it
    with open(jenkins_cfg, 'r') as cfg:
        for line in cfg.readlines():
            # This text in a file means that security is not configured
            if "AuthorizationStrategy$Unsecured" in line:
                exit_json(module)
    # Default assumption is that we do want security
    exit_json(module, True)


main()
