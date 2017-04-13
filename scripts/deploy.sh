#!/bin/bash -e

CINCH="$(readlink -f "$(dirname "$0")/../")"
# Extracts the version line from the setup.py script, and trims off the rest of the line to leave
# only the expected version
CINCH_VERSION=$(grep "${CINCH}/setup.py" -e 'version=' | sed -e "s/.*version='\(.*\)'.*/\1/")

docker login -p "${DOCKER_PASSWORD}" -u "${DOCKER_USER}"
docker push redhatqecinch/jenkins_slave:cent6-${CINCH_VERSION}
docker push redhatqecinch/jenkins_slave:cent7-${CINCH_VERSION}
