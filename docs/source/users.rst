Users
=====

Getting Started
===============

At its core, this software is nothing more than a collection of Ansible
playbook scripts for configuring a system. Any knowledge that you have that is
applicable to the broad spectrum of Ansible usage is applicable here.  You can
opt to install Ansible from your favorite package manager, or you can use the
version that is pinned in the **requirements.txt** file and has been tested
with the software (strongly recommended).

Before concluding there is a bug in these playbooks, make sure that the version
of Ansible you are using is the same as the version in the **requirements.txt**
file and that you have ensured there are no alterations from that version. It
is not intended or guaranteed that any changes from the stock version of
Ansible that has been tested should work.

Requirements
============

To setup your environment, you need to install Ansible. Since Ansible is
primarily distributed as a Python package, it is suggested that you use **pip**
to install Ansible on your system. You are welcome to try and use the version
that is installed by your favorite package manager, but be sure that you are
using a version at least as new as the version pinned in **requirements.txt**.

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

``sudo dnf install -y libvirt-devel python-virtualenv libyaml-devel
openssl-devel libffi-devel gcc redhat-rpm-config``

Installation
============

Once the system level packages are installed, you can install cinch using
**pip** (virtualenv strongly recommended):

Fedora
------

``virtualenv cinch && source cinch/bin/activate``

``pip install cinch``

RHEL7 and CentOS7
-----------------

RHEL7 and derivatives offer older versions of Python packaging tools that are
incompatible with some cinch dependencies.  To work-around this issue, we have
provided an `Ansible playbook
<https://github.com/RedHatQE/cinch/blob/master/cinch/install-rhel7.yml>`_ that
will install a newer version of the necessary Python packaging tools to allow
for installation on RHEL7.  This playbook is intended for use on Jenkins
masters and will install cinch into a virtualenv at
**/var/lib/jenkins/opt/cinch**.  For convenience, an optional `Jenkins Job
Builder template
<https://github.com/RedHatQE/cinch/blob/master/jjb/install-rhel7.yaml>`_ is
provided and will create a Jenkins job that will run the aforementioned
playbook on your Jenkins master.

Execution
=========

With linch-pin
--------------

The ``cinchpin`` command can be used to call `linch-pin
<http://linch-pin.readthedocs.io/en/latest/>`_ automatically to provision
instances and then configure the instances.  ``cinchpin`` supports a subset of
linch-pin commands, such as **rise**, **drop**, and **init**.

In the following example we will provision a RHEL7 instance in OpenStack as a
Jenkins slave.

First, create necessary credentials for linch-pin provisioning for your target
infrastructure in
*<venv-path>* **/lib/python2.7/site-packages/provision/roles/openstack/vars/os_creds.yml**: ::

    ---
    # openstack API endpoint
    endpoint: http://openstack-api-endpoint.example.com:5000/v2.0

    # project/tenant name
    project: myproject

    # project/tenant username and password
    username: myuser
    password: mypass

.. note::  The upcoming auth driver feature for linch-pin will make this step
 easier in the future.

Next, generate a linch-pin working directory for use with cinch by running the
following commands:

``mkdir /path/to/workdir``

``cinchpin init -w /path/to/workdir``

Create a layout file by saving the following example template as
**/path/to/workdir/layouts/cinch.yml** and edit to taste.  For the
**jenkins_user_password** variable, please use the `Ansible documentation
<https://docs.ansible.com/ansible/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module>`_
to generate a suitable password hash.  **For security in production
environments, DO NOT copy the existing hash from this example.** ::

    ---
    inventory_layout:
      hosts:
        cinch:
          count: 1
          # List all necessary 'cinch' roles here
          host_groups:
            - rhel7 # specify the appropriate Ansible role for your distribution
            - certificate_authority # optional role to install CA certificates
            - repositories # the 'repositories' role is required for a Jenkins master or slave
            - jenkins_slave
      host_groups:
        all:
          vars:
            # required variables for all hosts
            ansible_user: root
            ansible_private_key_file: /path/to/ssh/private_key
            ansible_connection: ssh
        certificate_authority:
          vars:
            # Add URLs from which to download CA certificates for installation
            certificate_authority_urls:
              - https://example.com/ca1.crt
              - https://example.com/ca2.crt
        repositories:
          vars:
            # Base URL for repository mirror
            rhel_base: http://example.com/content/dist/rhel/server/7/7Server
        jenkins_slave:
          vars:
            # Required variables for a Jenkins slave

            # The password for the Jenkins user account that will be created on the slave.
            # For security in production environments, DO NOT copy the
            # existing hash from this example.
            # https://docs.ansible.com/ansible/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module
            jenkins_user_password: '$6$rounds=656000$YQKMBktZ/Gaggxf0$KC7xhatWzdDJyvCDo7htomtiSsvd2MWN87RB3TsAbq1Nmwddy/z2Et8kQi1/tZkHjfD2vG1r7W2R9rjpaA1C5/'
            jenkins_master_url: 'http://jenkins.example.com' # URL to Jenkins master for the slave to connect to

Create a topology file by saving the following example template as
**/path/to/workdir/topologies/cinch.yml** and edit to taste::

    ---
    topology_name: "cinch_topology"

    # OpenStack project/tenant name
    site: "my-openstack-project-name"

    resource_groups:
      -
        resource_group_name: "cinch"
        res_group_type: "openstack"
        res_defs:
          - res_name: "resource"
            flavor: "m1.large"
            res_type: "os_server"
            image: "rhel-7.2-server-x86_64-released"
            count: 1 # Number of instances to create
            keypair: "openstack-keypair-name" # Name of SSH keypair configured for OpenStack account
            networks:
              - "openstack-network-name" # OpenStack network name

        # Name of credentials file to use for the OpenStack API
        assoc_creds: "os_creds"

.. note::  For more topology examples, including various host environments, see
           the `linch-pin documentation
           <https://linch-pin.readthedocs.io/en/latest/topologies.html>`_.

Provision and configure your Jenkins slave automatically with the following
command:

``cinchpin rise -w /path/to/workdir``

To terminate the OpenStack instance and remove the Jenkins slave from the
Jenkins master, run the following command:

``cinchpin drop -w /path/to/workdir``

.. note::  Once the working directory is configured successfully, a common next
 step would be to check this directory into source control where it can be
 consumed by CI automation tools such as Jenkins Job Builder or Jenkins
 Pipeline.

Manual
------

Execution of this software requires configuring an Ansible inventory that
points at the **jenkins\_master** and **jenkins\_slave** hosts that you want
configured. Use normal methods for setting **group\_vars** and **host\_vars**
within the inventory or its associated folders that suits your own needs and
preferences.

While most default settings should be functional, there are lots of options
configured in the various **default/main.yml** files within the various roles
folders. Check in those files for more details on specific options that can be
set and a description of what they each mean.

See a few examples of such in either the **inventory/** folder or inside of the
various **vagrant/** subfolders where known good working environments are
configured for development use.

The path **inventory/local** is excluded from use by the project and can be
leveraged for executing and storing your own local inventories, if the desire
arises. There is even a shell script in **bin/run\_jenkins\_local.sh** that
will execute **ansible-playbook** from the **.venv/** virtualenv and point it
to the **inventory/local/hosts** file to make executing against your own
environment as easy as a single command.


Support
=======

The playbooks should support, minimally, CentOS and RHEL versions 7+.  If you
encounter difficulties in those environments, please file bugs. There should be
no configuration necessary for a CentOS host, and a RHEL host requires only
that you configure the base URL for your local RHEL repository collection. See
documentation in the appropriate roles for details on that configuration.
