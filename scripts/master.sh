#!/bin/bash

set -xe
cinch="$(readlink -f "$(dirname "${0}")/../")"
container_base="${1}"
inventory="${2}"
pkg_mgr="${3}"
container_name=jmaster
if [ ! -e "${inventory}" ]; then
	echo "You must specify a valid inventory folder"
	exit 1
fi
########################################################
# Spin up container and get it rolling
########################################################
echo "Starting container"
ansible -i /dev/null \
	localhost \
	-m docker_container \
	-a "image=${container_base} name=${container_name} tty=true detach=true command='/usr/lib/systemd/systemd --system'"
# Fedora is lacking python in base image
docker exec -it "${container_name}" "${pkg_mgr}" install -y python
ansible -i "${inventory}" \
	all \
	-m "${pkg_mgr}" \
	-a 'name=sudo state=present'
ansible -i "${inventory}" \
	all \
	-m "${pkg_mgr}" \
	-a 'name=* state=latest'
########################################################
# Run cinch against the playbook
########################################################
echo "Building container into a Jenkins master"
ansible-playbook -i "${inventory}" \
	"${cinch}/cinch/site.yml" \
	-e jenkins_user_password=somedummyvalue
