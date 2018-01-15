def check_mode = {{ ansible_check_mode|to_json }}

def plugin = com.sonymobile.jenkins.plugins.kerberossso.PluginImpl.getInstance()

if (!plugin.@enabled) {
  if (!check_mode) plugin.@enabled = true
  println "Enabling Kerberos SSO"
}

// Need this to prevent a NPE on startup
if (!check_mode)  plugin.@password = hudson.util.Secret.fromString("changeme")
println "Setting dummy password"

if (plugin.@allowLocalhost) {
  if (!check_mode)  plugin.@allowLocalhost = false
  println "Disabling auto-login from localhost"
}

if (plugin.@allowUnsecureBasic) {
  if (!check_mode) plugin.@allowUnsecureBasic = false
  println "Disabling unsecured Basic Authentication"
}

if (!check_mode) plugin.save()
