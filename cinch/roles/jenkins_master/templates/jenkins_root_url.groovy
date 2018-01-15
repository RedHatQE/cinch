import jenkins.model.JenkinsLocationConfiguration;
import org.apache.commons.lang3.StringUtils;

String newUrl = "{{ _jenkins_url }}";
boolean changed = false;
def jlc = JenkinsLocationConfiguration.get()
def check_mode = {{ ansible_check_mode|to_json }};
String oldUrl = StringUtils.stripEnd(jlc.getUrl(), "/");

if( !oldUrl.equals(newUrl) ) {
	if ( !check_mode ) jlc.setUrl(newUrl);
	print "CHANGED: Updated base URL to " + newUrl;
	changed = true;
}

if( !check_mode && changed )
	jlc.save();
