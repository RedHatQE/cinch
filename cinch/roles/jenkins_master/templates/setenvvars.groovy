import jenkins.*;
import jenkins.model.*;
import hudson.*;
import hudson.model.*;
import hudson.slaves.*;

def j = Jenkins.getActiveInstance();
def globalNodes = j.getGlobalNodeProperties().getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class);
boolean isEmptyNode = (globalNodes.size() == 0);
def check_mode = {{ ansible_check_mode|to_json }};

{% for var in jenkins_envvars %}
if (isEmptyNode) {
  if ( !check_mode )
    j.globalNodeProperties.replaceBy([new EnvironmentVariablesNodeProperty()]);
  isEmptyNode = false;
}

if ( !check_mode )
  j.globalNodeProperties.get(0).getEnvVars().put("{{ var.key }}", "{{ var.value }}");
println "Adding environment variable {{ var.key }}={{ var.value }}";

{% endfor %}

if ( !check_mode )
  j.save();
