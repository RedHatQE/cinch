from ansible.module_utils.basic import AnsibleModule
from tempfile import NamedTemporaryFile
import subprocess
import os


MYFILE = """
import hudson.model.User;
User u = User.get("{0}");
def p = u.getProperty(jenkins.security.ApiTokenProperty.class);
println p.getApiToken();
"""


def main():
    module = AnsibleModule(
        argument_spec={
            'user': {'required': True, 'type': 'str'},
            'cli_jar': {'default':
                        '/var/cache/jenkins/war/WEB-INF/jenkins-cli.jar'},
            'jenkins_url': {'default': 'http://localhost:8080'}
        }
    )
    args = type('Args', (object,), module.params)
    groovy = NamedTemporaryFile(delete=False)
    groovy.write(MYFILE.format(args.user))
    groovy.close()
    process = ['/usr/bin/java',
               '-jar',
               args.cli_jar,
               '-s',
               args.jenkins_url,
               'groovy',
               groovy.name]
    p = subprocess.Popen(process,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate()
    os.unlink(groovy.name)
    success = False
    if p.returncode == 0:
        success = True
    module.exit_json(api_key=output.strip(),
                     err=err,
                     changed=False,
                     success=success)


main()
