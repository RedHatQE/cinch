#!/bin/bash

set -ve
cinch="$(readlink -f "$(dirname "${0}")/../")"
"${cinch}/scripts/centos_master.sh" 7
