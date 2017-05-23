import jenkins.model.Jenkins
def jenkins = Jenkins.instance

def executors = jenkins.getNumExecutors()
int jenkins_executors = {{ jenkins_executors|int }}

if (executors != jenkins_executors) {
    jenkins.setNumExecutors(jenkins_executors)
    jenkins.save()
    println "CHANGED: executors from " + executors + " to " + jenkins_executors
} else {
    println "No changes to executors necessary"
}
