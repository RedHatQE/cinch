#!/bin/bash

source ../shared.sh

venv || exit 1

playbook slave "$@" || exit 1
