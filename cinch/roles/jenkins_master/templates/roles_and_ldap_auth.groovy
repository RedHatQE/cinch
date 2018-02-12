import hudson.*;
import hudson.model.*;
import hudson.security.*;
import hudson.util.Secret;
import jenkins.*;
import jenkins.model.*;
import java.util.*;
import com.michelin.cio.hudson.plugins.rolestrategy.*;
import java.lang.reflect.*;
import jenkins.security.plugins.ldap.LDAPGroupMembershipStrategy;
import jenkins.security.plugins.ldap.FromGroupSearchLDAPGroupMembershipStrategy;

// Some Java/Groovy reflection magic to make sure we can access the portions of the
// scripts that are needed for sanity's sake
Constructor[] constructors = Role.class.getConstructors();
for ( Constructor<?> c : constructors ) {
	c.setAccessible(true);
}
Method assignRoleMethod = RoleBasedAuthorizationStrategy.class.getDeclaredMethod("assignRole",
                                                                                 String.class,
                                                                                 Role.class,
                                                                                 String.class);
assignRoleMethod.setAccessible(true);
Method getRoleMapMethod = RoleBasedAuthorizationStrategy.class.getDeclaredMethod("getRoleMap",
                                                                                 String.class);
getRoleMapMethod.setAccessible(true);

// *************************************************************************
// The real magic begins here
// *************************************************************************
def instance = Jenkins.getInstance();
def strategy = Hudson.instance.getAuthorizationStrategy();
boolean changed = false;

/**
 * Creates a role with the specified name and permissions within the provided
 * strategy.
 *
 * If there is already a role of that name, then the existing role
 * will be updated so its permissions match the given set. Will set the global
 * "changed" variable to "true" when it changes something.
 */
def Role createRole(String roleName,
                    Set<Permission> permissions,
                    RoleBasedAuthorizationStrategy strategy) {
	// First, check if role exists
	RoleMap map = strategy.getRoleMap(RoleBasedAuthorizationStrategy.GLOBAL);
	Role role = map.getRole(roleName);
	if (role == null) {
		role = new Role(roleName, permissions);
		strategy.addRole(RoleBasedAuthorizationStrategy.GLOBAL, role);
		println "CHANGED: Added role '" + roleName + "'";
		changed = true;
	} else {
		// Make sure the permissions are in line
		Set<Permission> currentPermissions = role.getPermissions();
		// First, insert any that are missing
		for ( Permission permission : permissions ) {
			if ( !currentPermissions.contains( permission ) ) {
				currentPermissions.add( permission );
				println "CHANGED: Added permission '" + permission.getId() +
				        "' to role '" + role.getName() + "'";
				changed = true;
			}
		}
		// Remove extraneous ones
		for ( Permission permission : currentPermissions ) {
			if ( !permissions.contains(permission) ) {
				currentPermissions.remove( permission );
				println "CHANGED: Removed permission '" + permission.getId() +
				        "' from role '" + role.getName() + "'";
				changed = true;
			}
		}
	}
	return role;
}

// Ensure that the system is using a RoleBasedAuthorizationStrategy
if( ! (strategy instanceof RoleBasedAuthorizationStrategy) ) {
	println "CHANGED: Created RoleBasedAuthorizationStrategy";
	strategy = new RoleBasedAuthorizationStrategy();
	instance.setAuthorizationStrategy(strategy);
	changed = true;
}

// Create the permissions for each role
Set<Permission> rolePermissions;
Role createdRole;

// Special treatment is given to the "admin" role.
rolePermissions = new HashSet<Permission>();
ArrayList<PermissionGroup> groups = new ArrayList<PermissionGroup>(PermissionGroup.getAll());
groups.remove(PermissionGroup.get(Permission.class));
for ( PermissionGroup group : groups ) {
	for ( Permission permission : group ) {
		rolePermissions.add(permission);
	}
}
createdRole = createRole("admin", rolePermissions, strategy);
strategy.assignRole(strategy.GLOBAL, createdRole, "{{ jenkins_admin.nickname }}");
{% for sid in jenkins_admin_sids %}
	strategy.assignRole(strategy.GLOBAL, createdRole, "{{ sid }}");
{% endfor %}

// Create the user-defined roles that are desired
{% for role in (jenkins_security_roles + jenkins_security_extra_roles) %}
	rolePermissions = new HashSet<Permission>();
	{% for permission in role.permissions %}
		rolePermissions.add(Permission.fromId("{{ permission }}"));
	{% endfor %}
	createdRole = createRole("{{ role.name }}", rolePermissions, strategy);
	{% for sid in role.sids %}
		strategy.assignRole(strategy.GLOBAL, createdRole, "{{ sid }}");
	{% endfor %}
{% endfor %}

/** **************************************************************************
 * Configure LDAP security in the same script, so that we don't have problems
 * with authentication after this fact.
 ** **************************************************************************
 */
def securityRealm = instance.getSecurityRealm();
LDAPSecurityRealm ldap;
// Arguments
String server = "{{ jenkins_ldap.server }}";
String rootDN = "{{ jenkins_ldap.root_dn }}";
String userSearchBase = "{{ jenkins_ldap.user_search_base | default('') }}";
String userSearch = "{{ jenkins_ldap.user_search }}";
String groupSearchBase = "{{ jenkins_ldap.group_search_base }}";
String groupSearchFilter = "{{ jenkins_ldap.group_search_filter }}";
LDAPGroupMembershipStrategy groupMembership =
    new FromGroupSearchLDAPGroupMembershipStrategy("{{ jenkins_ldap.group_membership }}");
String managerDN = "{{ jenkins_ldap.manager_dn | default('') }}";
Secret managerPassword = Secret.fromString("{{ jenkins_ldap.manager_password | default('') }}");
String displayNameAttr = "{{ jenkins_ldap.display_name_attr }}";
String emailAddrAttr = "{{ jenkins_ldap.email_addr_attr }}";
// Check that LDAP is even configured
try {
	ldap = (LDAPSecurityRealm) securityRealm;
} catch(ClassCastException cce) {
	ldap = null;
}
// Check that LDAP settings are correct
if ( ldap == null ||
     !ldap.server.equals(server) ||
     !ldap.rootDN.equals(rootDN) ||
     !ldap.userSearchBase.equals(userSearchBase) ||
     !ldap.userSearch.equals(userSearch) ||
     !ldap.groupSearchBase.equals(groupSearchBase) ||
     !ldap.groupSearchFilter.equals(groupSearchFilter) ||
     !ldap.groupMembershipStrategy.getFilter().equals(groupMembership) ||
     !ldap.groupSearch.equals(groupSearch) ||
     !ldap.managerDN.equals(managerDN) ||
     !ldap.managerPassword.equals(managerPassword) ||
     !ldap.displayNameAttributeName.equals(displayNameAttr) ||
     !ldap.mailAddressAttributeName.equals(emailAddrAttr)
   ) {
	ldap = new LDAPSecurityRealm(server,
	                             rootDN,
	                             userSearchBase,
	                             userSearch,
	                             groupSearchBase,
	                             groupSearchFilter,
	                             groupMembership,
	                             managerDN,
	                             managerPassword,
	                             false, // inhibitInferRootDN
	                             false, // disableMailAddressResolver
	                             null, // config cache
	                             null, // environment properties
	                             displayNameAttr,
	                             emailAddrAttr,
	                             null, // userIdStrategy
	                             null); // groupIdStrategy
	println "CHANGED: Updated security realm to LDAP"
	instance.setSecurityRealm(ldap);
	changed = true;
} else {
	println "No changes to LDAP necessary"
}

if ( changed )
	instance.save();
