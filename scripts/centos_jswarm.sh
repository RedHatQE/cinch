#!/bin/bash -e

CINCH="$(readlink -f "$(dirname "$0")/../")"
CENTOS_VERSION="${1}"
INVENTORY="${CINCH}/inventory/cent${CENTOS_VERSION}_jswarm_docker"
if [ ! -e "${INVENTORY}" ]; then
	echo "You must specify a CentOS version to continue"
	exit 1
fi
# Extracts the version line from the setup.py script, and trims off the rest of the line to leave
# only the expected version
CINCH_VERSION=$(grep "${CINCH}/setup.py" -e 'version=' | sed -e "s/.*version='\(.*\)'.*/\1/")

echo "*****************************************************"
echo "Building cinch container for version ${CINCH_VERSION}"
echo "*****************************************************"

echo "Starting container"
ansible -i /dev/null \
	localhost \
	-m docker_container \
	-a "image=centos:${CENTOS_VERSION} name=jswarm detach=true tty=true command=/bin/bash"
ansible -i "${INVENTORY}" all -m yum -a "name=sudo state=present"
ansible -i "${INVENTORY}" all -m yum -a "name=* state=latest"

echo "Building container with Ansible"
ansible-playbook -i "${INVENTORY}" \
	"${CINCH}/cinch/site.yml" \
	-e jenkins_user_password=some_dummy_value

echo "Committing container at tag ${CINCH_VERSION}"
docker commit \
	--change 'USER jenkins' \
	--change 'ENTRYPOINT ["/usr/local/bin/dockerize", "-template", "/etc/sysconfig/jenkins_swarm:/etc/sysconfig/jenkins_swarm.templated", "/usr/local/bin/jswarm.sh"]' \
	jswarm "cinch:cent${CENTOS_VERSION}-${CINCH_VERSION}"
