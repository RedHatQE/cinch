#!/bin/bash

set -ve
cinch="$(readlink -f "$(dirname "${0}")/../")"
fedora_version=25
inventory="${cinch}/inventory/fedora_master_docker/hosts"
"${cinch}/scripts/master.sh" "fedora:${fedora_version}" "${inventory}" dnf
