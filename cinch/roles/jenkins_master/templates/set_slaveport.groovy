import jenkins.model.Jenkins
def jenkins = Jenkins.instance
// Ansible+Jinja makes the boolean value from the template into leading
// uppercase, which is not valid in Groovy.  We use |to_json to ensure that the
// boolean value is lowercase.
def check_mode = {{ ansible_check_mode|to_json }}

def slave_agent_port = jenkins.getSlaveAgentPort()
int jenkins_slave_agent_port = {{ jenkins_slave_agent_port|int }}

def change_msg = "CHANGED: slave agent port from " + slave_agent_port +
    " to " + jenkins_slave_agent_port

if (slave_agent_port != jenkins_slave_agent_port) {
    if (check_mode) {
        println change_msg
    } else {
        jenkins.setSlaveAgentPort(jenkins_slave_agent_port)
        jenkins.save()
        println change_msg
    }
} else {
    println "No changes to slave agent port necessary"
}
