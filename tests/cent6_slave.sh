#!/bin/bash -xe
CINCH="$(readlink -f "$(dirname "$0")/../")"

${CINCH}/scripts/cent6_jswarm.sh
