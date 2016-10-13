#!/bin/bash

source ../shared.sh

vagrant_cycle slave || exit 1

venv || exit 1

playbook slave "$@" || exit 1
