Development
===========

ENVIRONMENTS
============

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
dependencies. To install the versions that have been tested as working with
this system, use the requirements.txt file in the top of the project to install
all the necessary software into a Python virtualenv. Alternatively, invoke the
script bin/ensure\_virtualenv.sh to install the Python dependencies into the
folder .venv/

If installing manually, you can activate your Python virtualenv of choice and
issue the command ``pip install -r requirements.txt``

Execution
---------

Once all of these depenencies are fulfilled, there are a number of folders
under the top level vagrant/ directory that contain minimally a Vagrantfile and
a hosts file. The Vagrantfile can be used to issue the command "vagrant up"
from within that directory to spin up a collection of machines, and the hosts
file can be used as the inventory input for running the Ansible playbooks
against the spun up Vagrant VMs.

Inside of each of those folders should also be a pair of shell scripts. These
scripts are named "full\_cycle.sh" and the other "configure.sh".
full\_cycle.sh will execute a ``vagrant destroy -f && vagrant up`` followed by
invoking the same commands that configure.sh invokes. configure.sh will ensure
a virtualenv has been created and the requirements.txt file has been installed
to that environment. It will then execute ansible-playbook from that virtualenv
against the hosts inventory file in the folder.

Customization
-------------

Both configure.sh and full\_cycle.sh will pass any arguments they receive,
unaltered, through to the ansible-playbook invocation at the end of the command
line. Thus, if any extra arguments need to be appended to the ansible-playbook
invocation, for instance passing in command-line variable overrides or setting
verbose flags, they can be added to the end of the invocation for the shell
script.
