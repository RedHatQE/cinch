#!/bin/bash -xe
cinch="$(readlink -f "$(dirname "$0")/../")"

"${cinch}/scripts/fedora_jswarm.sh"
