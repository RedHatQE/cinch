Common Config Options
=====================

All Options
-----------

To get the latest up-to-date list of all availble options in Cinch, consult the
files for each Ansible role in the cinch/roles/<role_name>/defaults/main.yml
files in the code base. Every variable should be documented, along with the
default value given.

Jenkins Plugins
---------------

Cinch configures what has been deemed and tested as a reasonable baseline set
of Jenkins plugins. Typically it will not be necessary to alter or remove
elements from this list. The current list can be found in the file
cinch/files/jenkins-plugin-lists/default.txt. Opening this file will give a
list of plugins, one per line. A specific version of a plugin can be specified
by a line that reads "myplugin==1.2.3" and will install specifically version
1.2.3 of that plugin.

If the set of default plugins is not acceptable to a user, they can override
the list by defining the variable jenkins_plugins in their host or group vars
for a Cinch run to include the items they want. This variable is an array of
strings, each string being the equivalent of one line from the default.txt
file.

If a user only wants to add some plugins that are not present in the default
set, without completely overriding the set, this can be accomplished by adding
entries to jenkins_extra_plugins in the same format as entries in the
jenkins_plugins variable. This allows the user to install more plugins than
the default, without needing to worry about falling out of sync with the
default set of plugins
