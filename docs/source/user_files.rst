User Files
==========

Motivation
----------

Anyone using Cinch to provision either a Jenkins master os slave may have the
need to perform configuration to the system that exceeds the ability of Cinch to
reasonably include support for within these playbooks. These could cover nearly
any aspect of system administration, monitoring, configuration, and setup. For
such a case, it is recommended that the user leverage the ability of Ansible to
file a host into multiple different inventory groups, and private configuration
be stored in private playbooks. Then those playbooks can be executed either
before or after (or both) the Cinch playbooks are executed.

However, there are a few basic system administration tasks that are general
enough, and simple enough, that Cinch has opted to support those features to
assist in the configuration of a Jenkins master. In addition to supporting
the ability to setup Yum/DNF repositories during configuration and configure
certificate authority chains, both of which are important to installing the
packages required by Cinch and to configure SSL options for Jenkins, another
feature supported by Cinch is the ability to upload arbitrary files from the
local system where Ansible is being hosted to the remote system being
configured.

Mechanisms
----------

Each Ansible host, or group, can have defined values of files to upload to the
remote hosts. These uploads happen at two different points during the execution
of Cinch. The first set of uploads occurs before any Cinch plays have been
executed except for verifying the host is reachable. This means that none of
the Cinch-related configurations will be available during this upload run,
unless they have previously been configured. This includes things like the
"jenkins" system user, configured repositories, certificate authorities, etc.
The second run happens at the very end - after both the master and any slaves
have been configured and are up and running. However, at this point, all such
configurations, users, etc are already present on the system.

Thus, it is important to realize a file cannot be uploaded to be owned by the
Jenkins user before the Jenkins user is created. If it is necessary to upload
a file as that user before the Jenkins service starts on a configured host,
then it will be necessary to use external playbooks or other methods to ensure
proper behavior.

Configuration
-------------

Configuring uploads either before or after a Cinch run is straightforward.
Simply override the values of the arrays "pre_upload_files" and
"post_upload_files" in the Ansible host or group configurations for all hosts
that require such a feature.

These arrays require identical structures. Each element in the array should
be an object hash with certain values defined. Those values are listed below:

==========  ===============
value       required?
==========  ===============
src         yes
dest        yes
owner       no
group       no
mode        no
==========  ===============

Example:

.. code:: yaml

    pre_upload_files:
      - src: /home/deployuser/somehost/ssl.key
        dest: /etc/apache2/ssl/ssl.key
        mode: 0600
    post_upload_files:
      - src: /home/deployuser/somehost/ssh
        dest: /var/lib/jenkins/.ssh
        owner: jenkins
        mode: 0600

Each of these values is passed directly into the Ansible module called
`copy <http://docs.ansible.com/ansible/copy_module.html>`_. Refer to that
module's documentation for information about the structure and values that
are permitted to be passed into these values. Note, especially, that this
module can be used to upload whole directories in addition to individual files.

If the need arises to support more of the options of that module, adding that
support to Cinch can be done. Please just open an issue in the `GitHub Issue
Tracker <https://github.com/RedHatQE/cinch/issues>`_ detailing the requested
functionality.
