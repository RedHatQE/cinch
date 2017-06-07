import hudson.model.User;
import hudson.tasks.Mailer.UserProperty;
import hudson.security.HudsonPrivateSecurityRealm;
import hudson.security.HudsonPrivateSecurityRealm.Details;
import org.jenkinsci.main.modules.cli.auth.ssh.UserPropertyImpl;

void createOrUpdateUser(String nick,
                        String email,
                        String password) {
	boolean changed = false;
	User user = User.getById(nick, false);
	// If user is null, then the user does not yet exist
	if ( user == null ) {
		// Synthetic or virtual users are created against this, even if the jenkins
		// is later going to be configured against LDAP or the like
		HudsonPrivateSecurityRealm realm = new HudsonPrivateSecurityRealm(false);
		user = realm.createAccount(nick, password);
		println "CHANGED: Created user " + nick;
		changed = true;
	}

	// Ensure the user's email is set properly
	UserProperty emailProperty = user.getProperty(UserProperty.class);
	if ( emailProperty == null || !emailProperty.getAddress().equals(email) ) {
		emailProperty = new UserProperty(email);
		user.addProperty(emailProperty);
		println "CHANGED: Set " + nick + "'s email to " + email;
		changed = true;
	}

	// Ensure the password is set properly
	Details details = user.getProperty(Details.class);
	if ( details == null || !details.isPasswordCorrect(password) ) {
		details = Details.fromPlainPassword(password);
		user.addProperty(details);
		println "CHANGED: Updated password for " + nick;
		changed = true;
	}

	if ( changed )
		user.save()
}

createOrUpdateUser("{{ jenkins_admin.nickname }}",
                   "{{ jenkins_admin.email }}",
                   "{{ jenkins_admin.password }}");
{% for user in jenkins_local_users %}
createOrUpdateUser("{{ user.nickname }}", "{{ user.email }}", "{{ user.password }}");
{% endfor %}
