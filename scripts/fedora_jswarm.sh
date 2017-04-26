#!/bin/bash -e

fedora_version=25
cinch="$(readlink -f "$(dirname "$0")/../")"
inventory="${cinch}/inventory/fedora_jswarm_docker"
"${cinch}/scripts/jswarm.sh" "fedora:${fedora_version}" "${inventory}" dnf
