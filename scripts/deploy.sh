#!/bin/bash -e

CINCH="$(readlink -f "$(dirname "$0")/../")"
# Extracts the version line from the setup.py script, and trims off the rest
# of the line to leave only the expected version
CINCH_VERSION=$(grep "${CINCH}/setup.py" -e 'version=' \
	| sed -e "s/.*version='\(.*\)'.*/\1/")
DISTRO="${1}"
LATEST="${2}"

echo "Deploying version '${CINCH_VERSION}' to '${DISTRO}'"

# Login to Docker - these environment variables are stored in TravisCI for
# safe keeping
docker login -p "${DOCKER_PASSWORD}" -u "${DOCKER_USER}"
# Push the latest builds of these images to Docker Hub
docker push "redhatqecinch/jenkins_slave:${DISTRO}-${CINCH_VERSION}"

# Only one version should be tagged as the latest, so let this be it
if [ x"${LATEST}" = "xtrue" ]; then
	echo "Tagging '${DISTRO}' as latest and pushing"
	# Tag the image as the "latest" version, for people wanting the
	# cutting edge
	docker tag "redhatqecinch/jenkins_slave:${DISTRO}-${CINCH_VERSION}" \
		redhatqecinch/jenkins_slave:latest
	docker push redhatqecinch/jenkins_slave:latest
fi
