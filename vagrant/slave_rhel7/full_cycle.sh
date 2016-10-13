#!/bin/bash

source ../shared.sh
vagrant_cycle slave_rhel7 || exit 1
venv || exit 1
playbook slave_rhel7 "$@" || exit 1
