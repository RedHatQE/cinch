import jenkins.model.Jenkins
def jenkins = Jenkins.instance

def slave_agent_port = jenkins.getSlaveAgentPort()
int jenkins_slave_agent_port = {{ jenkins_slave_agent_port|int }}

if (slave_agent_port != jenkins_slave_agent_port) {
    jenkins.setSlaveAgentPort(jenkins_slave_agent_port)
    jenkins.save()
    println "CHANGED: slave agent port from " + slave_agent_port + " to " + \
        jenkins_slave_agent_port
} else {
    println "No changes to slave agent port necessary"
}
