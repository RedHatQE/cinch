#!/bin/bash

set -xe
cinch="$(readlink -f "$(dirname "${0}")/../")"
container_base="${1}"
inventory="${2}"
pkg_mgr="${3}"
container_name=jmaster
# Extracts the version line from the setup.py script, and trims off the rest of the line to leave
# only the expected version
cinch_version=$(grep "${cinch}/setup.py" -e 'version=' | sed -e "s/.*version='\(.*\)'.*/\1/")
if [ ! -e "${inventory}" ]; then
	echo "You must specify a valid inventory folder"
	exit 1
fi
########################################################
# Spin up container and get it rolling
########################################################
echo "Starting container from image ${container_base}"
ansible -i /dev/null \
	localhost \
	-m docker_container \
	-a "image=${container_base} \
		name=${container_name} \
		tty=true \
		detach=true \
		command='/usr/lib/systemd/systemd \
		--system' \
		capabilities=SYS_ADMIN \
		$([[ $TRAVIS = true ]] && echo privileged=true)"
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
echo "Building container into a Jenkins master for Cinch ${cinch_version}"
ansible-playbook -i "${inventory}" \
	"${cinch}/cinch/site.yml" \
	-e jenkins_user_password=somedummyvalue
########################################################
# Run inspec against the container
########################################################
erb "${cinch}/tests/profile.yml.erb" > "${cinch}/tests/profile.yml"
inspec  --chef-license=accept-silent exec "${cinch}/tests/cinch" \
  --attrs "${cinch}/tests/profile.yml" -t "docker://${container_name}"
########################################################
# Finish and close up the container
########################################################
echo "Saving image"
docker commit \
	--change 'EXPOSE 8080' \
	--change 'EXPOSE 8009' \
	--change 'ENTRYPOINT ["/usr/lib/systemd/systemd", "--system"]' \
	"${container_name}" "redhatqecinch/jenkins_master:${container_base//:/}-${cinch_version}"
