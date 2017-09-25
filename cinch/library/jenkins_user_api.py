from ansible.module_utils.basic import AnsibleModule
from tempfile import NamedTemporaryFile
import subprocess
import os


# Due to the nature of Ansible modules, this string cannot reasonably be
# handled outside of this file. Ansible modules must be self-contained single
# file scripts that can be uploaded as a unit. In this case, we need to drop
# this Groovy script into a temporary file to execute with the Jenkins CLI
# command
MYFILE = """
import hudson.model.User;
User u = User.get("{0}");
def p = u.getProperty(jenkins.security.ApiTokenProperty.class);
println p.getApiToken();
"""


def main():
    """
    Write out a groovy file that can be executed by the jenkins-cli.jar command
    which will print out the value of a specified user's API key. Currently the
    name of the user is not sanitized in any manner, so a value that includes
    Groovy escape characters or the double quote character (e.g. if the name
    includes the backslash character (\\) or the quotation mark character ("),
    or something else strange like a tab, newline, null, etc) then it will
    cause a problem with the Groovy code. Such usernames are generally not
    permissible in systems like Jenkins. If they are used, then the provider
    should escape those characters when they are passed into this module."""
    module = AnsibleModule(
        argument_spec={
            'user': {'required': True, 'type': 'str'},
            'cli_jar': {'default':
                        '/var/cache/jenkins/war/WEB-INF/jenkins-cli.jar'},
            'jenkins_url': {'default': 'http://localhost:8080'},
            'remoting': {'required': True, 'type': 'bool'},
            'java_command': {'type': 'str', 'default': '/usr/bin/java'}
        }
    )
    # Permits accessing args as object instead of dict
    args = type('Args', (object,), module.params)
    # Create a temporary place to put the Groovy code. False on the automatic
    # delete option, otherwise the call to the file .close() method would cause
    # it to be deleted, whereas we want the file to persist until after the
    # command is executed
    groovy = NamedTemporaryFile(delete=False)
    groovy.write(MYFILE.format(args.user))
    groovy.close()
    process_named_args = [args.java_command,
                          '-jar',
                          args.cli_jar,
                          '-s',
                          args.jenkins_url]
    # Append -remoting argument to named argument list depending on the version
    # of Jenkins
    if args.remoting:
        process_named_args.append('-remoting')
    process_positional_args = ['groovy', groovy.name]
    process = process_named_args + process_positional_args
    # The groovy code simply prints out the value of the API key, so we want
    # to be able to capture that output
    err, output = None, None
    p = subprocess.Popen(process,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    try:
        output, err = p.communicate()
        os.unlink(groovy.name)
        # It's possible the Popen process has an error code for a whole host of
        # reasons
        if p.returncode == 0:
            module.exit_json(api_key=output.strip(),
                             err=err,
                             changed=False,
                             success=True)
        else:
            msg = "Error occurred while executing jenkins-cli.jar"
    except subprocess.CalledProcessError:
        msg = "Error received while attempting to execute Java"
        # If err and output are some type of empty, but not the empty string,
        # then we reached this point without any output. If they are the empty
        # string, then we reached this point but the subprocess output nothing
        # on the specified pipe. Providing this data, or a status message such
        # as these defaults, provides a better way for users to diagnose the
        # problems encountered
        if not err and err != "":
            err = "No stderr detected"
        if not output and output != "":
            output = "No stdout detected"
    # There are lots of reasons to fall through to here. But if we have, then
    # something has most definitely gone wrong. We should report on that
    module.fail_json(msg=msg,
                     stderr=err,
                     stdout=output,
                     api_key='')


main()
