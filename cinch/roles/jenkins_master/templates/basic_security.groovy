import hudson.security.*;

def check_mode = {{ ansible_check_mode|to_json }};

boolean changed = false;
def jenkins = jenkins.model.Jenkins.getActiveInstance();
AuthorizationStrategy strategy = jenkins.getAuthorizationStrategy();
if ( ! ( strategy instanceof AuthorizationStrategy.Unsecured ) ) {
	strategy = new AuthorizationStrategy.Unsecured();
	if ( !check_mode ) jenkins.setAuthorizationStrategy(strategy);
	println "CHANGED: Updated strategy to be unsecured."
	changed = true;
}
if ( ! (jenkins.getSecurityRealm() instanceof HudsonPrivateSecurityRealm) ) {
	HudsonPrivateSecurityRealm realm = new HudsonPrivateSecurityRealm(allowsSignup=false);
	if ( !check_mode ) jenkins.setSecurityRealm(realm);
	println "CHANGED: Updated security realm to be private realm"
	changed = true;
}

if ( !check_mode && changed )
	jenkins.save();
