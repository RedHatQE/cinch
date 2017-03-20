#!/bin/bash -xe
CINCH="$(readlink -f "$(dirname "$0")/../")"

"${CINCH}/scripts/centos_jswarm.sh" 6
