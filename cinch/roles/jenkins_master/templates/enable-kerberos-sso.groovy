def plugin = com.sonymobile.jenkins.plugins.kerberossso.PluginImpl.getInstance()
// Enable SSO
def f = plugin.getClass().getDeclaredField("enabled");
f.setAccessible(true);
println(f.get(plugin))
f.set(plugin, true);
// Need this to prevent a NPE on startup
def p = plugin.getClass().getDeclaredField("password");
p.setAccessible(true);
println(p.get(plugin))
p.set(plugin, hudson.util.Secret.fromString("changeme"));
// Disable localhost
def l = plugin.getClass().getDeclaredField("allowLocalhost");
l.setAccessible(true);
l.set(plugin, false);
// Disable unsecured Basic
def usb = plugin.getClass().getDeclaredField("allowUnsecureBasic");
usb.setAccessible(true);
usb.set(plugin, false);
// Save
plugin.save()
