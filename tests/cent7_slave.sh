#!/bin/bash -xe
CINCH="$(readlink -f "$(dirname "$0")/../")"

${CINCH}/scripts/cent7_jswarm.sh
