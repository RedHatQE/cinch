#!/bin/bash

set -ve
cinch="$(readlink -f "$(dirname "${0}")/../")"
centos_version="${1}"
inventory="${cinch}/inventory/cent${centos_version}_master_docker/hosts"
"${cinch}/scripts/master.sh" "centos:${centos_version}" "${inventory}" yum
