Development
===========

Environments
------------

Development occurs targeting each of the specific host environments that are
supported. The default development environment and targeted host is the latest
version of CentOS.

The fastest way to get yourself up and running is to leverage the Vagrant
machines held within the top-level vagrant folder. These are named according to
the roles that each one is designed to exercise.

Install
-------

To run the software locally, you need a few basic pieces of software installed.
The following packages for Fedora need to be installed, minimally, or the
equivalent packages for your distribution:

-  python-virtualenv
-  gcc
-  redhat-rpm-config
-  openssl-devel
-  libvirt-devel
-  libyaml-devel
-  vagrant

The only software actually required to run the playbooks is Ansible and its
dependencies. The other packages listed above are required only to install and
build Ansible and its dependencies, such as PyYAML. Thus, if you are looking
to package Cinch for a new distribution, the above packages, less vagrant,
are a good starting place for build dependencies.

If installing manually, you can activate your Python virtualenv of choice and
issue the command ``pip install /path/to/cinch``. As a developer, if you plan to make
changes to Cinch, then use pip in the local editable mode by issuing the
command ``pip install -e /path/to/cinch`` instead.

Execution
---------

Once all of these depenencies are fulfilled, there are a number of folders
under the top level vagrant/ directory that contain minimally a Vagrantfile.
The Vagrantfile can be used to issue the command "vagrant up"
from within that directory to spin up a collection of machines, against which
the cinch playbooks will be automatically executed. Consult the README in each
directory for more information about which machines will be created out of
that directory, and for any information that the user might need to supply.

Some of the Vagrantfile values will need to be supplied by the user,
specifically any values related to RHEL repository URLs as there is no public
version of those repositories available. Other values should all be provided
from within those directories already.

Merely issuing the command ``vagrant up`` should bring up the VMs for each
environment you configure. For the most part, it should be possible to run
each environment on your local system, but there is the potential that having
multiple environments running at the same time on the same host could result
in collissions between the IP addresses of the hosts. It certainly would lead
to provided URLs in the README files being incorrect.
