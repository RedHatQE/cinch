import jenkins.model.Jenkins
def jenkins = Jenkins.instance
// Ansible+Jinja makes the boolean value from the template into leading
// uppercase, which is not valid in Groovy.  We use |to_json to ensure that the
// boolean value is lowercase.
def check_mode = {{ ansible_check_mode|to_json }}

def executors = jenkins.getNumExecutors()
int jenkins_executors = {{ jenkins_executors|int }}

def change_msg = "CHANGED: executors from " + executors + " to " +
    jenkins_executors

if (executors != jenkins_executors) {
    if (check_mode == true) {
        println change_msg
    } else {
        jenkins.setNumExecutors(jenkins_executors)
        jenkins.save()
        println change_msg
    }
} else {
    println "No changes to executors necessary"
}
