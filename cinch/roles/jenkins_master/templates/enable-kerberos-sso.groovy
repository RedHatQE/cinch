boolean check_mode = {{ ansible_check_mode|to_json }}
boolean anonymous_access = {{ jenkins_kerberos_anonymous_access|to_json }}

def plugin = com.sonymobile.jenkins.plugins.kerberossso.PluginImpl.getInstance()

// TODO: Since kerberos-sso 1.4 there is no need to use the private field
// accessor ('@') for any of the fields.

if (!plugin.@enabled) {
  if (!check_mode) plugin.@enabled = true
  println "Enabling Kerberos SSO"
}

// Need this to prevent a NPE on startup
if (!check_mode) plugin.@password = hudson.util.Secret.fromString("changeme")
println "Setting dummy password"

if (plugin.@allowLocalhost) {
  if (!check_mode) plugin.@allowLocalhost = false
  println "Disabling auto-login from localhost"
}

if (plugin.@allowUnsecureBasic) {
  if (!check_mode) plugin.@allowUnsecureBasic = false
  println "Disabling unsecured Basic Authentication"
}

if (plugin.@anonymousAccess != anonymous_access) {
  if (!check_mode) plugin.@anonymousAccess = anonymous_access;
  println "${anonymous_access ? "Enabling" : "Disabling"} anonymous access"
}

if (!check_mode) plugin.save()
