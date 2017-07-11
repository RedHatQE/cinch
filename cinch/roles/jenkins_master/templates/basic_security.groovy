import hudson.security.*;

boolean changed = false;
def jenkins = jenkins.model.Jenkins.getActiveInstance();
AuthorizationStrategy strategy = jenkins.getAuthorizationStrategy();
if ( ! ( strategy instanceof AuthorizationStrategy.Unsecured ) ) {
	strategy = new AuthorizationStrategy.Unsecured();
	jenkins.setAuthorizationStrategy(strategy);
	println "CHANGED: Updated strategy to be unsecred."
	changed = true;
}
if ( ! (jenkins.getSecurityRealm() instanceof HudsonPrivateSecurityRealm) ) {
	HudsonPrivateSecurityRealm realm = new HudsonPrivateSecurityRealm(allowsSignup=false);
	jenkins.setSecurityRealm(realm);
	println "CHANGED: Updated security realm to be private realm"
	changed = true;
}

def check_mode = {{ ansible_check_mode|to_json }};

if ( check_mode && changed )
	jenkins.save();
