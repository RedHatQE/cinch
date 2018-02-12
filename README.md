![alt text](https://travis-ci.org/RedHatQE/cinch.svg?branch=master "build status")
[![codecov](https://codecov.io/gh/RedHatQE/cinch/branch/master/graph/badge.svg)](https://codecov.io/gh/RedHatQE/cinch)

# cinch

This folder contains an Ansible playbook for standing up and configuring
Jenkins masters and slaves. There are roles specifically for the creation of
those configurations, as well as several other roles which can be leveraged
for configuring and standing up resources of other types helpful in the
process of running continuous integration.

For full documentation on the configuration options of each role, see the
default vars YAML file in the particular role. Any of the values in that file
are intended to be overridden by the user.

Getting Started
---------------

Please see documentation at http://redhatqe-cinch.rtfd.io/

Settings
--------

Some notable defaults for Jenkins masters currently enabled are
- Java 8
- Jenkins LTS 2.63.3
- an extensive list of plugins found in files/jenkins-plugin-lists/default.txt
- SSL disabled, but Jenkins served off of port 80

Primary supported target operating systems are
- RHEL 7
- CentOS 7

IRC Support
---------------

`#redhatqe-cinch on chat.freenode.net`

