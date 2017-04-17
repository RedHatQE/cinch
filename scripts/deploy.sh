#!/bin/bash -e

CINCH="$(readlink -f "$(dirname "$0")/../")"
# Extracts the version line from the setup.py script, and trims off the rest
# of the line to leave only the expected version
CINCH_VERSION=$(grep "${CINCH}/setup.py" -e 'version=' \
	| sed -e "s/.*version='\(.*\)'.*/\1/")
echo "Deploying version '${CINCH_VERSION}'"

# Tag the CentOS 7 image as the "latest" version, for people wanting the
# cutting edge
docker tag "redhatqecinch/jenkins_slave:cent7-${CINCH_VERSION}" \
	redhatqecinch/jenkins_slave:latest
# Login to Docker - these environment variables are stored in TravisCI for
# safe keeping
docker login -p "${DOCKER_PASSWORD}" -u "${DOCKER_USER}"
# Push the latest builds of these images to Docker Hub
docker push "redhatqecinch/jenkins_slave:cent6-${CINCH_VERSION}"
docker push "redhatqecinch/jenkins_slave:cent7-${CINCH_VERSION}"
docker push redhatqecinch/jenkins_slave:latest
