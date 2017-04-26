#!/bin/bash -e

cinch="$(readlink -f "$(dirname "$0")/../")"
centos_version="${1}"
inventory="${cinch}/inventory/cent${centos_version}_jswarm_docker"
if [ ! -e "${inventory}" ]; then
	echo "You must specify a supported CentOS version to continue"
	exit 1
fi
"${cinch}/scripts/jswarm.sh" "centos:${centos_version}" "${inventory}" yum
