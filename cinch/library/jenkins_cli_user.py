#!/usr/bin/env python
#
# Author: Greg Hellings - <ghelling@redhat.com> or <greg.hellings@gmail.com>
#
# Module to configure users in Jenkins authorized to use CLI
import xml.etree.ElementTree as ET
import os
from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = '''
---
version_added: "2.1"
module: jenkins_cli_user
short_description: configure Jenkins CLI users with pub key
description:
  - This module configures admin users in Jenkins to utilize the specified
    SSH pubkey. Requires that role-based authentication be enabled and that
    a user be configured as an admin

options:
  jenkins_home:
    description:
     The root directory for the Jenkins install
    required: true
  jenkins_user:
    description:
      The name of the user to configure the SSH key for
  key_file:
    description:
      Path to the SSH keyfile to be listed as authorized
    required: true
  state:
    description:
      Currently limited to "present" - will create the user
    required: false

author: Gregory Hellings
'''


def main():
    module = AnsibleModule(
        argument_spec={
            'jenkins_home': {'required': True},
            'jenkins_user': {'required': True},
            'key_file': {'required': True},
            'state': {'choices': ['present'], 'default': 'present'}
        },
        supports_check_mode=False
    )
    params = type('Params', (object,), module.params)
    user_config_path = os.path.join(params.jenkins_home, "users")
    changed = False
    # This is the local SSH key file to read and enter into the Jenkins config
    # for the desginated user
    with open(params.key_file) as key:
        pub_key = key.read()
        user_cfg_file = os.path.join(user_config_path, params.jenkins_user,
                                     "config.xml")
        # Parsing the XML structure of the per-user configuration file, in
        # order to add the SSH keys
        usertree = ET.parse(user_cfg_file)
        userroot = usertree.getroot()
        keyroot = userroot.find("properties")
        keys = keyroot.getiterator("authorizedKeys")
        if keys:
            for key in keys:
                # The value of key.text is the appended public SSH keys that
                # should be usable by this character, separated each by a \n
                # character. Very much like an authoritzed_keys file for SSH
                # access. If this key is not a substring of the whole set of
                # ahtorized keys, then we append it to the list of keys and set
                # changed to true
                if pub_key not in str(key.text):
                    changed = True
                    if key.text is None:
                        key.text = pub_key
                    else:
                        key.text = str(key.text) + pub_key
        else:
            # No authorized keys have been added to the user hitherto, and even
            # the XML structure that holds the set of authorized keys is not
            # present, so we must create the XML structure to hold the
            # requested key. In this case, the module is definitely making a
            # change to the files
            changed = True
            prop = userroot.find("properties")
            ssh_auth = ET.SubElement(prop,
                                     "org.jenkinsci.main.modules"
                                     ".cli.auth.ssh."
                                     "UserPropertyImpl")
            auth_key = ET.SubElement(ssh_auth, "authorizedKeys")
            auth_key.text = pub_key
        if changed:
            usertree.write(user_cfg_file, encoding="UTF-8")
        module.exit_json(changed=changed)
    # This code should only be accessed if there was an exception within the
    # "with" block that prevents the module.exit_json line above from being
    # properly executed. Then this will return an error to the user, rather
    # than leaving them completely hanging.
    module.fail_json(msg="Roles not found - have you configured an admin "
                     "using the Role-based Authorization Strategy?")


main()
