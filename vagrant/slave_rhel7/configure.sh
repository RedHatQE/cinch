#!/bin/bash

source ../shared.sh
venv || exit 1
playbook slave_rhel7 "$@" || exit 1
