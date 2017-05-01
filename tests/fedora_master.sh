#!/bin/bash

set -ve
cinch="$(readlink -f "$(dirname "${0}")/../")"
"${cinch}/scripts/fedora_master.sh"
