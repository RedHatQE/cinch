// http://javadoc.jenkins-ci.org/jenkins/model/DownloadSettings.html

import jenkins.model.Jenkins
def jenkins = Jenkins.instance
// Ansible+Jinja makes the boolean value from the template into leading
// uppercase, which is not valid in Groovy.  We use |to_json to ensure that the
// boolean value is lowercase.
def check_mode = {{ ansible_check_mode|to_json }}

def ds = jenkins.getExtensionList(jenkins.model.DownloadSettings.class)[0]
def usebrowser = ds.isUseBrowser()
def jenkins_usebrowser = {{ jenkins_usebrowser|to_json }}

def change_msg = "CHANGED: setUseBrowser from " + usebrowser + " to " +
    jenkins_usebrowser

if (usebrowser != jenkins_usebrowser) {
    if (check_mode) {
        println change_msg
    } else {
        ds.setUseBrowser(jenkins_usebrowser)
        jenkins.save()
        println change_msg
    }
} else {
    println "No changes to setUseBrowser necessary"
}
