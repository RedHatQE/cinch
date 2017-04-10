Docker Image
============

For users who do not want to provision an entire system to run a Jenkins slave
there exists a Docker image which can quickly get a Jenkins Swarm connected
instance to run.

Source Image
------------

For every release of cinch that is made, a version of the Docker container is
pushed to Docker Hub. Multiple tags are pushed for each Cinch release. They
are named by combining source information image along with the version of
Cinch used to build them.

Currently there are images built off of

  - centos:7
  - centos:6

These get tagged into the Cinch image repository as

  - redhatqecinch/jenkins_slave:cent7-0.5.2
  - redhatqecinch/jenkins_slave:cent6-0.5.2

This indicates two images, one based on the centos:7 image and one based off
the centos:6 image. Both of them are built by the version 0.5.2 release of
Cinch.

Image Options
-------------

As with the rest of Cinch, there are some customizable image options that a
user must supply before the image will work with your infrastrucutre. However,
unlike using the Ansible-based solution to create your own system, there are
far fewer options. Other than the following options, all builds of the Cinch
Docker images utilize all default values for a Cinch slave instance.

There are two variables that the user is required to provide before the image
will run properly. Those are

  ====================                ===================
  Environment Variable                Explanation
  ====================                ===================
  JENKINS_MASTER_URL                  The URL to the Jenkins master instance
                                      that this slave should connect to

  JSLAVE_NAME                         The name this slave will be given on the Master node
  JSLAVE_LABEL                        The Jenkins label this slave will receive,
                                      which will be matched against jobs requiring
                                      certain labels for execution
  JSWARM_EXTRA_ARGS                   Additional command-line arguments to
                                      pass to the JSwarm client in the iamge
  ====================                ===================

If the container image is run directly from the Docker command line, these
options may be passed through `docker`'s -e option. When running the image
in Kubernetes or OpenShift, use that system's methods for passing in
environment variables to the iamge.

Customizing the Image
---------------------

Instead of running the base image provided, a group could choose to use a
Dockerfile to extend the base image provided to do such things as install
custom software, edit configurations, etc. If that is the case, then the
environment variables can absolutely be preset within the Dockerfile using its
ENV command, as with any other environment variable.

Extending the image in this way could simplify deployment, as the image could
include information such as the Jenkins Master URL already configured to
connect to the organization's Jenkins instance. Likewise, different slave
images could be pre-populated with packages and slave labels for building
different types of software or running different types of tasks. As nothing
more than a standard Docker image, the provided images can be made fully
extensible.

One note is that the image is set to run all commands as the user "jenkins".
If the image is being extended, then it might be necessary to set the USER
command in the extending Dockerfile to "USER root" if system software is
being installed.
