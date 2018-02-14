Users
=====

Quick Start
-----------

If you would rather not be bothered with the boring, gritty details, the
following quick steps will get you up and going with a Cinch installation,
after which you can jump down to the section on how to run Cinch, and skip the
installation paragraphs that immediately follow this one.

Fedora 25+
``````````

Execute the following commands

``sudo dnf install -y libvirt-devel python-virtualenv libyaml-devel
openssl-devel libffi-devel gcc redhat-rpm-config``

``virtualenv cinch && source cinch/bin/activate``

``pip install cinch``

RHEL/CentOS
```````````

See the sample  `Ansible playbook
<https://github.com/RedHatQE/cinch/blob/master/cinch/playbooks/install-rhel7.yml>`_
for steps to install Cinch into a virtualenv in RHEL/CentOS, as there are some
additional steps required in these systems.  Running that playbook as-is on
your local system will result in a virtualenv living at
``/var/lib/jenkins/opt/cinch`` that will contain the latest version of Cinch.

Ubuntu
``````

``apt-get install -y libvirt-dev python-virtualenv libyaml-dev openssl
libffi-dev gcc python-dev libssl-dev``

``virtualenv cinch && source cinch/bin/activate``

On older versions of Ubuntu (like 14.04) you should update pip (usually these
older systems come with a version of pip such as 1.5.4 instead of version 9+)

``pip install -U pip``

On all systems, continue on with the installation of Cinch itself

``pip install cinch``

.. note:: After Cinch is installed with the above quick start methods, you can
          jump down to the section about running Cinch to get a look at basic
          documentation on how the software should be used.

Getting Started
---------------

At its core, this software is nothing more than a collection of Ansible
playbook scripts for configuring a system. Any knowledge that you have that is
applicable to the broad spectrum of Ansible usage is applicable here.  You can
opt to install Ansible from your favorite package manager, or you can use the
version that is specified in **setup.py**

Before concluding there is a bug in these playbooks, make sure that the version
of Ansible you are using is the same as the version in the **setup.py**
file and that you have ensured there are no alterations from that version. It
is not intended or guaranteed that any changes from the stock version of
Ansible that has been tested should work.

Requirements
------------

To setup your environment, you need to install Ansible. Since Ansible is
primarily distributed as a Python package, it is suggested that you use **pip**
to install Ansible on your system. You are welcome to try and use the version
that is installed by your favorite package manager, but be sure that you are
using a version at least as new as the version pinned in **setup.py**.

It is recommended that you install Ansible from **pip** using a virtualenv, as
is the best practices recommendations for most Python packages that are
available from PyPI. In order to build and install Ansible, you will need to
install the following system packages:

.. note::  If you install cinch via **pip**, a supported version of Ansible
 will be brought in as a dependency.

-  gcc or appropriate system compiler
-  OpenSSL development package
-  libyaml development package
-  virtualenv package
-  libffi development package
-  libvirt development package

Use your system package manager to install these packages, if they are not
already present.

.. note::  You will need to install the development version of
 the libraries, as **pip** will attempt to build wrappers around some of those
 libraries during its install of Ansible and dependencies.

Here is an example of installing required system level packages for Fedora 25:


Installation
------------

Once the system level packages are installed, you can install cinch using
**pip** (virtualenv strongly recommended):

Fedora
``````

``virtualenv cinch && source cinch/bin/activate``

``pip install cinch``

RHEL7 and CentOS7
`````````````````

RHEL7 and derivatives offer older versions of Python packaging tools that are
incompatible with some cinch dependencies.  To work-around this issue, we have
provided an `Ansible playbook
<https://github.com/RedHatQE/cinch/blob/master/cinch/playbooks/install-rhel7.yml>`_
that will install a newer version of the necessary Python packaging tools to
allow for installation on RHEL7.  This playbook is intended for use on Jenkins
masters and will install cinch and linchpin into a virtualenv at
**/var/lib/jenkins/opt/**.  For convenience, an optional `Jenkins Job
Builder template
<https://github.com/RedHatQE/cinch/blob/master/jjb/install-rhel7.yaml>`_ is
provided and will create a Jenkins job that will run the aforementioned
playbook on your Jenkins master.

Execution
---------

With linchpin
``````````````

If you'd like to automate the process of provisioning a host to later configure
with cinch, the `linchpin project
<https://github.com/CentOS-PaaS-SIG/linchpin>`_ can be used for this task.
linchpin can dynamically generate an Ansible inventory file that cinch can
consume for host configuration.  In the following steps we will outline how to
configure cinch-specific values within a linchpin workspace.

.. note::  For linchpin topology and workspace examples, including various host
           environments, see the `linchpin documentation
           <https://linchpin.readthedocs.io/en/latest/managing_resources.html>`_.

Create a layout file by saving the following example template as
**/path/to/linchpin/workspace/layouts/mylayout.yml** and edit to taste based on
your cinch role requirements.  In this example we configure a RHEL7 Jenkins
slave::

    ---
    inventory_layout:
      hosts:
        cinch-group:
          count: 1
          host_groups:
            - rhel7
            - certificate_authority
            - repositories
            - jenkins_slave

Create an Ansible **group\_vars** file by saving the following example template
as **/path/to/linchpin/workspace/inventories/group_vars/all** and edit to taste
based on your desired configuration parameters.  In this example we configure a
RHEL7 Jenkins slave to attach to a Jenkins master which requires
authentication, along with some installed certificate authorities and
repositories::

    ---
    ansible_user: root
    ansible_private_key_file: "{{ inventory_dir }}/../keystore/ssh-key"
    ansible_connection: ssh
    # Add URLs from which to download CA certificates for installation
    certificate_authority_urls:
      - https://example.com/ca1.crt
      - https://example.com/ca2.crt
    # Base URL for repository mirror
    rhel_base: http://example.com/content/dist/rhel/server/7/7Server
    jenkins_master_url: 'http://jenkins.example.com' # URL to Jenkins master for the slave to connect to
    jslave_name: 'cinch-slave'
    jslave_label: 'cinch-slave'
    # If your Jenkins master requires authentication to connect a slave,
    # add credentials via the two variables below.  If anonymous users can
    # connect slaves to the master, do not include the following two
    # variables in this layout file.
    jenkins_slave_username: 'automation-user'
    jenkins_slave_password: 'jenkinsAPItoken'

Finally, If you'd like to automate this process in Jenkins, please see our
example `Jenkins Job Builder workflow template
<https://github.com/RedHatQE/cinch/blob/master/jjb/ci-jslave-project-sample.yaml>`_
for guidance on putting it all together.


Manual
``````

Execution of this software requires configuring an Ansible inventory that
points at the **jenkins\_master** and **jenkins\_slave** hosts that you want
configured. Use normal methods for setting **group\_vars** and **host\_vars**
within the inventory or its associated folders that suits your own needs and
preferences.

.. seealso:: While most default settings should be functional, there are lots
             of options configured in the various **default/main.yml** files
             within the various roles folders. Check in those files for more
             details on specific options that can be set and a description of
             what they each mean. *These files are heavily commented, and serve
             as the best source of documentation for the way that cinch
             configures a system.  If you feel the need to modify cinch
             playbooks directly, first check to see if the behavior you want is
             configurable via the provided Ansible variables.*

See a few examples of such in either the **inventory/** folder or inside of the
various **vagrant/** subfolders where known good working environments are
configured for development use.

The path **inventory/local** is excluded from use by the project and can be
leveraged for executing and storing your own local inventories, if the desire
arises. There is even a shell script in **bin/run\_jenkins\_local.sh** that
will execute **ansible-playbook** from the **.venv/** virtualenv and point it
to the **inventory/local/hosts** file to make executing against your own
environment as easy as a single command.

The cinch project can be used as a standard Ansible project, by running
**ansible-playbook** and calling **site.yml** for Jenkins master or slave
configuration and **teardown.yml** for removing a Jenkins slave from a Jenkins
master.

For convenience, we also provide CLI wrappers for these tasks.  These wrappers
simplify the task of finding and running the desired cinch playbooks for
configuration or teardown, and also can optionally pass through any additional
CLI arguments to the 'ansible-playbook' command that you may need.

The following commands are available:

- ``cinch`` - runs the **site.yml** playbook to configure a Jenkins master or
  slave
- ``teardown`` - runs the **teardown.yml** playbook to disconnect a Jenkins
  slave

Use the ``-h`` or ``--help`` arguments for the CLI wrappers to get further
info.


Support
-------

The playbooks should support, minimally, CentOS and RHEL versions 7+.  If you
encounter difficulties in those environments, please file bugs. There should be
no configuration necessary for a CentOS host, and a RHEL host requires only
that you configure the base URL for your local RHEL repository collection. See
documentation in the appropriate roles for details on that configuration.
