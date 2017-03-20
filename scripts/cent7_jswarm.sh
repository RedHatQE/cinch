#!/bin/bash -e

CINCH="$(readlink -f "$(dirname "$0")/../")"
CINCH_VERSION=$(grep "${CINCH}/setup.py" -e 'version=' | sed -e "s/.*version='\(.*\)'.*/\1/")

echo "*****************************************************"
echo "Building cinch container for version ${CINCH_VERSION}"
echo "*****************************************************"

echo "Starting container"
ansible -i /dev/null localhost -m docker_container -a "image=greghellings/centos_base:latest name=jswarm detach=true tty=true command=/bin/bash"
echo "Building container with Ansible"
ansible-playbook -i "${CINCH}/inventory/cent7_jswarm_docker" "${CINCH}/cinch/site.yml" \
	-e jenkins_user_password=some_dummy_value
echo "Committing container at tag ${CINCH_VERSION}"
docker commit \
	--change 'ENTRYPOINT ["/usr/local/bin/dockerize", "-template", "/etc/sysconfig/jenkins_swarm:/etc/sysconfig/jenkins_swarm.templated", "/opt/jswarm.sh"]' \
	jswarm cinch:${CINCH_VERSION}
