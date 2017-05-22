// http://javadoc.jenkins-ci.org/jenkins/model/DownloadSettings.html

import jenkins.model.Jenkins
def jenkins = Jenkins.instance

def ds = jenkins.getExtensionList(jenkins.model.DownloadSettings.class)[0]
def usebrowser = ds.isUseBrowser()

// Ansible+Jinja makes the boolean value from the template into leading
// uppercase, which is not valid in Groovy.  We use |to_json to ensure that the
// boolean value is lowercase.
def jenkins_usebrowser = {{ jenkins_usebrowser|to_json }}

if (usebrowser != jenkins_usebrowser) {
    ds.setUseBrowser(jenkins_usebrowser)
    jenkins.save()
    println "CHANGED: setUseBrowser from " + usebrowser + " to " + \
        jenkins_usebrowser
} else {
    println "No changes to setUseBrowser necessary"
}
