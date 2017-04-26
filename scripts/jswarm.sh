#!/bin/bash

set-ve
cinch="$(readlink -f "$(dirname "$0")/../")"
base_image="${1}"
inventory="${2}"
module="${3}"
# Extracts the version line from the setup.py script, and trims off the rest of the line to leave
# only the expected version
cinch_version=$(grep "${cinch}/setup.py" -e 'version=' | sed -e "s/.*version='\(.*\)'.*/\1/")
echo "*****************************************************"
echo "Building cinch container for version ${cinch_version}"
echo "*****************************************************"
echo "Starting container"
ansible -i /dev/null \
	localhost \
	-m docker_container \
	-a "image=${base_image} name=jswarm detach=true tty=true command=/bin/bash"
docker exec -it jswarm "${module}" install -y python
ansible -i "${inventory}" all -m "${module}" -a "name=sudo state=present"
ansible -i "${inventory}" all -m "${module}" -a "name=* state=latest"
echo "Building container with Ansible"
ansible-playbook -i "${inventory}" \
	"${cinch}/cinch/site.yml" \
	-e jenkins_user_password=some_dummy_value
echo "Committing container at tag ${cinch_version}"
docker commit \
	--change 'USER jenkins' \
	--change 'ENTRYPOINT ["/usr/local/bin/dockerize", "-template", "/etc/sysconfig/jenkins_swarm:/etc/sysconfig/jenkins_swarm.templated", "/usr/local/bin/jswarm.sh"]' \
	jswarm "redhatqecinch/jenkins_slave:${base_image//:/}-${cinch_version}"
