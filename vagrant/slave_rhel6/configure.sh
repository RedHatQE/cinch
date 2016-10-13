#!/bin/bash

source ../shared.sh
venv || exit 1
playbook slave_rhel6 "$@" || exit 1
